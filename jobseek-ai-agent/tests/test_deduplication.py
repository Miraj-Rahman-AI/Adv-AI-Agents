from core import Deduplicator


def test_deduplicate_by_url():
    jobs = [
        {
            "title": "AI Engineer",
            "company": "A",
            "location": "Beijing",
            "job_url": "https://example.com/job/1",
        },
        {
            "title": "AI Engineer",
            "company": "A",
            "location": "Beijing",
            "job_url": "https://example.com/job/1",
        },
    ]

    deduped = Deduplicator.deduplicate(jobs)

    assert len(deduped) == 1


def test_deduplicate_by_signature_when_url_missing():
    jobs = [
        {
            "title": "Machine Learning Engineer",
            "company": "B",
            "location": "Shanghai",
            "job_url": "",
        },
        {
            "title": "Machine Learning Engineer",
            "company": "B",
            "location": "Shanghai",
            "job_url": "",
        },
        {
            "title": "NLP Engineer",
            "company": "B",
            "location": "Shanghai",
            "job_url": "",
        },
    ]

    deduped = Deduplicator.deduplicate(jobs)

    assert len(deduped) == 2


def test_find_duplicates():
    jobs = [
        {
            "title": "AI Engineer",
            "company": "A",
            "location": "Beijing",
            "job_url": "https://example.com/job/1",
        },
        {
            "title": "AI Engineer",
            "company": "A",
            "location": "Beijing",
            "job_url": "https://example.com/job/1",
        },
        {
            "title": "NLP Engineer",
            "company": "C",
            "location": "Shanghai",
            "job_url": "https://example.com/job/2",
        },
    ]

    duplicates = Deduplicator.find_duplicates(jobs)

    assert len(duplicates) == 1
    assert duplicates[0] == (0, 1)
