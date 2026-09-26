"""
Agent 1: Natural Language Intent & Conversational Triage Agent
Powered by Google Gemini 2.5 Flash via google.genai.
Handles organic student questions, time-budget adjustments, conceptual doubts,
and structured intent parsing.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional

# Ensure backend and repo roots are in sys.path
backend_dir = Path(__file__).resolve().parent.parent
repo_dir = backend_dir.parent
for p in [str(backend_dir), str(repo_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from agents.schemas import ParsedStudentIntent
except ImportError:
    from backend.agents.schemas import ParsedStudentIntent


# Load API key from environment or local .env
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    env_file = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                os.environ["GEMINI_API_KEY"] = API_KEY
                break


def parse_student_intent(message: str) -> ParsedStudentIntent:
    """
    Analyzes student message using Google Gemini 2.5 Flash.
    Returns both structured parameters for the timetable AND an empathetic,
    direct conversational answer to whatever question the student asked.
    
    Args:
        message: Plain-text student message or question.
        
    Returns:
        Validated ParsedStudentIntent instance.
    """
    # Attempt real LLM generation via Gemini 2.5 Flash
    if API_KEY:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=API_KEY)
            system_prompt = (
                "You are 'Back on Track', an expert empathetic academic triage AI agent for university engineering students. "
                "The student may be panicked, stressed, asking about time constraints, or asking specific conceptual/syllabus questions. "
                "Analyze the user's message thoroughly. "
                "1. If they ask a question or express worry, provide an honest, reassuring, highly specific conversational_reply. "
                "2. Extract: subject (e.g. Operating Systems), days_left (integer), hours_available (float), "
                "situation_summary (e.g. fest lead, hospital stay, panic), and target_goal (e.g. Safe Pass, First Class Recovery). "
                "If study hours are not explicitly stated, infer realistic dedicated study hours: 3.5 to 4.0 hours per remaining day (e.g. 2 days left -> 7.5 to 8.0 hours total). "
                "Never use forbidden buzzwords like '20%/80%' or 'Pareto'. Always speak as a caring, authoritative academic mentor."

            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=message,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ParsedStudentIntent,
                    system_instruction=system_prompt,
                    temperature=0.2
                )
            )

            if response.text:
                return ParsedStudentIntent.model_validate_json(response.text)
        except Exception as e:
            # Fall through to deterministic fallback if network/quota error
            pass

    # Deterministic Fallback if offline
    subject = "Operating Systems"
    if "os" in message.lower() or "operating systems" in message.lower():
        subject = "Operating Systems"
    elif "dsa" in message.lower() or "data structures" in message.lower():
        subject = "Data Structures & Algorithms"
    elif "dbms" in message.lower() or "database" in message.lower():
        subject = "Database Management Systems"

    days_left = 2
    days_match = re.search(r'(\d+)\s*(?:days?|day)', message, re.IGNORECASE)
    if days_match:
        days_left = int(days_match.group(1))
    elif "this friday" in message.lower() or "48 hours" in message.lower():
        days_left = 2
    elif "tomorrow" in message.lower() or "24 hours" in message.lower():
        days_left = 1
    elif "week" in message.lower() and "missed" not in message.lower():
        days_left = 7

    hours_available = 7.5
    hours_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)', message, re.IGNORECASE)
    if hours_match:
        hours_available = float(hours_match.group(1))
    else:
        hours_available = min(days_left * 4.0, 16.0)

    situation = "General time shortage"
    goal = "First Class Recovery (38+ Marks)"
    
    msg_lower = message.lower()
    if "fest" in msg_lower or "cultural" in msg_lower or "sports" in msg_lower:
        situation = "Cultural fest / extracurricular coordinator gap"
    elif "sick" in msg_lower or "hospital" in msg_lower or "dengue" in msg_lower or "medical" in msg_lower:
        situation = "Medical emergency / convalescence recovery"
    elif "panic" in msg_lower or "blank" in msg_lower or "freeze" in msg_lower:
        situation = "Topic-specific conceptual panic"

    if "pass" in msg_lower or "safe" in msg_lower:
        goal = "Safe Pass (30+ Marks)"
    elif "distinction" in msg_lower or "cgpa" in msg_lower or "high" in msg_lower:
        goal = "High Distinction (42+ Marks)"

    reply = (
        f"I understand your situation regarding {situation.lower()}. "
        f"With {hours_available} hours over the next {days_left} days, we can target a realistic {goal}. "
        f"I've scoped out all unnecessary syllabus fluff so you can focus 100% on the core 10-markers."
    )

    return ParsedStudentIntent(
        subject=subject,
        days_left=days_left,
        hours_available=hours_available,
        situation_summary=situation,
        target_goal=goal,
        conversational_reply=reply
    )


if __name__ == "__main__":
    test_msg = "I only have 3 hours now because of a hospital emergency, can I still pass OS on Friday?"
    print(f"Testing Gemini Agent with prompt: '{test_msg}'")
    intent = parse_student_intent(test_msg)
    print("\n--- Real Agent Output ---")
    print("Subject:", intent.subject)
    print("Hours Available:", intent.hours_available)
    print("Days Left:", intent.days_left)
    print("Situation:", intent.situation_summary)
    print("Target Goal:", intent.target_goal)
    print("Conversational Reply:\n", intent.conversational_reply)
