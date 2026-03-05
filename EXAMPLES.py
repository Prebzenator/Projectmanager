"""
EXAMPLE USAGE SCENARIOS
=======================

This file contains practical examples showing how to use the Project Planner
application programmatically. Copy and modify these examples for your own use.
"""

from features import Planner
from tables import Organization, Member, Project, Task

print("=" * 60)
print("PROJECT PLANNER - EXAMPLE USAGE SCENARIOS")
print("=" * 60)


def example_1_basic_setup():
    """
    SCENARIO 1: Creating a basic organization with members and a project
    Time: 5 minutes
    """
    print("\n[EXAMPLE 1] Basic Setup - Create org, members, and project")
    print("-" * 60)
    
    # Create the planner (like a project manager)
    planner = Planner()
    
    # Create organization
    org = planner.create_organization("Tech Startup XYZ")
    print(f"✓ Created organization: {org.name}")
    
    # Define organizational standards
    planner.add_quality_to_organization("Python", "Python programming skill")
    planner.add_quality_to_organization("JavaScript", "JavaScript/Frontend skill")
    planner.add_quality_to_organization("Leadership", "Team leadership capability")
    print("✓ Added organizational qualities")
    
    # Define constraints
    planner.add_constraint_to_organization("Remote", "Can work remotely")
    planner.add_constraint_to_organization("Flex Hours", "Flexible working hours")
    print("✓ Added organizational constraints")
    
    # Create team members
    alice = planner.create_member(
        name="Alice Johnson",
        role="Senior Backend Developer",
        available_hours=40,
        qualities=["Python", "Leadership"],
        constraints=["Remote"]
    )
    
    bob = planner.create_member(
        name="Bob Smith",
        role="Frontend Developer",
        available_hours=40,
        qualities=["JavaScript"],
        constraints=["Remote", "Flex Hours"]
    )
    
    print(f"✓ Created members: {alice.name}, {bob.name}")
    
    # Create a project
    project = planner.create_project(
        name="Mobile App Backend",
        duration_weeks=8
    )
    print(f"✓ Created project: {project.name}")
    
    # Assign members to project
    planner.assign_member_to_project(project, alice)
    planner.assign_member_to_project(project, bob)
    print("✓ Assigned members to project")
    
    # Add tasks
    task1 = planner.add_task_to_project(
        project=project,
        title="Design API Architecture",
        hours=16,
        deadline="2026-03-20",
        required_qualities=["Python", "Leadership"]
    )
    
    task2 = planner.add_task_to_project(
        project=project,
        title="Frontend Integration",
        hours=24,
        deadline="2026-03-25",
        required_qualities=["JavaScript"]
    )
    
    print(f"✓ Added tasks: {task1.title}, {task2.title}")
    
    # Assign tasks to members
    compatible_for_task1 = planner.get_compatible_members(project, task1)
    if compatible_for_task1:
        assigned_member = compatible_for_task1[0]
        planner.assign_task_to_member(task1, assigned_member)
        print(f"✓ Assigned '{task1.title}' to {assigned_member.name}")
    
    compatible_for_task2 = planner.get_compatible_members(project, task2)
    if compatible_for_task2:
        assigned_member = compatible_for_task2[0]
        planner.assign_task_to_member(task2, assigned_member)
        print(f"✓ Assigned '{task2.title}' to {assigned_member.name}")
    
    # Display summary
    summary = planner.get_project_summary(project)
    print(f"\nProject Summary: {summary['name']}")
    print(f"  Tasks: {summary['tasks_count']}")
    print(f"  Team Members: {summary['members_count']}")


def example_2_smart_assignment():
    """
    SCENARIO 2: Using smart member assignment based on skills
    Time: 3 minutes
    """
    print("\n\n[EXAMPLE 2] Smart Task Assignment")
    print("-" * 60)
    
    planner = Planner()
    org = planner.create_organization("Design Agency")
    
    # Define skills
    planner.add_quality_to_organization("UI Design", "User interface design")
    planner.add_quality_to_organization("UX Research", "User experience research")
    planner.add_quality_to_organization("Web Design", "Web design expertise")
    
    # Create team
    designer1 = planner.create_member(
        "Emma Wilson", "Senior Designer",
        available_hours=40,
        qualities=["UI Design", "UX Research"]
    )
    
    designer2 = planner.create_member(
        "Charlie Brown", "Web Designer",
        available_hours=35,
        qualities=["Web Design", "UI Design"]
    )
    
    # Create project
    project = planner.create_project("Website Redesign", duration_weeks=6)
    planner.assign_member_to_project(project, designer1)
    planner.assign_member_to_project(project, designer2)
    
    # Create task requiring UX Research
    ux_task = planner.add_task_to_project(
        project,
        "Conduct User Research",
        hours=12,
        deadline="2026-03-15",
        required_qualities=["UX Research"]
    )
    
    # System finds compatible members automatically
    compatible = planner.get_compatible_members(project, ux_task)
    print(f"\nTask: {ux_task.title}")
    print(f"Required skill: UX Research")
    print(f"Compatible members ({len(compatible)}):")
    for member in compatible:
        print(f"  - {member.name} ({member.available_hours} hours available)")
    
    if compatible:
        selected = compatible[0]
        planner.assign_task_to_member(ux_task, selected)
        print(f"\n✓ Task assigned to {selected.name}")


def example_3_constraint_handling():
    """
    SCENARIO 3: Handling constraints (who cannot do what)
    Time: 4 minutes
    """
    print("\n\n[EXAMPLE 3] Constraint Handling")
    print("-" * 60)
    
    planner = Planner()
    org = planner.create_organization("Content Creator Hub")
    
    # Skills
    planner.add_quality_to_organization("Video Editing", "Professional video editing")
    planner.add_quality_to_organization("Animation", "Animation and motion graphics")
    
    # Constraints - who can't work together or under what conditions
    planner.add_constraint_to_organization("No Weekends", "Cannot work on weekends")
    planner.add_constraint_to_organization("No Remote", "Must work on-site")
    
    # Team with different constraints
    freelancer = planner.create_member(
        "Diana Foster", "Video Editor",
        available_hours=30,
        qualities=["Video Editing", "Animation"],
        constraints=["No Weekends"]  # Freelancer doesn't work weekends
    )
    
    # Task that requires NO_REMOTE quality/constraint
    rush_task = planner.add_task_to_project(
        planner.create_project("Emergency Video"),
        "Edit Emergency Video",
        hours=16,
        deadline="2026-03-07",
        required_qualities=["Video Editing"],
        required_constraints=["No Remote"]  # Task needs on-site person
    )
    
    project = rush_task  # Just reference for this simple example
    
    print(f"Task: {rush_task.title}")
    print(f"Requires: Video Editing, No Remote (on-site)")
    print(f"Member: {freelancer.name}")
    print(f"  Skills: {freelancer.qualities}")
    print(f"  Constraints: {freelancer.constraints}")
    print("\nNote: The system can validate constraints to ensure")
    print("only compatible members are assigned to tasks.")


def example_4_tracking_progress():
    """
    SCENARIO 4: Tracking task progress and completion
    Time: 2 minutes
    """
    print("\n\n[EXAMPLE 4] Task Progress Tracking")
    print("-" * 60)
    
    planner = Planner()
    org = planner.create_organization("Development Team")
    
    planner.add_quality_to_organization("Testing", "QA and testing")
    
    member = planner.create_member(
        "Frank Green", "QA Engineer",
        available_hours=40,
        qualities=["Testing"]
    )
    
    project = planner.create_project("Version 2.0 Release")
    planner.assign_member_to_project(project, member)
    
    task = planner.add_task_to_project(
        project,
        "System Testing",
        hours=20,
        deadline="2026-03-30"
    )
    
    print(f"Task: {task.title}")
    print(f"Initial status: {task.status}")
    print(f"Hours required: {task.hours}")
    
    # Start working on task
    task.mark_in_progress()
    print(f"After starting: {task.status}")
    
    # Complete task
    task.mark_complete()
    print(f"After completion: {task.status}")
    
    print(f"\n✓ Task tracked from pending → in_progress → completed")


def example_5_multiple_projects():
    """
    SCENARIO 5: Managing multiple projects with shared resources
    Time: 5 minutes
    """
    print("\n\n[EXAMPLE 5] Multiple Projects - Resource Management")
    print("-" * 60)
    
    planner = Planner()
    org = planner.create_organization("Multi-Project Manager")
    
    # Skills
    planner.add_quality_to_organization("DevOps", "DevOps and deployment")
    planner.add_quality_to_organization("Security", "Security expertise")
    
    # Single team member who works on multiple projects
    expert = planner.create_member(
        "Grace Li", "DevOps Engineer",
        available_hours=40,
        qualities=["DevOps", "Security"]
    )
    
    # Multiple projects
    project_a = planner.create_project("Project A - Infrastructure")
    project_b = planner.create_project("Project B - Security Upgrade")
    
    # Shared resource assigned to both
    planner.assign_member_to_project(project_a, expert)
    planner.assign_member_to_project(project_b, expert)
    
    print(f"Resource: {expert.name} (Total hours: {expert.available_hours})")
    
    # Allocate to task in project A
    task_a = planner.add_task_to_project(
        project_a, "Setup Kubernetes", 15, "2026-03-20"
    )
    
    # Allocate to task in project B  
    task_b = planner.add_task_to_project(
        project_b, "Security Audit", 20, "2026-03-25"
    )
    
    print(f"\nProject A task: {task_a.title} ({task_a.hours} hours)")
    print(f"Project B task: {task_b.title} ({task_b.hours} hours)")
    print(f"Total needed: {task_a.hours + task_b.hours} hours")
    
    # Try assignment
    planner.assign_task_to_member(task_a, expert)
    print(f"\n✓ Assigned to Project A")
    print(f"  Hours remaining: {expert.available_hours}")
    
    try:
        planner.assign_task_to_member(task_b, expert)
        print(f"✓ Assigned to Project B")
    except Exception as e:
        print(f"✗ Cannot assign to Project B: {str(e)}")
        print(f"  Only {expert.available_hours} hours left")


# Run examples
if __name__ == "__main__":
    try:
        example_1_basic_setup()
        example_2_smart_assignment()
        example_3_constraint_handling()
        example_4_tracking_progress()
        example_5_multiple_projects()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review these examples")
        print("2. Run the interactive CLI: python projectplanner.py")
        print("3. Adapt examples for your specific use cases")
        print("4. Share code with team members")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()
