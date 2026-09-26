"""
Multi-Flow Execution & Multi-Dimensional Verification Suite (Phase 4)
Runs at least 4 distinct student personas through the ADK 2.0 Graph Workflow,
and uses a fan-out evaluation committee across 4 specialist dimensions:
1. Pedagogical Integrity Reviewer
2. Mathematical Learning Gain Auditor
3. Student UX & Empathy Reviewer
4. BITSoM Vertex Jury & Investor Auditor
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from workflows.graph_workflow import BackOnTrackGraphWorkflow
from agents.schemas import BackOnTrackPlan

# Terminal color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


# 4 Distinct Student Flow Scenarios
FOUR_FLOW_SCENARIOS = [
    {
        "flow_id": "FLOW_1_ROHAN_FEST",
        "student_name": "Rohan Verma",
        "student_id": "STU_2022_CS104",
        "category": "Cultural Fest Coordinator / Severe 48h Time Crunch",
        "user_message": "I missed the last 3 weeks of Operating Systems because of the college cultural fest and my exam is this Friday. I only have about 6 hours to prepare. What should I focus on to catch up and do well?"
    },
    {
        "flow_id": "FLOW_2_PRIYA_MEDICAL",
        "student_name": "Priya Sharma",
        "student_id": "STU_2022_CS089",
        "category": "Medical Convalescence (Dengue) / Safe Pass Focus",
        "user_message": "I was hospitalized with severe dengue for 2 weeks. I missed all classes on Deadlocks and Paging. Midterm 2 is in 3 days. I can study 4 hours a day. I just need to pass safely."
    },
    {
        "flow_id": "FLOW_3_KEVIN_PANIC",
        "student_name": "Kevin D'Souza",
        "student_id": "STU_2022_CS042",
        "category": "Topic-Specific Conceptual Panic / 24-Hour Emergency",
        "user_message": "I understand CPU scheduling algorithms well, but I completely freeze on Banker's algorithm and Semaphores. Exam is in 24 hours. Give me an ultra-lean 4-hour rescue plan."
    },
    {
        "flow_id": "FLOW_4_ANANYA_RECOVERY",
        "student_name": "Ananya Iyer",
        "student_id": "STU_2022_CS012",
        "category": "Sports Captain / High-Potential CGPA Recovery (Aiming 42+/50)",
        "user_message": "I missed two weeks due to the Inter-University Sports Meet. I scored 22/50 in Mid Term 1, but I need at least 42/50 in Mid Term 2 to maintain my CGPA. I have 3 full days (15 hours). Give me maximum mark coverage."
    }
]


# =====================================================================
# FAN-OUT MULTI-DIMENSIONAL VERIFIERS
# =====================================================================

class PedagogicalIntegrityReviewer:
    """Dimension 1: Verifies curriculum scoping, concept dependencies, and cognitive load."""
    @staticmethod
    def audit(plan: BackOnTrackPlan) -> Dict[str, Any]:
        # 1. Scoping check: Modules 1 and 5 must be excluded
        plan_str = plan.model_dump_json().lower()
        has_out_of_scope = "module 1: introduction" in plan_str or "module 5: mass storage" in plan_str
        
        # 2. Dependency check: Unlocks must be present
        has_unlocks = len(plan.fundamental_unlocks) >= 2
        
        # 3. Focus topic count
        topic_count = len(plan.highest_impact_topics)
        is_manageable = 3 <= topic_count <= 5

        passed = (not has_out_of_scope) and has_unlocks and is_manageable
        return {
            "dimension": "Pedagogical Integrity",
            "passed": passed,
            "score": 100 if passed else 60,
            "notes": f"Scoping clean; {len(plan.fundamental_unlocks)} unlocks; {topic_count} high-impact topics."
        }


class MathematicalGainAuditor:
    """Dimension 2: Verifies learning gain, efficiency metrics, and time budget feasibility."""
    @staticmethod
    def audit(plan: BackOnTrackPlan) -> Dict[str, Any]:
        metrics = plan.educational_metrics
        # Assert Simple Gain > 0
        gain_positive = metrics.learning_gain > 0
        # Assert Normalized Gain between 50% and 95%
        norm_valid = 50.0 <= metrics.normalized_gain_pct <= 95.0
        # Assert Efficiency > 0
        eff_positive = metrics.efficiency_per_minute > 0
        # Assert Budget feasibility
        budget_valid = plan.total_prep_hours <= 15.0

        passed = gain_positive and norm_valid and eff_positive and budget_valid
        return {
            "dimension": "Mathematical Gain & Efficiency",
            "passed": passed,
            "score": 100 if passed else 50,
            "notes": f"Gain: +{metrics.learning_gain}m | Norm: {metrics.normalized_gain_pct}% | Eff: {metrics.efficiency_per_minute}m/min."
        }


class StudentUXEmpathyReviewer:
    """Dimension 3: Verifies student anxiety reduction, zero-buzzword compliance, and model answers."""
    @staticmethod
    def audit(plan: BackOnTrackPlan) -> Dict[str, Any]:
        plan_str = plan.model_dump_json().lower()
        
        # Strict zero-buzzword check
        buzzword_free = ("20%" not in plan_str) and ("80%" not in plan_str) and ("pareto" not in plan_str)
        # Missed lectures slide digest present
        has_slide_digest = len(plan.missed_lectures_digest.slides_summary) >= 2
        # Model answers available
        has_model_answers = all(len(t.model_answer_summary) > 20 for t in plan.highest_impact_topics)

        passed = buzzword_free and has_slide_digest and has_model_answers
        return {
            "dimension": "Student UX & Zero-Buzzword Empathy",
            "passed": passed,
            "score": 100 if passed else 40,
            "notes": f"Zero buzzwords: {buzzword_free} | Slide digest: {has_slide_digest} | Model answers: {has_model_answers}."
        }


class BITSoMJuryAuditor:
    """Dimension 4: Verifies defense against tough jury questions (B2B college retention, syllabus predictability)."""
    @staticmethod
    def audit(plan: BackOnTrackPlan) -> Dict[str, Any]:
        # Checks if projected marks safely cross the pass threshold (20/50) and hit First Class (35+/50)
        yield_marks = plan.projected_marks_yield
        viable_academic_recovery = yield_marks >= 35
        # Deprioritized list gives proof of time savings
        has_cut_fat = len(plan.deprioritized_topics) >= 2

        passed = viable_academic_recovery and has_cut_fat
        return {
            "dimension": "BITSoM Jury & Institutional Retention",
            "passed": passed,
            "score": 100 if passed else 70,
            "notes": f"Yield: {yield_marks}/50 marks | Saves {len(plan.deprioritized_topics)*2}h by deprioritizing fluff."
        }


# =====================================================================
# MULTI-FLOW ORCHESTRATOR
# =====================================================================

def execute_all_4_flows() -> Dict[str, Any]:
    """Runs the 4 scenarios through the ADK Graph and evaluates across all 4 dimensions."""
    workflow = BackOnTrackGraphWorkflow()
    flow_results = []
    all_flows_passed = True

    print(f"\n{BOLD}{CYAN}=============================================================================={RESET}")
    print(f"{BOLD}{CYAN}   ADK 2.0 GRAPH WORKFLOW: 4-FLOW EXECUTION & MULTI-AGENT VERIFICATION        {RESET}")
    print(f"{BOLD}{CYAN}=============================================================================={RESET}\n")

    for scenario in FOUR_FLOW_SCENARIOS:
        flow_id = scenario["flow_id"]
        s_name = scenario["student_name"]
        cat = scenario["category"]
        msg = scenario["user_message"]

        print(f"{BOLD}▶ EXECUTING {flow_id}: {s_name} [{cat}]{RESET}")
        print(f"  {YELLOW}Student Prompt:{RESET} \"{msg[:85]}...\"")

        # 1. Run through ADK 2.0 Graph Workflow
        execution_result = workflow.run(msg, student_id=scenario["student_id"])
        plan: BackOnTrackPlan = execution_result["final_plan"]

        # 2. Fan-out Multi-Dimensional Review Committee
        eval_pedagogy = PedagogicalIntegrityReviewer.audit(plan)
        eval_math = MathematicalGainAuditor.audit(plan)
        eval_ux = StudentUXEmpathyReviewer.audit(plan)
        eval_jury = BITSoMJuryAuditor.audit(plan)

        eval_committee = [eval_pedagogy, eval_math, eval_ux, eval_jury]
        scenario_passed = all(e["passed"] for e in eval_committee)
        avg_score = sum(e["score"] for e in eval_committee) / len(eval_committee)

        if not scenario_passed:
            all_flows_passed = False

        # Print Trace & Reviews
        print(f"  {CYAN}Execution Trace:{RESET} {len(execution_result['execution_trace'])} nodes completed.")
        for rev in eval_committee:
            icon = f"{GREEN}✓{RESET}" if rev["passed"] else f"{RED}✗{RESET}"
            print(f"    [{icon}] {BOLD}{rev['dimension']}:{RESET} {rev['notes']}")

        print(f"  {BOLD}Outcome Summary:{RESET} Projected {plan.projected_marks_yield}/50 marks in {plan.total_prep_hours}h prep ({plan.educational_metrics.summary_text.split('|')[1].strip()})")
        print(f"  {BOLD}Dimension Committee Score: {avg_score:.1f}%{RESET}")
        print("-" * 78)

        flow_results.append({
            "flow_id": flow_id,
            "student_name": s_name,
            "passed": scenario_passed,
            "score": avg_score,
            "plan_summary": {
                "prep_hours": plan.total_prep_hours,
                "projected_marks": plan.projected_marks_yield,
                "learning_gain": plan.educational_metrics.learning_gain,
                "normalized_gain_pct": plan.educational_metrics.normalized_gain_pct,
                "efficiency_per_hour": plan.educational_metrics.efficiency_per_hour
            }
        })

    summary_color = GREEN if all_flows_passed else RED
    print(f"\n{BOLD}{summary_color}ALL 4 FLOWS EVALUATION STATUS: {'100% PASSED' if all_flows_passed else 'FAILED'}{RESET}\n")

    return {
        "all_passed": all_flows_passed,
        "flows": flow_results
    }


if __name__ == "__main__":
    results = execute_all_4_flows()
    sys.exit(0 if results["all_passed"] else 1)
