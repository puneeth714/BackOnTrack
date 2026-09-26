"""
Pydantic Schemas & Data Contracts for Back on Track ADK Agents (Phase 3)
Strictly enforces structured, typed input/output across all agent invocations.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ParsedStudentIntent(BaseModel):
    """Structured extraction from student's plain-text input message."""
    subject: str = Field(
        default="Operating Systems",
        description="The course or subject mentioned by the student."
    )
    days_left: int = Field(
        default=2,
        ge=1,
        le=14,
        description="Days remaining until the exam."
    )
    hours_available: float = Field(
        default=7.5,
        ge=1.0,
        le=40.0,
        description="Total study hours the student can realistically dedicate."
    )
    situation_summary: str = Field(
        description="Summary of the interruption (fest lead, illness, emergency, backlog panic)."
    )
    target_goal: str = Field(
        default="First Class Recovery",
        description="Target outcome: Safe Pass (30+), First Class (38+), or High Distinction (45+)."
    )
    conversational_reply: str = Field(
        default="",
        description="Direct conversational answer and pedagogical guidance addressing whatever question or situation the student asked."
    )



class EducationalMetrics(BaseModel):
    """Quantitative learning gain & efficiency measurements."""
    s_pre: float = Field(description="Pre-test baseline score (scaled to 100).")
    s_post: float = Field(description="Post-session target score (scaled to 100).")
    learning_gain: float = Field(description="Simple gain: S_post - S_pre.")
    normalized_gain_pct: float = Field(description="Normalized gain %: (S_post - S_pre)/(100 - S_pre) * 100.")
    efficiency_per_minute: float = Field(description="Marks gained per minute of study.")
    efficiency_per_hour: float = Field(description="Marks gained per hour of study.")
    summary_text: str = Field(description="Human-readable summary of the metrics.")


class TopicPacingDetail(BaseModel):
    """Detailed mathematical pacing breakdown for a topic."""
    base_cohort_mins: float = Field(default=60.0, description="Standard cohort baseline mastery time in minutes.")
    personalized_mins: float = Field(default=75.0, description="Dynamically adjusted minutes based on attendance and test lags.")
    pace_multiplier: float = Field(default=1.0, description="Dynamic multiplier applied to cohort base.")
    buffer_added_mins: float = Field(default=0.0, description="Additional buffer minutes allocated for foundation recovery.")
    rationale: str = Field(default="", description="Reasoning behind personalized duration.")


class DynamicCheckpoint(BaseModel):
    """Simulated closed-loop pacing reroute scenario."""
    topic_name: str
    scenario_ahead: str
    scenario_behind: str


class AdaptivePacingOverview(BaseModel):
    """Overall adaptive pacing summary for the student's plan."""
    total_cohort_base_mins: float
    total_personalized_mins: float
    total_buffer_mins: float
    attendance_lag_factor: float
    recalibration_policy: str
    checkpoint_simulation: DynamicCheckpoint


class TriageTopic(BaseModel):
    """High-yield topic archetype prioritized by the engine."""
    topic_name: str
    module: str
    marks: int
    prep_hours: float
    pattern: str
    prerequisite: Optional[str] = None
    model_answer_summary: str
    pacing_detail: Optional[TopicPacingDetail] = None


class FundamentalUnlock(BaseModel):
    """20-minute conceptual unlock that prevents getting stuck in numericals."""
    concept_name: str
    reading_time_mins: int
    mental_model: str
    why_stuck: str
    unlocks_topics: List[str]


class DeprioritizedTopic(BaseModel):
    """Low-yield or optional topic that can be safely skipped."""
    topic_name: str
    module: str
    reason_to_skip: str
    hours_saved: float


class DayTask(BaseModel):
    """Atomic study task inside a day schedule."""
    task_name: str
    hours: float
    category: str  # Foundation Unlock, 10-Marker Practice, Formula Review


class DailySchedule(BaseModel):
    """Day-by-day atomic study block."""
    day_number: int
    day_title: str
    target_hours: float
    target_marks: int
    tasks: List[DayTask]


class ConfidenceMCQ(BaseModel):
    """High-yield diagnostic MCQ with instant rationale."""
    question: str
    options: List[str]
    correct_option_index: int
    explanation: str


class MissedLecturesDigestPayload(BaseModel):
    """Synthesized summary simulating lecture slide / PPT analysis."""
    period: str
    slides_summary: List[str]
    key_takeaway: str


class BackOnTrackPlan(BaseModel):
    """The master typed triage output produced by the ADK agent pipeline."""
    student_name: str
    target_exam: str
    total_prep_hours: float
    projected_marks_yield: int
    missed_lectures_digest: MissedLecturesDigestPayload
    educational_metrics: EducationalMetrics
    highest_impact_topics: List[TriageTopic]
    fundamental_unlocks: List[FundamentalUnlock]
    deprioritized_topics: List[DeprioritizedTopic]
    day_wise_schedule: List[DailySchedule]
    confidence_mcqs: List[ConfidenceMCQ]
    adaptive_pacing: Optional[AdaptivePacingOverview] = None


class PacingRecalibrationResult(BaseModel):
    """Result of dynamic closed-loop pace recalibration."""
    status: str
    action: str
    time_delta_mins: float
    new_remaining_budget_mins: float
    message: str

