"""
Project Planner Application
Main entry point for the application
"""

from frontend.cli import ProjectPlannerCLI
from tables.organization import Organization
from tables.member import Member
from tables.task import Task
from tables.project import Project


def run_interactive_mode():
    """Run the interactive CLI"""
    cli = ProjectPlannerCLI()
    cli.run()


def run_demo():
    """Run a demo showing how to use the system programmatically"""
    print("Running demo...")
    
    org = Organization("TestOrg")

    org.add_quality("strukturert")
    org.add_constraint("kan ikke jobbe helg")

    m1 = Member("Truls", "Leader", qualities=["strukturert"], available_hours=10)
    org.add_member(m1)

    project = Project("DemoProsjekt")
    org.add_project(project)

    t1 = Task("Skriv rapport", 5, "2026-03-10")
    project.add_task(t1, priority=1)

    print("Neste task:", project.scheduler.next_task())


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        run_interactive_mode()

