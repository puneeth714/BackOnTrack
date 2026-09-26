"""
Academic Knowledge Tool (Tool 2 of 2)
Consolidates Curriculum Scoping, 5-Year PYQ Question Weightage, and Prerequisite
Unlock Mental Models into a single unified knowledge provider.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


def get_academic_knowledge(exam_type: str = "Mid Term 2", subject: str = "Operating Systems") -> Dict[str, Any]:
    """
    Retrieves the scoped syllabus, past question paper patterns, and foundational
    unlock principles for the target assessment.
    
    Args:
        exam_type: Type of exam, e.g. "Mid Term 2" or "End Sem".
        subject: Course title, e.g. "Operating Systems".
        
    Returns:
        Structured dictionary containing:
        - Scoped in-scope modules vs excluded out-of-scope modules with academic reasons
        - High-probability question archetypes (10-markers)
        - Safe-to-deprioritize topics
        - Prerequisite unlock mental models
    """
    mock_dir = Path(__file__).resolve().parent.parent.parent / "mock_data"
    
    syllabus_file = mock_dir / "os_midterm_syllabus.json"
    pyq_file = mock_dir / "midterm_pyq_weightage.json"
    foundations_file = mock_dir / "fundamental_concepts_os.json"
    
    for f in [syllabus_file, pyq_file, foundations_file]:
        if not f.exists():
            raise FileNotFoundError(f"Academic data file not found: {f}")
            
    with open(syllabus_file, "r", encoding="utf-8") as f:
        syllabus_data = json.load(f)
    with open(pyq_file, "r", encoding="utf-8") as f:
        pyq_data = json.load(f)
    with open(foundations_file, "r", encoding="utf-8") as f:
        foundations_data = json.load(f)

    scoping = syllabus_data.get("syllabus_scoping_rules", {})
    active_modules = scoping.get("active_modules_for_midterm", [])
    excluded_modules = scoping.get("excluded_modules", [])
    
    # Extract high-yield topics vs safe-to-deprioritize
    high_yield_topics = []
    deprioritized_topics = []
    
    for mod in active_modules:
        for topic in mod.get("topics", []):
            if topic.get("impact_category") in ["CRITICAL_MUST_COVER", "FUNDAMENTAL_UNLOCK"]:
                high_yield_topics.append({
                    "topic_name": topic.get("name"),
                    "module": mod.get("module_name"),
                    "marks": topic.get("marks"),
                    "prep_hours": topic.get("prep_hours"),
                    "pattern": topic.get("pattern"),
                    "unlock_prerequisite": topic.get("unlock_prerequisite")
                })
            elif topic.get("impact_category") == "SAFELY_DEPRIORITIZE":
                deprioritized_topics.append({
                    "topic_name": topic.get("name"),
                    "module": mod.get("module_name"),
                    "reason": topic.get("pattern")
                })

    return {
        "status": "success",
        "subject": subject,
        "target_exam": exam_type,
        "syllabus_scoping": {
            "scoping_logic": scoping.get("scoping_logic"),
            "active_modules": [m.get("module_name") for m in active_modules],
            "active_module_details": active_modules,
            "excluded_modules": excluded_modules
        },
        "question_intelligence": {
            "total_marks": pyq_data.get("standard_paper_format", {}).get("total_marks", 50),
            "question_pairings": pyq_data.get("question_pattern_intelligence", []),
            "high_yield_topics": high_yield_topics,
            "deprioritized_topics": deprioritized_topics
        },
        "fundamental_unlocks": foundations_data.get("unlock_principles", [])
    }


if __name__ == "__main__":
    knowledge = get_academic_knowledge()
    print(f"Academic Knowledge Tool Loaded Successfully for: {knowledge['subject']}")
    print(f"Active Modules in Scope: {len(knowledge['syllabus_scoping']['active_modules'])}")
    print(f"Excluded Modules (Dropped): {[m['module_code'] for m in knowledge['syllabus_scoping']['excluded_modules']]}")
    print(f"High-Yield Question Archetypes: {len(knowledge['question_intelligence']['high_yield_topics'])}")
    print(f"Prerequisite Unlocks Available: {len(knowledge['fundamental_unlocks'])}")
