# System Workflow

## Overview

This document explains how JobSeek AI Agent processes a user goal into structured job results.

## Step-by-Step Execution Flow

### Step 1: User Input

User provides a goal: ```Find 50 AI Engineer internship jobs```


### Step 2: Planning

PlannerAgent:
- understands intent
- generates search queries

Example:
- AI Engineer internship
- Machine Learning Engineer campus recruitment
- NLP Engineer intern


### Step 3: Task Generation

SearchAgent:
- builds search tasks
- assigns sources and pages

Example: ```(query="AI Engineer internship", source="indeed", page=1)```


### Step 4: Data Collection

Tools:
- WebSearchTool → fetch search pages
- ScraperTool → extract content

Fallback:
- synthetic data if scraping fails


### Step 5: Parsing

ParserTool:
- extracts structured fields:
  - title
  - company
  - salary
  - requirements


### Step 6: Classification

ClassifierAgent:
- determines if job is AI-related
- filters irrelevant roles


### Step 7: Skill Extraction

SkillExtractorAgent:
- extracts:
  - Python
  - PyTorch
  - NLP
  - LLM
  - etc.


### Step 8: Data Processing

Core Layer:
- normalization
- validation
- deduplication


### Step 9: Iterative Improvement

QueryRewriterAgent:
- expands queries
- improves coverage

Loop continues until:
- target job count reached
OR
- max iterations reached


### Step 10: Export

ExporterTool:
- JSON
- CSV
- Markdown report


## Workflow Characteristics

- Iterative
- Self-improving
- Goal-driven
- Autonomous
- Modular


## Failure Handling

- retry mechanism
- fallback synthetic data
- error logging
