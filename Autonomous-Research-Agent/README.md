# Autonomous-Research-Agent
### An Advanced Multi-Agent AI System for Autonomous Academic Research, Paper Analysis, and Knowledge Synthesis
Autonomous-Research-Agent is a production-grade, research-oriented AI agent system designed to autonomously discover, analyze, and synthesize academic knowledge from scientific literature. Built using modern agent orchestration frameworks and large language models, this system enables fully automated academic research workflows from paper discovery to structured report generation.

This project is designed for:
- AI researchers
- PhD students
- Engineers building research agents
- Autonomous AI system developers
- Next-generation RAG and agentic AI research


## Key Capabilities
### Autonomous Paper Discovery
- Searches relevant papers from arXiv
- Extracts metadata and abstracts
- Filters papers based on research goals

### Intelligent Paper Analysis
- Converts PDF → Markdown
- Section-wise summarization
- Key contribution extraction
- Strength & limitation analysis

### Multi-Agent Research Workflow
- Specialized agents collaborate:
- Research planner agent
- Paper search agent
- Paper analyzer agent
- Report generator agent
- Task evaluator agent

### Goal-Oriented Research Reasoning
- Clarifies research objective via interactive reasoning
- Decomposes complex research goals
- Iteratively improves research results

### Automated Research Report Generation
- Structured academic report
- Bullet-point findings
- Key insights extraction
- Literature synthesis

## System Architecture
![Autonomous Research Agent](assets/Autonomous-Research-Agent%20Framework.png)

 ## Tech Stack
- Python 3.11+
- LangGraph (multi-agent orchestration)
- LangChain
- OpenAI / Anthropic / Cohere LLMs
- arXiv API
- Jina Reader
- Markdown processing pipeline
- VS Code + LangGraph Studio

  ##  Project Structure
 ``` 
Autonomous-Research-Agent/
│
├── researche_agent/
│   ├── agent/              # Multi-agent implementations
│   ├── chains/             # LLM reasoning chains
│   ├── searcher/           # arXiv search module
│   ├── service/            # PDF → Markdown + storage
│   ├── models/             # Data models
│   └── settings.py
│
├── fixtures/               # Test papers & samples
├── storage/markdown/       # Processed papers
├── logs/                   # Logs
├── langgraph.json          # LangGraph config
├── pyproject.toml
└── README.md
```

## Installation
### 1. Clone Repository
```
git clone https://github.com/Fantasy-Tech-Developer/Autonomous-Research-Agent.git
cd Autonomous-Research-Agent
```

### 2. Install uv (dependency manager)
```
pip install uv
```

### 3. Install dependencies
```
uv sync
```

## Environment Setup

Copy environment file:
```
cp .env.sample .env
```
Set API keys:
```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
COHERE_API_KEY=
JINA_API_KEY=
LANGSMITH_API_KEY= (optional)
```
## Running the System
#### Launch LangGraph Studio
```
uv run langgraph dev --no-reload
```
Open:
```
http://localhost:8123
```
Enter research goal → Run agent → Watch autonomous research process.

## Test Individual Agents
### Paper Analysis Agent
```
uv run python -m arxiv_researcher.agent.paper_analyzer_agent fixtures/sample.md
```
### Paper Search Agent
```
uv run python -m arxiv_researcher.agent.paper_search_agent
```

## Example Research Tasks
- "Find latest research on autonomous LLM agents"
- "Survey papers on RAG security"
- "Analyze multimodal LLM research trends"
- "Summarize top 10 papers on AI safety"

## Research & Engineering Goals

- Autonomous-Research-Agent aims to become a next-generation research intelligence system.
- Future directions:
- Self-improving research agents
- Multi-paper reasoning
- Research memory graph
- Citation network analysis
- AI scientist agents
- Fully autonomous literature review system

##  Author
**[Miraj Rahman](https://github.com/Miraj-Rahman-AI)**  
AI Researcher | Autonomous Agents | RAG Systems | Trustworthy AI



##  Support
If this project supports your research or learning,
please consider giving it a ⭐ on GitHub.

## ⚠️ License & Usage Restriction

© 2026 Fantasy Tech Developer. All rights reserved.

This project and its source code are the intellectual property of the author.

❌ Strictly prohibited:
- Copying this code
- Reusing any part of this project
- Modifying or redistributing
- Using for commercial or research purposes
- Training AI models on this repository
- Reproducing architecture, design, or implementation

No permission is granted to use, modify, distribute, or reproduce this software in any form.

This repository is provided for **viewing purposes only**.

Unauthorized use, reproduction, or distribution of this code or its concepts may result in legal action.

