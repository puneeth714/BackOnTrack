"""
Google ADK 2.0 Graph Workflow: Back on Track Engine (Phase 4)
Strict implementation of Google ADK 2.0 Graph Workflows using:
- from google.adk import Agent, Workflow, Event
- from google.adk.agents.llm_agent import LlmAgent

Orchestrates:
START -> MessageParser (ADK Agent) -> LMSExtractor (Tool 1) -> KnowledgeScoper (Tool 2) -> PlanSynthesizer (ADK Agent)
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parent.parent
repo_dir = backend_dir.parent
for p in [str(backend_dir), str(repo_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Load API key
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    env_file = repo_dir / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                os.environ["GEMINI_API_KEY"] = API_KEY
                os.environ["GOOGLE_API_KEY"] = API_KEY
                break

# Strict Google ADK 2.0 Imports
from google.adk import Agent, Workflow, Event
from google.adk.agents.llm_agent import LlmAgent

from agents.schemas import ParsedStudentIntent, BackOnTrackPlan
from agents.intent_agent import parse_student_intent
from agents.synthesizer_agent import synthesize_back_on_track_plan
from tools.lms_tool import get_student_lms_context
from tools.knowledge_tool import get_academic_knowledge
from tools.learning_gain_tool import calculate_learning_metrics, recalibrate_study_pace


# =========================================================================
# NODE 1: Intent Parser Agent (Google ADK LLM Agent)
# =========================================================================

intent_parser_adk_agent = Agent(
    name="intent_parser_agent",
    model="gemini-2.5-flash",
    output_schema=ParsedStudentIntent,
    instruction=(
        "You are an empathetic academic triage AI agent for university engineering students. "
        "Extract the subject, days left, study hours available, situation summary, and target goal. "
        "Always provide an empathetic conversational reply. Strictly avoid buzzwords like '20%/80%'."
    )
)


def node_intent_parser(user_message: str) -> Event:
    """Node 1 in ADK 2.0 Graph: Parses student natural language input."""
    intent = parse_student_intent(user_message)
    return Event(output=intent)


# =========================================================================
# NODE 2: LMS Context Extractor (Deterministic Tool Node)
# =========================================================================

def node_lms_extractor(event_input: Any, student_id: str = "STU_2022_CS104") -> Event:
    """Node 2 in ADK 2.0 Graph: Pulls student attendance, test lags, and slide digest."""
    intent = event_input.output if isinstance(event_input, Event) else event_input
    lms_context = get_student_lms_context(student_id)
    return Event(output={
        "intent": intent,
        "lms_context": lms_context
    })


# =========================================================================
# NODE 3: Academic Knowledge Scoper (Deterministic Tool Node)
# =========================================================================

def node_knowledge_scoper(event_input: Any) -> Event:
    """Node 3 in ADK 2.0 Graph: Scopes Mid Term 2 active modules and drops Mod 1 & 5."""
    data = event_input.output if isinstance(event_input, Event) else event_input
    intent: ParsedStudentIntent = data["intent"]
    lms_context = data["lms_context"]
    
    knowledge = get_academic_knowledge(exam_type="Mid Term 2", subject=intent.subject)
    return Event(output={
        "intent": intent,
        "lms_context": lms_context,
        "knowledge": knowledge
    })


# =========================================================================
# NODE 4: Plan Synthesizer Agent (Google ADK Reasoning & Synthesis Agent)
# =========================================================================

plan_synthesizer_adk_agent = Agent(
    name="plan_synthesizer_agent",
    model="gemini-2.5-flash",
    output_schema=BackOnTrackPlan,
    instruction=(
        "Synthesize a typed BackOnTrackPlan prioritizing highest-impact 10-markers. "
        "Calculate quantitative learning gain metrics and personalized pacing buffers. "
        "Strictly omit out-of-scope modules."
    )
)


def node_plan_synthesizer(event_input: Any) -> Event:
    """Node 4 in ADK 2.0 Graph: Synthesizes final typed BackOnTrackPlan with math metrics."""
    data = event_input.output if isinstance(event_input, Event) else event_input
    intent = data["intent"]
    lms_context = data["lms_context"]
    knowledge = data["knowledge"]

    plan = synthesize_back_on_track_plan(intent, lms_context, knowledge)
    return Event(output=plan)


# =========================================================================
# ROOT GOOGLE ADK 2.0 GRAPH WORKFLOW DEFINITION
# =========================================================================

back_on_track_adk_workflow = Workflow(
    name="back_on_track_workflow",
    description="Autonomous Academic Triage and Catch-up Engine using Google ADK 2.0 Graph",
    edges=[
        (
            "START",
            node_intent_parser,
            node_lms_extractor,
            node_knowledge_scoper,
            node_plan_synthesizer
        )
    ]
)


class BackOnTrackGraphWorkflow:
    """
    Execution controller exposing the ADK 2.0 Graph runner and dynamic recalibration.
    """

    def __init__(self, workflow: Workflow = back_on_track_adk_workflow):
        self.workflow = workflow
        self.name = workflow.name
        self.description = workflow.description

    def run(self, user_message: str, student_id: str = "STU_2022_CS104") -> Dict[str, Any]:
        """
        Executes the linear ADK 2.0 graph from START to FINISH.
        Passes Event(output=...) sequentially through all nodes.
        """
        trace = []

        # Step 1: Parse Intent (Node 1)
        ev1 = node_intent_parser(user_message)
        intent: ParsedStudentIntent = ev1.output
        trace.append({
            "step": 1,
            "node": "Node_1_IntentParser",
            "summary": f"Extracted: {intent.days_left} days left, {intent.hours_available}h budget"
        })

        # Step 2: LMS Context Extractor (Node 2)
        ev2 = node_lms_extractor(ev1, student_id=student_id)
        lms_ctx = ev2.output["lms_context"]
        trace.append({
            "step": 2,
            "node": "Node_2_LMSExtractor",
            "summary": f"LMS Connected: {lms_ctx['student_name']} (Att: {lms_ctx['attendance_metrics']['attendance_pct']}%)"
        })

        # Step 3: Academic Knowledge Scoper (Node 3)
        ev3 = node_knowledge_scoper(ev2)
        knowledge = ev3.output["knowledge"]
        dropped = len(knowledge["syllabus_scoping"]["excluded_modules"])
        trace.append({
            "step": 3,
            "node": "Node_3_KnowledgeScoper",
            "summary": f"Syllabus Scoped: {len(knowledge['syllabus_scoping']['active_modules'])} active modules ({dropped} modules dropped)"
        })

        # Step 4: Plan Synthesizer (Node 4)
        ev4 = node_plan_synthesizer(ev3)
        plan: BackOnTrackPlan = ev4.output
        trace.append({
            "step": 4,
            "node": "Node_4_PlanSynthesizer",
            "summary": f"Plan Synthesized: {plan.projected_marks_yield}/50 marks projected ({plan.educational_metrics.normalized_gain_pct}% normalized gain)"
        })

        return {
            "workflow_name": self.name,
            "status": "SUCCESS",
            "execution_trace": trace,
            "final_plan": plan,
            "adk_workflow": self.workflow
        }

    def recalibrate(
        self,
        topic_completed: str,
        estimated_mins: float,
        actual_spent_mins: float,
        remaining_budget_mins: float,
        current_topics: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Closed-loop dynamic pacing recalibration engine."""
        return recalibrate_study_pace(
            topic_completed=topic_completed,
            estimated_mins=estimated_mins,
            actual_spent_mins=actual_spent_mins,
            remaining_budget_mins=remaining_budget_mins,
            current_planned_topics=current_topics
        )


# Global singleton instance representing the ADK root agent
root_workflow = BackOnTrackGraphWorkflow()


if __name__ == "__main__":
    print(f"=== Running Google ADK 2.0 Workflow: '{back_on_track_adk_workflow.name}' ===")
    print("Graph Edges Configured:", back_on_track_adk_workflow.edges)

    test_msg = "I missed the last 3 weeks of Operating Systems and my exam is this Friday. I only have about 6 hours to prepare. What should I focus on to catch up and do well?"
    result = root_workflow.run(test_msg)

    print("\n--- ADK 2.0 Graph Workflow Execution Trace ---")
    for step in result["execution_trace"]:
        print(f"[{step['step']}] {step['node']} -> {step['summary']}")

    plan = result["final_plan"]
    print("\n--- Final Plan Summary ---")
    print(f"Student: {plan.student_name} | Exam: {plan.target_exam}")
    print(f"Total Prep: {plan.total_prep_hours} hrs | Projected Yield: {plan.projected_marks_yield}/50 Marks")
    print(f"Educational Metrics: {plan.educational_metrics.summary_text}")
    print(f"Top Focus Topics: {[t.topic_name for t in plan.highest_impact_topics]}")
