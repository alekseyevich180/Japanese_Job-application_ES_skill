#!/usr/bin/env python3
"""Collect authorized OneCareer pages through an interactive browser session.

The script is intentionally semi-automatic. It opens OneCareer in a real browser
profile so the user can log in with their own account, then it iterates through
company names from a text file. For each company, the user confirms the page in
the browser and presses Enter in the terminal before the script saves HTML and
visible text.

It does not call private APIs, bypass login, solve CAPTCHA, or evade access
controls.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Iterable

from browser_control import BrowserSession, BrowserSettings


ONECAREER_HOST_SUFFIXES = (
    "onecareer.jp",
    "id.onecareer.jp",
)


def slugify(value: str) -> str:
    value = value.strip()
    value = re.sub(r"[\\/:*?\"<>|]+", "_", value)
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("._")[:80] or "company"


def read_companies(path: Path) -> list[dict[str, str]]:
    """Read company lines.

    Supported formats:
    - company name
    - company name,https://www.onecareer.jp/...
    - https://www.onecareer.jp/...   (URL-only; company name is inferred)
    """
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parsed = next(csv.reader([line]))
            name = parsed[0].strip()
            url = parsed[1].strip() if len(parsed) > 1 else ""
            if name.startswith(("http://", "https://")) and not url:
                url = name
                name = urllib.parse.urlparse(url).path.strip("/").split("/")[-1] or "onecareer"
            rows.append({"name": name, "url": url})
    if not rows:
        raise SystemExit(f"No companies found in {path}")
    return rows


def host_allowed(url: str) -> bool:
    host = urllib.parse.urlparse(url).hostname or ""
    return any(host == suffix or host.endswith("." + suffix) for suffix in ONECAREER_HOST_SUFFIXES)


def build_search_url(template: str, company: str) -> str:
    encoded = urllib.parse.quote(company)
    return template.format(query=encoded, company=encoded)


def write_page(out_dir: Path, company: str, url: str, title: str, html: str, text: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(company)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = out_dir / f"{slug}_{stamp}"

    html_path = base.with_suffix(".html")
    text_path = base.with_suffix(".txt")
    meta_path = base.with_suffix(".json")

    html_path.write_text(html, encoding="utf-8")
    text_path.write_text(text.strip() + "\n", encoding="utf-8")
    meta_path.write_text(
        json.dumps(
            {
                "company": company,
                "url": url,
                "title": title,
                "saved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "html": str(html_path),
                "text": str(text_path),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    with (out_dir / "index.jsonl").open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "company": company,
                    "url": url,
                    "title": title,
                    "text": str(text_path),
                    "saved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                },
                ensure_ascii=False,
            )
            + "\n"
        )

    print(f"Saved text: {text_path}")


def prompt_continue(message: str) -> str:
    try:
        return input(message).strip().lower()
    except EOFError:
        return "q"


def iter_companies(companies: Iterable[dict[str, str]]) -> Iterable[dict[str, str]]:
    for index, company in enumerate(companies, start=1):
        print()
        print(f"[{index}] {company['name']}")
        yield company


def main() -> int:
    parser = argparse.ArgumentParser(description="Interactively collect authorized OneCareer pages.")
    parser.add_argument("--companies", required=True, help="Text or CSV file with company names.")
    parser.add_argument("--out", default="fetched/onecareer", help="Output directory.")
    parser.add_argument("--profile", default=".browser-profiles/onecareer", help="Persistent browser profile directory.")
    parser.add_argument(
        "--search-url-template",
        default="https://www.onecareer.jp/experiences?keyword={query}",
        help="URL template. Use {query} for URL-encoded company name.",
    )
    parser.add_argument("--headless", action="store_true", help="Run browser headless. Not recommended for login.")
    parser.add_argument("--timeout-ms", type=int, default=15000, help="Page load timeout in milliseconds.")
    args = parser.parse_args()

    companies = read_companies(Path(args.companies))
    out_dir = Path(args.out)
    settings = BrowserSettings(
        profile_dir=Path(args.profile),
        headless=args.headless,
        timeout_ms=args.timeout_ms,
    )

    with BrowserSession(settings) as browser:
        print("A browser window is open. Log in to OneCareer if needed.")
        print("After login, return to this terminal and press Enter.")
        browser.goto("https://www.onecareer.jp/")
        prompt_continue("Press Enter after login is ready, or type q to quit: ")

        for company in iter_companies(companies):
            target_url = company["url"] or build_search_url(args.search_url_template, company["name"])
            if not host_allowed(target_url):
                print(f"Skipped non-OneCareer URL: {target_url}")
                continue

            loaded = browser.goto(target_url)
            if not loaded:
                print("Page load timed out. You can still adjust the page manually.")

            print("Use the browser to open the exact OneCareer page you want to save.")
            print("For ES research, open the company, ES, or experience page that is useful.")
            action = prompt_continue("Press Enter to save current page, s to skip, q to quit: ")
            if action == "q":
                break
            if action == "s":
                continue

            current_url = browser.current_url()
            if not host_allowed(current_url):
                print(f"Refusing to save non-OneCareer page: {current_url}")
                continue

            title = browser.title()
            html = browser.html()
            text = browser.body_text()
            write_page(out_dir, company["name"], current_url, title, html, text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
