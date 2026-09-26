# Google ADK 2.0 - Graph Workflows & Execution Control

---

## 1. Why Graph Workflows in ADK 2.0?

Standard prompt-based agents can be unpredictable and hallucinate sequencing. 
**Graph-based workflows** let you define deterministic execution graphs (`edges`) where:
1. Pure Python functions execute deterministic calculations, database reads, and LMS lookups.
2. Generative AI agents perform reasoning, natural language parsing, and synthesis.
3. Every node passes data via typed **`Event`** payloads without needing global shared mutable state.

---

## 2. Graph Syntax & Edge Wiring

```python
from google.adk import Agent, Workflow, Event
from pydantic import BaseModel

# Node 1: Code function (Deterministic)
def parse_student_input(node_input: str):
    """Extracts days and course from student message."""
    return Event(output={"days_left": 2, "subject": "Operating Systems"})

# Node 2: AI Agent (LLM Reasoning)
scope_reasoning_agent = Agent(
    name="scope_reasoning_agent",
    model="gemini-flash-latest",
    instruction="""
    Given the subject and upcoming exam date, reason about which syllabus
    modules are active and which modules should be filtered out.
    """
)

# Node 3: Code function (Deterministic)
def finalize_schedule(node_input: dict):
    return Event(
        message=f"Your catch-up plan is ready! Focused on: {node_input}",
    )

# Root Workflow Graph
root_agent = Workflow(
    name="root_agent",
    edges=[
        ("START", parse_student_input, scope_reasoning_agent, finalize_schedule)
    ],
)
```

---

## 3. Data Passing Mechanisms in Graphs

Within a graph-based workflow, nodes pass data to downstream steps through **Events**:

### 1. `Event(output=...)`
- Used to pass structured information to the immediate **next node** in the graph.
- The next node receives this value directly as its input parameter.
```python
def fetch_lms_node(node_input: dict):
    lms_data = {"attendance": 59.4, "exam": "Mid Term 2"}
    return Event(output=lms_data)
```

### 2. `Event(message=...)`
- Data intended directly as a visible response to the end user.
- Emitted to the user interface/chat client.

### 3. Session State (`state`)
- For data that needs to be accessed by multiple nodes non-sequentially:
```python
def save_context_node(ctx, node_input):
    ctx.state["student_id"] = "STU_104"
    return Event(output="context_saved")
```

State Key Scopes:
- `temp:` — Discarded after the current invocation ends.
- `user:` — Persists across all sessions for this specific user.
- `app:` — Shared globally across all users of the application.
- *(no prefix)* — Persists for the lifetime of the conversation session.

---

## 4. Conditional Branching & Dynamic Routes

Nodes can choose which edge to take at runtime by returning a routing key:

```python
def evaluation_router_node(node_input: dict):
    if node_input.get("hours_available") < 4:
        return Event(route="ultra_panic_branch", output=node_input)
    else:
        return Event(route="standard_recovery_branch", output=node_input)

# Workflow with branching
root_agent = Workflow(
    name="branching_triage",
    edges=[
        ("START", evaluation_router_node),
        ("ultra_panic_branch", lean_pass_agent),
        ("standard_recovery_branch", full_triage_agent),
    ],
)
```
