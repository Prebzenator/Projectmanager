"""
QUICK START GUIDE
=================

This guide helps team members get started with the Project Planner application.

OPTION 1: RUNNING THE INTERACTIVE APPLICATION (Recommended for new users)
=========================================================================

From PowerShell or Command Prompt in the projectplanner directory:

    C:\Users\truls\AppData\Local\Python\bin\python3.exe projectplanner.py

This launches an interactive menu where you can:
1. Create an organization
2. Define qualities and constraints
3. Add team members with skills
4. Create projects
5. Add tasks to projects
6. Assign tasks to members

The CLI is in Norwegian and provides step-by-step guidance.


OPTION 2: RUNNING DEMO MODE
============================

To see the application in action with sample data:

    C:\Users\truls\AppData\Local\Python\bin\python3.exe projectplanner.py demo

This demonstrates how to create an organization, members, and tasks.


OPTION 3: USING THE PLANNER PROGRAMMATICALLY
==============================================

Create a Python script to automate organization management:

    from features import Planner
    from tables import Organization, Member, Project, Task

    # Initialize planner
    planner = Planner()
    
    # Create organization
    org = planner.create_organization("My Company")
    
    # Add organizational standards
    planner.add_quality_to_organization("Python", "Python programming skill")
    planner.add_quality_to_organization("Leadership", "Team management")
    planner.add_constraint_to_organization("Remote", "Can work remotely")
    
    # Create and add members
    member = planner.create_member(
        name="John Doe",
        role="Developer",
        available_hours=40,
        qualities=["Python"],
        constraints=["Remote"]
    )
    
    # Create project
    project = planner.create_project("Web App Development", duration_weeks=12)
    planner.assign_member_to_project(project, member)
    
    # Add tasks
    task = planner.add_task_to_project(
        project,
        title="Build API",
        hours=32,
        deadline="2026-04-01",
        required_qualities=["Python"]
    )
    
    # Assign task to compatible member
    compatible_members = planner.get_compatible_members(project, task)
    if compatible_members:
        planner.assign_task_to_member(task, compatible_members[0])


PROJECT STRUCTURE OVERVIEW
==========================

tables/              - Data models (Organization, Member, Project, Task, etc.)
features/            - Core logic (Planner, Scheduler)
frontend/            - User interface (CLI)
projectplanner.py   - Application entry point


KEY CLASSES
===========

Planner              - Main orchestrator (create_organization, create_member, etc.)
Organization        - Container for members, projects, qualities, constraints
Project             - Collection of tasks and team assignments
Task                - Unit of work with requirements
Member              - Team member with skills and availability
Attributes          - Qualities and constraints definitions


EXAMPLE WORKFLOW
================

1. Launch: python3.exe projectplanner.py
2. Create organization
3. Add qualities (Python, Leadership, etc.)
4. Add constraints (Remote, No weekends, etc.)
5. Add team members with their skills
6. Create a project
7. Assign team members to project
8. Add tasks to project
9. System helps match qualified members to tasks
10. Monitor project progress


FOR TEAM DEVELOPERS
===================

To add new features:

1. Create functionality in appropriate module:
   - Data models: tables/
   - Business logic: features/
   - User interface: frontend/

2. Add CLI menu items in frontend/cli.py

3. Test with example data using the Planner class

4. Update documentation in README.md

5. Share code via version control


TROUBLESHOOTING
===============

Q: "Python not found" error
A: Use full path: C:\Users\truls\AppData\Local\Python\bin\python3.exe projectplanner.py

Q: Import errors
A: Make sure you're in the projectplanner directory and all __init__.py files exist

Q: Feature ideas
A: See README.md "Future Features" section or discuss with team


CONTACT & NEXT STEPS
====================

This is Version 0.1.0 - a foundation basis for team development.

Next steps:
- Review the README.md for detailed documentation
- Run the interactive application to understand the workflow
- Extract feature requirements for your team area
- Implement features using the Planner class as the main orchestrator
- Add CLI menu items for new features
- Test with sample data


FEATURES IMPLEMENTED
====================

✓ Organization management
✓ Quality and constraint system
✓ Member management with skills tracking
✓ Project creation and management
✓ Task creation with requirements
✓ Intelligent member assignment
✓ Task scheduling (priority queue)
✓ Interactive CLI in Norwegian
✓ Programmatic API for automation


READY TO START? 
===============

Run: C:\Users\truls\AppData\Local\Python\bin\python3.exe projectplanner.py

Then select: 1. Lag organisasjon (Create organization)

Happy coding! 🎉
"""

print(__doc__)
