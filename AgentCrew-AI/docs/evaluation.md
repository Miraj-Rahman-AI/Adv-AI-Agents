
# AgentCrew-AI Evaluation Protocol

## 1. Objectives

Evaluate the effectiveness, efficiency, and reliability
of collaborative multi-agent task execution.

## 2. Evaluation Dimensions

### Task Completion

Measure the fraction of tasks that complete successfully.

Task Completion Rate:

TCR = Completed Tasks / Total Tasks

### Reliability

Measure failed and blocked tasks separately.

Failure Rate:

FR = Failed Tasks / Total Tasks

### Execution Efficiency

Measure total workflow execution time.

Compare sequential and dependency-aware execution
on equivalent task inputs.

### Collaboration

Track successful dependency resolution and the
number of structured coordination messages.

### Authorization

Evaluate whether unauthorized tool requests are rejected
before execution.

## 3. Suggested Baselines

1. Single-agent execution
2. Sequential multi-agent execution
3. Dependency-aware multi-agent execution
4. Multi-agent execution without reviewer

Not all baselines are implemented in the initial code.

## 4. Experimental Tasks

Use tasks with predefined objectives, permitted source
materials, expected outputs, and success criteria.

Possible categories include:

- Local document research
- Structured information synthesis
- Multi-step analysis
- Authorized tool execution
- Dependency recovery
- Invalid task planning
- Unauthorized tool requests

## 5. Execution Records

Record:

- Experiment identifier
- Task objective
- Model provider and model
- Agent assignments
- Task statuses
- Tool events
- Error outcomes
- Execution duration
- Final output
- Evaluation results

The initial implementation captures workflow events
and basic completion metrics.

Token usage, monetary cost, and multi-run aggregate
statistics require additional instrumentation.

## 6. Repeated Experiments

Use consistent:

- Task collections
- Evaluation criteria
- Model settings
- Tool configurations
- Authorization policies

For stochastic model inference, repeat experiments and
report variability.

## 7. Result Interpretation

Mock-mode results validate orchestration and software
behavior only.

They cannot establish that LLM-based collaboration
improves reasoning, accuracy, or scientific performance.

Real-model performance claims require independent
experimental evaluation.
