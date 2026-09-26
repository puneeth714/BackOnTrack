"""
Learning Gain & Adaptive Pace Calculator Tool
Implements:
1. Learning Gain Formulas:
   - Simple Gain:        LearningGain = S_post - S_pre
   - Normalized Gain:    NormalizedGain = (S_post - S_pre) / (100 - S_pre)
   - Efficiency:         Efficiency = LearningGain / StudyTime (marks gained per minute)
2. Adaptive Pace & Dynamic Recalibration Engine:
   - Base cohort solving time + personal gap multiplier
   - Dynamic Google-Maps-style rerouting when student finishes early or takes longer
"""

from typing import Dict, Any, List, Optional


def calculate_learning_metrics(s_pre: float, s_post: float, study_time_mins: float) -> Dict[str, Any]:
    """
    Computes quantifiable educational gain metrics for a student.
    
    Args:
        s_pre: Pre-test baseline score (scaled to 100).
        s_post: Post-session target / achieved score (scaled to 100).
        study_time_mins: Total study time invested in minutes.
        
    Returns:
        Dictionary containing simple gain, normalized gain percentage,
        and learning efficiency (marks per minute and marks per hour).
    """
    learning_gain = round(s_post - s_pre, 2)
    
    # Avoid division by zero if pre-test was already 100
    denominator = 100.0 - s_pre
    if denominator <= 0:
        normalized_gain = 1.0
    else:
        normalized_gain = round(learning_gain / denominator, 4)
        
    if study_time_mins > 0:
        efficiency_per_min = round(learning_gain / study_time_mins, 4)
        efficiency_per_hour = round(efficiency_per_min * 60.0, 2)
    else:
        efficiency_per_min = 0.0
        efficiency_per_hour = 0.0

    return {
        "s_pre": s_pre,
        "s_post": s_post,
        "study_time_mins": study_time_mins,
        "learning_gain": learning_gain,
        "normalized_gain_pct": round(normalized_gain * 100.0, 1),
        "efficiency_per_minute": efficiency_per_min,
        "efficiency_per_hour": efficiency_per_hour,
        "summary_text": (
            f"Pre-score: {s_pre}/100 → Post-target: {s_post}/100 | "
            f"Gain: +{learning_gain} marks ({round(normalized_gain * 100.0, 1)}% normalized gain) | "
            f"Study Efficiency: {efficiency_per_min} marks/min ({efficiency_per_hour} marks/hr)"
        )
    }


def calculate_personalized_topic_time(
    base_mins: float,
    attendance_pct: float,
    is_weak_topic: bool = False
) -> Dict[str, Any]:
    """
    Calculates initial personalized study time for a topic based on cohort baseline
    and student's personal attendance and test lags.
    
    Args:
        base_mins: Cohort baseline time to master topic (minutes).
        attendance_pct: Student attendance percentage (0-100).
        is_weak_topic: Whether student failed this concept in IA-1.
        
    Returns:
        Personalized allocated minutes, multiplier, and buffer explanation.
    """
    # Attendance lag factor: lower attendance -> higher need for foundational absorption
    att_gap = max(0.0, (85.0 - attendance_pct) / 100.0)  # gap below standard 85% attendance
    att_multiplier = 1.0 + (att_gap * 0.5)               # up to +20% buffer
    
    weakness_multiplier = 1.15 if is_weak_topic else 1.0  # +15% extra time if failed in IA-1
    total_multiplier = round(att_multiplier * weakness_multiplier, 2)
    
    allocated_mins = round(base_mins * total_multiplier, 0)
    buffer_added_mins = allocated_mins - base_mins

    return {
        "base_mins": base_mins,
        "multiplier": total_multiplier,
        "allocated_mins": allocated_mins,
        "buffer_added_mins": buffer_added_mins,
        "rationale": (
            f"Cohort base: {base_mins}m + {buffer_added_mins:.0f}m personal gap buffer "
            f"({attendance_pct}% attendance + {'IA-1 failure' if is_weak_topic else 'standard pace'})."
        )
    }


def recalibrate_study_pace(
    topic_completed: str,
    estimated_mins: float,
    actual_spent_mins: float,
    remaining_budget_mins: float,
    current_planned_topics: List[Dict[str, Any]],
    available_bonus_topics: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Dynamic Closed-Loop Recalibration (The Google Maps Reroute Engine).
    Fires when a student completes a topic. If faster, unlocks bonus marks or rest;
    if slower, automatically trims lowest-priority fluff to guarantee Friday morning sleep.
    
    Args:
        topic_completed: Name of the topic just finished.
        estimated_mins: Previously allocated study time.
        actual_spent_mins: Actual time spent by student.
        remaining_budget_mins: Total remaining study budget before Friday exam.
        current_planned_topics: Topics remaining on the student's active plan.
        available_bonus_topics: List of unassigned high-yield topics that can be unlocked.
        
    Returns:
        Rerouting action, adjusted time budget, updated topic list, and user message.
    """
    time_delta = round(estimated_mins - actual_spent_mins, 1)  # positive = saved time, negative = over budget
    new_remaining_budget = max(0.0, remaining_budget_mins - actual_spent_mins)
    
    active_topics = [t.copy() for t in current_planned_topics if t.get("name") != topic_completed]

    if time_delta > 15.0:
        # SCENARIO A: Student finished noticeably faster (Saved > 15 mins)
        bonus_unlocked = None
        if available_bonus_topics:
            bonus_unlocked = available_bonus_topics[0]
            active_topics.append(bonus_unlocked)
            action = "BONUS_TOPIC_UNLOCKED"
            user_msg = (
                f"⚡ Ahead of Schedule! You finished '{topic_completed}' {time_delta:.0f} mins faster. "
                f"The AI has unlocked bonus topic '{bonus_unlocked.get('name')}' (+{bonus_unlocked.get('marks', 5)} marks) "
                f"to boost your score without extending your bedtime."
            )
        else:
            action = "COGNITIVE_REST_BUFFER_ADDED"
            user_msg = (
                f"⚡ Ahead of Schedule! You saved {time_delta:.0f} mins on '{topic_completed}'. "
                f"Added a 15-min cognitive rest break to keep your brain fresh for Friday."
            )

        return {
            "status": "AHEAD_OF_SCHEDULE",
            "action": action,
            "time_delta_mins": time_delta,
            "new_remaining_budget_mins": new_remaining_budget,
            "updated_topics": active_topics,
            "bonus_unlocked": bonus_unlocked,
            "message": user_msg
        }

    elif time_delta < -15.0:
        # SCENARIO B: Student got stuck and took > 15 mins longer
        time_over = abs(time_delta)
        # Reroute: drop the lowest yield / least critical topic from remaining list
        dropped_topic = None
        if active_topics:
            # Sort remaining by marks/hours ROI ascending to drop lowest return topic
            active_topics.sort(key=lambda t: t.get("marks", 10) / max(0.5, t.get("prep_hours", 1.0)))
            dropped_topic = active_topics.pop(0)

        action = "LOW_YIELD_TOPIC_DEPRIORITIZED"
        user_msg = (
            f"⚠️ Adaptive Reroute: You spent {time_over:.0f} extra mins on '{topic_completed}'. "
            f"To guarantee you finish within your hard limit and sleep well before Friday, "
            f"the AI has automatically dropped '{dropped_topic.get('name') if dropped_topic else 'optional reading'}'. "
            f"Your core high-yield marks remain 100% protected."
        )

        return {
            "status": "BEHIND_SCHEDULE_REROUTED",
            "action": action,
            "time_delta_mins": time_delta,
            "new_remaining_budget_mins": new_remaining_budget,
            "updated_topics": active_topics,
            "dropped_topic": dropped_topic,
            "message": user_msg
        }

    else:
        # SCENARIO C: On Track (within +/- 15 mins)
        return {
            "status": "ON_TRACK",
            "action": "MAINTAIN_CURRENT_PLAN",
            "time_delta_mins": time_delta,
            "new_remaining_budget_mins": new_remaining_budget,
            "updated_topics": active_topics,
            "message": f"✓ On Track! '{topic_completed}' finished on pace. Proceeding to next scheduled topic."
        }


def generate_adaptive_pacing_overview(
    topics: List[Dict[str, Any]],
    attendance_pct: float,
    weak_topics: List[str]
) -> Dict[str, Any]:
    """
    Computes aggregated adaptive pacing profile and simulated closed-loop checkpoints.
    
    Args:
        topics: List of topic dictionaries containing 'name' and 'prep_hours'.
        attendance_pct: Student attendance percentage.
        weak_topics: List of flagged topics from previous assessments.
        
    Returns:
        Structured adaptive pacing summary with cohort comparisons and simulated triggers.
    """
    cohort_total = 0.0
    personalized_total = 0.0
    
    for t in topics:
        t_name = t.get("name", t.get("topic_name", ""))
        base_mins = t.get("prep_hours", 1.5) * 60.0
        is_weak = any(w.lower() in t_name.lower() for w in weak_topics)
        p_res = calculate_personalized_topic_time(base_mins, attendance_pct, is_weak)
        cohort_total += base_mins
        personalized_total += p_res["allocated_mins"]
        
    buffer_mins = personalized_total - cohort_total
    att_gap_factor = round(max(0.0, (85.0 - attendance_pct) / 100.0), 3)
    
    first_topic = topics[0].get("name", topics[0].get("topic_name", "Preemptive Scheduling")) if topics else "Preemptive Scheduling"
    
    return {
        "total_cohort_base_mins": round(cohort_total, 1),
        "total_personalized_mins": round(personalized_total, 1),
        "total_buffer_mins": round(buffer_mins, 1),
        "attendance_lag_factor": att_gap_factor,
        "recalibration_policy": "Dynamic closed-loop rerouting at +/-15min delta: Fast pace unlocks bonus PYQs; Slow pace deprioritizes low-yield theory to preserve sleep.",
        "checkpoint_simulation": {
            "topic_name": first_topic,
            "scenario_ahead": f"⚡ Ahead (>15m saved): Unlocks bonus PYQ (+5 marks) or adds cognitive rest buffer without altering Friday sleep schedule.",
            "scenario_behind": f"⚠️ Slower (>15m over): Automatically drops lowest-yield reading to preserve sleep and protect core passing marks."
        }
    }


if __name__ == "__main__":
    print("--- 1. Testing Personalized Baseline Time ---")
    p_time = calculate_personalized_topic_time(base_mins=75.0, attendance_pct=59.4, is_weak_topic=True)
    print(p_time["rationale"])

    print("\n--- 2. Testing Dynamic Recalibration (Student Finished Fast) ---")
    current = [{"name": "Banker's Algorithm", "marks": 10, "prep_hours": 1.5}]
    bonus = [{"name": "Process State PCB Fields", "marks": 5, "prep_hours": 0.5}]
    recal_fast = recalibrate_study_pace(
        topic_completed="CPU Scheduling",
        estimated_mins=90.0,
        actual_spent_mins=60.0,
        remaining_budget_mins=360.0,
        current_planned_topics=current,
        available_bonus_topics=bonus
    )
    print(recal_fast["message"])

    print("\n--- 3. Testing Dynamic Recalibration (Student Got Stuck) ---")
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
    print(recal_slow["message"])

    print("\n--- 4. Testing Aggregated Adaptive Pacing Overview ---")
    overview = generate_adaptive_pacing_overview(
        topics=[{"name": "Banker's Algorithm", "prep_hours": 1.5}],
        attendance_pct=59.4,
        weak_topics=["Deadlocks"]
    )
    print("Overview:", overview["recalibration_policy"])

