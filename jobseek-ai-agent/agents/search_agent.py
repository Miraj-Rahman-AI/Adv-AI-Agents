from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from config.constants import SUPPORTED_SOURCES
from config.settings import Settings


@dataclass
class SearchTask:
    """Represents a search job to run against a specific source."""
    query: str
    source: str
    page: int = 1


class SearchAgent:
    """
    Search agent responsible for constructing search tasks across multiple
    enabled job platforms.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def build_search_tasks(self, queries: List[str], max_pages_per_query: int = 1) -> List[SearchTask]:
        """
        Create search tasks for all enabled sources and provided queries.
        """
        tasks: List[SearchTask] = []

        enabled_sources = self._get_enabled_sources()
        for query in queries:
            for source in enabled_sources:
                for page in range(1, max_pages_per_query + 1):
                    tasks.append(SearchTask(query=query, source=source, page=page))

        return tasks

    def summarize_search_strategy(self, queries: List[str]) -> Dict[str, List[str]]:
        """
        Summarize how the search will be distributed across enabled sources.
        """
        enabled_sources = self._get_enabled_sources()
        return {source: queries for source in enabled_sources}

    def _get_enabled_sources(self) -> List[str]:
        """
        Get list of enabled supported sources from settings.
        """
        enabled = []
        for source in SUPPORTED_SOURCES:
            if self.settings.enabled_sites.get(source, False):
                enabled.append(source)
        return enabled

    @staticmethod
    def pretty_print(tasks: List[SearchTask]) -> None:
        """
        Print search tasks in readable format.
        """
        print("=" * 60)
        print("Search Tasks")
        print("=" * 60)
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. source={task.source} | page={task.page} | query={task.query}")
        print("=" * 60)
