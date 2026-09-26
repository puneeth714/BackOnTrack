"""
LMS Context Tool (Tool 1 of 2)
Simulates retrieving student profile, attendance logs, past internal assessment
scores, and the 3-week missed lecture slide digest from the college LMS database.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


def get_student_lms_context(student_id: str = "STU_2022_CS104") -> Dict[str, Any]:
    """
    Retrieves the student's academic standing, attendance gaps, recent IA-1 marks,
    and a synthesized digest of missed lecture slides directly from the LMS database.
    
    Args:
        student_id: Unique university student identifier (default: Rohan Verma).
        
    Returns:
        Structured dictionary containing student profile, upcoming exam target,
        attendance logs, diagnostic lags, and the missed lectures summary.
    """
    # Locate mock_data relative to this file
    data_path = Path(__file__).resolve().parent.parent.parent / "mock_data" / "lms_student_context.json"
    
    if not data_path.exists():
        raise FileNotFoundError(f"LMS student context database not found at {data_path}")
        
    with open(data_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    # Roster of test personas for multi-flow evaluation
    ROSTER = {
        "STU_2022_CS104": {
            "name": "Sunder",
            "attendance": 59.4,
            "ia1": 8,
            "reason": "Cultural Fest Lead Coordinator & medical fever",
            "weak_topics": ["Process Synchronization & Semaphores", "Deadlocks"]
        },
        "STU_2022_CS089": {
            "name": "Priya Sharma",
            "attendance": 64.0,
            "ia1": 14,
            "reason": "Hospitalized with severe dengue fever (2 weeks)",
            "weak_topics": ["Deadlocks Banker's Algorithm", "Paging Hardware"]
        },
        "STU_2022_CS042": {
            "name": "Kevin D'Souza",
            "attendance": 78.0,
            "ia1": 24,
            "reason": "Hackathon & placement preparation crunch",
            "weak_topics": ["Semaphores Concurrency", "Banker's Algorithm"]
        },
        "STU_2022_CS012": {
            "name": "Ananya Iyer",
            "attendance": 68.5,
            "ia1": 22,
            "reason": "Inter-University Sports Tournament Captain",
            "weak_topics": ["Process Synchronization", "Deadlock Detection"]
        }
    }

    profile = ROSTER.get(student_id, ROSTER["STU_2022_CS104"])

    student = raw_data.get("student", {})
    course = raw_data.get("current_course", {})
    exam = raw_data.get("upcoming_exam", {})
    attendance = raw_data.get("attendance_and_engagement_logs", {})
    diagnostics = raw_data.get("academic_history_and_diagnostics", {})
    
    # Extract the simulated slide digest for missed classes
    slide_digest = attendance.get("lms_activity_signals", {}).get("missed_lectures_digest", {})

    return {
        "status": "success",
        "student_id": student_id,
        "student_name": profile["name"],
        "course_code": course.get("course_code", "CS304"),
        "course_title": course.get("course_title", "Operating Systems"),
        "target_exam": {
            "name": exam.get("exam_type", "Mid Term Exam 2"),
            "date": exam.get("exam_date", "2026-10-16"),
            "day": exam.get("exam_day", "Friday"),
            "total_marks": exam.get("total_marks", 50)
        },
        "attendance_metrics": {
            "attendance_pct": profile["attendance"],
            "status": "CRITICAL_SHORTAGE_WARNING" if profile["attendance"] < 65 else "SATISFACTORY",
            "interruption_reason": profile["reason"],
            "duration": attendance.get("interruption_period", {}).get("duration", "3 weeks missed")
        },
        "academic_lags": {
            "mid_term_1_score": profile["ia1"],
            "mid_term_1_max": 50,
            "flagged_weak_topics": profile["weak_topics"],
            "detailed_signals": diagnostics.get("specific_weak_areas_flagged", [])
        },
        "missed_lectures_digest": {
            "period": slide_digest.get("period", "Weeks 7 to 9 (15 Lecture Hours)"),
            "slides_summary": slide_digest.get("slides_summary", []),
            "key_takeaway": slide_digest.get("key_takeaway_for_student", "")
        }
    }


if __name__ == "__main__":
    context = get_student_lms_context()
    print(f"LMS Context Tool Loaded Successfully for: {context['student_name']}")
    print(f"Target Exam: {context['target_exam']['name']} on {context['target_exam']['date']}")
    print(f"Flagged Weak Areas: {context['academic_lags']['flagged_weak_topics']}")
    print(f"Missed Lecture Summary Lines: {len(context['missed_lectures_digest']['slides_summary'])}")
