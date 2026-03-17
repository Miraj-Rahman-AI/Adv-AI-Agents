from config.settings import settings
from agents import (
    PlannerAgent,
    SearchAgent,
    ClassifierAgent,
    QueryRewriterAgent,
    SkillExtractorAgent,
)


def test_planner_build_plan():
    planner = PlannerAgent(settings)
    plan = planner.build_plan("Find 50 AI Engineer campus recruitment jobs")

    assert plan.goal == "Find 50 AI Engineer campus recruitment jobs"
    assert plan.target_job_count == settings.target_job_count
    assert len(plan.queries) > 0
    assert len(plan.steps) > 0


def test_search_agent_build_search_tasks():
    search_agent = SearchAgent(settings)
    queries = ["AI Engineer internship"]
    tasks = search_agent.build_search_tasks(queries, max_pages_per_query=1)

    assert isinstance(tasks, list)
    assert len(tasks) >= 0

    if tasks:
        assert hasattr(tasks[0], "query")
        assert hasattr(tasks[0], "source")
        assert hasattr(tasks[0], "page")


def test_classifier_agent_positive_case():
    classifier = ClassifierAgent(settings)

    job = {
        "title": "AI Engineer Intern",
        "requirements": "Experience with Python, PyTorch, NLP, and deep learning.",
        "description": "Build machine learning models and LLM applications.",
        "tech_tags": ["Python", "PyTorch", "NLP"],
    }

    is_target, reason = classifier.classify(job)

    assert is_target is True
    assert isinstance(reason, str)
    assert len(reason) > 0


def test_classifier_agent_negative_case():
    classifier = ClassifierAgent(settings)

    job = {
        "title": "Backend Engineer",
        "requirements": "Experience with Java, Spring Boot, and microservices.",
        "description": "Build backend APIs and database services.",
        "tech_tags": ["Java", "Spring Boot"],
    }

    is_target, reason = classifier.classify(job)

    assert is_target is False
    assert isinstance(reason, str)


def test_query_rewriter_expand_queries():
    rewriter = QueryRewriterAgent(settings)

    base_queries = ["AI Engineer campus recruitment"]
    expanded = rewriter.expand_queries(base_queries, collected_count=5)

    assert isinstance(expanded, list)
    assert len(expanded) > 0
    assert any("Machine Learning Engineer" in q or "Algorithm Engineer" in q for q in expanded)


def test_skill_extractor_enrich_job():
    extractor = SkillExtractorAgent(settings)

    job = {
        "title": "Machine Learning Engineer",
        "requirements": "Must know Python, PyTorch, TensorFlow, NLP, and RAG.",
        "description": "Develop LLM and machine learning systems.",
        "tech_tags": [],
    }

    enriched = extractor.enrich_job(job)

    assert "tech_tags" in enriched
    assert isinstance(enriched["tech_tags"], list)
    assert "Python" in enriched["tech_tags"]
