from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
from urllib.parse import quote_plus

import requests

from config.settings import Settings


@dataclass
class SearchResult:
    """Represents a single search result item."""
    title: str
    url: str
    snippet: str
    source: str


class WebSearchTool:
    """
    Lightweight search tool for generating search URLs and optionally
    retrieving simple HTML results.

    This starter version is intentionally conservative:
    - It can generate site-specific search URLs
    - It can fetch HTML pages
    - It does not depend on an external commercial search API

    Later, you can replace this with:
    - SerpAPI
    - Tavily
    - Brave Search API
    - Google Custom Search API
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.headers = {
            "User-Agent": self.settings.user_agent,
        }

    def build_search_url(self, query: str, source: str, page: int = 1) -> str:
        """
        Build a source-specific search URL.
        """
        encoded_query = quote_plus(query)

        routing = {
            "indeed": f"https://www.indeed.com/jobs?q={encoded_query}&start={(page - 1) * 10}",
            "linkedin": f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}&start={(page - 1) * 25}",
            "lagou": f"https://www.lagou.com/wn/jobs?kd={encoded_query}&pn={page}",
            "zhipin": f"https://www.zhipin.com/web/geek/job?query={encoded_query}&page={page}",
            "liepin": f"https://www.liepin.com/zhaopin/?key={encoded_query}&curPage={page}",
        }

        if source not in routing:
            raise ValueError(f"Unsupported search source: {source}")

        return routing[source]

    def fetch_search_page(self, query: str, source: str, page: int = 1) -> Dict[str, str]:
        """
        Fetch raw HTML for a given source-specific search page.
        """
        url = self.build_search_url(query=query, source=source, page=page)

        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.settings.request_timeout,
        )
        response.raise_for_status()

        return {
            "source": source,
            "query": query,
            "page": str(page),
            "url": url,
            "html": response.text,
        }

    def batch_build_urls(self, queries: List[str], sources: List[str], max_pages: int = 1) -> List[Dict[str, str]]:
        """
        Build multiple search URLs without fetching them.
        """
        tasks: List[Dict[str, str]] = []

        for query in queries:
            for source in sources:
                for page in range(1, max_pages + 1):
                    tasks.append(
                        {
                            "query": query,
                            "source": source,
                            "page": str(page),
                            "url": self.build_search_url(query, source, page),
                        }
                    )
        return tasks

    @staticmethod
    def pretty_print(tasks: List[Dict[str, str]]) -> None:
        """
        Pretty print generated search tasks.
        """
        print("=" * 60)
        print("Generated Search URLs")
        print("=" * 60)
        for idx, task in enumerate(tasks, start=1):
            print(
                f"{idx}. source={task['source']} | page={task['page']} | "
                f"query={task['query']}\n   -> {task['url']}"
            )
        print("=" * 60)
