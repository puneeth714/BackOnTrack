"""
Unit tests for the two streamlined deterministic tools:
1. lms_tool.py
2. knowledge_tool.py
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from tools.lms_tool import get_student_lms_context
from tools.knowledge_tool import get_academic_knowledge
from tools.learning_gain_tool import calculate_learning_metrics


def test_lms_tool():
    print("Testing LMS Context Tool...")
    data = get_student_lms_context("STU_2022_CS104")
    assert data["status"] == "success"
    assert data["student_name"] == "Rohan Verma"
    assert data["target_exam"]["name"] == "Mid Term Exam (Internal Assessment 2)"
    assert data["target_exam"]["total_marks"] == 50
    assert data["attendance_metrics"]["attendance_pct"] == 59.4
    assert len(data["academic_lags"]["flagged_weak_topics"]) >= 2
    assert "Process Synchronization & Semaphores" in data["academic_lags"]["flagged_weak_topics"]
    
    # Assert Missed Lecture Digest is present
    digest = data["missed_lectures_digest"]
    assert len(digest["slides_summary"]) == 3
    assert "Peterson's software solution" in digest["slides_summary"][0]
    print("  ✓ LMS Context Tool passed all contract checks.")


def test_knowledge_tool():
    print("Testing Academic Knowledge Tool...")
    data = get_academic_knowledge("Mid Term 2", "Operating Systems")
    assert data["status"] == "success"
    assert data["target_exam"] == "Mid Term 2"
    
    # Scoping checks: Modules 1 and 5 must be excluded
    excluded_codes = [m["module_code"] for m in data["syllabus_scoping"]["excluded_modules"]]
    assert "M1" in excluded_codes
    assert "M5" in excluded_codes
    assert len(data["syllabus_scoping"]["active_modules"]) == 3
    
    # Question Intelligence checks
    high_yield = data["question_intelligence"]["high_yield_topics"]
    topic_names = [t["topic_name"] for t in high_yield]
    assert any("Scheduling" in t for t in topic_names)
    assert any("Producer-Consumer" in t for t in topic_names)
    assert any("Banker's" in t for t in topic_names)
    assert any("Paging" in t for t in topic_names)
    
    # Unlocks check
    unlocks = data["fundamental_unlocks"]
    assert len(unlocks) == 4
    unlock_names = [u["concept_name"] for u in unlocks]
    assert any("Process States" in u for u in unlock_names)
    assert any("Semaphore" in u for u in unlock_names)
    print("  ✓ Academic Knowledge Tool passed all contract checks.")


from tools.learning_gain_tool import (
    calculate_learning_metrics,
    calculate_personalized_topic_time,
    recalibrate_study_pace,
    generate_adaptive_pacing_overview
)



def test_learning_gain_tool():
    print("Testing Learning Gain & Efficiency Tool...")
    # S_pre = 16 (8/50 scaled to 100), S_post = 76 (38/50 scaled to 100), StudyTime = 450 mins (7.5h)
    metrics = calculate_learning_metrics(s_pre=16.0, s_post=76.0, study_time_mins=450.0)
    
    # Simple Gain: 76 - 16 = 60
    assert metrics["learning_gain"] == 60.0
    
    # Normalized Gain: 60 / (100 - 16) = 60 / 84 = 71.4%
    assert metrics["normalized_gain_pct"] == 71.4
    
    # Efficiency: 60 / 450 = 0.1333 marks/min = 8.0 marks/hr
    assert metrics["efficiency_per_minute"] == 0.1333
    assert metrics["efficiency_per_hour"] == 8.0
    print("  ✓ Learning Gain Tool passed all math & normalization assertions.")


def test_adaptive_pace_engine():
    print("Testing Adaptive Pace Recalibration Engine...")
    
    # 1. Test Personal Baseline Allocation
    p_time = calculate_personalized_topic_time(base_mins=75.0, attendance_pct=59.4, is_weak_topic=True)
    assert p_time["allocated_mins"] > 75.0  # Buffer added due to attendance & IA-1 lag
    assert p_time["buffer_added_mins"] >= 20.0
    print("  ✓ Personalized Baseline Time correctly applied attendance & weakness buffer.")
    
    # 2. Test Fast Pace (Ahead of Schedule)
    recal_fast = recalibrate_study_pace(
        topic_completed="CPU Scheduling",
        estimated_mins=90.0,
        actual_spent_mins=60.0,
        remaining_budget_mins=360.0,
        current_planned_topics=[{"name": "Banker's Algorithm", "marks": 10, "prep_hours": 1.5}],
        available_bonus_topics=[{"name": "Process State PCB Fields", "marks": 5, "prep_hours": 0.5}]
    )
    assert recal_fast["status"] == "AHEAD_OF_SCHEDULE"
    assert recal_fast["action"] == "BONUS_TOPIC_UNLOCKED"
    assert recal_fast["time_delta_mins"] == 30.0
    assert any(t["name"] == "Process State PCB Fields" for t in recal_fast["updated_topics"])
    print("  ✓ Fast pace correctly triggered bonus topic unlock.")
    
    # 3. Test Slow Pace (Behind Schedule)
    recal_slow = recalibrate_study_pace(
        topic_completed="Producer-Consumer",
        estimated_mins=60.0,
        actual_spent_mins=95.0,
        remaining_budget_mins=240.0,
        current_planned_topics=[
            {"name": "Segmentation Hardware", "marks": 4, "prep_hours": 1.5},
            {"name": "Banker's Algorithm", "marks": 10, "prep_hours": 1.5}
        ]
    )
    assert recal_slow["status"] == "BEHIND_SCHEDULE_REROUTED"
    assert recal_slow["action"] == "LOW_YIELD_TOPIC_DEPRIORITIZED"
    assert recal_slow["dropped_topic"]["name"] == "Segmentation Hardware"
    print("  ✓ Slow pace correctly trimmed lowest-yield topic to protect sleep.")

    # 4. Test Aggregated Adaptive Pacing Overview
    overview = generate_adaptive_pacing_overview(
        topics=[
            {"name": "Preemptive Scheduling (SRTF, Round Robin)", "prep_hours": 2.0},
            {"name": "Banker's Algorithm for Deadlock Avoidance", "prep_hours": 1.5}
        ],
        attendance_pct=59.4,
        weak_topics=["Process Synchronization & Semaphores", "Banker's Algorithm"]
    )
    assert overview["total_cohort_base_mins"] == 210.0
    assert overview["total_personalized_mins"] > 210.0
    assert overview["total_buffer_mins"] > 0
    assert "checkpoint_simulation" in overview
    print("  ✓ Aggregated Adaptive Pacing Overview calculated cohort base and dynamic buffers correctly.")



if __name__ == "__main__":
    test_lms_tool()
    test_knowledge_tool()
    test_learning_gain_tool()
    test_adaptive_pace_engine()
    print("\nAll Phase 2 tool tests (LMS, Knowledge, Learning Gain, Pace Engine) PASSED successfully!")
