# Interview Notes

## Project Summary

JobSeek AI Agent is an **Agentic AI system** that automates job discovery using LLM-based reasoning and tool orchestration.

It simulates how a human searches for jobs but does it autonomously and at scale.

## Key Highlights

- Agent-based architecture
- LLM-driven decision making
- Iterative query optimization
- Multi-source data aggregation
- Structured output generation


## Why This Project is Important

Traditional systems:
- static scrapers
- keyword matching

This system:
- reasons about queries
- adapts dynamically
- filters semantically

## Technical Challenges

### 1. Noisy Web Data
Solution:
- parser + normalizer + validator

### 2. Irrelevant Job Filtering
Solution:
- classifier agent + prompt engineering


### 3. Query Coverage Problem
Solution:
- query rewriting agent


### 4. Duplicate Jobs
Solution:
- deduplicator with URL + signature matching

### 5. System Stability
Solution:
- retry mechanism
- fallback data


## Design Decisions

- Agent + Tool separation
- Modular architecture
- JSON-based outputs
- Prompt-driven reasoning


## How This Differs From RAG Systems

- RAG → retrieve + generate
- This system → **act + reason + iterate**

It is closer to:
- AutoGPT
- LangGraph agents
- real-world AI automation systems


## Possible Improvements

- RL-based agent optimization
- job ranking model
- personalized recommendation system
- multi-language support
- real-time pipeline


## If Interviewer Asks “What Did You Learn?”

You can answer:

- how to design agent systems
- how to combine LLM + tools
- how to structure production AI projects
- how to handle real-world noisy data
- how to build scalable pipelines


## One-Line Pitch

> "I built an autonomous AI agent that searches, filters, and structures AI job opportunities using LLM reasoning and tool orchestration."


## Bonus: If Asked About Scaling

- add async scraping
- distributed workers
- message queues (Kafka)
- vector database for ranking
