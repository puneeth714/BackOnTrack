# "Back on Track" - Google ADK 2.0 Python Implementation

This document provides the reference Python implementation for running the **"Back on Track"** Graph workflow in Google ADK 2.0.

---

## 1. Directory Structure

```text
back_on_track_agent/
    agent.py             # Main ADK Workflow definition
    lms_connector.py     # Deterministic LMS reader
    .env                 # GOOGLE_API_KEY
```

---

## 2. Python Code (`agent.py`)

```python
"""
Back on Track - AI Academic Recovery Engine
Built with Google Agent Development Kit (ADK) 2.0
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from google.adk import Agent, Workflow, Event

# =====================================================================
# DATA CONTRACTS (PYDANTIC SCHEMAS)
# =====================================================================

class ParsedStudentIntent(BaseModel):
    subject: str = Field(description="Subject mentioned by student, e.g. Operating Systems")
    days_left: int = Field(description="Days remaining until the exam")
    hours_available: float = Field(default=8.0, description="Available study hours inferred or stated")
    student_sentiment: str = Field(description="Anxiety / panic / recovery focus")

class ScopedSyllabusContext(BaseModel):
    target_exam: str
    active_modules: List[str]
    excluded_modules: List[str]
    scoping_rationale: str

class TriageOutput(BaseModel):
    highest_impact_topics: List[Dict[str, Any]]
    fundamental_unlocks: List[Dict[str, Any]]
    deprioritized_topics: List[str]
    day_wise_schedule: List[Dict[str, Any]]
    confidence_mcqs: List[Dict[str, Any]]

# =====================================================================
# NODE 1: PARSE STUDENT NATURAL LANGUAGE INPUT (LLM Agent Node)
# =====================================================================

message_parser_agent = Agent(
    name="message_parser_agent",
    model="gemini-flash-latest",
    output_schema=ParsedStudentIntent,
    instruction="""
    You are an intent parser for the 'Back on Track' academic engine.
    Extract the subject, days left, and student situation from the user's plain-text message.
    Example: 'I missed the last 3 weeks of OS and my exam is this Friday. I only have about 2 days.'
    -> subject: 'Operating Systems', days_left: 2, student_sentiment: 'Interruption recovery'
    """
)

# =====================================================================
# NODE 2: RETRIEVE LMS CONTEXT (Deterministic Function Node)
# =====================================================================

def fetch_lms_context_node(parsed_intent: ParsedStudentIntent) -> Event:
    """
    Simulates pulling student records from the college LMS database.
    Reads student attendance, IA-1 scores, and upcoming Mid Term 2 exam details.
    """
    data_dir = Path(__file__).parent.parent
    
    # Load synthetic LMS context
    with open(data_dir / "lms_student_context.json") as f:
        lms_profile = json.load(f)
        
    combined_context = {
        "intent": parsed_intent.model_dump(),
        "lms": lms_profile
    }
    return Event(output=combined_context)

# =====================================================================
# NODE 3: MID TERM SYLLABUS SCOPER (Reasoning Agent Node)
# =====================================================================

syllabus_scoper_agent = Agent(
    name="syllabus_scoper_agent",
    model="gemini-flash-latest",
    instruction="""
    You are the Academic Curriculum Scoper.
    Look at the target exam ('Mid Term 2').
    Reason about which syllabus modules are active:
    - Exclude Module 1 (already covered in Mid Term 1).
    - Exclude Module 5 (File systems/Storage - post-midterm).
    - Scope strictly to: Module 2 (Part B - CPU scheduling), Module 3 (Sync & Deadlocks), Module 4 (Part A - Paging).
    Output the filtered active modules and the rationale.
    """
)

# =====================================================================
# NODE 4: PYQ WEIGHTAGE & GAP MATCHER (Deterministic Function Node)
# =====================================================================

def match_gaps_with_pyq_node(node_input: Any) -> Event:
    """
    Cross-references the student's 0-mark areas in IA-1 with 100% recurring PYQ questions.
    """
    data_dir = Path(__file__).parent.parent
    
    with open(data_dir / "midterm_pyq_weightage.json") as f:
        pyq_data = json.load(f)
    with open(data_dir / "fundamental_concepts_os.json") as f:
        foundations = json.load(f)

    curated_payload = {
        "pyq_patterns": pyq_data["question_pattern_intelligence"],
        "fundamental_unlocks": foundations["unlock_principles"]
    }
    return Event(output=curated_payload)

# =====================================================================
# NODE 5: PLAN SYNTHESIZER & CONFIDENCE BOOSTER (LLM Agent Node)
# =====================================================================

plan_synthesizer_agent = Agent(
    name="plan_synthesizer_agent",
    model="gemini-flash-latest",
    output_schema=TriageOutput,
    instruction="""
    Synthesize the final 'Back on Track' output for the student:
    1. Highest-Impact Topics: Rank by marks yield vs prep hours (e.g. CPU Scheduling SRTF, Banker's, Producer-Consumer).
    2. Fundamental Concepts to clear first: State transition, Semaphore token model, Need matrix.
    3. Safe to Deprioritize: Mention Dining Philosophers, Multilevel feedback queues.
    4. 2-Day Hour-by-Hour Survival Plan: Balanced for ~7.5 hours total study time.
    5. Two high-probability practice MCQs.
    
    IMPORTANT: Never use the phrase '20%/80%'. Use 'Highest-impact topics' and 'Critical topics'.
    """
)

# =====================================================================
# ROOT WORKFLOW GRAPH DEFINITION (Google ADK 2.0 Graph)
# =====================================================================

root_agent = Workflow(
    name="back_on_track_workflow",
    description="Transforms a student emergency into an immediate catch-up roadmap.",
    edges=[
        (
            "START",
            message_parser_agent,
            fetch_lms_context_node,
            syllabus_scoper_agent,
            match_gaps_with_pyq_node,
            plan_synthesizer_agent
        )
    ],
)
```

---

## 3. How to Run Locally

```bash
# 1. Install ADK
pip install google-adk

# 2. Test in CLI
adk run back_on_track_agent

# 3. Test in Web UI
adk web --port 8000
```
Open `http://localhost:8000` to interactively debug each node's input, output, and latency trace.
