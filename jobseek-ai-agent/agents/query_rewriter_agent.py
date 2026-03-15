from __future__ import annotations

from typing import List, Set

from config.constants import QUERY_EXPANSION_TERMS
from config.settings import Settings


class QueryRewriterAgent:
    """
    Rewrites or expands search queries when initial search results
    are insufficient.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def expand_queries(self, base_queries: List[str], collected_count: int) -> List[str]:
        """
        Expand queries based on current collection status.

        If collected_count is far below target, generate broader variants.
        """
        if collected_count >= self.settings.target_job_count:
            return []

        expanded: Set[str] = set()

        for query in base_queries:
            expanded.add(query)

            for suffix in QUERY_EXPANSION_TERMS[:6]:
                expanded.add(f"{query} {suffix}")

            if "AI Engineer" in query:
                expanded.add(query.replace("AI Engineer", "Machine Learning Engineer"))
                expanded.add(query.replace("AI Engineer", "Algorithm Engineer"))
                expanded.add(query.replace("AI Engineer", "LLM Engineer"))
                expanded.add(query.replace("AI Engineer", "Deep Learning Engineer"))

            if "campus recruitment" in query:
                expanded.add(query.replace("campus recruitment", "internship"))
                expanded.add(query.replace("campus recruitment", "new grad"))

            if "internship" in query:
                expanded.add(query.replace("internship", "campus recruitment"))

        # Remove duplicates while preserving deterministic order
        ordered = sorted(expanded)
        return ordered

    @staticmethod
    def select_next_batch(expanded_queries: List[str], limit: int = 10) -> List[str]:
        """
        Select the next batch of rewritten queries to avoid over-expansion.
        """
        return expanded_queries[:limit]
