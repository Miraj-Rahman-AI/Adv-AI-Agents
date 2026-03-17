from tools import ParserTool


def test_parse_raw_job_record():
    parser = ParserTool()

    raw_job = {
        "title": "AI Engineer",
        "company": "Example Tech",
        "location": "Beijing",
        "salary": "20K-30K",
        "tech_tags": ["Python", "PyTorch"],
        "requirements": "Experience with NLP and deep learning.",
        "description": "Build machine learning pipelines.",
        "source": "indeed",
        "job_url": "https://example.com/job/1",
    }

    parsed = parser.parse_raw_job_record(raw_job)

    assert parsed["title"] == "AI Engineer"
    assert parsed["company"] == "Example Tech"
    assert parsed["location"] == "Beijing"
    assert parsed["source"] == "indeed"
    assert parsed["job_url"] == "https://example.com/job/1"


def test_parse_job_page():
    parser = ParserTool()

    page = {
        "url": "https://example.com/job/2",
        "title": "AI Engineer Intern - Example AI Lab",
        "text": (
            "Company: Example AI Lab "
            "Location: Shanghai "
            "Salary: 15K-25K "
            "Requirements: Python, PyTorch, NLP, transformer models."
        ),
        "html": """
        <html>
            <head><title>AI Engineer Intern - Example AI Lab</title></head>
            <body>
                <h1>AI Engineer Intern</h1>
                <p>Company: Example AI Lab</p>
                <p>Location: Shanghai</p>
                <p>Salary: 15K-25K</p>
                <p>Requirements: Python, PyTorch, NLP, transformer models.</p>
            </body>
        </html>
        """,
        "source": "indeed",
    }

    job = parser.parse_job_page(page, source="indeed")

    assert job["title"] != ""
    assert job["salary"] != ""
    assert job["source"] == "indeed"
    assert job["job_url"] == "https://example.com/job/2"


def test_parse_search_results_links():
    parser = ParserTool()

    html = """
    <html>
        <body>
            <a href="https://example.com/jobs/123">Job 1</a>
            <a href="https://example.com/about">About</a>
            <a href="https://example.com/career/456">Job 2</a>
            <a href="https://example.com/contact">Contact</a>
        </body>
    </html>
    """

    links = parser.parse_search_results_links(html)

    assert isinstance(links, list)
    assert "https://example.com/jobs/123" in links
    assert "https://example.com/career/456" in links
