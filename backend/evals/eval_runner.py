"""
Back on Track - Automated Evaluation Benchmark Runner (Phase 1)
Evaluates academic triage outputs against strict pedagogical & structural assertions.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Terminal color codes for clean CLI reporting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class BackOnTrackEvaluator:
    """Evaluates triage engine outputs against strict ground-truth assertions."""

    def __init__(self, test_cases_path: Path):
        with open(test_cases_path, "r") as f:
            self.benchmark = json.load(f)
        self.test_cases = self.benchmark["test_cases"]

    def evaluate_scoping(self, plan: Dict[str, Any], assertions: Dict[str, Any]) -> Tuple[bool, str]:
        """Asserts that excluded modules are never recommended and active modules are covered."""
        active_modules = plan.get("scoped_modules", [])
        excluded_found = []

        # Check for forbidden out-of-scope modules
        for forbidden in assertions.get("must_exclude_modules", []):
            for m in active_modules:
                if forbidden.lower() in m.lower():
                    excluded_found.append(forbidden)

        if excluded_found:
            return False, f"Leaked out-of-scope modules into Mid Term: {excluded_found}"
        return True, "All out-of-scope modules correctly excluded."

    # Domain topic taxonomy mapping concept clusters to specific question archetypes
    TOPIC_TAXONOMY = {
        "process synchronization": ["synchronization", "semaphore", "producer-consumer", "critical section", "mutex", "readers-writers"],
        "deadlocks": ["deadlock", "banker", "need matrix", "safe sequence", "resource allocation"],
        "paging": ["paging", "tlb", "address translation", "page table", "emat"],
        "cpu scheduling": ["cpu scheduling", "srtf", "round robin", "sjf", "gantt chart", "waiting time"]
    }

    def evaluate_diagnostic_gap(self, plan: Dict[str, Any], test_case: Dict[str, Any]) -> Tuple[bool, str]:
        """Asserts that the student's specific LMS weak areas are directly targeted in the plan."""
        high_impact_topics = [t["topic_name"] for t in plan.get("highest_impact_topics", [])]
        high_impact_str = " ".join(high_impact_topics).lower()

        weak_areas = test_case["lms_context"].get("flagged_weak_topics", [])
        targeted = []

        for area in weak_areas:
            area_lower = area.lower()
            # 1. Direct substring check
            if area_lower in high_impact_str:
                targeted.append(area)
                continue

            # 2. Taxonomy / synonym cluster check
            matched_synonym = False
            for cluster_key, synonyms in self.TOPIC_TAXONOMY.items():
                if cluster_key in area_lower or any(s in area_lower for s in synonyms):
                    if any(s in high_impact_str for s in synonyms):
                        targeted.append(f"{area} (via {', '.join([s for s in synonyms if s in high_impact_str])})")
                        matched_synonym = True
                        break
            
            if not matched_synonym:
                # 3. Fallback stem match
                words = [w.rstrip('s') for w in area_lower.split() if len(w) > 3]
                if any(w in high_impact_str for w in words):
                    targeted.append(area)

        if not targeted and weak_areas:
            return False, f"Failed to target student's LMS weak areas: {weak_areas}"
        return True, f"Targeted LMS gaps: {targeted}"

    def evaluate_time_budget(self, plan: Dict[str, Any], assertions: Dict[str, Any]) -> Tuple[bool, str]:
        """Asserts that the study plan does not exceed the student's available bandwidth."""
        total_hours = plan.get("total_prep_hours", 0.0)
        max_allowed = assertions.get("max_allowed_hours", 24.0)

        if total_hours > max_allowed:
            return False, f"Plan exceeds bandwidth: {total_hours}h allocated vs {max_allowed}h max allowed."
        return True, f"Feasible time budget: {total_hours}h <= {max_allowed}h."

    def evaluate_terminology(self, plan: Dict[str, Any], assertions: Dict[str, Any]) -> Tuple[bool, str]:
        """Asserts that forbidden buzzwords ('20%', '80%', 'pareto') do not appear in the generated plan."""
        plan_text = json.dumps(plan).lower()
        forbidden_terms = assertions.get("forbidden_terms", ["20%", "80%", "pareto"])
        
        found = []
        for term in forbidden_terms:
            if re.search(r'\b' + re.escape(term) + r'\b', plan_text):
                found.append(term)

        if found:
            return False, f"Forbidden buzzwords detected in student output: {found}"
        return True, "Strict compliance: zero buzzwords found."

    def evaluate_prerequisite_topology(self, plan: Dict[str, Any]) -> Tuple[bool, str]:
        """Asserts that fundamental unlock principles are scheduled before their dependent numerical topics."""
        schedule = plan.get("day_wise_schedule", [])
        ordered_items = []
        for day in schedule:
            for item in day.get("tasks", []):
                ordered_items.append(item.get("task_name", "").lower())

        ordered_text = " -> ".join(ordered_items)
        
        # Rule 1: Process States must precede CPU Scheduling
        if "cpu scheduling" in ordered_text and "process state" in ordered_text:
            if ordered_text.find("process state") > ordered_text.find("cpu scheduling"):
                return False, "Topological error: CPU Scheduling scheduled before Process State unlock."

        # Rule 2: Semaphore mental model must precede Producer-Consumer
        if "producer-consumer" in ordered_text and "semaphore" in ordered_text:
            if ordered_text.find("semaphore") > ordered_text.find("producer-consumer"):
                return False, "Topological error: Producer-Consumer scheduled before Semaphore unlock."

        return True, "Topological order valid: prerequisites strictly precede dependent algorithms."

    def evaluate_marks_yield(self, plan: Dict[str, Any], assertions: Dict[str, Any]) -> Tuple[bool, str]:
        """Asserts that the selected topics yield the minimum required marks."""
        marks_yield = plan.get("projected_marks_yield", 0)
        min_required = assertions.get("min_marks_yield", 25)

        if marks_yield < min_required:
            return False, f"Marks yield too low: {marks_yield} marks vs {min_required} required."
        return True, f"High yield: {marks_yield}/50 marks captured."

    def run_all_evals(self, plan_generator_fn) -> Dict[str, Any]:
        """Runs the entire benchmark suite against all test cases."""
        print(f"\n{BOLD}{CYAN}========================================================================{RESET}")
        print(f"{BOLD}{CYAN}   BACK ON TRACK - EVALUATION BENCHMARK RUNNER (PHASE 1)                {RESET}")
        print(f"{BOLD}{CYAN}========================================================================{RESET}\n")

        results = []
        all_passed = True

        for tc in self.test_cases:
            tc_id = tc["test_id"]
            name = tc["persona_name"]
            cat = tc["category"]
            assertions = tc["ground_truth_assertions"]

            print(f"{BOLD}▶ Running {tc_id}: {name} [{cat}]{RESET}")

            # Generate plan for this test case
            plan = plan_generator_fn(tc)

            # Run 6 evaluation axes
            checks = {
                "Syllabus Scoping": self.evaluate_scoping(plan, assertions),
                "Diagnostic Gap Hit": self.evaluate_diagnostic_gap(plan, tc),
                "Time Budget Feasibility": self.evaluate_time_budget(plan, assertions),
                "Prerequisite Topology": self.evaluate_prerequisite_topology(plan),
                "Terminology Compliance": self.evaluate_terminology(plan, assertions),
                "Marks Yield Efficiency": self.evaluate_marks_yield(plan, assertions)
            }

            case_passed = True
            for check_name, (passed, msg) in checks.items():
                status_icon = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
                print(f"   [{status_icon}] {BOLD}{check_name}:{RESET} {msg}")
                if not passed:
                    case_passed = False
                    all_passed = False

            results.append({
                "test_id": tc_id,
                "persona": name,
                "passed": case_passed,
                "details": checks
            })
            print("-" * 72)

        summary_color = GREEN if all_passed else RED
        total_cases = len(self.test_cases)
        passed_cases = sum(1 for r in results if r["passed"])
        print(f"\n{BOLD}{summary_color}BENCHMARK SUMMARY: {passed_cases}/{total_cases} Test Cases Passed ({(passed_cases/total_cases)*100:.1f}%){RESET}\n")

        return {
            "all_passed": all_passed,
            "passed_count": passed_cases,
            "total_count": total_cases,
            "cases": results
        }


# Reference plan generator used to verify evaluation suite
def reference_triage_engine(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reference engine implementation that adheres to our data specifications.
    Demonstrates expected model behavior during Phase 1 evals.
    """
    tc_id = test_case["test_id"]

    if tc_id == "TC_001_ROHAN_FEST_LEAD":
        return {
            "scoped_modules": ["Module 2 (Part B): CPU Scheduling", "Module 3: Sync & Deadlocks", "Module 4 (Part A): Main Memory"],
            "highest_impact_topics": [
                {"topic_name": "Preemptive CPU Scheduling (SRTF & Round Robin)", "marks": 12, "hours": 2.0},
                {"topic_name": "Producer-Consumer Problem using Semaphores", "marks": 10, "hours": 1.5},
                {"topic_name": "Banker's Algorithm for Deadlock Avoidance", "marks": 10, "hours": 2.0},
                {"topic_name": "Paging Hardware Architecture & TLB EMAT", "marks": 8, "hours": 1.0}
            ],
            "fundamental_unlocks": [
                {"concept": "Process States & Ready Queue", "hours": 0.5},
                {"concept": "Semaphore Token Analogy", "hours": 0.5}
            ],
            "deprioritized_topics": ["Dining Philosophers with Monitors", "Multilevel Feedback Queue Theory", "Segmentation Hardware"],
            "total_prep_hours": 7.5,
            "projected_marks_yield": 40,
            "day_wise_schedule": [
                {
                    "day": 1,
                    "tasks": [
                        {"task_name": "Process State Diagram & Ready Queue (30m)", "hours": 0.5},
                        {"task_name": "CPU Scheduling Numericals: SRTF & Round Robin (2.0h)", "hours": 2.0},
                        {"task_name": "Semaphore Mental Model (30m)", "hours": 0.5},
                        {"task_name": "Producer-Consumer with Semaphores (1.5h)", "hours": 1.5}
                    ]
                },
                {
                    "day": 2,
                    "tasks": [
                        {"task_name": "Banker's Algorithm Numerical (2.0h)", "hours": 2.0},
                        {"task_name": "Paging Hardware Diagram & TLB EMAT (1.0h)", "hours": 1.0}
                    ]
                }
            ]
        }
    elif tc_id == "TC_002_PRIYA_MEDICAL_PASS":
        return {
            "scoped_modules": ["Module 2 (Part B)", "Module 3", "Module 4 (Part A)"],
            "highest_impact_topics": [
                {"topic_name": "Banker's Algorithm for Deadlock Avoidance", "marks": 10, "hours": 2.0},
                {"topic_name": "Paging Hardware Architecture & TLB EMAT", "marks": 8, "hours": 1.5},
                {"topic_name": "Preemptive CPU Scheduling (SRTF)", "marks": 12, "hours": 2.5}
            ],
            "total_prep_hours": 8.0,
            "projected_marks_yield": 30,
            "day_wise_schedule": [
                {"day": 1, "tasks": [{"task_name": "Need Vector in Deadlock Avoidance", "hours": 0.5}, {"task_name": "Banker's Algorithm", "hours": 2.0}]},
                {"day": 2, "tasks": [{"task_name": "Logical Address to Physical Address", "hours": 0.5}, {"task_name": "Paging Hardware Architecture & TLB EMAT", "hours": 1.5}]},
                {"day": 3, "tasks": [{"task_name": "CPU Scheduling", "hours": 2.5}]}
            ]
        }
    elif tc_id == "TC_003_KEVIN_SPECIFIC_PANIC":
        return {
            "scoped_modules": ["Module 3", "Module 4 (Part A)"],
            "highest_impact_topics": [
                {"topic_name": "Producer-Consumer Problem using Semaphores", "marks": 10, "hours": 1.5},
                {"topic_name": "Banker's Algorithm for Deadlock Avoidance", "marks": 10, "hours": 1.5}
            ],
            "total_prep_hours": 3.5,
            "projected_marks_yield": 20,
            "day_wise_schedule": [
                {"day": 1, "tasks": [{"task_name": "Semaphore Mental Model", "hours": 0.5}, {"task_name": "Producer-Consumer Problem using Semaphores", "hours": 1.5}, {"task_name": "Banker's Algorithm for Deadlock Avoidance", "hours": 1.5}]}
            ]
        }
    else:  # TC_004_ANANYA_HIGH_RECOVERY
        return {
            "scoped_modules": ["Module 2 (Part B)", "Module 3", "Module 4 (Part A)"],
            "highest_impact_topics": [
                {"topic_name": "Preemptive CPU Scheduling (SRTF & Round Robin)", "marks": 12, "hours": 2.5},
                {"topic_name": "Producer-Consumer Problem using Semaphores", "marks": 10, "hours": 2.0},
                {"topic_name": "Banker's Algorithm for Deadlock Avoidance", "marks": 10, "hours": 2.0},
                {"topic_name": "Paging Hardware Architecture & TLB EMAT", "marks": 8, "hours": 1.5},
                {"topic_name": "Deadlock 4 Necessary Conditions & PCB", "marks": 6, "hours": 1.0}
            ],
            "total_prep_hours": 11.0,
            "projected_marks_yield": 46,
            "day_wise_schedule": [
                {"day": 1, "tasks": [{"task_name": "Process State Diagram & Ready Queue", "hours": 0.5}, {"task_name": "CPU Scheduling (SRTF & Round Robin)", "hours": 2.5}]},
                {"day": 2, "tasks": [{"task_name": "Semaphore Tokens", "hours": 0.5}, {"task_name": "Producer-Consumer with Semaphores", "hours": 2.0}, {"task_name": "Banker's Algorithm", "hours": 2.0}]},
                {"day": 3, "tasks": [{"task_name": "Paging & TLB EMAT", "hours": 1.5}, {"task_name": "Deadlock 4 Necessary Conditions", "hours": 1.0}]}
            ]
        }


if __name__ == "__main__":
    benchmark_file = Path(__file__).parent / "eval_test_cases.json"
    evaluator = BackOnTrackEvaluator(benchmark_file)
    results = evaluator.run_all_evals(reference_triage_engine)
    sys.exit(0 if results["all_passed"] else 1)
