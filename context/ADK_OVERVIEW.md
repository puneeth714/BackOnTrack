# Google Agent Development Kit (ADK) 2.0 - Overview & Reference

> **Official Documentation Source:** [adk.dev](https://adk.dev/) | [llms.txt](https://adk.dev/llms.txt) | [llms-full.txt](https://adk.dev/llms-full.txt)

---

## 1. What is Google ADK?

The **Agent Development Kit (ADK)** is an open-source, code-first toolkit developed by Google for building, evaluating, and deploying sophisticated multi-agent AI systems with flexibility and control. 

ADK v2.0 introduces **Graph-based agent workflows**, offering declarative control over deterministic processes while seamlessly embedding generative AI reasoning nodes.

### Key Capabilities:
- **Graph-Based Agent Workflows:** Combines code functions, deterministic tool calls, human input, and generative LLMs into a directed execution graph.
- **Multi-Agent Orchestration:** Supports Sequential, Parallel, Loop, and dynamic routing patterns.
- **Model Flexibility:** Native first-class support for Google Gemini (`gemini-flash-latest`, `gemini-pro-latest`, `gemini-2.0-flash`), Gemma, Anthropic Claude, OpenAI, Ollama, and LiteLLM.
- **Type-Safe Data Contracts:** Built on Pydantic (Python), Zod (TypeScript), and Go structs.
- **CLI & Developer Tools:** Interactive terminal test runner (`adk run`) and local development UI (`adk web`).

---

## 2. Installation & Setup (Python)

### Requirements
- Python 3.10+
- `pip`

### Step 1: Install the Package
```bash
pip install google-adk
```

### Step 2: Set Environment Variables
ADK uses the Gemini API by default. Set your Google AI Studio API key:
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```
Or write to a `.env` file:
```bash
echo 'GOOGLE_API_KEY="your-gemini-api-key"' > .env
```

---

## 3. ADK CLI Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `adk create <project_name>` | Scaffolds a new agent project directory with `agent.py`, `.env`, `__init__.py`. | `adk create back_on_track` |
| `adk run <project_dir>` | Runs an interactive command-line interface to chat and test the agent. | `adk run back_on_track` |
| `adk web --port 8000` | Starts a local web development UI at `http://localhost:8000` to visualize conversations and tool calls. | `adk web --port 8000` |

---

## 4. Project Structure

When created with `adk create`, the project layout is:
```text
my_agent/
    agent.py      # Main agent/workflow definition (must export root_agent)
    .env          # API keys (GOOGLE_API_KEY)
    __init__.py
```
> **Rule:** Every ADK project must define a `root_agent` in `agent.py`. It can be a single `Agent` or a multi-node `Workflow`.
