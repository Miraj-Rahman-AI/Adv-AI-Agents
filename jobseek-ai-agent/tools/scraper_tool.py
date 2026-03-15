from __future__ import annotations

from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup

from config.settings import Settings


class ScraperTool:
    """
    Generic webpage scraper.

    Responsibilities:
    - Fetch raw HTML from a URL
    - Parse title and text content
    - Return structured page content for downstream parsing

    Later you can extend this with:
    - Selenium support for dynamic pages
    - Playwright support
    - anti-bot handling
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.headers = {
            "User-Agent": self.settings.user_agent,
        }

    def fetch(self, url: str) -> Dict[str, str]:
        """
        Fetch a webpage and return raw HTML.
        """
        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.settings.request_timeout,
        )
        response.raise_for_status()

        return {
            "url": url,
            "html": response.text,
            "status_code": str(response.status_code),
        }

    def scrape_page(self, url: str) -> Dict[str, str]:
        """
        Fetch and extract readable content from a webpage.
        """
        raw = self.fetch(url)
        soup = BeautifulSoup(raw["html"], "lxml")

        title = self._safe_text(soup.title.string if soup.title else "")
        body_text = self._extract_body_text(soup)

        return {
            "url": url,
            "title": title,
            "text": body_text,
            "html": raw["html"],
        }

    def extract_links(self, html: str, base_source: Optional[str] = None) -> list[str]:
        """
        Extract all links from HTML.
        """
        soup = BeautifulSoup(html, "lxml")
        links = []

        for tag in soup.find_all("a", href=True):
            href = tag["href"].strip()
            if href and href not in links:
                links.append(href)

        if base_source:
            print(f"[INFO] Extracted {len(links)} links from source={base_source}")

        return links

    @staticmethod
    def _extract_body_text(soup: BeautifulSoup) -> str:
        """
        Extract visible text from HTML.
        """
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return " ".join(text.split())

    @staticmethod
    def _safe_text(value: Optional[str]) -> str:
        """
        Normalize optional string values.
        """
        if not value:
            return ""
        return " ".join(value.split())
