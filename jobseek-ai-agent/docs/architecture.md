# System Architecture

## Overview

JobSeek AI Agent is an **Agentic AI system** designed to autonomously discover, collect, filter, and structure AI-related job postings from multiple recruitment platforms.

The system follows a **modular, layered architecture** combining:
- LLM-powered agents
- tool orchestration
- pipeline processing
- structured data validation
  

## High-Level Architecture
JobSeek AI Agent follows an Agentic AI workflow architecture, where an intelligent agent coordinates multiple tools and reasoning modules.

<p align="center">
  <img src="assets/Agentic Al Job Search System.png" width="95%">
</p>


## Core Components

### 1. Agents Layer
Responsible for reasoning and decision-making.

- **PlannerAgent**
  - Converts user goal → search plan
  - Generates initial queries

- **SearchAgent**
  - Builds structured search tasks

- **ClassifierAgent**
  - Determines whether a job is AI-related

- **QueryRewriterAgent**
  - Expands queries when results are insufficient

- **SkillExtractorAgent**
  - Extracts technical skills from job descriptions


### 2. Tools Layer
Handles external interactions.

- **WebSearchTool** → fetch search pages  
- **ScraperTool** → retrieve job content  
- **ParserTool** → extract structured fields  
- **ExporterTool** → save outputs  
- **SiteRouterTool** → manage job platforms  


### 3. Pipeline Layer
Handles data flow and processing.

- **Orchestrator**
  - Controls execution loop
  - Manages iterations

- **JobPipeline**
  - Parsing → Classification → Enrichment → Deduplication

- **PipelineState**
  - Tracks system state and progress


### 4. Core Layer
Ensures data consistency and quality.

- **Schemas** → enforce structure  
- **Models** → standard data objects  
- **Deduplicator** → remove duplicates  
- **Validators** → ensure correctness  
- **Normalizer** → standardize fields  


### 5. Prompt Layer

- Defines LLM reasoning behavior
- Includes:
  - classification
  - skill extraction
  - query rewriting


## Design Principles

- Modular and extensible
- Agent-tool separation
- Iterative reasoning loop
- Fail-safe fallback mechanisms
- Production-ready structure


## Future Improvements

- Multi-agent collaboration
- Real-time streaming pipeline
- RAG-based job ranking
- Distributed scraping
- Reinforcement learning optimization
