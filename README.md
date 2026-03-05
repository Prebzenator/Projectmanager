# Project Planner

A comprehensive project planning and task management application for organizations. Create organizations, manage members with specific qualities and constraints, define projects, and intelligently assign tasks based on team member capabilities.

## Version
0.1.0 - Foundation Basis

## Features

### Core Functionality
- **Organization Management**: Create and manage organizations with custom qualities and constraints
- **Member Management**: Add team members with specific skills/qualities and constraints
- **Project Management**: Create projects and organize tasks within them
- **Task Management**: Define tasks with duration, deadlines, skill requirements, and constraints
- **Smart Assignment**: Automatically find compatible team members for tasks based on their qualities and availability
- **Task Scheduling**: Built-in priority queue for intelligent task scheduling

## Project Structure

```
projectplanner/
├── __init__.py              # Package initialization and exports
├── projectplanner.py        # Application entry point
├── README.md               # This file
├── docs/                   # Documentation (expandable)
│
├── tables/                 # Data models
│   ├── __init__.py
│   ├── attributes.py       # Attributes class (qualities/constraints)
│   ├── member.py          # Member class
│   ├── organization.py    # Organization class
│   ├── project.py         # Project class
│   └── task.py            # Task class
│
├── features/              # Core business logic
│   ├── __init__.py
│   ├── planner.py         # Planner class (main orchestrator)
│   └── scheduler.py       # Scheduler class (task prioritization)
│
└── frontend/              # User interface
    ├── __init__.py
    └── cli.py             # Interactive CLI interface
```

## Installation & Usage

### Running the Application

**Interactive Mode (CLI):**
```bash
python projectplanner.py
```

**Demo Mode:**
```bash
python projectplanner.py demo
```

### Quick Start Example

```python
from features import Planner

# Create planner and organization
planner = Planner()
org = planner.create_organization("My Company")

# Define organizational qualities and constraints
planner.add_quality_to_organization("Python", "Python programming skill")
planner.add_quality_to_organization("Leadership", "Team leadership skills")
planner.add_constraint_to_organization("Remote", "Can work remotely")

# Create members
member1 = planner.create_member(
    name="Alice",
    role="Senior Developer",
    available_hours=40,
    qualities=["Python", "Leadership"],
    constraints=["Remote"]
)

# Create a project
project = planner.create_project("Website Redesign", duration_weeks=8)
planner.assign_member_to_project(project, member1)

# Add tasks to project
task1 = planner.add_task_to_project(
    project,
    title="Design Architecture",
    hours=16,
    deadline="2026-03-20",
    required_qualities=["Leadership"]
)

# Find compatible members and assign
compatible = planner.get_compatible_members(project, task1)
if compatible:
    planner.assign_task_to_member(task1, compatible[0])
```

## Core Classes

### Planner (`features/planner.py`)

Main orchestrator class handling organization, member, project, and task management.

**Key Methods:**
- `create_organization(name)` - Create new organization
- `create_member(...)` - Create team member
- `create_project(...)` - Create project
- `add_task_to_project(...)` - Add task
- `get_compatible_members(...)` - Find qualified members
- `assign_task_to_member(...)` - Assign task to member

### Data Models

- **Organization** - Container for members, projects, qualities, constraints
- **Member** - Team member with skills, constraints, and availability
- **Project** - Collection of tasks and team assignments
- **Task** - Unit of work with requirements and tracking
- **Attributes** - Qualities and constraints definitions

## Extensibility Guide

The foundation is designed for team collaboration. Areas for extension:

### 1. Add Advanced Scheduling
- Extend `features/scheduler.py`
- Implement deadline-based or resource-based scheduling

### 2. Add Data Persistence
- Create `storage/` module
- Implement database or file-based persistence

### 3. Add Reporting Features
- Create `reporting/` module
- Generate status reports and analytics

### 4. Add REST API
- Create `api/` module using Flask/FastAPI
- Enable web-based access

### 5. Add Cost & Resource Tracking
- Extend Task and Member models
- Add budget and rate tracking

### 6. Add Notifications
- Create `notifications/` module
- Implement alerts and reminders

### 7. Create Web UI
- Build web interface with React/Vue/Angular
- Create GUI with PyQt or Tkinter

### 8. Add Testing
- Create `tests/` directory
- Add unit and integration tests

## Notes for Team Development

### Code Organization
- **Minimal dependencies**: Python standard library only
- **Object-oriented design**: Easy to extend and test
- **Clear separation**: Models, features, and frontend separated

### Development Workflow
1. Extract feature requirements
2. Create module in appropriate folder
3. Implement using existing classes
4. Add CLI menu items
5. Test with example data

### Integration Points
- `Planner` class: Main orchestrator
- `CLI`: User interface layer
- `tables/`: Core data structures

## Future Features

- [ ] Dependency management
- [ ] Critical path analysis
- [ ] Team capacity planning
- [ ] Multi-project resource management
- [ ] Time tracking and reporting
- [ ] Skill development tracking
- [ ] Automated task assignment
- [ ] Calendar integration
- [ ] Real-time collaboration
- [ ] Data persistence

---

**Version 0.1.0** - Foundation basis ready for team feature development
