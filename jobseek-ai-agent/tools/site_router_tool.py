from __future__ import annotations

from typing import Dict, List

from config.constants import SUPPORTED_SOURCES
from config.settings import Settings


class SiteRouterTool:
    """
    Route queries to enabled job platforms and manage source selection logic.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_enabled_sources(self) -> List[str]:
        """
        Return enabled sources in supported-source order.
        """
        enabled = []
        for source in SUPPORTED_SOURCES:
            if self.settings.enabled_sites.get(source, False):
                enabled.append(source)
        return enabled

    def route_queries(self, queries: List[str]) -> List[Dict[str, str]]:
        """
        Produce query-source routing tasks.
        """
        routes: List[Dict[str, str]] = []
        sources = self.get_enabled_sources()

        for query in queries:
            for source in sources:
                routes.append({"query": query, "source": source})

        return routes

    def fallback_source(self, failed_source: str) -> str | None:
        """
        Return the next available source if one source fails.
        """
        sources = self.get_enabled_sources()

        if failed_source not in sources:
            return sources[0] if sources else None

        idx = sources.index(failed_source)
        if idx + 1 < len(sources):
            return sources[idx + 1]

        return None

    @staticmethod
    def pretty_print(routes: List[Dict[str, str]]) -> None:
        """
        Pretty print routing decisions.
        """
        print("=" * 60)
        print("Site Routing Tasks")
        print("=" * 60)
        for idx, route in enumerate(routes, start=1):
            print(f"{idx}. source={route['source']} | query={route['query']}")
        print("=" * 60)
