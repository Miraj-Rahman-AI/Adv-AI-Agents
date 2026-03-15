from __future__ import annotations

# ============================================================
# Project-level constants for JobSeek AI Agent
# ============================================================

PROJECT_NAME = "JobSeek AI Agent"
PROJECT_VERSION = "0.1.0"
PROJECT_DESCRIPTION = (
    "An Agentic AI system for autonomous AI Engineer job discovery, "
    "semantic filtering, and structured output generation."
)

# ============================================================
# Default search queries
# ============================================================

DEFAULT_JOB_QUERIES = [
    "AI Engineer campus recruitment",
    "AI Engineer internship",
    "Machine Learning Engineer internship",
    "Algorithm Engineer campus recruitment",
    "LLM Engineer internship",
    "Deep Learning Engineer campus recruitment",
    "NLP Engineer internship",
    "Computer Vision Engineer internship",
]

QUERY_EXPANSION_TERMS = [
    "fresh graduate",
    "new grad",
    "campus",
    "internship",
    "校招",
    "实习",
    "应届生",
    "算法工程师",
    "机器学习工程师",
    "大模型工程师",
    "人工智能工程师",
]

# ============================================================
# Job field schema
# ============================================================

JOB_FIELDS = [
    "title",
    "company",
    "location",
    "salary",
    "tech_tags",
    "requirements",
    "source",
    "job_url",
]

REQUIRED_JOB_FIELDS = [
    "title",
    "company",
    "source",
    "job_url",
]

# ============================================================
# AI-related keywords for simple rule-based screening
# ============================================================

AI_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "ml",
    "nlp",
    "natural language processing",
    "computer vision",
    "cv",
    "llm",
    "large language model",
    "transformer",
    "recommendation system",
    "pytorch",
    "tensorflow",
    "rag",
    "agent",
    "multimodal",
    "generative ai",
]

NON_TARGET_ROLE_KEYWORDS = [
    "backend",
    "front-end",
    "frontend",
    "full stack",
    "devops",
    "qa",
    "test engineer",
    "hr",
    "sales",
    "product manager",
    "operations",
]

# ============================================================
# Technical tag vocabulary
# ============================================================

TECH_TAG_VOCAB = [
    "Python",
    "PyTorch",
    "TensorFlow",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "OpenCV",
    "NLP",
    "Computer Vision",
    "LLM",
    "RAG",
    "Transformers",
    "LangChain",
    "LangGraph",
    "CUDA",
    "MLOps",
    "Recommendation Systems",
    "Deep Learning",
    "Machine Learning",
    "Data Mining",
]

# ============================================================
# Retry and pipeline control
# ============================================================

MAX_RETRY_ATTEMPTS = 3
RETRY_WAIT_SECONDS = 2
DEFAULT_REQUEST_TIMEOUT = 20
DEFAULT_MAX_ITERATIONS = 10
DEFAULT_TARGET_JOB_COUNT = 50

# ============================================================
# Supported job sources
# ============================================================

SUPPORTED_SOURCES = [
    "linkedin",
    "indeed",
    "lagou",
    "zhipin",
    "liepin",
]

# ============================================================
# Export filenames
# ============================================================

DEFAULT_RAW_FILENAME = "jobs_raw.json"
DEFAULT_CLEAN_FILENAME = "jobs_clean.json"
DEFAULT_OUTPUT_JSON = "jobs.json"
DEFAULT_OUTPUT_CSV = "jobs.csv"
DEFAULT_OUTPUT_REPORT = "report.md"

# ============================================================
# Prompt task identifiers
# ============================================================

PROMPT_CLASSIFY_JOB = "classify_job"
PROMPT_EXTRACT_SKILLS = "extract_skills"
PROMPT_REWRITE_QUERY = "rewrite_query"
