"""
PROJECT PLANNER APPLICATION
Assignment Analysis & Documentation
================================

This document analyzes the Project Planner application from a
Data Structures and Algorithms perspective (IS211).
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                          PROJECT PLANNER APPLICATION                       ║
║                     Data Structures & Algorithms Analysis                  ║
╚════════════════════════════════════════════════════════════════════════════╝


1. BUSINESS IDEA DESCRIPTION
================================

Business Problem:
-----------------
In organizations (startups, teams, agencies), project managers face a critical 
challenge: efficiently allocating tasks to team members. Key problems:

  • How do you match team members to tasks based on their skills?
  • How do you prevent over-allocating tasks to people with limited time?
  • How do you ensure tasks with specific requirements get assigned correctly?
  • How do you prioritize which task gets done first?

Target Users:
--------------
  • Project managers and team leads (5-50+ person organizations)
  • Organizations with diverse skill sets
  • Companies managing multiple concurrent projects
  • Startups needing efficient resource allocation

How Software Solves It:
------------------------
The Project Planner application provides:
  • Centralized task and resource management
  • Automated skill-based task matching
  • Availability tracking and prevention of over-allocation
  • Priority-based task scheduling
  • Real-time project status visibility


2. APPLICATION FEATURES & ARCHITECTURE
=======================================

Core Classes:

Organization (tables/organization.py):
  - Container for everything
  - Properties: name, members[], projects[], qualities[], constraints[]
  - Methods: add_member(), add_project(), add_quality(), add_constraint()

Member (tables/member.py):
  - Represents a team member
  - Properties: name, role, qualities[], constraints[], available_hours
  - Why available_hours matters: Tracks capacity to prevent over-allocation

Project (tables/project.py):
  - Represents a project
  - Properties: name, duration_weeks, tasks[], members[], scheduler
  - Scheduler: Priority queue for task ordering

Task (tables/task.py):
  - Represents a unit of work
  - Properties: title, hours, deadline, required_qualities[], required_constraints[], 
                dependencies[], status, assigned_to
  - Status tracking: pending → assigned → in_progress → completed

Attributes (tables/attributes.py):
  - Represents organizational standards
  - Used for Qualities (skills) and Constraints (limitations)
  - Properties: name, description

Planner (features/planner.py):
  - Main orchestrator/manager class
  - Key methods explained below

Scheduler (features/scheduler.py):
  - Priority queue implementation using heap
  - Methods: add_task(priority), next_task()


Main Features:

1. Organization Setup
   - Define organizational qualities (Python, Leadership, UI Design, etc.)
   - Define organizational constraints (Remote, No weekends, etc.)
   - These become standards that members and tasks reference

2. Member Management
   - Add members with specific qualities and constraints
   - Track available hours per person
   - Hours automatically deducted when tasks assigned
   - Prevents over-allocation

3. Project Management
   - Create projects with duration
   - Assign members to specific projects
   - Each project has its own task queue

4. Task Allocation
   - Add tasks to projects with requirements
   - Specify required_qualities (must haves)
   - Specify required_constraints (nice to haves/exclusions)
   - Automatic matching to find compatible members
   - Assignment with validation

5. Smart Assignment Algorithm
   - Find members matching ALL required qualities
   - Exclude members with conflicting constraints
   - Check available hours
   - Assign with proper error handling

6. Task Scheduling
   - Uses priority queue (heap)
   - Get next task to work on by priority
   - O(log n) insertion and retrieval


3. TIME COMPLEXITY ANALYSIS
============================

Different time complexities appear in different parts:

O(1) - CONSTANT TIME
=====================

Operations that take constant time regardless of input size:

Example 1: Member.available_hours decrement (assign_task_to_member)
  Code location: features/planner.py, line ~150
  
  def assign_task_to_member(self, task: Task, member: Member) -> None:
      if task.hours > member.available_hours:
          raise TaskAssignmentError(...)
      member.available_hours -= task.hours  # <- O(1) operation
      task.assigned_to = member
      task.status = "assigned"
  
  Why O(1): Simple arithmetic subtraction and variable assignment
  Time: Always takes same time, regardless of data set size
  Best/Worst case: Same - always one subtraction

Example 2: Adding member to organization (add_member)
  Code: tables/organization.py
  
  def add_member(self, member):
      self.members.append(member)  # <- O(1) amortized append
  
  Why O(1): Python list append is O(1) amortized complexity

Example 3: Creating new objects
  Code: Planner.create_member()
  
  member = Member(name, role, qualities, constraints, available_hours)
  return member
  
  Why O(1): Object creation time doesn't depend on data set size


O(log n) - LOGARITHMIC TIME
============================

Operations that work with logarithmic complexity:

Scheduler Priority Queue Operations:
  Code location: features/scheduler.py
  
  def add_task(self, task, priority):
      heapq.heappush(self.queue, (priority, self.counter, task))
      # heappush operation: O(log n)
      self.counter += 1
  
  def next_task(self):
      if not self.queue:
          return None
      return heapq.heappop(self.queue)[2]
      # heappop operation: O(log n)
  
  Why O(log n):
    • Python's heapq uses binary heap data structure
    • Adding one element requires going up the tree: ~log n comparisons
    • Removing top element requires reorganizing: ~log n operations
    • With n tasks, inserting/removing each is O(log n)
  
  Example:
    • 100 tasks: log₂(100) ≈ 6.6 comparisons
    • 1000 tasks: log₂(1000) ≈ 10 comparisons
    • 1,000,000 tasks: log₂(1,000,000) ≈ 20 comparisons

Use case in application:
  When you add multiple tasks to project:
    task1 → heappush: O(log 1)
    task2 → heappush: O(log 2)
    task3 → heappush: O(log 3)
    ...
    task100 → heappush: O(log 100)
  
  Total: O(n log n) for adding n tasks


O(n) - LINEAR TIME
===================

Operations that scale linearly with input:

Example 1: get_compatible_members (Core Algorithm)
  Code location: features/planner.py, lines ~120-135
  
  def get_compatible_members(self, project: Project, task: Task) -> List[Member]:
      compatible = []
      for member in project.members:              # O(m) - loop through members
          # Each member has qualities list
          if all(quality in member.qualities      # O(q) - check required qualities
                 for quality in task.required_qualities):
              
              if not any(constraint in member.constraints  # O(c) - check constraints
                        for constraint in task.required_constraints):
                  compatible.append(member)      # O(1) append
      return compatible
  
  Time Complexity: O(m * (q + c))
  where:
    m = number of members in project
    q = number of required qualities for this task
    c = number of required constraints
  
  Why not better?
    • Must check EVERY member in project
    • For EACH member, must verify ALL required qualities
    • For EACH member, must verify NO conflicting constraints
  
  In practice (typical scenario):
    m = 10 members
    q = 2 qualities
    c = 1 constraint
    Total checks: 10 * (2 + 1) = 30 operations
  
  Worst case (large team):
    m = 100 team members
    q = 10 required qualities
    c = 5 constraints
    Total checks: 100 * (10 + 5) = 1,500 operations

Example 2: Finding available member (find_available_member)
  Code location: features/planner.py, lines ~140-155
  
  def find_available_member(self, project: Project, task: Task) -> Optional[Member]:
      compatible = self.get_compatible_members(project, task)  # O(n)
      compatible.sort(key=lambda m: m.available_hours, reverse=True)  # O(n log n)
      
      for member in compatible:                   # O(n)
          if member.available_hours >= task.hours:
              return member
      return None
  
  Overall: O(n log n) due to sorting (see below)


O(n log n) - LINEARITHMIC TIME
===============================

Operations combining linear and logarithmic complexity:

Example: Sorting compatible members
  Code location: features/planner.py (find_available_member)
  
  compatible_members = [alice, bob, charlie, diana, emma]
  compatible_members.sort(key=lambda m: m.available_hours, reverse=True)
  
  Time: O(n log n)
  
  Why:
    • Python's sort is TimSort algorithm
    • Best case: O(n) - already mostly sorted
    • Average case: O(n log n)
    • Worst case: O(n log n)
  
  With 100 compatible members:
    100 * log₂(100) ≈ 100 * 6.6 ≈ 660 comparisons
  
  Real-world impact:
    • 10 people to sort: 33 comparisons
    • 100 people to sort: 664 comparisons
    • 1000 people to sort: 9,965 comparisons


COMPLEXITY SUMMARY TABLE
=========================

Operation                          Complexity      Best  Average  Worst
─────────────────────────────────────────────────────────────────────────
Member.available_hours -= X        O(1)            O(1)  O(1)     O(1)
Add member to org                  O(1)            O(1)  O(1)     O(1)
Add task to project                O(log n)        O(log n) O(log n) O(log n)
Get next task (scheduler)          O(log n)        O(log n) O(log n) O(log n)
Get compatible members             O(m*(q+c))      O(m)  O(m*q)   O(m*q)
Sort members by hours              O(n log n)      O(n)  O(n log n) O(n log n)
Find available member              O(n log n)      O(n)  O(n log n) O(n log n)


4. DATA STRUCTURES USED
=======================

Data Structure 1: HEAP (Priority Queue)
========================================

Location: features/scheduler.py
Implementation: Python's heapq module

What it does:
  • Maintains tasks in priority order
  • Always gives you the highest priority task quickly
  • Used for task scheduling

Code:
  class Scheduler:
      def __init__(self):
          self.queue = []                    # <- This is a heap
          self.counter = 0
      
      def add_task(self, task, priority):
          heapq.heappush(self.queue, (priority, self.counter, task))
      
      def next_task(self):
          if not self.queue:
              return None
          return heapq.heappop(self.queue)[2]

Why this structure:
  • Efficient retrieval of highest-priority task: O(log n)
  • Efficient insertion of new tasks: O(log n)
  • Better than unsorted list O(n) or sorted list O(n)
  • Perfect for task scheduling

Real-world benefit:
  • 1000 tasks: getting next task takes ~10 operations instead of 500+

Visual representation of heap:
  
  Priority order (tree structure):
                    (1, alice)
                   /          \\
            (2, bob)           (3, charlie)
           /        \\        /
    (4, diana)  (5, emma) (6, frank)


Data Structure 2: LIST (Dynamic Arrays)
========================================

Location: Throughout the application
  tables/organization.py - members[], projects[], qualities[], constraints[]
  tables/project.py - tasks[], members[]
  tables/member.py - qualities[], constraints[]

Code examples:
  class Organization:
      def __init__(self, name):
          self.members = []              # <- LIST
          self.projects = []             # <- LIST
          self.qualities = []            # <- LIST
          self.constraints = []          # <- LIST
  
  def add_member(self, member):
      self.members.append(member)        # <- O(1) amortized

Why this structure:
  • Efficient access: O(1) if you know index
  • Efficient append: O(1) amortized
  • Ordered iteration: Important for compatibility checks
  • Simple and flexible
  • Good for variable-sized collections

Real-world usage:
  • Store 5-100 team members
  • Store 1-20 projects
  • Store 3-10 organizational qualities

Visual representation:

  members list:
  ┌─────────────────────────────────────┐
  │ [alice, bob, charlie, diana, ...]   │
  └─────────────────────────────────────┘
   0      1      2       3       4

  qualities list:
  ┌────────────────────────────────────────────────┐
  │ [Python, JavaScript, Leadership, UI Design]    │
  └────────────────────────────────────────────────┘
   0        1           2          3


additional implicit structure: HASH CHECKS

While not explicitly a hash table, the "in" operator:
  
  if quality in member.qualities:      # Python uses hash under the hood
  
  Time: O(n) for list, but optimized by Python
  
  For small lists (5-10 qualities): effectively O(1) behavior
  For large lists: O(n) linear search


5. WHY THESE STRUCTURES ARE COMPLETE
=====================================

Requirement: At least 2 different data structures ✓
  1. HEAP:    for priority-based task scheduling
  2. LIST:    for storing collections of members, tasks, projects

Requirement: Multiple time complexities ✓
  1. O(1):    direct assignments, appends
  2. O(log n): heap operations (add/remove from scheduler)
  3. O(n):    iterating through all members for compatibility
  4. O(n log n): sorting members by availability


6. ALGORITHMIC EFFICIENCY IN PRACTICE
======================================

Scenario: Company with 50 people, 5 projects, 20 tasks

Adding all 20 tasks to scheduler:
  20 * log(20) ≈ 20 * 4.3 ≈ 86 heap operations
  Time: < 1ms

Finding compatible members for a task (requires 3 qualities):
  50 members * 3 qualities ≈ 150 operations
  Time: < 1ms

Sorting 45 compatible members by hours:
  45 * log(45) ≈ 45 * 5.5 ≈ 248 operations
  Time: < 1ms

Total workflow for assigning all tasks:
  86 + (20 * 150) + (20 * 248) ≈ 8,000 operations
  Time: < 10ms on modern computer


7. OPTIMIZATION OPPORTUNITIES (For Future Enhancement)
======================================================

Current bottleneck: get_compatible_members is O(m * q)

Optimization Option 1: Hash Set for Qualities
  Current:
    if quality in member.qualities:  # O(q) for list
  
  Optimized:
    member.qualities = {"Python", "Leadership"}  # O(1) set lookup
    if quality in member.qualities:  # O(1) average case

Optimization Option 2: Pre-index by Skill
  Build a skill-to-members mapping:
    {
      "Python": [alice, bob, diana],
      "Leadership": [alice, charlie],
      "UI Design": [emma, frank]
    }
  
  Then: Find compatible = Find intersection of all required skill sets
  Complexity: O(result size) instead of O(m * q)


8. CONCLUSION
=============

The Project Planner demonstrates:

Data Structures:
  ✓ HEAP: Priority queue for intelligent task scheduling
  ✓ LISTS: Dynamic collections for organization, members, projects, tasks

Time Complexities:
  ✓ O(1): Basic operations (assignments, appends)
  ✓ O(log n): Heap push/pop for task scheduling  
  ✓ O(n): Member compatibility checking
  ✓ O(n log n): Sorting members by availability

Practical Application:
  • All operations complete in milliseconds for realistic team sizes
  • Scalable to 100+ projects and 1000+ team members
  • Ready for production use with minor optimizations


═══════════════════════════════════════════════════════════════════════════════
End of Technical Analysis
═══════════════════════════════════════════════════════════════════════════════
""")
