
# AgentCrew-AI Installation Guide

## Requirements

- Python 3.11 or newer
- Git
- pip
- Optional OpenAI-compatible API access
- Optional Ollama installation

## 1. Clone

```bash
git clone https://github.com/Miraj-Rahman-AI/Adv-AI-Agents.git
cd Adv-AI-Agents/AgentCrew-AI
```

## 2. Virtual Environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## 4. Environment Configuration

Create a local environment file from the template.

macOS / Linux:

```bash
cp .env.example .env
```

Configure:

```dotenv
LLM_PROVIDER=mock
```

## 5. Run Mock Workflow

```bash
agentcrew run \
  --task "Analyze AgentCrew-AI architecture and security" \
  --provider mock \
  --docs-dir docs
```

## 6. Run Ollama

Install Ollama and obtain a supported model.

For example:

```bash
ollama pull qwen3:8b
```

Set:

```dotenv
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3:8b
OLLAMA_BASE_URL=http://localhost:11434/v1
```

Run:

```bash
agentcrew run \
  --task "Analyze multi-agent orchestration" \
  --provider ollama \
  --docs-dir docs
```

## 7. Hosted Model Configuration

Configure an API key and model:

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=your_actual_api_key
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

Never commit the `.env` file.

## 8. Run Tests

```bash
python -m pytest tests/ -v
```

## 9. Execution Traces

To explicitly export a JSONL trace:

```bash
agentcrew run \
  --task "Compare agent roles" \
  --provider mock \
  --docs-dir docs \
  --trace-path runs/example.jsonl
```

## Troubleshooting

**ModuleNotFoundError**

Install the package in editable mode.

**No supporting documents found**

Check that `--docs-dir` points to a directory containing
relevant Markdown files.

**Model connection error**

Verify the API endpoint, model name, credentials,
and inference service availability.

**Invalid model JSON**

The current adapter requires JSON objects.
Try a model with reliable structured-output behavior
or use mock mode for integration testing.

**PermissionError**

Check trusted agent and tool configuration. Do not
bypass authorization checks to make a task succeed.
