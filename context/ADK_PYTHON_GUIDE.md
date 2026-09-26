# Google ADK 2.0 - Python Developer Guide

---

## 1. Core Classes & Imports

```python
from google.adk import Agent, Workflow, Event
from pydantic import BaseModel, Field
from typing import List, Optional
```

---

## 2. Defining a Single LLM Agent with Tools

```python
from google.adk.agents.llm_agent import Agent

# 1. Define a tool function with type hints and docstring
def lookup_student_lms_record(student_id: str) -> dict:
    """Retrieves student attendance, past marks, and flagged weak areas from the LMS."""
    return {
        "student_id": student_id,
        "attendance_pct": 59.4,
        "mid_term_1_score": "8/50",
        "lag_topics": ["Process Synchronization", "Deadlocks"]
    }

# 2. Define the Agent
root_agent = Agent(
    name="academic_advisor_agent",
    model="gemini-flash-latest",
    description="Helps students in academic distress catch up.",
    instruction="""
    You are an empathetic, tactical academic triage advisor.
    When a student tells you they are crunched for time, retrieve their LMS profile using
    the 'lookup_student_lms_record' tool and give them a high-yield study plan.
    """,
    tools=[lookup_student_lms_record],
)
```

---

## 3. Pydantic Structured Input & Output Schemas

You can enforce strict type contracts on both agent inputs and function outputs:

```python
class TriagePlan(BaseModel):
    target_exam: str = Field(description="Name of the upcoming exam")
    hours_available: float = Field(description="Total study hours available")
    critical_topics: List[str] = Field(description="Top 3-4 topics by historical exam weightage")
    prerequisite_unlocks: List[str] = Field(description="Concepts that must be cleared first")
    deprioritized_topics: List[str] = Field(description="Low-yield topics that can be safely skipped")

# Agent with structured output
triage_agent = Agent(
    name="triage_agent",
    model="gemini-flash-latest",
    output_schema=TriagePlan,
    instruction="Generate a structured recovery plan for the student based on their input.",
)
```

---

## 4. Models Supported in ADK Python

- `gemini-flash-latest` (Default, recommended for fast multi-agent reasoning and tool-calling)
- `gemini-pro-latest` (Recommended for complex math proofs and deep conceptual breakdowns)
- `gemini-2.0-flash`
- Anthropic Claude (via Claude API adapter)
- OpenAI GPT-4o / GPT-4o-mini
- Local Ollama models (e.g. `ollama/llama3.2`)
