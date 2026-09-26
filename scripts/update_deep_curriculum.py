"""
Updates course_content_tool.py and option3.html with deep, comprehensive,
textbook-grade curriculum extracted directly from Sri Indu R20CSE2202 (92 Pages).
"""

import json
from pathlib import Path

DEEP_TOPICS = {
    "cpu-scheduling": {
        "topic_id": "cpu-scheduling",
        "title": "Preemptive CPU Scheduling (SRTF & Round Robin)",
        "module": "Unit II • Lectures 11-15 (P.19-24)",
        "citation": "Official Curriculum: Sri Indu R20CSE2202 P.19-24 • Unit II",
        "marks": 12,
        "estimated_minutes": 50,
        "mental_model": (
            "<h3>1. Fundamental CPU Scheduling Concepts & State Machine</h3>"
            "<p>CPU scheduling is the basis of multiprogrammed operating systems. By switching the CPU among processes, the OS makes the computer more productive. The lifecycle of a process consists of alternating cycles of <strong>CPU execution (CPU bursts)</strong> and <strong>I/O wait (I/O bursts)</strong>.</p>"
            "<p><strong>When do CPU scheduling decisions take place?</strong> According to Sri Indu Lecture Notes (P.19), scheduling decisions occur under four distinct state transitions:</p>"
            "<ul>"
            "<li><strong>Case 1:</strong> When a process switches from the <em>Running state to the Waiting state</em> (for example, as the result of an I/O request or an invocation of <code>wait()</code>).</li>"
            "<li><strong>Case 2:</strong> When a process switches from the <em>Running state to the Ready state</em> (for example, when a hardware timer interrupt occurs or higher priority process arrives).</li>"
            "<li><strong>Case 3:</strong> When a process switches from the <em>Waiting state to the Ready state</em> (for example, at completion of an I/O operation).</li>"
            "<li><strong>Case 4:</strong> When a process <em>Terminates</em>.</li>"
            "</ul>"
            "<p><strong>Preemptive vs Non-Preemptive Scheduling:</strong> When scheduling takes place only under Case 1 and Case 4, the scheduling scheme is <strong>Non-Preemptive (Cooperative)</strong>. Once the CPU has been allocated to a process, the process keeps the CPU until it voluntarily releases it. Under Cases 2 and 3, scheduling is <strong>Preemptive</strong>—the kernel forcibly interrupts the currently running process and context-switches the CPU to another process.</p>"
            "<h3>2. The Dispatcher and Dispatch Latency</h3>"
            "<p>The <strong>Dispatcher</strong> is the kernel module that gives control of the CPU to the process selected by the short-term CPU scheduler. Its functions include: (1) Switching context (saving registers to current PCB, loading next PCB), (2) Switching to user mode, and (3) Jumping to the proper location in the user program to restart execution.</p>"
            "<p>The time taken by the dispatcher to stop one process and start another running is called <strong>Dispatch Latency</strong>.</p>"
            "<h3>3. Optimization Scheduling Criteria</h3>"
            "<ul>"
            "<li><strong>CPU Utilization:</strong> Keep the CPU as busy as possible (typically 40% in light load to 90% in heavy load).</li>"
            "<li><strong>Throughput:</strong> Number of processes that complete execution per time unit.</li>"
            "<li><strong>Turnaround Time (TAT):</strong> Interval from the time of submission of a process to the time of completion: <code>TAT = Completion Time (CT) - Arrival Time (AT)</code>.</li>"
            "<li><strong>Waiting Time (WT):</strong> Total amount of time spent waiting in the Ready queue: <code>WT = Turnaround Time (TAT) - Burst Time (BT)</code>.</li>"
            "<li><strong>Response Time (RT):</strong> Time from process submission until the first response is produced (crucial in time-sharing interactive systems).</li>"
            "</ul>"
            "<h3>4. Shortest Remaining Time First (SRTF) Algorithm</h3>"
            "<p>SRTF is the preemptive version of Shortest Job First (SJF). At every instant when a new process arrives in the Ready queue, the scheduler compares the remaining CPU burst time of the currently running process with the burst time of the arriving process. If the arriving process requires strictly less CPU time than the current process has remaining, the running process is preempted.</p>"
            "<p><strong>Mathematical Optimality:</strong> SJF/SRTF is provably optimal because placing shorter jobs before longer jobs decreases the waiting time of the shorter jobs far more than it increases the waiting time of the longer jobs, minimizing cumulative average waiting time.</p>"
            "<h3>5. Round Robin (RR) Scheduling & Time Quantum Trade-offs</h3>"
            "<p>Designed for time-sharing systems, Round Robin defines a small unit of time called a <strong>Time Quantum (q)</strong> (typically 10 to 100 milliseconds). The Ready queue is treated as a circular FIFO queue. If the process burst exceeds <code>q</code>, the process is preempted and put back at the tail of the queue. If its burst is less than <code>q</code>, it releases the CPU voluntarily.</p>"
            "<p><strong>Quantum Sizing Rule of Thumb:</strong> If <code>q</code> is extremely large, RR degenerates into FCFS (subject to the convoy effect). If <code>q</code> is extremely small, RR creates excessive context-switch overhead. In practice, <strong>80% of CPU bursts should be shorter than the time quantum <code>q</code></strong>.</p>"
        ),
        "visual_diagram": (
            "========================================================================================\n"
            "COMPREHENSIVE GANTT CHART: SRTF PREEMPTION STEP-BY-STEP (Sri Indu Notes P.20-22)\n"
            "========================================================================================\n"
            "Given Process Table:\n"
            "+---------+--------------+------------+\n"
            "| Process | Arrival Time | Burst Time |\n"
            "+---------+--------------+------------+\n"
            "|   P1    |      0       |     8      |\n"
            "|   P2    |      1       |     4      |\n"
            "|   P3    |      2       |     9      |\n"
            "|   P4    |      3       |     5      |\n"
            "+---------+--------------+------------+\n\n"
            "Step-by-Step Scheduling Decisions:\n"
            "  * t = 0: Only P1 is in Ready Queue. P1 is scheduled. (Remaining BT: 8)\n"
            "  * t = 1: P2 arrives (BT: 4). P1 has executed for 1ms -> P1 remaining BT = 7.\n"
            "           Compare P2 (4) vs P1 (7) -> 4 < 7 -> PREEMPT P1! Context-switch to P2.\n"
            "  * t = 2: P3 arrives (BT: 9). P2 has remaining BT = 3. 3 < 9 -> P2 continues.\n"
            "  * t = 3: P4 arrives (BT: 5). P2 has remaining BT = 2. 2 < 5 -> P2 continues.\n"
            "  * t = 5: P2 finishes! Ready queue has: P1 (rem: 7), P3 (rem: 9), P4 (rem: 5).\n"
            "           Shortest remaining is P4 (5) -> P4 executes from t = 5 to 10.\n"
            "  * t = 10: P4 finishes! Ready queue has: P1 (rem: 7), P3 (rem: 9).\n"
            "            Shortest remaining is P1 (7) -> P1 executes from t = 10 to 17.\n"
            "  * t = 17: P1 finishes! Only P3 remains (9) -> P3 executes from t = 17 to 26.\n"
            "  * t = 26: P3 finishes. All processes completed.\n\n"
            "Final Gantt Chart:\n"
            "+-------+-------+-------+---------+---------+\n"
            "|  P1   |  P2   |  P4   |   P1    |   P3    |\n"
            "+-------+-------+-------+---------+---------+\n"
            "0       1       5       10        17        26"
        ),
        "model_answer": (
            "EXACT 10-MARK UNIVERSITY MODEL ANSWER (Sri Indu JNTUH Scheme):\n\n"
            "Step 1: Construct the Completion, Turnaround, and Waiting Time Table:\n"
            "+---------+----+----+----+-------------------+-------------------+\n"
            "| Process | AT | BT | CT | TAT = CT - AT     | WT = TAT - BT     |\n"
            "+---------+----+----+----+-------------------+-------------------+\n"
            "|   P1    | 0  | 8  | 17 | 17 - 0 = 17 ms    | 17 - 8 = 9 ms     |\n"
            "|   P2    | 1  | 4  | 5  | 5 - 1  = 4 ms     | 4 - 4  = 0 ms     |\n"
            "|   P3    | 2  | 9  | 26 | 26 - 2 = 24 ms    | 24 - 9 = 15 ms    |\n"
            "|   P4    | 3  | 5  | 10 | 10 - 3 = 7 ms     | 7 - 5  = 2 ms     |\n"
            "+---------+----+----+----+-------------------+-------------------+\n\n"
            "Step 2: Calculate Average Turnaround Time:\n"
            "  Avg TAT = (TAT_P1 + TAT_P2 + TAT_P3 + TAT_P4) / 4\n"
            "  Avg TAT = (17 + 4 + 24 + 7) / 4 = 52 / 4 = 13.0 ms.  [2 Marks]\n\n"
            "Step 3: Calculate Average Waiting Time:\n"
            "  Avg WT = (WT_P1 + WT_P2 + WT_P3 + WT_P4) / 4\n"
            "  Avg WT = (9 + 0 + 15 + 2) / 4 = 26 / 4 = 6.5 ms.    [3 Marks]\n\n"
            "Step 4: Verification of Response Times:\n"
            "  RT_P1 = 0 - 0 = 0 ms\n"
            "  RT_P2 = 1 - 1 = 0 ms\n"
            "  RT_P4 = 5 - 3 = 2 ms\n"
            "  RT_P3 = 17 - 2 = 15 ms\n"
            "  Avg Response Time = (0 + 0 + 2 + 15) / 4 = 4.25 ms."
        ),
        "common_trap": (
            "CRITICAL EXAM TRAPS IDENTIFIED IN SRI INDU EXAM EVALUATIONS:\n\n"
            "• Trap 1: Forgetting elapsed execution time on preemption: When P2 arrives at t=1, P1 has already run for 1 ms. "
            "Its remaining burst time is 7 ms, NOT 8 ms! If you evaluate P1 with 8 ms, your preemption logic and Completion Times will be completely wrong.\n\n"
            "• Trap 2: Direct subtraction trap for Waiting Time: Many students mistakenly write WT = CT - BT. "
            "This formula is ONLY valid if Arrival Time = 0. When Arrival Time > 0, you MUST use: WT = TAT - BT = (CT - AT) - BT. Direct subtraction ignores the arrival delay!\n\n"
            "• Trap 3: Tie-breaking arrival order: If two processes in the Ready queue have identical remaining bursts, FCFS order of arrival MUST break the tie. Never pick arbitrarily."
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
        "estimated_minutes": 55,
        "mental_model": (
            "<h3>1. The Critical-Section Problem</h3>"
            "<p>A <strong>race condition</strong> occurs when several processes access and manipulate the same data concurrently, and the outcome of the execution depends on the particular order in which the access takes place. To prevent race conditions, concurrent processes must be synchronized.</p>"
            "<p>A solution to the critical-section problem must satisfy the following three fundamental requirements (Sri Indu Notes P.31):</p>"
            "<ol>"
            "<li><strong>Mutual Exclusion:</strong> If process <code>Pi</code> is executing in its critical section, then no other processes can be executing in their critical sections.</li>"
            "<li><strong>Progress:</strong> If no process is executing in its critical section and some processes wish to enter their critical sections, only those processes that are not executing in their remainder sections can participate in deciding which will enter next, and this selection cannot be postponed indefinitely.</li>"
            "<li><strong>Bounded Waiting:</strong> There must exist a bound on the number of times that other processes are allowed to enter their critical sections after a process has made a request to enter and before that request is granted.</li>"
            "</ol>"
            "<h3>2. Peterson's Software Solution</h3>"
            "<p>Peterson's solution is a classic software-based solution restricted to two processes (<code>P0</code> and <code>P1</code>). The processes share two variables: <code>boolean flag[2]; int turn;</code>. If <code>flag[i] == true</code>, process <code>Pi</code> wants to enter the critical section. Variable <code>turn</code> indicates whose turn it is.</p>"
            "<pre>do {\n  flag[i] = true;\n  turn = j;\n  while (flag[j] && turn == j); // Busy wait\n  // CRITICAL SECTION\n  flag[i] = false;\n  // REMAINDER SECTION\n} while (true);</pre>"
            "<h3>3. Hardware Synchronization: TestAndSet and Swap</h3>"
            "<p>On modern multiprocessor architectures, atomic hardware instructions guarantee mutual exclusion without race conditions. The <code>TestAndSet(boolean *target)</code> instruction executes atomically: it reads the old value of target and sets target to true simultaneously in a single memory bus cycle.</p>"
            "<h3>4. Semaphores: Definition and Types</h3>"
            "<p>A <strong>Semaphore</strong> <code>S</code> is an integer synchronization tool that, apart from initialization, is accessed only through two standard atomic operations: <code>wait()</code> (historically called <code>P</code> from Dutch <em>proberen</em>, to test) and <code>signal()</code> (historically called <code>V</code> from <em>verhogen</em>, to increment).</p>"
            "<pre>wait(S) {\n  while (S <= 0); // Busy wait (in spinlocks)\n  S--;\n}\nsignal(S) {\n  S++;\n}</pre>"
            "<p><strong>Counting Semaphore vs Binary Semaphore:</strong></p>"
            "<ul>"
            "<li><strong>Counting Semaphore:</strong> Its integer value can range over an unrestricted domain. It is used to control access to a given resource consisting of a finite number of identical instances (initialized to the number of resources).</li>"
            "<li><strong>Binary Semaphore:</strong> Its integer value can range only between <code>0</code> and <code>1</code>. It functions as a mutex lock.</li>"
            "</ul>"
            "<p><strong>Block & Wakeup Implementation (Eliminating Busy Waiting):</strong> Instead of busy waiting in a spinlock, a process executing <code>wait()</code> when <code>S <= 0</code> suspends itself, placing its PCB on the semaphore's waiting queue using <code>block()</code>. When another process calls <code>signal()</code>, it invokes <code>wakeup()</code> to move a process from the waiting queue to the Ready queue.</p>"
            "<h3>5. Classical Synchronization Problem: Bounded-Buffer (Producer-Consumer)</h3>"
            "<p>We have a pool of <code>n</code> buffers, each capable of holding one item. We use three semaphores:</p>"
            "<ul>"
            "<li><code>mutex</code> (binary semaphore initialized to <code>1</code>): protects buffer insertion/removal for mutual exclusion.</li>"
            "<li><code>empty</code> (counting semaphore initialized to <code>n</code>): counts the number of empty buffer slots.</li>"
            "<li><code>full</code> (counting semaphore initialized to <code>0</code>): counts the number of filled buffer slots.</li>"
            "</ul>"
        ),
        "visual_diagram": (
            "========================================================================================\n"
            "BOUNDED-BUFFER SYNCHRONIZATION ARCHITECTURE & SEMAPHORE STATE FLOW\n"
            "========================================================================================\n\n"
            "      PRODUCER PROCESS                                CONSUMER PROCESS\n"
            "      ----------------                                ----------------\n"
            "       produce item                                      wait(full)   <-- Blocks if empty (full==0)\n"
            "            |                                                |\n"
            "       wait(empty)  <-- Blocks if full (empty==0)        wait(mutex)  <-- Locks buffer\n"
            "            |                                                |\n"
            "       wait(mutex)  <-- Locks buffer                    remove item from buffer\n"
            "            |                                                |\n"
            "       insert item into buffer                          signal(mutex) <-- Unlocks buffer\n"
            "            |                                                |\n"
            "       signal(mutex)<-- Unlocks buffer                  signal(empty) <-- Increments free slots\n"
            "            |                                                |\n"
            "       signal(full) <-- Increments filled slots          consume item\n\n"
            "                     +---------------------------------------+\n"
            "                     |  SHARED BUFFER POOL (Capacity N = 5)  |\n"
            "                     | [ Item 0 ] [ Item 1 ] [ ] [ ] [ ]     |\n"
            "                     +---------------------------------------+\n"
            "                     | mutex = 1 (Binary Lock)               |\n"
            "                     | empty = 3 (Free Slots Available)      |\n"
            "                     | full  = 2 (Items Ready to Consume)    |\n"
            "                     +---------------------------------------+"
        ),
        "model_answer": (
            "EXACT 10-MARK UNIVERSITY MODEL ANSWER (Sri Indu JNTUH Scheme):\n\n"
            "// Global Shared Variables & Semaphores:\n"
            "#define BUFFER_SIZE 10\n"
            "typedef int item;\n"
            "item buffer[BUFFER_SIZE];\n"
            "int in = 0, out = 0;\n\n"
            "semaphore mutex = 1;  // Controls critical section access\n"
            "semaphore empty = BUFFER_SIZE; // Initially all 10 slots are vacant\n"
            "semaphore full = 0;   // Initially 0 slots are filled\n\n"
            "// Producer Code:\n"
            "void producer(void) {\n"
            "    item next_produced;\n"
            "    while (1) {\n"
            "        next_produced = produce_item();\n"
            "        wait(empty);  // Decrement empty slot count; wait if buffer full\n"
            "        wait(mutex);  // Enter critical section\n\n"
            "        buffer[in] = next_produced;\n"
            "        in = (in + 1) % BUFFER_SIZE;\n\n"
            "        signal(mutex); // Exit critical section\n"
            "        signal(full);  // Increment filled slot count; wake up consumer\n"
            "    }\n"
            "}\n\n"
            "// Consumer Code:\n"
            "void consumer(void) {\n"
            "    item next_consumed;\n"
            "    while (1) {\n"
            "        wait(full);   // Decrement filled slot count; wait if buffer empty\n"
            "        wait(mutex);  // Enter critical section\n\n"
            "        next_consumed = buffer[out];\n"
            "        out = (out + 1) % BUFFER_SIZE;\n\n"
            "        signal(mutex); // Exit critical section\n"
            "        signal(empty); // Increment empty slot count; wake up producer\n\n"
            "        consume_item(next_consumed);\n"
            "    }\n"
            "}\n\n"
            "Examiner Step-Marking Scheme Breakdown:\n"
            "• Semaphore Declarations and Correct Initial Values: [2 Marks]\n"
            "• Producer Implementation with wait(empty) before wait(mutex): [3 Marks]\n"
            "• Consumer Implementation with wait(full) before wait(mutex): [3 Marks]\n"
            "• Explanation of Mutual Exclusion and Deadlock Prevention: [2 Marks]"
        ),
        "common_trap": (
            "CRITICAL EXAM TRAPS IDENTIFIED IN SRI INDU EXAM EVALUATIONS:\n\n"
            "• Trap 1: Deadlock Inversion Bug (Order of Wait Operations): "
            "If you write `wait(mutex)` BEFORE `wait(empty)` in the Producer: suppose the buffer is full (`empty == 0`). "
            "The producer acquires `mutex`, then executes `wait(empty)` and blocks! When the consumer tries to run, it calls `wait(mutex)` "
            "and blocks because the sleeping producer holds the lock. Both processes freeze permanently in Deadlock!\n\n"
            "• Trap 2: Incorrect Initial Semaphore Values: Initializing `empty = 0` and `full = N` completely halts the system on line 1. "
            "`empty` represents vacant slots and must equal capacity `N`; `full` represents available items and must equal `0`.\n\n"
            "• Trap 3: Busy Waiting vs Blocking: Stating that semaphores always use spinlocks. Modern operating systems implement semaphores "
            "with a waiting queue using `block()` and `wakeup()` system calls, eliminating CPU waste."
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
        "estimated_minutes": 60,
        "mental_model": (
            "<h3>1. Deadlock Definition & System Model</h3>"
            "<p>A set of processes is in a <strong>deadlock state</strong> if each process in the set is waiting for an event that can be caused only by another process in the set. None of the processes can run, none of them can release any resources, and none of them can be awakened.</p>"
            "<p>Resources may be physical (Printers, Memory Space, CPU Cycles) or logical (Files, Semaphores, Database Locks). Under normal operation, a process utilizes a resource in three steps: (1) Request, (2) Use, and (3) Release.</p>"
            "<h3>2. Coffman's Four Necessary Conditions for Deadlock</h3>"
            "<p>A deadlock situation can arise if and only if the following four conditions hold simultaneously in a system (Sri Indu Notes P.44):</p>"
            "<ol>"
            "<li><strong>Mutual Exclusion:</strong> At least one resource must be held in a non-shareable mode (only one process can use it at a time).</li>"
            "<li><strong>Hold and Wait:</strong> A process must be currently holding at least one resource and waiting to acquire additional resources that are currently being held by other processes.</li>"
            "<li><strong>No Preemption:</strong> Resources cannot be preempted; that is, a resource can be released only voluntarily by the process holding it after that process has completed its task.</li>"
            "<li><strong>Circular Wait:</strong> A closed chain of processes exists such that each process holds at least one resource needed by the next process in the chain (<code>P0 -> P1 -> P2 -> ... -> Pn -> P0</code>).</li>"
            "</ol>"
            "<h3>3. Resource-Allocation Graphs (RAG)</h3>"
            "<p>A directed graph where vertices <code>V</code> are divided into Processes <code>P = {P1, ..., Pn}</code> and Resource Types <code>R = {R1, ..., Rm}</code>.</p>"
            "<ul>"
            "<li><strong>Request Edge:</strong> Directed edge <code>Pi -> Rj</code> (process <code>Pi</code> has requested an instance of <code>Rj</code>).</li>"
            "<li><strong>Assignment Edge:</strong> Directed edge <code>Rj -> Pi</code> (an instance of resource <code>Rj</code> has been allocated to <code>Pi</code>).</li>"
            "<li><strong>Theorem on Cycles:</strong> If the graph contains <em>no cycles</em>, the system is NOT in a deadlock. If the graph contains a cycle: if every resource has exactly one instance, a deadlock <em>definitely exists</em>. If resources have multiple instances, a cycle indicates a deadlock <em>is possible</em>, but not certain.</li>"
            "</ul>"
            "<h3>4. Deadlock Avoidance & The Banker's Algorithm</h3>"
            "<p>Deadlock avoidance requires that the OS is given advance information regarding the maximum resources each process will ever claim. A state is <strong>Safe</strong> if the system can allocate resources to each process (up to its maximum) in some order and still avoid a deadlock. More formally, a state is safe if there exists a <strong>Safe Sequence</strong> <code>&lt;P1, P2, ..., Pn&gt;</code> of processes such that for each <code>Pi</code>, the resources that <code>Pi</code> can still request can be satisfied by the currently available resources plus the resources already held by all preceding <code>Pj (j &lt; i)</code>.</p>"
            "<p><strong>Core Banker's Algorithm Data Structures:</strong></p>"
            "<ul>"
            "<li><code>Available[m]</code>: Vector of length <code>m</code>. If <code>Available[j] = k</code>, there are <code>k</code> instances of resource <code>Rj</code> currently available.</li>"
            "<li><code>Max[n][m]</code>: <code>n x m</code> matrix. If <code>Max[i][j] = k</code>, process <code>Pi</code> may request at most <code>k</code> instances of <code>Rj</code>.</li>"
            "<li><code>Allocation[n][m]</code>: <code>n x m</code> matrix. If <code>Allocation[i][j] = k</code>, <code>Pi</code> is currently allocated <code>k</code> instances of <code>Rj</code>.</li>"
            "<li><code>Need[n][m]</code>: <code>n x m</code> matrix. <strong>Need[i][j] = Max[i][j] - Allocation[i][j]</strong>.</li>"
            "</ul>"
        ),
        "visual_diagram": (
            "========================================================================================\n"
            "BANKER'S ALGORITHM COMPLETE UNIVERSITY NUMERICAL WORKED EXAMPLE (Sri Indu P.48)\n"
            "========================================================================================\n"
            "5 Processes: P0, P1, P2, P3, P4\n"
            "3 Resource Types: A (10 total instances), B (5 total instances), C (7 total instances)\n\n"
            "Snapshot at Time T0:\n"
            "+---------+--------------+--------------+--------------+--------------+\n"
            "| Process |  Allocation  |     Max      |     Need     |  Available   |\n"
            "|         |   A   B   C  |   A   B   C  |   A   B   C  |   A   B   C  |\n"
            "+---------+--------------+--------------+--------------+--------------+\n"
            "|   P0    |   0   1   0  |   7   5   3  |   7   4   3  |   3   3   2  |\n"
            "|   P1    |   2   0   0  |   3   2   2  |   1   2   2  |              |\n"
            "|   P2    |   3   0   2  |   9   0   2  |   6   0   0  |              |\n"
            "|   P3    |   2   1   1  |   2   2   2  |   0   1   1  |              |\n"
            "|   P4    |   0   0   2  |   4   3   3  |   4   3   1  |              |\n"
            "+---------+--------------+--------------+--------------+--------------+\n\n"
            "Safety Algorithm Execution Steps:\n"
            "Initial: Work = Available = [3, 3, 2], Finish[0..4] = false\n\n"
            "Iteration 1: Check P0: Need[0] = [7, 4, 3] <= Work [3, 3, 2]? False.\n"
            "             Check P1: Need[1] = [1, 2, 2] <= Work [3, 3, 2]? TRUE!\n"
            "             -> P1 finishes: Work = Work + Allocation[1] = [3,3,2] + [2,0,0] = [5, 3, 2]\n"
            "             -> Finish[1] = true. Sequence: <P1>\n\n"
            "Iteration 2: Check P3: Need[3] = [0, 1, 1] <= Work [5, 3, 2]? TRUE!\n"
            "             -> P3 finishes: Work = Work + Allocation[3] = [5,3,2] + [2,1,1] = [7, 4, 3]\n"
            "             -> Finish[3] = true. Sequence: <P1, P3>\n\n"
            "Iteration 3: Check P4: Need[4] = [4, 3, 1] <= Work [7, 4, 3]? TRUE!\n"
            "             -> P4 finishes: Work = Work + Allocation[4] = [7,4,3] + [0,0,2] = [7, 4, 5]\n"
            "             -> Finish[4] = true. Sequence: <P1, P3, P4>\n\n"
            "Iteration 4: Check P0: Need[0] = [7, 4, 3] <= Work [7, 4, 5]? TRUE!\n"
            "             -> P0 finishes: Work = Work + Allocation[0] = [7,4,5] + [0,1,0] = [7, 5, 5]\n"
            "             -> Finish[0] = true. Sequence: <P1, P3, P4, P0>\n\n"
            "Iteration 5: Check P2: Need[2] = [6, 0, 0] <= Work [7, 5, 5]? TRUE!\n"
            "             -> P2 finishes: Work = Work + Allocation[2] = [7,5,5] + [3,0,2] = [10, 5, 7]\n"
            "             -> Finish[2] = true. Sequence: <P1, P3, P4, P0, P2>\n\n"
            "Result: System is in a SAFE STATE with Safe Sequence: <P1, P3, P4, P0, P2>"
        ),
        "model_answer": (
            "EXACT 10-MARK UNIVERSITY MODEL ANSWER (Sri Indu JNTUH Scheme):\n\n"
            "Question: Given the resource allocation snapshot at T0, verify if the system is in a safe state. "
            "If yes, find the safe sequence. What happens if P1 requests [1, 0, 2]?\n\n"
            "Part A: Need Matrix Calculation (Need = Max - Allocation): [3 Marks]\n"
            "  Need[0] = [7-0, 5-1, 3-0] = [7, 4, 3]\n"
            "  Need[1] = [3-2, 2-0, 2-0] = [1, 2, 2]\n"
            "  Need[2] = [9-3, 0-0, 2-2] = [6, 0, 0]\n"
            "  Need[3] = [2-2, 2-1, 2-1] = [0, 1, 1]\n"
            "  Need[4] = [4-0, 3-0, 3-2] = [4, 3, 1]\n\n"
            "Part B: Safety Algorithm Execution & Step-by-Step Table: [4 Marks]\n"
            "+------+--------------+--------------+------------------+--------------+-------------+\n"
            "| Step | Process (Pi) |  Need[i]     | Work Vector      | Need <= Work | New Work    |\n"
            "+------+--------------+--------------+------------------+--------------+-------------+\n"
            "|  1   |      P1      |  [1, 2, 2]   | [3, 3, 2]        | Yes          | [5, 3, 2]   |\n"
            "|  2   |      P3      |  [0, 1, 1]   | [5, 3, 2]        | Yes          | [7, 4, 3]   |\n"
            "|  3   |      P4      |  [4, 3, 1]   | [7, 4, 3]        | Yes          | [7, 4, 5]   |\n"
            "|  4   |      P0      |  [7, 4, 3]   | [7, 4, 5]        | Yes          | [7, 5, 5]   |\n"
            "|  5   |      P2      |  [6, 0, 0]   | [7, 5, 5]        | Yes          | [10, 5, 7]  |\n"
            "+------+--------------+--------------+------------------+--------------+-------------+\n"
            "All Finish[i] == true. Safe Sequence = <P1, P3, P4, P0, P2>.\n\n"
            "Part C: Resource Request Algorithm for Request[1] = [1, 0, 2]: [3 Marks]\n"
            "1. Check Request[1] <= Need[1]: [1, 0, 2] <= [1, 2, 2] -> TRUE.\n"
            "2. Check Request[1] <= Available: [1, 0, 2] <= [3, 3, 2] -> TRUE.\n"
            "3. Pretend to allocate:\n"
            "   Available = Available - Request[1] = [3, 3, 2] - [1, 0, 2] = [2, 3, 0]\n"
            "   Allocation[1] = Allocation[1] + Request[1] = [2, 0, 0] + [1, 0, 2] = [3, 0, 2]\n"
            "   Need[1] = Need[1] - Request[1] = [1, 2, 2] - [1, 0, 2] = [0, 2, 0]\n"
            "4. Run Safety algorithm with new state: Safe sequence <P1, P3, P4, P0, P2> still exists.\n"
            "Conclusion: The request of P1 can be granted immediately."
        ),
        "common_trap": (
            "CRITICAL EXAM TRAPS IDENTIFIED IN SRI INDU EXAM EVALUATIONS:\n\n"
            "• Trap 1: Adding Max instead of Allocation to Work: When process Pi finishes, `Work = Work + Allocation[i]`. "
            "Students repeatedly write `Work = Work + Max[i]`. This is completely fatal: a process only returns what it was holding in RAM/devices (its Allocation), NOT its theoretical ceiling!\n\n"
            "• Trap 2: Vector comparison rule: `Need[i] <= Work` requires EVERY single component `Need[i][j] <= Work[j]`. "
            "If even one component is strictly greater (e.g. Need is [2, 4, 1] and Work is [3, 3, 5]), the process CANNOT run yet. Students often look at the sum instead of element-by-element.\n\n"
            "• Trap 3: Confusing Unsafe State with Deadlock: An unsafe state is NOT necessarily a deadlock; it is merely a state where the OS cannot guarantee avoiding one if all processes request their maximums simultaneously."
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
        "estimated_minutes": 45,
        "mental_model": (
            "<h3>1. Logical vs Physical Address Spaces & The MMU</h3>"
            "<p>An address generated by the CPU is referred to as a <strong>Logical Address</strong> (or Virtual Address). An address seen by the memory unit (loaded into the Memory Address Register MAR) is referred to as a <strong>Physical Address</strong>.</p>"
            "<p>The hardware device that maps logical addresses to physical addresses at runtime is the <strong>Memory Management Unit (MMU)</strong>. In the simplest scheme, the base register is called a <strong>Relocation Register</strong>: the value in the relocation register is added to every address generated by a user process before it is sent to memory.</p>"
            "<h3>2. Contiguous Memory Allocation & Fragmentation</h3>"
            "<p>Main memory must accommodate both the OS and various user processes. In contiguous memory allocation, each process is contained in a single contiguous section of memory.</p>"
            "<ul>"
            "<li><strong>External Fragmentation:</strong> Exists when total memory space exists to satisfy a request, but it is not contiguous (storage is fragmented into a large number of small holes). The <em>50-percent rule</em> states that for allocated blocks, 0.5 N blocks will be lost to fragmentation.</li>"
            "<li><strong>Internal Fragmentation:</strong> Unused memory that is internal to a partition or allocated block (e.g. allocating a 4 KB page to a process needing only 1 byte).</li>"
            "</ul>"
            "<h3>3. Paging Hardware Architecture</h3>"
            "<p><strong>Paging</strong> is a memory-management scheme that permits the physical address space of a process to be noncontiguous. Physical memory is broken into fixed-sized blocks called <strong>Frames</strong>. Logical memory is broken into blocks of the same size called <strong>Pages</strong>.</p>"
            "<p>Every address generated by the CPU is divided into two parts:</p>"
            "<ul>"
            "<li><strong>Page Number (p):</strong> Used as an index into a per-process <strong>Page Table</strong>. The page table contains the base address of each page in physical memory (frame number <code>f</code>).</li>"
            "<li><strong>Page Offset (d):</strong> Combined with the base frame address to define the physical memory address that is sent to the memory unit.</li>"
            "</ul>"
            "<p>If the logical address space is <code>2^m</code> and a page size is <code>2^n</code> addressing units (bytes), the high-order <code>m - n</code> bits designate the page number <code>p</code>, and the <code>n</code> low-order bits designate the page offset <code>d</code>.</p>"
            "<h3>4. Translation Lookaside Buffer (TLB)</h3>"
            "<p>Because the Page Table is stored in main memory, accessing a memory location requires TWO memory accesses: one for the page-table entry and one for the actual byte. This halves execution speed! To solve this, a special, small, fast hardware cache called a <strong>Translation Lookaside Buffer (TLB)</strong> is used.</p>"
            "<p>The TLB contains only a few page-table entries (typically 64 to 1024). When the CPU generates a logical address, its page number is presented simultaneously to all TLB entries in parallel hardware lookup:</p>"
            "<ul>"
            "<li><strong>TLB Hit:</strong> The page number is found in the TLB. The frame number is immediately available and used to access memory. Total time: <code>t_tlb + t_mem</code>.</li>"
            "<li><strong>TLB Miss:</strong> The page number is not in the TLB. The CPU must access the page table in main memory to obtain the frame number, update the TLB, and then access the operand in main memory. Total time: <code>t_tlb + 2 * t_mem</code>.</li>"
            "</ul>"
            "<h3>5. Effective Memory Access Time (EMAT) Formula</h3>"
            "<p>Let <code>h</code> be the TLB Hit Ratio (percentage of times that a page number is found in the TLB). Let <code>t</code> be the TLB search time, and <code>m</code> be the main memory access time:</p>"
            "<p style='font-size:1.1em; font-weight:bold; color:#1e40af;'>EMAT = h * (t + m) + (1 - h) * (t + 2 * m)</p>"
        ),
        "visual_diagram": (
            "========================================================================================\n"
            "PAGING HARDWARE WITH TRANSLATION LOOKASIDE BUFFER (TLB) ARCHITECTURE (Sri Indu P.55)\n"
            "========================================================================================\n\n"
            "       CPU Logical Address\n"
            "       +--------+--------+\n"
            "       |   p    |   d    |\n"
            "       +--------+--------+\n"
            "           |         |\n"
            "           |         +------------------------------------+\n"
            "           v                                              |\n"
            "       [ TLB Lookup ] (Associative Hardware Cache)        |\n"
            "       +--------+--------+                                |\n"
            "       |  Page  | Frame  |                                |\n"
            "       +--------+--------+                                |\n"
            "       |   p1   |   f2   |                                |\n"
            "       +--------+--------+                                |\n"
            "          /          \\                                    |\n"
            "      TLB Hit       TLB Miss                              |\n"
            "         |             |                                  |\n"
            "         |             v                                  |\n"
            "         |      [ Page Table in RAM ]                     |\n"
            "         |      +--------+--------+                       |\n"
            "         |      |  Index | Frame  |                       |\n"
            "         |      |    p   |   f    |                       |\n"
            "         |      +--------+--------+                       |\n"
            "         |             |                                  |\n"
            "         +-----> (f) <-+                                  |\n"
            "                  |                                       |\n"
            "                  v                                       v\n"
            "         +-----------------+------------------------------+\n"
            "         | Frame Number: f |       Page Offset: d         | Physical Address\n"
            "         +-----------------+------------------------------+\n"
            "                                   |\n"
            "                                   v\n"
            "                       [ Physical RAM Memory ]"
        ),
        "model_answer": (
            "EXACT 10-MARK UNIVERSITY MODEL ANSWER (Sri Indu JNTUH Scheme):\n\n"
            "Question: Explain Paging Hardware with TLB. If TLB access time is 20 ns, main memory access "
            "time is 100 ns, and TLB hit ratio is 85%, calculate the Effective Memory Access Time (EMAT).\n\n"
            "Step 1: State the Address Translation Mechanism: [3 Marks]\n"
            "• The CPU generates logical address (p, d). Page number p is first searched in associative TLB cache.\n"
            "• If TLB hit: frame number f is retrieved in 20 ns. Physical address (f, d) accesses RAM in 100 ns.\n"
            "• If TLB miss: Page Table in RAM is accessed (+100 ns). Frame f is loaded, TLB is updated, and RAM data is accessed (+100 ns).\n\n"
            "Step 2: State the EMAT Formula: [2 Marks]\n"
            "  EMAT = h * (t_tlb + t_mem) + (1 - h) * (t_tlb + 2 * t_mem)\n"
            "  Where:\n"
            "    h = Hit ratio = 0.85\n"
            "    t_tlb = TLB search time = 20 ns\n"
            "    t_mem = Main memory access time = 100 ns\n\n"
            "Step 3: Step-by-Step Numerical Substitution: [4 Marks]\n"
            "  Time on TLB Hit  = 20 ns + 100 ns = 120 ns\n"
            "  Time on TLB Miss = 20 ns + 2 * (100 ns) = 20 ns + 200 ns = 220 ns\n\n"
            "  EMAT = 0.85 * (120 ns) + (1 - 0.85) * (220 ns)\n"
            "  EMAT = 0.85 * 120 + 0.15 * 220\n"
            "  EMAT = 102.0 ns + 33.0 ns\n"
            "  EMAT = 135.0 ns.\n\n"
            "Step 4: Conclude Performance Gain: [1 Mark]\n"
            "  Without TLB, every memory reference requires 2 * 100 = 200 ns.\n"
            "  With 85% TLB hit ratio, access time is reduced from 200 ns to 135 ns (32.5% faster execution)."
        ),
        "common_trap": (
            "CRITICAL EXAM TRAPS IDENTIFIED IN SRI INDU EXAM EVALUATIONS:\n\n"
            "• Trap 1: The Missing (2 * M) Penalty on Miss: Students frequently write the miss time as `(t + m)` instead of `(t + 2 * m)`. "
            "Remember: on a TLB miss, you MUST make TWO memory accesses: 1st access to read the Page Table entry in RAM, and 2nd access to fetch the actual operand from RAM.\n\n"
            "• Trap 2: Modifying the Page Offset (d): In paging address translation, the page offset `d` NEVER changes between logical and physical addresses! Only the page number `p` is translated into frame `f`.\n\n"
            "• Trap 3: Fragmentation Classification: Paging completely ELIMINATES external fragmentation. However, it still suffers from INTERNAL fragmentation in the last allocated frame of a process."
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
        "estimated_minutes": 50,
        "mental_model": (
            "<h3>1. Virtual Memory & Demand Paging</h3>"
            "<p><strong>Virtual Memory</strong> is a technique that allows the execution of processes that are not completely in memory. Its chief advantage is that programs can be much larger than physical memory. Furthermore, it abstracts main memory into an extremely large, uniform array of storage.</p>"
            "<p><strong>Demand Paging:</strong> Pages are loaded only when they are demanded during program execution; pages that are never accessed are never loaded into physical RAM. A <em>lazy swapper (pager)</em> is used: it never swaps a page into memory unless that page is needed.</p>"
            "<p><strong>Valid-Invalid Bit Scheme:</strong> With each page-table entry, a valid-invalid bit is associated (<code>1 = valid</code>: page is legal and in memory; <code>0 = invalid</code>: page is either not in process logical address space or is currently on backing store disk).</p>"
            "<h3>2. The Six-Step Page Fault Handling Routine</h3>"
            "<p>When a process tries to access an invalid page, a <strong>Page Fault</strong> hardware trap occurs. The OS handles it through these exact 6 steps (Sri Indu Notes P.66):</p>"
            "<ol>"
            "<li>We check an internal table (usually in the PCB) to determine whether the reference was a valid or invalid memory access. If invalid, terminate process.</li>"
            "<li>If the reference was valid, we find a free frame (from the free-frame list in physical RAM).</li>"
            "<li>We schedule a disk operation to read the desired page from the backing store into the newly allocated frame.</li>"
            "<li>When the disk read is complete, we modify the internal table and the Page Table to indicate that the page is now in memory (set frame number <code>f</code>, set valid bit to <code>1</code>).</li>"
            "<li>We restart the instruction that was interrupted by the page fault exception. The process can now access the page as though it had always been in memory.</li>"
            "</ol>"
            "<h3>3. Page Replacement Algorithms</h3>"
            "<p>When a page fault occurs and NO frames are free in RAM, the OS must choose a <strong>Victim Frame</strong> to write to disk (swap out) and replace with the desired page. A <strong>Modify (Dirty) bit</strong> is used: if dirty bit is 0, the page has not been modified since being read from disk, so it does NOT need to be written back, cutting overhead in half.</p>"
            "<ul>"
            "<li><strong>FIFO (First-In, First-Out):</strong> Associates with each page the time when that page was brought into memory. When a page must be replaced, the oldest page is chosen. <em>Disadvantage:</em> Suffers from Belady's Anomaly!</li>"
            "<li><strong>Optimal Page Replacement (OPT / MIN):</strong> Replaces the page that will not be used for the longest period of time in the future. Provably produces the lowest page fault rate. <em>Disadvantage:</em> Requires impossible future knowledge of reference strings; used only as an offline benchmark to compare other algorithms.</li>"
            "<li><strong>LRU (Least Recently Used):</strong> Associates with each page the time of its last use. Replaces the page that has not been used for the longest period of time. <em>Advantage:</em> Belongs to the class of <strong>Stack Algorithms</strong> and is provably immune to Belady's Anomaly.</li>"
            "</ul>"
            "<h3>4. Belady's Anomaly Detailed Proof</h3>"
            "<p><strong>Definition:</strong> For some page-replacement algorithms, the page-fault rate may counter-intuitively <em>increase</em> as the number of allocated physical page frames increases.</p>"
            "<p><strong>Mathematical Proof on FIFO with Reference String:</strong> <code>1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5</code></p>"
            "<ul>"
            "<li>With <strong>3 Frames:</strong> Total Page Faults = <strong>9</strong>.</li>"
            "<li>With <strong>4 Frames:</strong> Total Page Faults = <strong>10</strong> (Page fault rate increased despite giving the process MORE memory!).</li>"
            "</ul>"
            "<h3>5. Thrashing & The Working-Set Model</h3>"
            "<p>If a process does not have enough frames to hold all the pages in its active locality, it will quickly page-fault. It must replace some page, but because all its pages are in active use, it must immediately fault again. This high paging activity is called <strong>Thrashing</strong>.</p>"
            "<p>As page fault frequency spikes, the OS dispatcher sees CPU utilization dropping and tries to increase multiprogramming by bringing in MORE processes, worsening the bottleneck until CPU throughput collapses to near zero.</p>"
        ),
        "visual_diagram": (
            "========================================================================================\n"
            "BELADY'S ANOMALY SIMULATION: 3 FRAMES (9 FAULTS) VS 4 FRAMES (10 FAULTS) (Sri Indu P.71)\n"
            "========================================================================================\n\n"
            "Reference String: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5\n\n"
            "--- Simulation with 3 Frames (FIFO) ---\n"
            "Ref:   1   2   3   4   1   2   5   1   2   3   4   5\n"
            "F1:   [1]  1   1  [4]  4   4  [5]  5   5  [3]  3   3\n"
            "F2:    -  [2]  2   2  [1]  1   1  [1]  1   1  [4]  4\n"
            "F3:    -   -  [3]  3   3  [2]  2   2  [2]  2   2  [5]\n"
            "Fault: *   *   *   *   *   *   *           *   *   *   (Total: 9 Page Faults)\n\n"
            "--- Simulation with 4 Frames (FIFO) ---\n"
            "Ref:   1   2   3   4   1   2   5   1   2   3   4   5\n"
            "F1:   [1]  1   1   1   1   1  [5]  5   5   5  [4]  4\n"
            "F2:    -  [2]  2   2   2   2   2  [1]  1   1   1  [5]\n"
            "F3:    -   -  [3]  3   3   3   3   3  [2]  2   2   2\n"
            "F4:    -   -   -  [4]  4   4   4   4   4  [3]  3   3\n"
            "Fault: *   *   *   *           *   *   *   *   *   *   (Total: 10 Page Faults!)\n\n"
            "RESULT: Giving the process 4 frames causes 10 faults vs 9 faults with 3 frames!\n"
            "This phenomenon is Belady's Anomaly."
        ),
        "model_answer": (
            "EXACT 10-MARK UNIVERSITY MODEL ANSWER (Sri Indu JNTUH Scheme):\n\n"
            "Question: Define Belady's Anomaly. Demonstrate it with a reference string under FIFO. "
            "Why does LRU not suffer from this anomaly?\n\n"
            "Part 1: Definition of Belady's Anomaly: [2 Marks]\n"
            "• Belady's Anomaly is the counter-intuitive phenomenon in virtual memory page replacement where "
            "increasing the number of physical page frames allocated to a process results in an INCREASE in the total number of page faults.\n"
            "• It occurs in FIFO because FIFO does not possess the stack property.\n\n"
            "Part 2: Step-by-Step Simulation Table (String: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5): [5 Marks]\n"
            "+--------+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            "| String | 1 | 2 | 3 | 4 | 1 | 2 | 5 | 1 | 2 | 3 | 4 | 5 |\n"
            "+--------+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            "| 3-FIFO | F | F | F | F | F | F | F | H | H | F | F | F | -> 9 Faults\n"
            "| 4-FIFO | F | F | F | F | H | H | F | F | F | F | F | F | -> 10 Faults!\n"
            "+--------+---+---+---+---+---+---+---+---+---+---+---+---+\n"
            "Where F = Page Fault, H = Page Hit.\n\n"
            "Part 3: Why LRU is Immune (Stack Algorithm Property): [3 Marks]\n"
            "• A Page Replacement algorithm is called a Stack Algorithm if the set of pages in memory for n frames "
            "is ALWAYS a strict subset of the set of pages in memory for n+1 frames: S(n) ⊆ S(n+1).\n"
            "• For LRU, the n frames always hold the n most recently used pages. With n+1 frames, it holds those same n pages "
            "plus one more. Thus, any page hit in n frames is guaranteed to be a hit in n+1 frames.\n"
            "• Therefore, LRU and Optimal algorithms can NEVER exhibit Belady's Anomaly."
        ),
        "common_trap": (
            "CRITICAL EXAM TRAPS IDENTIFIED IN SRI INDU EXAM EVALUATIONS:\n\n"
            "• Trap 1: Claiming Belady's Anomaly occurs in LRU or Optimal: Belady's Anomaly NEVER occurs in LRU or Optimal algorithms. "
            "LRU and Optimal are provably stack algorithms. Writing that LRU exhibits Belady's Anomaly will cause examiners to deduct full marks.\n\n"
            "• Trap 2: Dirty Bit functionality: Students forget that page replacement only requires disk writes if the page was modified (dirty bit = 1). "
            "If dirty bit is 0, the page is simply overwritten in RAM without writing to swap disk.\n\n"
            "• Trap 3: Cause of Thrashing: Thrashing is NOT caused by slow hard drives or low RAM alone. "
            "It is caused when the SUM OF LOCALITIES (Working Sets) of all active processes exceeds total physical memory capacity."
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

# Write to backend/tools/course_content_tool.py
tool_code = f'''"""
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

TOPIC_CONTENT_STORE: Dict[str, Dict[str, Any]] = {json.dumps(DEEP_TOPICS, indent=4)}

OVERALL_MOCK_EXAM = {json.dumps(OVERALL_MOCK_EXAM, indent=4)}

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
    topic_data = get_topic_content(topic_id)
    if API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=API_KEY)
            prompt = (
                f"Topic: {{topic_data['title']}} ({{topic_data['module']}})\\n"
                f"Topic Core Concept: {{topic_data['mental_model']}}\\n"
                f"Student Question: {{student_question}}\\n\\n"
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

    return f"Here is how to think about {{topic_data['title']}}: {{topic_data['mental_model']}}"
'''

target_tool = Path("/home/puneeth/programmes/bitsom_vertex/backend/tools/course_content_tool.py")
target_tool.write_text(tool_code)
print(f"Updated {target_tool} successfully ({len(tool_code)} bytes).")
