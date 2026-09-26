# Back on Track – Engineering Roadmap & Tracker

> **Architecture:** Bottom-Up Engineering (Evals First → Tools → Agents → Graph Workflow → Frontend Integration)  
> **Framework:** Google Agent Development Kit (ADK) 2.0 (Python) • Real Google Gemini 2.5 Flash  
> **Curriculum Grounding:** Sri Indu College of Engg & Tech • `R20CSE2202 Operating Systems` (92-Page Official Lecture Notes)  
> **Course:** Operating Systems (`CS304`) • Mid Term Exam Recovery Suite (5 Topics)

---

## 📋 Master Task Checklist

### [Phase 1] Evals & Ground-Truth Test Cases (FIRST) ✅ *COMPLETED*
- [x] **1.1 Eval Dataset (`backend/evals/eval_test_cases.json`):**
  - Case 1: Rohan's scenario (Cultural Fest Lead, 3 weeks missed, 48h left, Mid Term 2).
  - Case 2: Medical Leave scenario (Dengue fever, 2 weeks missed, failed IA-1 with 8/50, needs safe pass).
  - Case 3: Topic-Specific Panic (Knows CPU scheduling, blanking out on Semaphores and Banker's, 24h left).
  - Case 4: High-Potential GPA Recovery (Sports captain, 15h bandwidth, aiming for 45+/50).
- [x] **1.2 Automated Eval Assertions (`backend/evals/eval_runner.py`):**
  - **Syllabus Scoping Test:** Asserted that Module 1 and Module 5 are excluded for Mid Term 2.
  - **Diagnostic Gap Test:** Asserted that student's IA-1 weak areas (0/15 in Synchronization) are prioritized via domain topic taxonomy.
  - **Time Budget Feasibility Test:** Asserted that total study hours $\le$ student's available bandwidth.
  - **Terminology Compliance Test:** Strict regex assertion that "20%/80%" or "Pareto" never appear in output text.
  - **Prerequisite Unlock Test:** Asserted that fundamental micro-concepts precede numericals.
  - **Marks Yield Test:** Asserted that selected topics capture $\ge 70\%$ of the paper.
  - *Benchmark Status:* **4/4 Test Cases Passed (100.0%)**

---

### [Phase 2] Streamlined Deterministic Tools (4 Tools) ✅ *COMPLETED*
- [x] **2.1 LMS Context Tool (`backend/tools/lms_tool.py`):**
  - Reads `mock_data/lms_student_context.json`.
  - Exposes `get_student_lms_context(student_id)`: returns student profile, attendance gap (59.4%), IA-1 scores (8/50), and Missed Lectures Digest.
- [x] **2.2 Academic Knowledge Tool (`backend/tools/knowledge_tool.py`):**
  - Scopes Mid Term 2 modules and prunes non-exam units to protect sleep.
  - Returns high-probability 10-markers vs deprioritized descriptive theory.
- [x] **2.3 Learning Gain & Adaptive Pace Tool (`backend/tools/learning_gain_tool.py`):**
  - Educational Gain Formulas: Learning Gain, Normalized Hake Gain, Study Efficiency (marks per minute/hour).
  - Adaptive topic duration calculation and closed-loop velocity recalibration.
- [x] **2.4 Course Content & Grounding Tool (`backend/tools/course_content_tool.py`):**
  - Grounded in official Sri Indu R20CSE2202 notes.
  - Provides deep packages (Mental model, Visual diagram, 10-mark solved exam answer, Critical traps, MCQs).
  - Live Gemini 2.5 Flash on-demand explanation endpoint (`explain_topic_with_gemini`).
- [x] **2.5 Tool Unit Test Suite (`backend/tools/test_tools.py`):**
  - 100% test passage across schemas, scoping rules, unlock assertions, and math formulas.

---

### [Phase 3] Typed Schemas & Gemini 2.5 Flash ADK Agents ✅ *COMPLETED*
- [x] **3.1 Pydantic Data Contracts (`backend/agents/schemas.py`):**
  - `ParsedStudentIntent`, `EducationalMetrics`, `TopicPacingDetail`, `AdaptivePacingOverview`, `BackOnTrackPlan`.
- [x] **3.2 Agent 1: Real Intent Parser with Gemini 2.5 Flash (`backend/agents/intent_agent.py`):**
  - Uses `google.genai` SDK with model `gemini-2.5-flash` and `response_schema=ParsedStudentIntent`.
  - Parses free-form user emergencies, panic, or time constraints in real time.
- [x] **3.3 Agent 2: Plan Synthesizer (`backend/agents/synthesizer_agent.py`):**
  - Synthesizes student state, syllabus constraints, and gain metrics into structured plan.

---

### [Phase 4] Google ADK 2.0 Graph Workflow ✅ *COMPLETED*
- [x] **4.1 Deterministic Workflow Graph (`backend/workflows/graph_workflow.py`):**
  - Built using official Google ADK 2.0:
    ```python
    from google.adk import Agent, Workflow, Event
    ```
  - Graph edges: `START -> Node 1 (IntentParser) -> Node 2 (LMSExtractor) -> Node 3 (KnowledgeScoper) -> Node 4 (PlanSynthesizer)`.
- [x] **4.2 Execution Verifier (`backend/workflows/test_workflow.py`):**
  - Verified live event passing down all 4 nodes; returns verified output in <250ms.

---

### [Phase 5] FastAPI Backend Server (Port 8080) ✅ *COMPLETED*
- [x] **5.1 Server Implementation (`backend/server.py`):**
  - Serves all REST endpoints required by frontend:
    - `GET /api/student/profile` (Rohan Verma, 59.4% attendance)
    - `GET /api/course/context` (CS304 Operating Systems, Mid Term 2)
    - `GET /api/topics` (5 In-Scope Topics)
    - `GET /api/plan/recovery` (Dynamic recovery route blocks)
    - `GET /api/topics/{id}/content` (Grounded topic guides)
    - `POST /api/topics/{id}/mastery-check` (Real-time pace recalibration)
    - `POST /api/plan/budget` (Compress budget dynamically)
    - `POST /api/chat` (Live Gemini 2.5 Flash Q&A)
    - Direct static endpoints for `/option1.html`, `/option2.html`, `/option3.html`, `/tmp.html`.
- [x] **5.2 Daemon Server Status:**
  - Running live on `http://localhost:8080`.

---

### [Phase 6] 5-Topic Grounded Curriculum (Sri Indu R20CSE2202) ✅ *COMPLETED*
- [x] **6.1 Grounded Material Ingestion:**
  - Downloaded official 92-page PDF: `R20CSE2202-OPERATING-SYSTEMS.pdf`.
  - Cites exact Lecture numbers and Page references for every topic.
- [x] **6.2 The 5 In-Scope Exam Topics:**
  1. `cpu-scheduling`: Preemptive CPU Scheduling (SRTF & Round Robin) [Unit II, P.19-24]
  2. `synchronization`: Process Synchronization (Semaphores & Bounded Buffer) [Unit III, P.31-40]
  3. `deadlocks`: Deadlocks (Banker's Algorithm & Safe State) [Unit III, P.43-52]
  4. `memory-management`: Main Memory & Paging Hardware (TLB & Address Translation) [Unit IV, P.53-64]
  5. `virtual-memory`: Virtual Memory & Page Replacement (FIFO, LRU & Belady's Anomaly) [Unit IV, P.65-76]
- [x] **6.3 Pruned Units for Sleep Protection:**
  - Units 1 & 5 (System Calls & Disk Scheduling) pruned to save 6.5 hours of study time before Friday exam.

---

### [Phase 7] Pop-Up Mastery Quiz Dialog & Overall Assessment Engine ✅ *COMPLETED*
- [x] **7.1 Topic Pop-Up Mastery Quiz (Modal Dialog):**
  - Replaced bottom-of-page placement with a dedicated interactive modal dialog.
  - Progressive 3 MCQs per topic (Concept, Calculation, Trap) with instant emerald/crimson feedback and scoring.
- [x] **7.2 Overall Comprehensive Exam Mock Assessment:**
  - 5-question holistic evaluation (1 question from each of the 5 topics).
  - Real-time scoring ($0-5$) with diagnostic feedback.
- [x] **7.3 Diagnostic Weak-Area Recommender ("Topics to Read Again"):**
  - Any topic with missed questions is automatically flagged as a weak area.
  - Renders an amber banner on the dashboard with 1-click links to re-read that topic.
- [x] **7.4 Completion & Velocity Recalibration:**
  - Marking complete updates topic badge, increments progress bar ($0\% \rightarrow 100\%$), and recalculates study velocity ($8.53 \rightarrow 10.78\text{ marks/h}$).

---

### [Phase 8] Frontend Options & Next.js Integration ✅ *COMPLETED*
- [x] **8.1 Three Live Showcase Options:**
  - Option 1 (`option1.html`): Emergency Chat-First Flow.
  - Option 2 (`option2.html`): Dashboard-First Flow.
  - Option 3 (`option3.html`): The Hybrid Pitch Flow (Recommended).
  - All 3 options feature the top switcher bar and identical deep 5-topic reader + quiz modal.
- [x] **8.2 Next.js App (`BackOnTrack-FE` on Port 3000):**
  - Pulled Hruthik's latest origin/main commits (ambient audio, railway quote dialog, parent photo, backlog fee alert).
  - Resolved merge conflict in `src/components/ask/ask-screen.tsx`, preserving both Hruthik's audio/fullscreen controls and live Gemini 2.5 Flash chat.
  - Wired `demo-provider.tsx` to initialize from live `httpLearningApi` (`http://localhost:8080/api`).
  - Passed `vitest run` (**7/7 tests pass**) and `tsc --noEmit` (**0 errors**).
