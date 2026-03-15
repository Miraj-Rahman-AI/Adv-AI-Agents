from __future__ import annotations

import re
from typing import Any, Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from config.constants import JOB_FIELDS


class ParserTool:
    """
    Parse raw page content or raw scraped job records into normalized
    structured job dictionaries.

    This starter parser uses simple heuristics. Later, you can replace or
    augment it with:
    - LLM-based extraction
    - site-specific parsers
    - CSS/XPath selector-based extraction
    """

    SALARY_PATTERN = re.compile(
        r"(\d{1,3}[kK]?\s*[-~至]\s*\d{1,3}[kK]?)|(\d{1,3}\s*-\s*\d{1,3}\s*[kK]?)"
    )

    def parse_job_page(self, page: Dict[str, str], source: str | None = None) -> Dict[str, Any]:
        """
        Parse a single webpage into a structured job record.
        """
        html = page.get("html", "")
        url = page.get("url", "")
        text = page.get("text", "")
        fallback_title = page.get("title", "")

        soup = BeautifulSoup(html, "lxml")

        title = self._extract_title(soup, fallback_title=fallback_title)
        salary = self._extract_salary(text)
        location = self._extract_location(text)
        company = self._extract_company(text, fallback_title=fallback_title)
        requirements = self._extract_requirements(text)

        parsed = {
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "tech_tags": [],
            "requirements": requirements,
            "description": text[:4000],
            "source": source or self._infer_source_from_url(url),
            "job_url": url,
        }

        return self._normalize_job(parsed)

    def parse_search_results_links(self, search_html: str) -> List[str]:
        """
        Extract candidate links from a search result page.
        """
        soup = BeautifulSoup(search_html, "lxml")
        links: List[str] = []

        for tag in soup.find_all("a", href=True):
            href = tag["href"].strip()

            if not href:
                continue

            if self._looks_like_job_link(href) and href not in links:
                links.append(href)

        return links

    def parse_raw_job_record(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a raw job dictionary to the standard schema.
        """
        parsed = {
            "title": raw_job.get("title", ""),
            "company": raw_job.get("company", ""),
            "location": raw_job.get("location", ""),
            "salary": raw_job.get("salary", ""),
            "tech_tags": raw_job.get("tech_tags", []),
            "requirements": raw_job.get("requirements", ""),
            "description": raw_job.get("description", ""),
            "source": raw_job.get("source", ""),
            "job_url": raw_job.get("job_url", raw_job.get("url", "")),
        }

        return self._normalize_job(parsed)

    def _normalize_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure consistent schema and field defaults.
        """
        normalized: Dict[str, Any] = {}

        for field in JOB_FIELDS:
            normalized[field] = job.get(field, "" if field != "tech_tags" else [])

        if not isinstance(normalized["tech_tags"], list):
            normalized["tech_tags"] = []

        return normalized

    @staticmethod
    def _extract_title(soup: BeautifulSoup, fallback_title: str = "") -> str:
        """
        Extract best-effort page title.
        """
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)

        if fallback_title:
            return fallback_title.strip()

        if soup.title and soup.title.string:
            return soup.title.string.strip()

        return ""

    @staticmethod
    def _extract_salary(text: str) -> str:
        """
        Extract salary expression from page text.
        """
        match = ParserTool.SALARY_PATTERN.search(text)
        return match.group(0).strip() if match else ""

    @staticmethod
    def _extract_location(text: str) -> str:
        """
        Best-effort location extraction.
        """
        candidates = [
            "Beijing", "Shanghai", "Shenzhen", "Guangzhou", "Hangzhou",
            "Chengdu", "Nanjing", "Wuhan", "Xi'an", "Suzhou",
            "北京", "上海", "深圳", "广州", "杭州", "成都", "南京", "武汉", "西安", "苏州",
        ]
        lowered = text.lower()
        for city in candidates:
            if city.lower() in lowered:
                return city
        return ""

    @staticmethod
    def _extract_company(text: str, fallback_title: str = "") -> str:
        """
        Very simple heuristic for company extraction.
        """
        patterns = [
            r"Company[:：]\s*([^\n|]{2,80})",
            r"公司[:：]\s*([^\n|]{2,80})",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip()

        if "-" in fallback_title:
            parts = [p.strip() for p in fallback_title.split("-")]
            if len(parts) >= 2:
                return parts[-1]

        return ""

    @staticmethod
    def _extract_requirements(text: str) -> str:
        """
        Best-effort extraction of requirement-related content.
        """
        lowered = text.lower()

        markers = [
            "requirements",
            "qualification",
            "job requirements",
            "岗位要求",
            "任职要求",
            "职位要求",
        ]

        for marker in markers:
            idx = lowered.find(marker.lower())
            if idx != -1:
                snippet = text[idx: idx + 800]
                return " ".join(snippet.split())

        return " ".join(text[:800].split())

    @staticmethod
    def _infer_source_from_url(url: str) -> str:
        """
        Infer source site from URL hostname.
        """
        hostname = urlparse(url).netloc.lower()

        if "indeed" in hostname:
            return "indeed"
        if "linkedin" in hostname:
            return "linkedin"
        if "lagou" in hostname:
            return "lagou"
        if "zhipin" in hostname:
            return "zhipin"
        if "liepin" in hostname:
            return "liepin"

        return ""

    @staticmethod
    def _looks_like_job_link(href: str) -> bool:
        """
        Heuristic filter to identify likely job URLs.
        """
        href_lower = href.lower()
        patterns = [
            "job",
            "jobs",
            "position",
            "career",
            "careers",
            "zhaopin",
            "geek/job",
        ]
        return any(pattern in href_lower for pattern in patterns)
