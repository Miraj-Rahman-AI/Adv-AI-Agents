# JobSeek AI Agent
### Autonomous Agentic AI System for AI Engineer Job Discovery

JobSeek AI Agent is an **Agentic AI-powered automation system** that autonomously searches, collects, filters, and structures **AI Engineer campus recruitment and internship job postings** from multiple recruitment platforms. Unlike traditional web crawlers, this system uses **Large Language Models (LLMs)** combined with **tool orchestration and autonomous planning** to perform complex job discovery workflows. The agent can dynamically generate search queries, scrape job listings, analyze job descriptions, extract relevant technical skills, and output structured job datasets. This project demonstrates how **Agentic AI systems can automate real-world information gathering tasks**, showcasing capabilities such as autonomous task planning, tool usage, semantic reasoning, and iterative search optimization.


# Project Motivation
Searching for AI Engineer job opportunities across multiple platforms is time-consuming and inefficient. Each recruitment website presents job information differently, requiring manual filtering and comparison. The goal of this project is to build an **intelligent AI agent that automates the entire job search pipeline**, allowing users to automatically collect and organize AI-related job opportunities.

JobSeek AI Agent can automatically:
- Search multiple recruitment websites
- Discover AI-related job postings
- Extract key job information
- Filter relevant AI Engineer roles
- Remove duplicate job listings
- Generate structured job datasets
This project demonstrates the potential of **Agentic AI architectures in real-world automation scenarios**.


# Key Features
## Autonomous Task Planning

The agent begins by interpreting the user goal and decomposing it into smaller executable tasks.

Example user goal: ```Find 50 AI Engineer campus recruitment jobs```


The agent automatically plans the workflow: ```Search → Scrape → Parse → Filter → Deduplicate → Export```

This planning capability allows the agent to operate autonomously without manual intervention.


## Multi-Platform Job Discovery

The agent collects job postings from **multiple recruitment platforms** such as:

- LinkedIn
- Indeed
- Lagou
- Zhipin
- Liepin
- Company career websites

If one platform fails or returns insufficient results, the agent automatically switches to another source.


## Iterative Search Strategy

If the collected job postings are fewer than the required number, the agent dynamically expands its search queries.

Example query expansion strategy:
- AI Engineer
- Machine Learning Engineer
- Algorithm Engineer
- LLM Engineer
- Deep Learning Engineer
- Data Scientist

This iterative process ensures the agent eventually gathers the required number of job postings.


## LLM-Based Semantic Job Filtering

The system uses **Large Language Models (LLMs)** to determine whether a job posting truly belongs to the AI engineering domain. The classifier analyzes job descriptions and identifies relevant technical domains such as:
- Machine Learning
- Deep Learning
- Natural Language Processing
- Computer Vision
- Large Language Models
- Data Science

This prevents the agent from collecting unrelated roles such as backend engineering or general software development positions.

## Automatic Technical Skill Extraction
The agent extracts **technical skill tags** from job descriptions using semantic analysis.
Example extracted skills include:
- Python
- PyTorch
- TensorFlow
- Transformers
- NLP
- Computer Vision
- Recommendation Systems
These tags help create structured technical skill profiles for each job posting.

## Data Cleaning and Deduplication
The system automatically cleans and standardizes collected job data by performing:
- Duplicate job detection
- Missing data handling
- Field normalization
- Structured formatting
This ensures that the final dataset is clean, consistent, and ready for analysis.

## Structured Output Generation
The final job dataset is exported in structured formats:
- JSON
- CSV

Example output format:

```json
{
"title": "AI Engineer",
"company": "Example Tech",
"location": "Beijing",
"salary": "20K-35K",
"tech_tags": ["Python", "PyTorch", "NLP"],
"requirements": "Experience with machine learning and deep learning frameworks",
"source": "LinkedIn",
"job_url": "https://example.com/job"
}
```

## System Architecture
JobSeek AI Agent follows an Agentic AI workflow architecture, where an intelligent agent coordinates multiple tools and reasoning modules.

<p align="center">
  <img src="assets/Agentic Al Job Search System.png" width="95%">
</p>

# Technology Stack

## Programming Language
- Python

## Agent Frameworks
- LangChain
- LangGraph
- OpenAI Tool Calling
- ReAct Agents

## Web Data Collection
- Selenium
- BeautifulSoup
- Requests

## Data Processing
- Pandas
- Regex
- JSON

## AI Models
- OpenAI GPT
- Local LLMs (optional)


## Repository Structure
```
jobseek-ai-agent/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py
├── assets/
│   └── Automated Pipeline for Finding Al Engineer Jobs.png
│
├── config/
│   ├── settings.py
│   └── constants.py
│
├── agents/
│   ├── __init__.py
│   ├── planner_agent.py
│   ├── search_agent.py
│   ├── classifier_agent.py
│   ├── query_rewriter_agent.py
│   └── skill_extractor_agent.py
│
├── tools/
│   ├── web_search_tool.py
│   ├── scraper_tool.py
│   ├── parser_tool.py
│   ├── exporter_tool.py
│   └── site_router_tool.py
│
├── pipeline/
│   ├── job_pipeline.py
│   ├── orchestrator.py
│   └── state.py
│
├── core/
│   ├── models.py
│   ├── schemas.py
│   ├── deduplicator.py
│   ├── validators.py
│   └── normalizer.py
│
├── prompts/
│   ├── classify_job.txt
│   ├── extract_skills.txt
│   └── rewrite_query.txt
│
├── utils/
│   ├── logger.py
│   ├── helpers.py
│   ├── retry.py
│   └── io.py
│
├── data/
│   ├── raw/
│   │   └── jobs_raw.json
│   ├── processed/
│   │   └── jobs_clean.json
│   └── sample/
│       └── sample_jobs.json
│
├── output/
│   ├── jobs.csv
│   ├── jobs.json
│   └── report.md
│
├── tests/
│   ├── test_agents.py
│   ├── test_parser.py
│   ├── test_deduplication.py
│   └── test_pipeline.py
│
├── examples/
│   ├── demo_run.py
│   └── example_output.json
│
└── docs/
    ├── architecture.md
    ├── workflow.md
    └── interview_notes.md
```

## Installation
Clone the repository:
```
git clone https://github.com/Miraj-Rahman-AI/Adv-AI-Agents/edit/main/jobseek-ai-agent.git
cd jobseek-ai-agent
```
Create a virtual environment:
```
python -m venv venv
```
Activate the environment:
```
source venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```
### Running the Agent
Run the autonomous job search system:
```
python main.py
```
The agent will automatically perform the following steps:
- Generate job search queries
- Collect job postings from multiple platforms
- Filter AI-related job roles
- Extract structured job information
- Remove duplicate listings
- Export results as structured datasets

Generated datasets will be saved in:
```
output/jobs.csv
output/jobs.json
```
## Example Output
Example job entry:
```
Title: AI Engineer
Company: Tencent
Location: Shenzhen
Salary: 25K-40K
Tech Tags: Python, PyTorch, NLP, Transformers
Source: Lagou
URL: https://example-job-url
```
# Agent Capabilities Demonstrated
This project demonstrates several core **Agentic AI capabilities**:
- Autonomous task planning
- External tool orchestration
- LLM-powered semantic reasoning
- Iterative query optimization
- Multi-source information aggregation
- Structured data generation

# Possible Extensions
Future improvements could include:
- Real-time job monitoring agents
- AI-powered job recommendation systems
- Resume-job matching automation
- Skill gap analysis for candidates
- Multi-language job discovery
- Autonomous job application assistants


# Use Cases
- Automated job search assistants
- AI recruitment intelligence tools
- Career analytics platforms
- Agentic AI research experiments


##  Author
**[Miraj Rahman](https://github.com/Miraj-Rahman-AI)**  
AI Researcher | Autonomous Agents | RAG Systems | Trustworthy AI


##  Support
If this project supports your research or learning,
please consider giving it a ⭐ on GitHub.

## ⚠️ License & Usage Restriction
© 2026 Mirage-AI. All rights reserved.
No permission is granted to use, modify, distribute, or reproduce this software in any form. This repository is provided for **viewing purposes only**. Unauthorized use, reproduction, or distribution of this code or its concepts may result in legal action.

