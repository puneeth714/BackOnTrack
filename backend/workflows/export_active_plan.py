"""
Active Plan Exporter
Executes the ADK 2.0 Graph Workflow and exports the typed plan directly to
frontend/active_plan.json for instant UI consumption.
"""

import json
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from workflows.graph_workflow import root_workflow


def export_plan_to_frontend(
    user_message: str = "I missed the last 3 weeks of Operating Systems and my exam is this Friday. I only have about 6 hours to prepare. What should I focus on to catch up and do well?",
    student_id: str = "STU_2022_CS104"
):
    project_root = Path(__file__).resolve().parent.parent.parent
    frontend_dir = project_root / "frontend"
    output_file = frontend_dir / "active_plan.json"

    print(f"Executing ADK Graph for: '{user_message[:60]}...'")
    result = root_workflow.run(user_message, student_id=student_id)
    plan = result["final_plan"]

    # Export plan as formatted JSON
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(plan.model_dump_json(indent=2))

    print(f"✓ Successfully exported active plan to: {output_file}")
    print(f"  Student: {plan.student_name} | Target Exam: {plan.target_exam}")
    print(f"  Yield: {plan.projected_marks_yield}/50 | Efficiency: {plan.educational_metrics.efficiency_per_hour} marks/hr")
    return output_file


if __name__ == "__main__":
    export_plan_to_frontend()
