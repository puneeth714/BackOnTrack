"""
Agent 2: Plan Synthesizer Agent
Combines Student Intent, LMS Context, Academic Knowledge, and the Learning Gain Tool
into a typed, validated BackOnTrackPlan.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Ensure backend root and repo root are in sys.path
backend_dir = Path(__file__).resolve().parent.parent
repo_dir = backend_dir.parent
for p in [str(backend_dir), str(repo_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from agents.schemas import (
        ParsedStudentIntent,
        BackOnTrackPlan,
        EducationalMetrics,
        TriageTopic,
        FundamentalUnlock,
        DeprioritizedTopic,
        DayTask,
        DailySchedule,
        ConfidenceMCQ,
        MissedLecturesDigestPayload,
        TopicPacingDetail,
        DynamicCheckpoint,
        AdaptivePacingOverview
    )
    from tools.lms_tool import get_student_lms_context
    from tools.knowledge_tool import get_academic_knowledge
    from tools.learning_gain_tool import (
        calculate_learning_metrics,
        calculate_personalized_topic_time,
        generate_adaptive_pacing_overview
    )
except ImportError:
    from backend.agents.schemas import (
        ParsedStudentIntent,
        BackOnTrackPlan,
        EducationalMetrics,
        TriageTopic,
        FundamentalUnlock,
        DeprioritizedTopic,
        DayTask,
        DailySchedule,
        ConfidenceMCQ,
        MissedLecturesDigestPayload,
        TopicPacingDetail,
        DynamicCheckpoint,
        AdaptivePacingOverview
    )
    from backend.tools.lms_tool import get_student_lms_context
    from backend.tools.knowledge_tool import get_academic_knowledge
    from backend.tools.learning_gain_tool import (
        calculate_learning_metrics,
        calculate_personalized_topic_time,
        generate_adaptive_pacing_overview
    )



def synthesize_back_on_track_plan(
    intent: ParsedStudentIntent,
    lms_context: Dict[str, Any],
    academic_knowledge: Dict[str, Any]
) -> BackOnTrackPlan:
    """
    Synthesizes a complete academic recovery plan for the student.
    
    Args:
        intent: Parsed student intent and time budget.
        lms_context: LMS data containing attendance, test history, and slide digest.
        academic_knowledge: Scoped syllabus, PYQ patterns, and prerequisite unlocks.
        
    Returns:
        Validated BackOnTrackPlan instance.
    """
    student_name = lms_context.get("student_name", "Rohan Verma")
    target_exam = lms_context.get("target_exam", {}).get("name", "Mid Term 2 Exam")
    
    # 1. Digest of missed lectures (simulating PPT/PDF analysis)
    digest_raw = lms_context.get("missed_lectures_digest", {})
    missed_digest = MissedLecturesDigestPayload(
        period=digest_raw.get("period", "Weeks 7 to 9 (15 Lecture Hours)"),
        slides_summary=digest_raw.get("slides_summary", []),
        key_takeaway=digest_raw.get("key_takeaway", "Core algorithmic focus missed.")
    )

    # 2. Select Highest-Impact Topics & Compute Personalized Pacing
    raw_high_yield = academic_knowledge.get("question_intelligence", {}).get("high_yield_topics", [])
    selected_topics: List[TriageTopic] = []
    
    attendance_pct = lms_context.get("attendance_metrics", {}).get("attendance_pct", 75.0)
    weak_topics = lms_context.get("academic_lags", {}).get("flagged_weak_topics", [])
    
    model_summaries = {
        "Preemptive Scheduling (SRTF, Round Robin)": "Draw Gantt chart tick-by-tick at arrival times. Tabulate CT, TAT (CT-AT), and WT (TAT-BT). Box the average WT.",
        "Producer-Consumer Bounded Buffer Problem": "Declare mutex=1, empty=N, full=0. Write standard 15-line C pseudocode for producer and consumer loops with wait() and signal().",
        "Banker's Algorithm for Deadlock Avoidance": "Compute Need matrix = Max - Allocation. Trace step-by-step safety sequence Work=Work+Alloc. State final safe vector.",
        "Paging Hardware, TLB & Address Translation": "Draw CPU logical address (p, d) -> TLB check -> Page table -> Physical address (f, d). Apply EMAT formula."
    }

    for item in raw_high_yield:
        t_name = item.get("topic_name")
        if t_name in model_summaries:
            base_mins = item.get("prep_hours", 1.5) * 60.0
            is_weak = any(w.lower() in t_name.lower() for w in weak_topics)
            p_res = calculate_personalized_topic_time(
                base_mins=base_mins,
                attendance_pct=attendance_pct,
                is_weak_topic=is_weak
            )
            pacing_detail = TopicPacingDetail(
                base_cohort_mins=p_res["base_mins"],
                personalized_mins=p_res["allocated_mins"],
                pace_multiplier=p_res["multiplier"],
                buffer_added_mins=p_res["buffer_added_mins"],
                rationale=p_res["rationale"]
            )
            selected_topics.append(TriageTopic(
                topic_name=t_name,
                module=item.get("module"),
                marks=item.get("marks", 10),
                prep_hours=item.get("prep_hours", 2.0),
                pattern=item.get("pattern", "Compulsory 10-marker"),
                prerequisite=item.get("unlock_prerequisite"),
                model_answer_summary=model_summaries.get(t_name, ""),
                pacing_detail=pacing_detail
            ))

    # 3. Fundamental Unlocks (Prerequisites)
    raw_unlocks = academic_knowledge.get("fundamental_unlocks", [])
    fundamental_unlocks: List[FundamentalUnlock] = []
    for u in raw_unlocks[:3]:  # Top 3 essential unlocks
        fundamental_unlocks.append(FundamentalUnlock(
            concept_name=u.get("concept_name"),
            reading_time_mins=u.get("reading_time_minutes", 20),
            mental_model=u.get("the_1_minute_mental_model", ""),
            why_stuck=u.get("why_students_get_stuck", ""),
            unlocks_topics=u.get("unlocks_topics", [])
        ))

    # 4. Safe-to-Deprioritize Topics
    raw_deprioritized = academic_knowledge.get("question_intelligence", {}).get("deprioritized_topics", [])
    deprioritized: List[DeprioritizedTopic] = []
    for d in raw_deprioritized:
        deprioritized.append(DeprioritizedTopic(
            topic_name=d.get("topic_name"),
            module=d.get("module"),
            reason_to_skip=d.get("reason"),
            hours_saved=2.0
        ))

    # 5. Build Day-by-Day Schedule based on intent.days_left
    days_left = intent.days_left
    schedules: List[DailySchedule] = []
    
    if days_left <= 2:
        # Thursday / Friday morning sprint
        schedules.append(DailySchedule(
            day_number=1,
            day_title="Day 1 (Thursday): Concurrency & CPU Sched Sprint",
            target_hours=4.5,
            target_marks=22,
            tasks=[
                DayTask(task_name="Process State Diagram & Ready Queue Unlock", hours=0.5, category="Foundation Unlock"),
                DayTask(task_name="Preemptive Scheduling (SRTF & Round Robin) Numericals", hours=2.0, category="10-Marker Practice"),
                DayTask(task_name="Semaphore Token Mental Model", hours=0.5, category="Foundation Unlock"),
                DayTask(task_name="Producer-Consumer Problem with Semaphores Code", hours=1.5, category="10-Marker Practice")
            ]
        ))
        schedules.append(DailySchedule(
            day_number=2,
            day_title="Day 2 (Friday Morning): Deadlocks & Paging Lock-in",
            target_hours=3.0,
            target_marks=18,
            tasks=[
                DayTask(task_name="Need Vector Rule Unlock", hours=0.5, category="Foundation Unlock"),
                DayTask(task_name="Banker's Algorithm Safety Sequence Numerical", hours=1.5, category="10-Marker Practice"),
                DayTask(task_name="Paging Hardware Diagram & TLB Access Time Formula", hours=1.0, category="10-Marker Practice")
            ]
        ))
    else:
        # 3+ Days spread
        schedules.append(DailySchedule(
            day_number=1,
            day_title="Day 1: CPU Scheduling & Process Models",
            target_hours=3.5,
            target_marks=18,
            tasks=[
                DayTask(task_name="Process State Diagram Unlock", hours=0.5, category="Foundation Unlock"),
                DayTask(task_name="SRTF & Round Robin Practice", hours=3.0, category="10-Marker Practice")
            ]
        ))
        schedules.append(DailySchedule(
            day_number=2,
            day_title="Day 2: Synchronization & Deadlocks",
            target_hours=4.0,
            target_marks=20,
            tasks=[
                DayTask(task_name="Semaphore Tokens & Producer-Consumer", hours=2.0, category="10-Marker Practice"),
                DayTask(task_name="Banker's Algorithm Practice", hours=2.0, category="10-Marker Practice")
            ]
        ))

    # 6. Confidence MCQs
    confidence_mcqs = [
        ConfidenceMCQ(
            question="In Banker's Algorithm, if Max[i] = [7, 5, 3] and Allocation[i] = [2, 1, 2], what is Need[i]?",
            options=["[9, 6, 5]", "[5, 4, 1]", "[7, 5, 3]", "[2, 1, 2]"],
            correct_option_index=1,
            explanation="Need = Max - Allocation = [7-2, 5-1, 3-2] = [5, 4, 1]."
        ),
        ConfidenceMCQ(
            question="What is the initial value of semaphore 'empty' in bounded buffer of size N?",
            options=["0", "1", "N", "-1"],
            correct_option_index=2,
            explanation="Initially all N buffer slots are empty, so empty is initialized to N."
        )
    ]

    total_prep_hours = sum(s.target_hours for s in schedules)
    projected_marks = 40  # 40 out of 50 marks

    # 7. Compute Quantitative Educational Metrics (User's Formulas)
    # Pre-score: IA-1 score (8/50) scaled to 100 = 16.0
    # Post-score: Projected yield (40/50) scaled to 100 = 80.0
    s_pre = (lms_context.get("academic_lags", {}).get("mid_term_1_score", 8) / 50.0) * 100.0
    s_post = (projected_marks / 50.0) * 100.0
    study_time_mins = total_prep_hours * 60.0

    raw_metrics = calculate_learning_metrics(s_pre=s_pre, s_post=s_post, study_time_mins=study_time_mins)
    educational_metrics = EducationalMetrics(
        s_pre=raw_metrics["s_pre"],
        s_post=raw_metrics["s_post"],
        learning_gain=raw_metrics["learning_gain"],
        normalized_gain_pct=raw_metrics["normalized_gain_pct"],
        efficiency_per_minute=raw_metrics["efficiency_per_minute"],
        efficiency_per_hour=raw_metrics["efficiency_per_hour"],
        summary_text=raw_metrics["summary_text"]
    )

    # 8. Compute Aggregated Adaptive Pacing Overview
    pacing_overview_dict = generate_adaptive_pacing_overview(
        topics=[{"name": t.topic_name, "prep_hours": t.prep_hours} for t in selected_topics],
        attendance_pct=attendance_pct,
        weak_topics=weak_topics
    )
    checkpoint_sim = DynamicCheckpoint(
        topic_name=pacing_overview_dict["checkpoint_simulation"]["topic_name"],
        scenario_ahead=pacing_overview_dict["checkpoint_simulation"]["scenario_ahead"],
        scenario_behind=pacing_overview_dict["checkpoint_simulation"]["scenario_behind"]
    )
    adaptive_pacing = AdaptivePacingOverview(
        total_cohort_base_mins=pacing_overview_dict["total_cohort_base_mins"],
        total_personalized_mins=pacing_overview_dict["total_personalized_mins"],
        total_buffer_mins=pacing_overview_dict["total_buffer_mins"],
        attendance_lag_factor=pacing_overview_dict["attendance_lag_factor"],
        recalibration_policy=pacing_overview_dict["recalibration_policy"],
        checkpoint_simulation=checkpoint_sim
    )

    return BackOnTrackPlan(
        student_name=student_name,
        target_exam=target_exam,
        total_prep_hours=total_prep_hours,
        projected_marks_yield=projected_marks,
        missed_lectures_digest=missed_digest,
        educational_metrics=educational_metrics,
        highest_impact_topics=selected_topics,
        fundamental_unlocks=fundamental_unlocks,
        deprioritized_topics=deprioritized,
        day_wise_schedule=schedules,
        confidence_mcqs=confidence_mcqs,
        adaptive_pacing=adaptive_pacing
    )



if __name__ == "__main__":
    from backend.agents.intent_agent import parse_student_intent
    
    intent = parse_student_intent("I missed 3 weeks of OS because of cultural fest, exam this Friday, have 2 days left.")
    lms = get_student_lms_context()
    knowledge = get_academic_knowledge()
    
    plan = synthesize_back_on_track_plan(intent, lms, knowledge)
    print("Synthesized Back on Track Plan:")
    print(f"Student: {plan.student_name} | Exam: {plan.target_exam}")
    print(f"Total Prep: {plan.total_prep_hours} hrs | Projected Yield: {plan.projected_marks_yield}/50 Marks")
    print(f"Educational Metrics: {plan.educational_metrics.summary_text}")
    print(f"Topics: {[t.topic_name for t in plan.highest_impact_topics]}")
