"""
Unit test suite for Phase 3 ADK Agents:
1. intent_agent.py
2. synthesizer_agent.py
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from agents.schemas import ParsedStudentIntent, BackOnTrackPlan
from agents.intent_agent import parse_student_intent
from agents.synthesizer_agent import synthesize_back_on_track_plan
from tools.lms_tool import get_student_lms_context
from tools.knowledge_tool import get_academic_knowledge


def test_intent_agent():
    print("Testing Agent 1 (Intent Parser)...")
    msg = "I missed the last 3 weeks of Operating Systems because of the college cultural fest and my exam is this Friday. I only have about 2 days to prepare. What should I focus on to catch up and do well?"
    intent = parse_student_intent(msg)
    
    assert isinstance(intent, ParsedStudentIntent)
    assert intent.subject == "Operating Systems"
    assert intent.days_left == 2
    assert intent.hours_available <= 10.0
    assert "fest" in intent.situation_summary.lower()

    print(f"  ✓ Intent Parser Agent passed. Extracted: {intent.days_left} days left, {intent.hours_available}h.")


def test_synthesizer_agent():
    print("Testing Agent 2 (Plan Synthesizer with Educational Metrics)...")
    msg = "I missed 3 weeks of OS due to fest, exam on Friday, 2 days left."
    intent = parse_student_intent(msg)
    lms = get_student_lms_context("STU_2022_CS104")
    knowledge = get_academic_knowledge("Mid Term 2", "Operating Systems")
    
    plan = synthesize_back_on_track_plan(intent, lms, knowledge)
    
    assert isinstance(plan, BackOnTrackPlan)
    assert plan.student_name == "Rohan Verma"
    assert plan.total_prep_hours <= 8.0
    assert plan.projected_marks_yield >= 35
    
    # Assert Educational Metrics are populated
    metrics = plan.educational_metrics
    assert metrics.s_pre == 16.0  # (8/50) * 100
    assert metrics.s_post == 80.0  # (40/50) * 100
    assert metrics.learning_gain == 64.0
    assert metrics.normalized_gain_pct == 76.2  # 64 / (100 - 16)
    assert metrics.efficiency_per_minute > 0
    assert metrics.efficiency_per_hour > 0
    
    # Assert Missed Lecture Digest is included
    assert len(plan.missed_lectures_digest.slides_summary) >= 3
    
    # Assert Topics and Schedule
    assert len(plan.highest_impact_topics) >= 3
    assert len(plan.fundamental_unlocks) >= 2
    assert len(plan.day_wise_schedule) == 2
    assert len(plan.confidence_mcqs) >= 2
    
    # Assert Adaptive Pacing and Topic Breakdown
    assert plan.adaptive_pacing is not None
    assert plan.adaptive_pacing.total_cohort_base_mins > 0
    assert plan.adaptive_pacing.total_personalized_mins >= plan.adaptive_pacing.total_cohort_base_mins
    assert plan.adaptive_pacing.checkpoint_simulation is not None
    assert len(plan.highest_impact_topics[0].pacing_detail.rationale) > 0
    print(f"  ✓ Adaptive Pacing verified: Cohort Base {plan.adaptive_pacing.total_cohort_base_mins}m -> Personalized {plan.adaptive_pacing.total_personalized_mins}m (+{plan.adaptive_pacing.total_buffer_mins}m buffer)")

    # Assert Zero Buzzwords
    plan_json = plan.model_dump_json().lower()
    assert "20%" not in plan_json
    assert "80%" not in plan_json
    assert "pareto" not in plan_json
    
    print(f"  ✓ Plan Synthesizer Agent passed all contract checks.")
    print(f"    Metric Summary: {metrics.summary_text}")



if __name__ == "__main__":
    test_intent_agent()
    test_synthesizer_agent()
    print("\nAll Phase 3 Agent tests PASSED successfully!")
