from config.settings import settings
from pipeline import PipelineState, JobPipeline


def test_pipeline_state_summary():
    state = PipelineState(
        goal="Find 50 AI Engineer campus recruitment jobs",
        target_job_count=50,
        max_iterations=10,
    )

    summary = state.summary()

    assert summary["goal"] == "Find 50 AI Engineer campus recruitment jobs"
    assert summary["target_job_count"] == 50
    assert summary["current_iteration"] == 0


def test_job_pipeline_process_jobs():
    pipeline = JobPipeline(settings)

    state = PipelineState(
        goal="Find 50 AI Engineer campus recruitment jobs",
        target_job_count=50,
        max_iterations=10,
    )

    state.raw_jobs = [
        {
            "title": "AI Engineer Intern",
            "company": "Example Tech",
            "location": "Beijing",
            "salary": "15K-20K",
            "tech_tags": [],
            "requirements": "Python, PyTorch, NLP, deep learning.",
            "description": "Develop machine learning and LLM systems.",
            "source": "indeed",
            "job_url": "https://example.com/job/1",
        },
        {
            "title": "Backend Engineer",
            "company": "Other Tech",
            "location": "Shanghai",
            "salary": "20K-30K",
            "tech_tags": [],
            "requirements": "Java, Spring Boot, API development.",
            "description": "Build backend services.",
            "source": "indeed",
            "job_url": "https://example.com/job/2",
        },
    ]

    final_jobs = pipeline.process_jobs(state)

    assert isinstance(final_jobs, list)
    assert len(final_jobs) == 1
    assert final_jobs[0]["title"] == "AI Engineer Intern"


def test_job_pipeline_parse_pages_to_jobs():
    pipeline = JobPipeline(settings)

    state = PipelineState(
        goal="Find 50 AI Engineer campus recruitment jobs",
        target_job_count=50,
        max_iterations=10,
    )

    pages = [
        {
            "url": "https://example.com/job/3",
            "title": "Machine Learning Engineer - Example Lab",
            "text": (
                "Company: Example Lab "
                "Location: Shenzhen "
                "Salary: 20K-35K "
                "Requirements: Python, TensorFlow, computer vision."
            ),
            "html": """
            <html>
                <head><title>Machine Learning Engineer - Example Lab</title></head>
                <body>
                    <h1>Machine Learning Engineer</h1>
                    <p>Company: Example Lab</p>
                    <p>Location: Shenzhen</p>
                    <p>Salary: 20K-35K</p>
                    <p>Requirements: Python, TensorFlow, computer vision.</p>
                </body>
            </html>
            """,
            "source": "lagou",
        }
    ]

    parsed_jobs = pipeline.parse_pages_to_jobs(pages, state)

    assert len(parsed_jobs) == 1
    assert parsed_jobs[0]["title"] != ""
    assert parsed_jobs[0]["source"] == "lagou"
