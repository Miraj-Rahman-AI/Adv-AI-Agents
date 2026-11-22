
# AgentCrew-AI Agent Roles

## Agent Execution Contract

All specialized agents inherit from BaseAgent.

Each agent implements:

```python
async def execute(
    self,
    task: AgentTask,
    context: dict,
) -> AgentResult:
    ...
```

AgentResult contains:

- task_id
- agent_name
- success
- output
- error
- attempts

## 1. Coordinator

**Module:** `agents/coordinator.py`

**Input:** User objective.

**Responsibility:** Interpret the objective and determine
success criteria.

**Output:** Goal and success criteria.

## 2. Planner

**Module:** `agents/planner.py`

**Input:** Objective and coordination result.

**Responsibility:** Generate structured tasks and dependencies.

**Output:** Task list.

The TaskManager validates the plan before execution.

## 3. Researcher

**Module:** `agents/researcher.py`

**Input:** Objective and permitted document sources.

**Tool:** `document_search`

**Responsibility:** Retrieve evidence and produce findings.

**Output:** Summary, source excerpts, and findings.

## 4. Executor

**Module:** `agents/executor.py`

**Input:** Task payload containing an approved tool request.

**Tool:** `calculator`

**Responsibility:** Execute authorized operations.

**Output:** Tool name and execution result.

Example task payload:

```json
{
  "tool": "calculator",
  "arguments": {
    "expression": "(25 + 15) / 2"
  }
}
```

## 5. Analyst

**Module:** `agents/analyst.py`

**Input:** Objective, assigned task, and dependency results.

**Responsibility:** Develop analysis criteria and interpret
available inputs.

**Output:** Analysis, criteria, and limitations.

## 6. Reviewer

**Module:** `agents/reviewer.py`

**Input:** Research and analysis outputs.

**Responsibility:** Validate research provenance and
task requirements.

**Output:** Approval decision and issues.

## 7. Synthesizer

**Module:** `agents/synthesizer.py`

**Input:** Research, analysis, and approved review outputs.

**Responsibility:** Produce the final report.

**Output:** Markdown report.

## Role Isolation

An agent's role does not itself grant unrestricted tool use.

Allowed tools are defined in trusted configuration files.

Application-level authorization must also permit a tool
before execution.
