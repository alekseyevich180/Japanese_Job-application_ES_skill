#!/usr/bin/env python3
"""Fetch authorized web pages for ES research using user-configured credentials.

This helper is intentionally conservative: it supports normal GET/login flows,
domain allowlists, environment-based credentials, and rate limiting. It does not
attempt to bypass CAPTCHA, paywalls, access controls, or technical blocks.
"""

from __future__ import annotations

import argparse
import html.parser
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Any


class TextExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
        if tag in {"p", "div", "section", "article", "br", "li", "h1", "h2", "h3"}:
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1
        if tag in {"p", "div", "section", "article", "li", "h1", "h2", "h3"}:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            text = data.strip()
            if text:
                self._parts.append(text)

    def text(self) -> str:
        joined = " ".join(self._parts)
        joined = re.sub(r"[ \t\r\f\v]+", " ", joined)
        joined = re.sub(r"\n\s+", "\n", joined)
        joined = re.sub(r"\n{3,}", "\n\n", joined)
        return joined.strip() + "\n"


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def site_config(config: dict[str, Any], site_name: str) -> dict[str, Any]:
    try:
        site = config["sites"][site_name]
    except KeyError as exc:
        raise SystemExit(f"Site '{site_name}' not found in config.") from exc
    if not isinstance(site, dict):
        raise SystemExit(f"Site '{site_name}' must be an object.")
    return site


def host_allowed(url: str, allowed_domains: list[str]) -> bool:
    host = urllib.parse.urlparse(url).hostname or ""
    return any(host == domain or host.endswith("." + domain) for domain in allowed_domains)


def build_opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))


def request(
    opener: urllib.request.OpenerDirector,
    url: str,
    *,
    data: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> tuple[str, str]:
    encoded_data = None
    if data is not None:
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=encoded_data, headers=headers or {})
    with opener.open(req, timeout=timeout) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        final_url = response.geturl()
    return raw.decode(charset, errors="replace"), final_url


def env_required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def add_cookie_header(headers: dict[str, str], cookie_env: str | None) -> None:
    if cookie_env:
        cookie = env_required(cookie_env)
        headers["Cookie"] = cookie


def extract_csrf(html: str, pattern: str | None) -> str | None:
    if not pattern:
        return None
    match = re.search(pattern, html)
    if not match:
        raise SystemExit("Configured csrf_regex did not match the login page.")
    return match.group(1)


def login(opener: urllib.request.OpenerDirector, site: dict[str, Any], headers: dict[str, str]) -> None:
    login_url = site.get("login_url")
    if not login_url:
        return

    username_env = site.get("username_env")
    password_env = site.get("password_env")
    if not username_env or not password_env:
        raise SystemExit("login_url requires username_env and password_env.")

    login_page, _ = request(opener, login_url, headers=headers)
    payload = dict(site.get("login_payload", {}))
    payload[site.get("username_field", "username")] = env_required(username_env)
    payload[site.get("password_field", "password")] = env_required(password_env)

    csrf = extract_csrf(login_page, site.get("csrf_regex"))
    if csrf:
        payload[site.get("csrf_field", "csrf_token")] = csrf

    request(opener, login_url, data=payload, headers=headers)


def write_outputs(out_dir: Path, url: str, html: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", urllib.parse.urlparse(url).netloc + urllib.parse.urlparse(url).path)
    slug = slug.strip("_") or "page"
    html_path = out_dir / f"{slug}.html"
    text_path = out_dir / f"{slug}.txt"

    extractor = TextExtractor()
    extractor.feed(html)

    html_path.write_text(html, encoding="utf-8")
    text_path.write_text(extractor.text(), encoding="utf-8")
    print(f"Wrote HTML: {html_path}")
    print(f"Wrote text: {text_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch authorized pages for Japanese ES research.")
    parser.add_argument("--config", required=True, help="Path to JSON config.")
    parser.add_argument("--site", required=True, help="Site key in config.")
    parser.add_argument("--url", required=True, help="URL to fetch.")
    parser.add_argument("--out", default="fetched", help="Output directory.")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    site = site_config(config, args.site)
    allowed_domains = site.get("allowed_domains", [])
    if not allowed_domains or not host_allowed(args.url, allowed_domains):
        raise SystemExit("URL host is not in the configured allowed_domains.")

    headers = {
        "User-Agent": site.get("user_agent", "japanese-es-writing-research/1.0"),
        **site.get("headers", {}),
    }
    add_cookie_header(headers, site.get("session_cookie_env"))

    rate_seconds = float(site.get("rate_seconds", 2.0))
    opener = build_opener()
    login(opener, site, headers)
    time.sleep(rate_seconds)

    try:
        html, final_url = request(opener, args.url, headers=headers)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"HTTP error {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"URL error: {exc.reason}") from exc

    if not host_allowed(final_url, allowed_domains):
        raise SystemExit("Final URL host is not in the configured allowed_domains.")
    write_outputs(Path(args.out), final_url, html)
    return 0


if __name__ == "__main__":
    sys.exit(main())
