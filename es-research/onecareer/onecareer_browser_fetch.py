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

TARGET_TEMPLATES = {
    "es": "https://www.onecareer.jp/experiences?keyword={query}",
    "company": "https://www.onecareer.jp/companies?keyword={query}",
    "career": "https://www.google.com/search?q={query}+採用+キャリアプラン",
    "values": "https://www.google.com/search?q={query}+採用+価値観+求める人物像",
}

TARGET_LABELS = {
    "es": "OneCareer ES / selection experiences",
    "company": "OneCareer company page",
    "career": "career plan / career path research",
    "values": "company values / desired candidate profile research",
}


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


def write_page(out_dir: Path, company: str, page_type: str, url: str, title: str, html: str, text: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(company)
    type_slug = slugify(page_type)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = out_dir / f"{slug}_{type_slug}_{stamp}"

    html_path = base.with_suffix(".html")
    text_path = base.with_suffix(".txt")
    meta_path = base.with_suffix(".json")

    html_path.write_text(html, encoding="utf-8")
    text_path.write_text(text.strip() + "\n", encoding="utf-8")
    meta_path.write_text(
        json.dumps(
            {
                "company": company,
                "page_type": page_type,
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
                    "page_type": page_type,
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


def parse_targets(raw_targets: str) -> list[str]:
    targets = [target.strip() for target in raw_targets.split(",") if target.strip()]
    unknown = [target for target in targets if target not in TARGET_TEMPLATES]
    if unknown:
        raise SystemExit(f"Unknown research target(s): {', '.join(unknown)}")
    return targets


def target_url(target: str, company: dict[str, str], search_url_template: str) -> str:
    if target == "es" and company["url"]:
        return company["url"]
    template = search_url_template if target == "es" else TARGET_TEMPLATES[target]
    return build_search_url(template, company["name"])


def can_save_url(url: str, *, allow_any_domain: bool) -> bool:
    if host_allowed(url):
        return True
    if allow_any_domain and urllib.parse.urlparse(url).scheme in {"http", "https"}:
        return True
    return False


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
    parser.add_argument(
        "--targets",
        default="es,company,career,values",
        help="Comma-separated targets: es, company, career, values.",
    )
    parser.add_argument(
        "--allow-any-domain",
        action="store_true",
        help="Allow saving official/recruiting pages outside OneCareer after manual confirmation.",
    )
    args = parser.parse_args()

    companies = read_companies(Path(args.companies))
    targets = parse_targets(args.targets)
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

        should_quit = False
        for company in iter_companies(companies):
            for target in targets:
                print(f"Target: {target} - {TARGET_LABELS[target]}")
                start_url = target_url(target, company, args.search_url_template)
                if not can_save_url(start_url, allow_any_domain=True):
                    print(f"Skipped unsupported URL: {start_url}")
                    continue

                loaded = browser.goto(start_url)
                if not loaded:
                    print("Page load timed out. You can still adjust the page manually.")

                print("Use the browser to open the exact page you want to save.")
                if target == "es":
                    print("Open a OneCareer ES, interview, or selection-experience page.")
                elif target == "company":
                    print("Open the OneCareer company page or relevant company overview page.")
                elif target == "career":
                    print("Open a career plan, career path, recruiting, or employee-growth page.")
                elif target == "values":
                    print("Open a values, mission, culture, or desired-candidate-profile page.")

                action = prompt_continue("Press Enter to save current page, s to skip, n for next company, q to quit: ")
                if action == "q":
                    should_quit = True
                    break
                if action == "n":
                    break
                if action == "s":
                    continue

                current_url = browser.current_url()
                if not can_save_url(current_url, allow_any_domain=args.allow_any_domain):
                    print(f"Refusing to save outside OneCareer without --allow-any-domain: {current_url}")
                    continue

                title = browser.title()
                html = browser.html()
                text = browser.body_text()
                write_page(out_dir, company["name"], target, current_url, title, html, text)

            if should_quit:
                break

    return 0


if __name__ == "__main__":
    sys.exit(main())
