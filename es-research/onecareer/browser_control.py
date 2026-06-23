#!/usr/bin/env python3
"""Small Playwright wrapper for authorized browser-based research scripts.

Keep browser mechanics here so site-specific collectors can focus on search,
confirmation, and output rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class BrowserSettings:
    profile_dir: Path
    headless: bool = False
    timeout_ms: int = 15000
    viewport_width: int = 1440
    viewport_height: int = 1000


def load_playwright() -> tuple[Any, type[Exception]]:
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: playwright\n"
            "Install it with:\n"
            "  python -m pip install playwright\n"
            "  python -m playwright install chromium"
        ) from exc
    return sync_playwright, PlaywrightTimeoutError


class BrowserSession:
    def __init__(self, settings: BrowserSettings) -> None:
        self.settings = settings
        self._sync_playwright: Any = None
        self._playwright: Any = None
        self._context: Any = None
        self._page: Any = None
        self._timeout_error: type[Exception] | None = None

    def __enter__(self) -> "BrowserSession":
        sync_playwright, timeout_error = load_playwright()
        self._timeout_error = timeout_error
        self._sync_playwright = sync_playwright()
        self._playwright = self._sync_playwright.start()
        self._context = self._playwright.chromium.launch_persistent_context(
            str(self.settings.profile_dir),
            headless=self.settings.headless,
            viewport={
                "width": self.settings.viewport_width,
                "height": self.settings.viewport_height,
            },
        )
        self._page = self._context.pages[0] if self._context.pages else self._context.new_page()
        self._page.set_default_timeout(self.settings.timeout_ms)
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._context is not None:
            self._context.close()
        if self._playwright is not None:
            self._playwright.stop()

    @property
    def page(self) -> Any:
        if self._page is None:
            raise RuntimeError("BrowserSession is not open.")
        return self._page

    def goto(self, url: str, *, wait_until: str = "domcontentloaded") -> bool:
        try:
            self.page.goto(url, wait_until=wait_until)
            return True
        except Exception as exc:
            if self._timeout_error is not None and isinstance(exc, self._timeout_error):
                return False
            raise

    def current_url(self) -> str:
        return str(self.page.url)

    def title(self) -> str:
        return str(self.page.title())

    def html(self) -> str:
        return str(self.page.content())

    def body_text(self) -> str:
        return str(self.page.locator("body").inner_text(timeout=self.settings.timeout_ms))
