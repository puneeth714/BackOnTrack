"""
Tool 4: Course Content & Interactive Learning Tool
Provides structured, bite-sized learning packages for each in-scope topic
grounded strictly in the official Sri Indu Institute Operating Systems curriculum
(R20CSE2202, JNTUH, 92 Pages, prepared by A. Sandeep, Assistant Professor).
Powers on-demand conceptual Q&A via Google Gemini 2.5 Flash.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional

# Load API key
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    env_file = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                os.environ["GEMINI_API_KEY"] = API_KEY
                break


TOPIC_CONTENT_STORE: Dict[str, Dict[str, Any]] = {
    "cpu-scheduling": {
        "topic_id": "cpu-scheduling",
        "title": "Preemptive CPU Scheduling (SRTF & Round Robin)",
        "module": "Unit II • Lectures 11-15 (P.19-24)",
        "citation": "Official Curriculum: Sri Indu R20CSE2202 P.19-24 • Unit II",
        "marks": 12,
        "estimated_minutes": 35,
        "mental_model": (
            "Shortest Remaining Time First (SRTF) is preemptive Shortest Job First (SJF). "
            "At every single arrival timestamp t, the OS compares the newly arrived process's burst time "
            "with the currently executing process's remaining burst time. If the new process is strictly shorter, "
            "the running process is context-switched back to the Ready Queue."
        ),
        "visual_diagram": (
            "Gantt Chart Tick-by-Tick Preemption:\n"
            "t=0: P1 arrives (BT: 8) -> P1 runs [0 to 1]\n"
            "t=1: P2 arrives (BT: 4) vs P1 remaining (7) -> 4 < 7 -> Preempt P1!\n"
            "t=1 to 5: P2 completes entirely (at t=5)\n"
            "t=5: P4 arrives (BT: 5) vs P1 (7) -> 5 < 7 -> Run P4 [5 to 10]\n"
            "Gantt: | P1 (0-1) | P2 (1-5) | P4 (5-10) | P1 (10-17) | P3 (17-26) |"
        ),
        "model_answer": (
            "Step 1: Draw Gantt chart marking arrival timestamps tick-by-tick.\n"
            "Step 2: Tabulate Completion Time (CT), Turnaround Time (TAT = CT - AT).\n"
            "Step 3: Tabulate Waiting Time (WT = TAT - BT).\n"
            "Step 4: Box final Average WT: Avg WT = (9 + 0 + 15 + 2) / 4 = 6.5 ms."
        ),
        "common_trap": (
            "Tick-by-tick arrival preemption trap: When P2 arrives at t=1, P1 has already run for 1ms. "
            "Its remaining burst is 7ms, NOT 8ms! Forgetting elapsed time ruins CT, TAT, and WT. "
            "Also remember: TAT = CT - AT, WT = TAT - BT. Never calculate WT = CT - BT directly."
        ),
        "mastery_check": {
            "question": "In SRTF, if P1 (remaining: 5ms) is executing and P2 (burst: 3ms) arrives at t=2, what happens?",
            "options": [
                "P1 continues until its 5ms finishes",
                "P1 is preempted and P2 executes immediately",
                "Both processes execute concurrently in round robin",
                "Operating system crashes with deadlock"
            ],
            "correct_index": 1,
            "explanation": "Correct! SRTF is strictly preemptive. Since P2's burst (3ms) is less than P1's remaining time (5ms), the CPU context-switches to P2."
        },
        "mcqs": [
            {
                "q": "Under which condition is CPU scheduling strictly non-preemptive?",
                "opts": [
                    "When a timer interrupt expires",
                    "When a process switches from Running to Waiting state (I/O request)",
                    "When a higher-priority process arrives in Ready queue",
                    "When a process completes its Round Robin time quantum"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.19: Scheduling is non-preemptive only when a process voluntarily relinquishes CPU: (1) Running to Waiting, or (2) Terminating."
            },
            {
                "q": "In Round Robin with time quantum q=4ms, if process P1 requires 3ms CPU burst, what happens?",
                "opts": [
                    "P1 holds the CPU for 4ms idling the remaining 1ms",
                    "P1 releases the CPU voluntarily at 3ms, scheduler immediately picks next process",
                    "P1 is preempted at 3ms and placed back in ready queue",
                    "Context switch penalty doubles to 2ms"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.22: If burst is less than time quantum, the process voluntarily releases CPU upon completion; the OS does not waste the remaining slice."
            },
            {
                "q": "Which scheduling algorithm provably gives the minimum average waiting time for a given set of processes?",
                "opts": [
                    "First-Come, First-Served (FCFS)",
                    "Shortest-Job-First / SRTF",
                    "Priority Scheduling without aging",
                    "Round Robin with small quantum"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.20: SJF/SRTF is mathematically optimal because moving short jobs before long jobs reduces total cumulative queue wait times."
            }
        ]
    },
    "synchronization": {
        "topic_id": "synchronization",
        "title": "Process Synchronization (Semaphores & Bounded Buffer)",
        "module": "Unit III • Lectures 16-20 (P.31-40)",
        "citation": "Official Curriculum: Sri Indu R20CSE2202 P.31-40 • Unit III",
        "marks": 10,
        "estimated_minutes": 40,
        "mental_model": (
            "Think of a physical shelf with N storage compartments: "
            "'mutex' (1) ensures mutual exclusion so only one producer or consumer touches the buffer at once. "
            "'empty' (N) is a counting semaphore tracking free slots. "
            "'full' (0) is a counting semaphore tracking filled slots."
        ),
        "visual_diagram": (
            "Shared Buffer (N slots):\n"
            "[ Item 1 ] [ Item 2 ] [ Empty ] [ Empty ]\n"
            "mutex = 1 (Binary lock for buffer access)\n"
            "empty = N (Counting semaphore: available vacant slots)\n"
            "full  = 0 (Counting semaphore: currently filled slots)"
        ),
        "model_answer": (
            "semaphore mutex = 1;\n"
            "semaphore empty = N;\n"
            "semaphore full = 0;\n\n"
            "void Producer() {\n"
            "    while (1) {\n"
            "        item = produce_item();\n"
            "        wait(empty);\n"
            "        wait(mutex);\n"
            "        insert_buffer(item);\n"
            "        signal(mutex);\n"
            "        signal(full);\n"
            "    }\n"
            "}\n\n"
            "void Consumer() {\n"
            "    while (1) {\n"
            "        wait(full);\n"
            "        wait(mutex);\n"
            "        item = remove_buffer();\n"
            "        signal(mutex);\n"
            "        signal(empty);\n"
            "        consume_item(item);\n"
            "    }\n"
            "}"
        ),
        "common_trap": (
            "Deadlock wait order swap: Writing wait(mutex) before wait(empty). If the buffer is full (empty=0), "
            "the producer locks mutex and blocks on empty. The consumer is now blocked on mutex, creating irreversible deadlock!"
        ),
        "mastery_check": {
            "question": "What is the initial value of semaphore 'empty' in a bounded buffer of capacity N?",
            "options": ["0", "1", "N", "-1"],
            "correct_index": 2,
            "explanation": "Correct! Initially, all N buffer slots are vacant, so 'empty' is initialized to N."
        },
        "mcqs": [
            {
                "q": "In the Producer-Consumer problem with buffer capacity N, what are the initial values of mutex, empty, and full?",
                "opts": [
                    "mutex = 0, empty = 0, full = N",
                    "mutex = 1, empty = N, full = 0",
                    "mutex = 1, empty = 0, full = N",
                    "mutex = N, empty = 1, full = 0"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.38: mutex is a binary semaphore initialized to 1, empty is initialized to N (all slots vacant), and full is initialized to 0."
            },
            {
                "q": "What happens if a developer swaps the wait sequence in Producer to: wait(mutex); wait(empty);?",
                "opts": [
                    "Buffer overflow occurs when buffer is full",
                    "Mutual exclusion is violated",
                    "Permanent Deadlock occurs when buffer is full",
                    "No effect, code behaves identically"
                ],
                "correct": 2,
                "exp": "Sri Indu Notes P.39: If buffer is full, producer acquires mutex, then sleeps waiting on empty. Consumer cannot enter to empty buffer because producer holds mutex!"
            },
            {
                "q": "Which hardware primitive provides an atomic operation to implement spinlocks in multiprocessor architectures?",
                "opts": [
                    "test_and_set() / compare_and_swap()",
                    "fork() and exec()",
                    "pipe() and signal()",
                    "malloc() and free()"
                ],
                "correct": 0,
                "exp": "Sri Indu Notes P.33: test_and_set() executes atomically with hardware memory bus locking, preventing race conditions between CPUs."
            }
        ]
    },
    "deadlocks": {
        "topic_id": "deadlocks",
        "title": "Deadlocks (Banker's Algorithm & Safe State Verification)",
        "module": "Unit III • Lectures 25-28 (P.43-52)",
        "citation": "Official Curriculum: Sri Indu R20CSE2202 P.43-52 • Unit III",
        "marks": 10,
        "estimated_minutes": 45,
        "mental_model": (
            "A bank will never allocate cash to customers unless it is guaranteed that at least one customer "
            "can finish their project, return all their borrowed funds, and allow subsequent customers to complete. "
            "If every process can complete in some sequential order, the state is SAFE."
        ),
        "visual_diagram": (
            "Safety Check Equation:\n"
            "Need[i][j] = Max[i][j] - Allocation[i][j]\n\n"
            "Check condition: If Need[i] <= Available -> Safe to execute Pi!\n"
            "After completion: New Available = Available + Allocation[i]"
        ),
        "model_answer": (
            "Step 1: Compute Need Matrix: Need = Max - Allocation.\n"
            "Step 2: Initialize Work = Available and Finish[i] = false for all i.\n"
            "Step 3: Find Pi where Finish[i] == false and Need[i] <= Work.\n"
            "Step 4: Update Work = Work + Allocation[i], mark Finish[i] = true, append Pi to SafeSequence.\n"
            "Step 5: Output Safe Sequence (e.g. <P1, P3, P4, P0, P2>) and conclude state is SAFE."
        ),
        "common_trap": (
            "Vector addition error: When updating Work upon process completion, students add Max instead of Allocation. "
            "When a process finishes, it only returns what it was currently holding (Allocation), NOT its theoretical Maximum!"
        ),
        "mastery_check": {
            "question": "In Banker's Algorithm, if Max[i] = [7, 5, 3] and Allocation[i] = [2, 1, 2], what is Need[i]?",
            "options": ["[9, 6, 5]", "[5, 4, 1]", "[7, 5, 3]", "[2, 1, 2]"],
            "correct_index": 1,
            "explanation": "Correct! Need = Max - Allocation = [7-2, 5-1, 3-2] = [5, 4, 1]."
        },
        "mcqs": [
            {
                "q": "In Banker's algorithm, if Max[i] = [7, 5, 3] and Allocation[i] = [2, 1, 2], what is the Need[i] vector?",
                "opts": ["[9, 6, 5]", "[5, 4, 1]", "[7, 5, 3]", "[2, 1, 2]"],
                "correct": 1,
                "exp": "Sri Indu Notes P.48: Need[i] = Max[i] - Allocation[i] = [7-2, 5-1, 3-2] = [5, 4, 1]."
            },
            {
                "q": "When a process Pi successfully finishes in Banker's Safety Algorithm, how is the Work vector updated?",
                "opts": [
                    "Work = Work + Need[i]",
                    "Work = Work + Allocation[i]",
                    "Work = Work - Allocation[i]",
                    "Work = Max[i]"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.47: When Pi terminates, it releases its currently allocated resources, so Work = Work + Allocation[i]."
            },
            {
                "q": "Which of the following is NOT one of Coffman's four necessary conditions for deadlock?",
                "opts": [
                    "Mutual Exclusion",
                    "Hold and Wait",
                    "Preemption Allowed",
                    "Circular Wait"
                ],
                "correct": 2,
                "exp": "Sri Indu Notes P.44: The condition is 'NO PREEMPTION'—resources cannot be forcibly taken from a process holding them."
            }
        ]
    },
    "memory-management": {
        "topic_id": "memory-management",
        "title": "Main Memory & Paging Hardware (TLB & Address Translation)",
        "module": "Unit IV • Lectures 29-33 (P.53-64)",
        "citation": "Official Curriculum: Sri Indu R20CSE2202 P.53-64 • Unit IV",
        "marks": 10,
        "estimated_minutes": 30,
        "mental_model": (
            "Logical address is like a book page and line number (p, d). "
            "The Page Table is the index mapping page p to physical library shelf frame f. "
            "The TLB (Translation Lookaside Buffer) is an associative hardware cache storing the most recent translations."
        ),
        "visual_diagram": (
            "CPU Logical Address (p, d)\n"
            "       |\n"
            "  [ Check TLB ]\n"
            "   /         \\\n"
            "Hit (20ns)    Miss (Access Page Table in RAM ~100ns)\n"
            "   \\         /\n"
            "Physical Address (f, d) in RAM"
        ),
        "model_answer": (
            "Step 1: Draw clean textbook diagram: CPU -> (p, d) -> TLB -> Page Table -> (f, d) -> RAM.\n"
            "Step 2: State Effective Memory Access Time (EMAT) formula:\n"
            "        EMAT = h * (t + m) + (1 - h) * (t + 2 * m)\n"
            "Step 3: Solve numerical: If hit ratio h=0.80, t=20ns, m=100ns:\n"
            "        EMAT = 0.80 * (20 + 100) + 0.20 * (20 + 200) = 96 + 44 = 140 ns."
        ),
        "common_trap": (
            "The (2 * M) miss penalty: On a TLB miss, RAM is accessed TWICE: "
            "1st access reads the Page Table entry in RAM, 2nd access fetches the actual data byte. "
            "Never write (t + m) for a miss! Also remember paging eliminates external fragmentation, but causes internal fragmentation."
        ),
        "mastery_check": {
            "question": "How many memory accesses are required on a TLB miss in single-level paging?",
            "options": ["1 access", "2 accesses", "3 accesses", "0 accesses"],
            "correct_index": 1,
            "explanation": "Correct! 1st access reads the Page Table entry in RAM, 2nd access retrieves the actual data."
        },
        "mcqs": [
            {
                "q": "If TLB hit ratio is 80%, TLB search time is 20ns, and main memory access time is 100ns, what is the Effective Memory Access Time (EMAT)?",
                "opts": ["100 ns", "120 ns", "140 ns", "220 ns"],
                "correct": 2,
                "exp": "EMAT = 0.80 * (20 + 100) + 0.20 * (20 + 200) = 0.80 * 120 + 0.20 * 220 = 96 + 44 = 140 ns."
            },
            {
                "q": "In paging hardware, what is the exact function of the page offset (d)?",
                "opts": [
                    "Identifies the page number in the swap partition",
                    "Indexes directly into the physical frame without alteration",
                    "Calculates the hit ratio of the translation lookaside buffer",
                    "Stores the dirty bit for page write-backs"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.54: Offset (d) remains invariant during address translation; it is concatenated with base frame address (f) to produce physical address."
            },
            {
                "q": "Paging hardware completely eliminates which type of memory fragmentation?",
                "opts": [
                    "Internal fragmentation",
                    "External fragmentation",
                    "Virtual fragmentation",
                    "TLB fragmentation"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.56: Because any physical frame can be allocated to any process page, external fragmentation is completely eliminated."
            }
        ]
    },
    "virtual-memory": {
        "topic_id": "virtual-memory",
        "title": "Virtual Memory & Page Replacement (FIFO, LRU & Belady's Anomaly)",
        "module": "Unit IV • Lectures 34-37 (P.65-76)",
        "citation": "Official Curriculum: Sri Indu R20CSE2202 P.65-76 • Unit IV",
        "marks": 10,
        "estimated_minutes": 30,
        "mental_model": (
            "Demand paging brings pages into physical RAM only when referenced. "
            "When RAM is full, page replacement algorithms choose a victim frame to swap out. "
            "FIFO replaces the oldest page, while LRU replaces the page unused for the longest time."
        ),
        "visual_diagram": (
            "Reference String: 1, 2, 3, 4, 1, 2, 5 (3 Frames)\n"
            "1 -> [1, -, -] (Fault)\n"
            "2 -> [1, 2, -] (Fault)\n"
            "3 -> [1, 2, 3] (Fault)\n"
            "4 -> [4, 2, 3] (Fault - Replaces 1)\n"
            "1 -> [4, 1, 3] (Fault - Replaces 2)"
        ),
        "model_answer": (
            "Step 1: Define Belady's Anomaly: For some page-replacement algorithms, the page-fault rate may increase as the number of allocated frames increases.\n"
            "Step 2: Simulate reference string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 under FIFO with 3 frames (9 faults) vs 4 frames (10 faults).\n"
            "Step 3: Conclude that FIFO is not a stack algorithm and suffers from Belady's Anomaly, unlike LRU."
        ),
        "common_trap": (
            "Belady's Anomaly applies to FIFO, never to LRU or Optimal. LRU is a stack algorithm where n frames is a subset of n+1 frames. "
            "Optimal replacement replaces the page that will not be used for longest time in the future (theoretical benchmark)."
        ),
        "mastery_check": {
            "question": "What is Belady's Anomaly in operating systems page replacement?",
            "options": [
                "Page faults decrease with fewer frames",
                "Increasing allocated frames increases total page faults",
                "LRU behaves identically to FIFO",
                "Excessive thrashing on magnetic disks"
            ],
            "correct_index": 1,
            "explanation": "Correct! Belady's Anomaly describes how increasing frames in FIFO can counter-intuitively increase page faults."
        },
        "mcqs": [
            {
                "q": "What is Belady's Anomaly in operating systems page replacement?",
                "opts": [
                    "Page fault rate decreases as frame count decreases",
                    "Increasing the number of allocated frames increases the total number of page faults",
                    "LRU and FIFO produce identical page faults",
                    "Thrashing caused by low CPU clock speed"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.71: Belady's Anomaly is the counter-intuitive phenomenon where increasing the number of page frames causes more page faults in FIFO."
            },
            {
                "q": "Why is Least Recently Used (LRU) immune to Belady's Anomaly?",
                "opts": [
                    "LRU requires special associative hardware registers",
                    "LRU belongs to the class of stack algorithms where n frames is a subset of n+1 frames",
                    "LRU uses dirty bits to prevent writes to backing store",
                    "LRU relies on future knowledge of page requests"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.72: In a stack algorithm, the set of pages in memory for n frames is always a strict subset of pages for n+1 frames."
            },
            {
                "q": "What condition triggers Thrashing in a virtual memory system?",
                "opts": [
                    "CPU scheduling quantum is set too high",
                    "Processes spend more time paging and swapping than executing useful instructions",
                    "TLB hit ratio reaches 99%",
                    "Deadlock occurs between producer and consumer"
                ],
                "correct": 1,
                "exp": "Sri Indu Notes P.75: When total working sets exceed physical memory, page faults cascade and CPU utilization drops to near zero."
            }
        ]
    }
}


OVERALL_MOCK_EXAM = [
    {
        "topicKey": "cpu-scheduling",
        "topicTitle": "Topic 1: CPU Scheduling",
        "q": "In Shortest Remaining Time First (SRTF), if P1 (rem: 5ms) is running and P2 (burst: 3ms) arrives at t=2, what action does the CPU scheduler take?",
        "opts": [
            "P1 runs to completion",
            "P1 is immediately preempted and P2 runs",
            "P1 and P2 run concurrently in Round Robin",
            "P2 is killed with an arrival error"
        ],
        "correct": 1,
        "exp": "SRTF is strictly preemptive. 3ms < 5ms, so P1 is immediately preempted to the Ready Queue."
    },
    {
        "topicKey": "synchronization",
        "topicTitle": "Topic 2: Synchronization",
        "q": "In the Producer-Consumer problem, what is the initial value of counting semaphore 'empty' for a buffer with capacity N?",
        "opts": ["0", "1", "N", "-1"],
        "correct": 2,
        "exp": "Initial empty buffer has all N slots vacant, so semaphore empty is initialized to N."
    },
    {
        "topicKey": "deadlocks",
        "topicTitle": "Topic 3: Deadlocks",
        "q": "In Banker's Algorithm, if Max[i] = [7, 5, 3] and Allocation[i] = [2, 1, 2], what is the Need[i] vector?",
        "opts": ["[9, 6, 5]", "[5, 4, 1]", "[7, 5, 3]", "[2, 1, 2]"],
        "correct": 1,
        "exp": "Need = Max - Allocation = [7-2, 5-1, 3-2] = [5, 4, 1]."
    },
    {
        "topicKey": "memory-management",
        "topicTitle": "Topic 4: Paging & Memory",
        "q": "With TLB hit ratio 80%, TLB search time 20ns, and memory access 100ns, what is the Effective Memory Access Time (EMAT)?",
        "opts": ["120 ns", "140 ns", "200 ns", "100 ns"],
        "correct": 1,
        "exp": "EMAT = 0.8*(20+100) + 0.2*(20+200) = 96 + 44 = 140 ns."
    },
    {
        "topicKey": "virtual-memory",
        "topicTitle": "Topic 5: Virtual Memory",
        "q": "Which page replacement algorithm suffers from Belady's Anomaly where adding frames causes more page faults?",
        "opts": ["LRU", "Optimal", "FIFO", "LFU"],
        "correct": 2,
        "exp": "FIFO is not a stack algorithm and can generate more page faults when allocated additional frames."
    }
]


def get_topic_content(topic_id: str) -> Dict[str, Any]:
    """Retrieves structured course package for a topic."""
    tid = topic_id.lower().replace("_", "-")
    if "sched" in tid or "srtf" in tid:
        tid = "cpu-scheduling"
    elif "sync" in tid or "producer" in tid or "sema" in tid:
        tid = "synchronization"
    elif "deadlock" in tid or "banker" in tid:
        tid = "deadlocks"
    elif "virtual" in tid or "replace" in tid or "fifo" in tid or "lru" in tid or "vm" in tid:
        tid = "virtual-memory"
    elif "page" in tid or "memory" in tid or "tlb" in tid:
        tid = "memory-management"

    return TOPIC_CONTENT_STORE.get(tid, TOPIC_CONTENT_STORE["cpu-scheduling"])


def get_mock_exam() -> List[Dict[str, Any]]:
    """Returns the 5 cross-topic Midterm 2 Mock Exam questions."""
    return OVERALL_MOCK_EXAM


def explain_topic_with_gemini(topic_id: str, student_question: str) -> str:
    """
    Uses Google Gemini 2.5 Flash to answer ANY organic question from the student
    about this specific topic in a clear, pedagogical manner.
    """
    topic_data = get_topic_content(topic_id)
    if API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=API_KEY)
            prompt = (
                f"Topic: {topic_data['title']} ({topic_data['module']})\n"
                f"Topic Core Concept: {topic_data['mental_model']}\n"
                f"Student Question: {student_question}\n\n"
                "Please provide a clear, concise, step-by-step academic explanation to help the student understand "
                "this topic for their university Operating Systems exam. Use concrete analogies and code/numerical formulas where helpful. "
                "Never use forbidden buzzwords like '20%/80%' or 'Pareto'."
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            if response.text:
                return response.text
            elif hasattr(response, "candidates") and response.candidates:
                cand = response.candidates[0]
                if cand.content and cand.content.parts:
                    return "".join(part.text for part in cand.content.parts if hasattr(part, "text") and part.text)
        except Exception:
            pass

    return f"Here is how to think about {topic_data['title']}: {topic_data['mental_model']}"
