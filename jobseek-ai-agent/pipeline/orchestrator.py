from __future__ import annotations

from typing import Any, Dict, List

from agents import PlannerAgent, QueryRewriterAgent, SearchAgent
from config.settings import Settings
from pipeline.job_pipeline import JobPipeline
from pipeline.state import PipelineState
from tools import ScraperTool, SiteRouterTool, WebSearchTool


class JobSeekOrchestrator:
    """
    Main orchestrator for the Agentic AI job search system.

    High-level workflow:
    1. Build plan
    2. Generate search tasks
    3. Fetch search pages
    4. Scrape / parse candidate pages
    5. Process and classify jobs
    6. Rewrite queries if results are insufficient
    7. Export final outputs
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.planner = PlannerAgent(settings)
        self.search_agent = SearchAgent(settings)
        self.query_rewriter = QueryRewriterAgent(settings)

        self.web_search_tool = WebSearchTool(settings)
        self.scraper_tool = ScraperTool(settings)
        self.site_router_tool = SiteRouterTool(settings)

        self.job_pipeline = JobPipeline(settings)

    def run(self, goal: str) -> PipelineState:
        """
        Execute the end-to-end orchestration loop.
        """
        state = PipelineState(
            goal=goal,
            target_job_count=self.settings.target_job_count,
            max_iterations=self.settings.max_iterations,
        )

        plan = self.planner.build_plan(goal)
        state.initial_queries = plan.queries.copy()
        state.active_queries = plan.queries.copy()

        state.log(f"[PLAN] Goal='{goal}'")
        state.log(f"[PLAN] Initial queries={state.initial_queries}")

        while not state.should_stop():
            state.next_iteration()
            state.log(f"[ITERATION] Starting iteration {state.current_iteration}")

            current_queries = self._select_iteration_queries(state)
            if not current_queries:
                state.log("[STOP] No more queries available.")
                break

            enabled_sources = self.site_router_tool.get_enabled_sources()
            if not enabled_sources:
                state.add_error("[CONFIG] No enabled job sources found.")
                break

            search_tasks = self._build_search_tasks(current_queries)
            for task in search_tasks:
                state.add_search_task(task)

            pages = self._collect_pages(search_tasks, state)
            for page in pages:
                state.add_page(page)

            raw_jobs = self.job_pipeline.parse_pages_to_jobs(pages, state)
            for job in raw_jobs:
                state.add_raw_job(job)

            final_jobs = self.job_pipeline.process_jobs(state)

            state.log(
                f"[RESULT] iteration={state.current_iteration} "
                f"| raw_jobs={len(state.raw_jobs)} "
                f"| processed_jobs={len(state.processed_jobs)} "
                f"| final_jobs={len(final_jobs)}"
            )

            if len(final_jobs) >= self.settings.target_job_count:
                state.log("[SUCCESS] Target job count reached.")
                break

            expanded_queries = self.query_rewriter.expand_queries(
                base_queries=current_queries,
                collected_count=len(final_jobs),
            )
            next_batch = self.query_rewriter.select_next_batch(expanded_queries, limit=10)
            state.active_queries.extend(
                [q for q in next_batch if q not in state.attempted_queries and q not in state.active_queries]
            )

            state.log(
                f"[REWRITE] expanded={len(expanded_queries)} "
                f"| next_batch={len(next_batch)} "
                f"| active_queries={len(state.active_queries)}"
            )

            if state.current_iteration >= self.settings.max_iterations:
                state.log("[STOP] Reached maximum iterations.")
                break

        export_paths = self.job_pipeline.export_results(state.final_jobs)
        state.log(f"[EXPORT] {export_paths}")

        return state

    def _select_iteration_queries(self, state: PipelineState, limit: int = 5) -> List[str]:
        """
        Select the next batch of queries that have not yet been attempted.
        """
        selected: List[str] = []

        for query in state.active_queries:
            if query in state.attempted_queries:
                continue

            selected.append(query)
            state.mark_query_attempted(query)

            if len(selected) >= limit:
                break

        return selected

    def _build_search_tasks(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Build search tasks using SearchAgent.
        """
        max_pages_per_query = 1
        tasks = self.search_agent.build_search_tasks(
            queries=queries,
            max_pages_per_query=max_pages_per_query,
        )

        return [
            {
                "query": task.query,
                "source": task.source,
                "page": task.page,
            }
            for task in tasks
        ]

    def _collect_pages(self, tasks: List[Dict[str, Any]], state: PipelineState) -> List[Dict[str, Any]]:
        """
        Collect pages from search tasks.

        This starter implementation supports two modes:
        - conservative mode: fetch search result pages only
        - demo fallback: create synthetic pages if live scraping fails

        In a production version, this stage should:
        1. fetch search pages
        2. parse candidate job links
        3. fetch actual job detail pages
        """
        pages: List[Dict[str, Any]] = []

        for task in tasks:
            query = task["query"]
            source = task["source"]
            page_num = task["page"]

            try:
                search_page = self.web_search_tool.fetch_search_page(
                    query=query,
                    source=source,
                    page=page_num,
                )

                # For now, treat search page itself as a parseable page
                pages.append(
                    {
                        "url": search_page["url"],
                        "title": f"{query} - {source}",
                        "text": self._build_demo_text(query=query, source=source),
                        "html": search_page["html"],
                        "source": source,
                    }
                )

                state.log(
                    f"[FETCH] source={source} | page={page_num} | query='{query}'"
                )

            except Exception as exc:
                state.add_error(
                    f"[FETCH_ERROR] source={source} | page={page_num} "
                    f"| query='{query}' | error={exc}"
                )

                # Demo fallback page to keep pipeline runnable in restricted cases
                fallback_page = self._build_fallback_page(query=query, source=source, page=page_num)
                pages.append(fallback_page)

                state.log(
                    f"[FALLBACK] Used synthetic page for source={source} "
                    f"| page={page_num} | query='{query}'"
                )

        return pages

    @staticmethod
    def _build_demo_text(query: str, source: str) -> str:
        """
        Build fallback-like readable text for starter parsing.
        """
        return (
            f"Title: {query} | Company: Example Tech | Location: Beijing | "
            f"Salary: 20K-30K | Requirements: Python, PyTorch, NLP, transformer models, "
            f"machine learning, deep learning. Source: {source}."
        )

    @staticmethod
    def _build_fallback_page(query: str, source: str, page: int) -> Dict[str, str]:
        """
        Build a synthetic page when a live fetch fails, so the end-to-end
        system can still be demonstrated.
        """
        title = f"{query} - Demo Role - {source}"
        text = (
            f"Company: Demo AI Lab | Location: Shanghai | Salary: 18K-28K | "
            f"Requirements: Python, PyTorch, NLP, computer vision, large language models. "
            f"Job Title: {query}"
        )
        html = f"""
        <html>
          <head><title>{title}</title></head>
          <body>
            <h1>{query}</h1>
            <p>Company: Demo AI Lab</p>
            <p>Location: Shanghai</p>
            <p>Salary: 18K-28K</p>
            <p>Requirements: Python, PyTorch, NLP, computer vision, large language models.</p>
          </body>
        </html>
        """.strip()

        return {
            "url": f"https://demo.{source}.com/search?page={page}&q={query.replace(' ', '+')}",
            "title": title,
            "text": text,
            "html": html,
            "source": source,
        }


def run_jobseek_agent(settings: Settings, goal: str) -> PipelineState:
    """
    Convenience function for running the orchestrator.
    """
    orchestrator = JobSeekOrchestrator(settings)
    return orchestrator.run(goal)
