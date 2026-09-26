# 🎯 BackOnTrack — AI Exam Recovery Engine
### BITSoM Vertex Builders' Pitch Fest 2026 • Operating Systems (CS304 / R20CSE2202)
[![Next.js 15](https://img.shields.io/badge/Next.js-15%20App%20Router-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Google ADK 2.0](https://img.shields.io/badge/Google%20ADK-2.0%20Multi--Agent-4285F4?logo=google)](https://cloud.google.com/vertex-ai)
[![Gemini 2.5 Flash](https://img.shields.io/badge/Gemini-2.5%20Flash-orange?logo=googlegemini)](https://ai.google.dev/)
[![Tests Passing](https://img.shields.io/badge/tests-7%2F7%20passing-brightgreen)](https://github.com/puneeth714/BackOnTrack)

---

## 📌 Executive Summary & Problem Statement

In Indian engineering colleges (JNTU, Anna University, VTU, autonomous institutes), **over 38% of students accumulate backlogs / arrears** during their 2nd and 3rd years. Missing 2–3 weeks due to illness, attendance shortages, or family crises typically results in failing Internal Assessments (Midterms), which cascades into semester-end backlogs.

### 💰 The Financial & Career Penalty:
* **The College Backlog Penalty:** A student failing Midterm 2 enters academic probation, must pay a **₹3,500 supplementary backlog registration fee** per subject, and suffers a **6-month delay** to graduation with a permanent "Arrear" stamp on their mark sheet.
* **The BackOnTrack Recovery Pass:** A **₹300 one-time pass** (91.4% direct cost reduction, saving ₹3,200) that diagnoses learning gaps, triages official syllabus notes, and generates an adaptive **4.3-hour recovery pathway** guaranteeing the required passing score (20/50 marks).

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    Student[👤 Student in Distress] -->|Types Situation in Intake Chat| FE[Next.js 15 UI Client :3000]
    FE -->|POST /api/agent/triage| API[FastAPI Orchestration Gateway :8080]

    subgraph ADK["Google Agent Development Kit (ADK) 2.0 Graph Pipeline"]
        N1[🤖 IntentParserAgent<br/>Gemini 2.5 Flash] -->|Extracts Time & Mood Constraints| N2[🛠️ LMSExtractorTool<br/>Student Profile: 59.4% att, 8/50 Mid-1]
        N2 -->|Queries Target Marks| N3[🛠️ KnowledgeScoperTool<br/>Sri Indu R20CSE2202 PDF Scoper]
        N3 -->|Prunes Low-Yield Theory| N4[🤖 PlanSynthesizerAgent<br/>Gemini 2.5 Flash Knapsack Optimizer]
    end

    API --> ADK
    ADK -->|Returns Execution Trace + 5-Topic Adaptive Plan| FE

    subgraph GroundedEngine["Curriculum Grounding & Mastery Recalibration"]
        FE -->|POST /api/topics/{id}/ask| GeminiQA[Gemini 2.5 Grounded Explainer]
        FE -->|POST /api/topics/{id}/mastery-check| Recalibrator[Dynamic Schedule Recalibration]
        Recalibrator -->|Updates Remaining Time & Readiness| FE
    end
```

---

## 📚 Grounded Course Curriculum (Sri Indu Autonomous R20CSE2202)

All study modules, formulas, traps, and MCQs are grounded directly in the official **Sri Indu Institute of Engineering & Technology 92-page lecture notes**:

| # | Topic | Unit & Citation | Compulsory Exam Yield | Estimated Time | Key Concepts & Numerical Traps |
|---|-------|-----------------|----------------------|----------------|--------------------------------|
| **1** | **CPU Scheduling** | Unit II (P.19–24) | **12 Marks** | 45 min | SRTF preemption Gantt chart, Round Robin quantum simulation, TAT = CT - AT, WT = TAT - BT |
| **2** | **Process Synchronization** | Unit II (P.28–34) | **10 Marks** | 50 min | Critical Section 3 criteria, Peterson's 2-process solution, Counting Semaphores, Producer-Consumer bounded buffer |
| **3** | **Deadlocks** | Unit III (P.41–48) | **12 Marks** | 60 min | 4 Coffman conditions, Banker's Algorithm Safety matrix ($Need = Max - Allocation$), Resource-Request algorithm |
| **4** | **Main Memory & Paging** | Unit IV (P.52–59) | **10 Marks** | 40 min | Paging MMU hardware, Page table base register (PTBR), TLB Hit/Miss effective memory access time ($EMAT = h(t + m) + (1-h)(t + 2m)$) |
| **5** | **Virtual Memory** | Unit IV (P.63–71) | **10 Marks** | 35 min | Demand paging, FIFO anomaly (Belady's), Optimal (OPT), Least Recently Used (LRU) stack/counter implementation |

**Total In-Scope Preparation:** 230 minutes (~3.8 hours) • **Guaranteed Mark Yield:** 34–40 Marks (Passing threshold: 20/50).

---

## ⚡ The Live Demo & PRD Reproduction Flow

To reproduce the exact pitch demonstration for judges:

### Step 1: Open the Application
Navigate to `http://localhost:3000/student` in your browser.

### Step 2: Intake Chat & Live ADK 2.0 Execution Trace
1. In the triage chat box at the top, select the pre-filled prompt or type:
   > *"Sir I was hospitalized with dengue for 3 weeks and got only 8/50 in Mid-1. My Mid-2 exam is tomorrow morning and I only have 4 hours left. Please help me pass!"*
2. Click **Generate Recovery Plan**.
3. Observe the **Live Google ADK 2.0 Multi-Agent Execution Pipeline** render in real-time with pulse indicators:
   * **Node 1: IntentParserAgent** (Gemini 2.5 Flash parses 4.0h limit, high panic, pass target).
   * **Node 2: LMSExtractorTool** (Retrieves Rohan Verma, 59.4% attendance, 8/50 in IA-1).
   * **Node 3: KnowledgeScoperTool** (Identifies Units II, III, IV as compulsory 10–12 markers).
   * **Node 4: PlanSynthesizerAgent** (Compiles optimal 5-topic route, yielding 34 marks in 230 min).
4. Expand any execution node to inspect raw JSON payload arguments and model reasoning.

### Step 3: The Unified Recovery Plan & Price ROI Comparison
1. Review the **Backlog Insurance ROI Banner**:
   * **University Backlog Fee:** ₹3,500 + 6-month semester delay.
   * **BackOnTrack AI Pass:** ₹300 (91% cost reduction, saving ₹3,200).
2. Review the **Metric Strip**:
   * Displays `Time available: 6.0h (230m left)` which dynamically updates as topics are completed.
3. Review the **Next Best Block**:
   * Explicitly labeled as `Step 1 of 5 in Recovery Route (Active Focus)`: **CPU Scheduling (45 min)**.
   * Provides immediate access to:
     * **Start Focus Mode (45m)** (timed Pomodoro focus session with audio).
     * **Study Guide** (grounded syllabus notes).
     * **⚡ Pop-up Quiz** (3 topic MCQs).

### Step 4: Grounded Study Guide & Instant Gemini Q&A
1. Click **Study Guide** on Topic 1 (or any topic in the list below):
   * Inspect the formatted syllabus notes, Gantt chart, step-by-step algorithms, and common traps.
   * Use the embedded **"Ask Gemini about this concept"** box to ask a custom question (e.g., *"What is dispatch latency?"*) and receive an instant grounded response.

### Step 5: Pop-up Quiz & Dynamic Time Recalibration
1. Click **⚡ Pop-up Quiz** (tab in modal):
   * Answer the 3 syllabus-grounded questions.
   * Click **Mark Mastered & Recalibrate Plan**.
2. **Observe Dynamic Recalibration in Real-Time:**
   * Topic 1 duration changes to **✓ 0 min / Mastered**.
   * Active study time remaining decrements from **230 min ➔ 185 min** in the Metric Strip and route header.
   * Exam readiness score jumps from **46% ➔ 56%** (+10%).
   * "Next Best Block" automatically advances to **Step 2: Process Synchronization (50 min)**!

### Step 6: Midterm 2 Mock Exam
1. Click **Take Mock Exam** in the purple banner at the top of the Recovery Route.
2. Complete the 5-question multi-topic diagnostic exam.
3. Review your final percentage score and question-by-question explanations.

---

## 🛠️ Installation & Local Setup

### Prerequisites
* **Python 3.10+** (with virtual environment support)
* **Node.js 18+** & **corepack** (or `pnpm`)
* A valid `GEMINI_API_KEY` (optional; deterministic fallback included)

### 1. Clone the Repository
```bash
git clone https://github.com/puneeth714/BackOnTrack.git
cd BackOnTrack
```

### 2. Configure Environment Variables
Create `.env` in the root folder:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8080
```

Create `BackOnTrack-FE/.env.local`:
```bash
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080/api
NEXT_PUBLIC_DEMO_MODE=false
```

### 3. Start the Backend API Server
```bash
# In the root repository
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python3 backend/server.py
# Server runs on http://localhost:8080
```

### 4. Start the Frontend Next.js Client
```bash
cd BackOnTrack-FE
corepack pnpm install
corepack pnpm dev --port 3000
# Web client runs on http://localhost:3000
```

### 5. Run Verification & Unit Tests
```bash
cd BackOnTrack-FE
corepack pnpm typecheck   # TypeScript check (0 errors)
corepack pnpm test        # Vitest suite (7/7 passing)
```

---

## 📂 Repository Structure

```
BackOnTrack/
├── backend/
│   ├── server.py                  # FastAPI gateway, CORS, REST & Gemini endpoints
│   ├── agents/
│   │   ├── triage_agent.py        # Google ADK 2.0 triage orchestrator
│   │   ├── intent_agent.py        # Gemini intent classification agent
│   │   └── plan_synthesizer.py    # Knapsack recovery plan synthesizer
│   ├── tools/
│   │   ├── lms_tool.py            # Student college profile & attendance extractor
│   │   ├── syllabus_tool.py       # Sri Indu R20CSE2202 syllabus scoper
│   │   ├── course_content_tool.py # Grounded study guides & 15 MCQs
│   │   └── learning_gain_tool.py  # Adaptive pacing & dynamic time recalibration
│   └── requirements.txt           # Python dependencies
├── BackOnTrack-FE/                # Next.js 15 App Router Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── overview/          # OverviewScreen & live ADK execution trace
│   │   │   ├── plan/              # RecoveryRoute, TopicStudyModal, MockExamModal
│   │   │   ├── focus/             # FocusScreen (Pomodoro timer & study music engine)
│   │   │   └── ui/                # Accessible design system components
│   │   ├── services/api/          # HTTP client & type definitions
│   │   └── state/demo-provider.tsx# Global recovery state & closed-loop updates
│   └── package.json
├── R20CSE2202-OPERATING-SYSTEMS.pdf # Official 92-page Sri Indu lecture notes
└── README.md                      # Comprehensive project documentation
```

---

## 🏆 Vertex Pitch Fest 2026 Credits & Team
* **Track:** AI for Student Academic Recovery
* **Institution Target:** JNTUH / Sri Indu Institute of Engineering & Technology Autonomous
* **Built by:** Puneeth & Team BackOnTrack
