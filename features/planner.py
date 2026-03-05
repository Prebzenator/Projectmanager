"""
Planner module - Core logic for project planning and task assignment
"""

from typing import List, Optional
from tables.task import Task
from tables.member import Member
from tables.project import Project
from tables.organization import Organization
from tables.attributes import Attributes


class TaskAssignmentError(Exception):
    """Exception raised when task assignment fails"""
    pass


class Planner:
    """
    Main planner class handling organization, member, project, and task management.
    Provides methods for assigning tasks to members based on qualities and constraints.
    """
    
    def __init__(self):
        self.organization = None
    
    def create_organization(self, name: str) -> Organization:
        """Create a new organization"""
        self.organization = Organization(name)
        return self.organization
    
    def add_quality_to_organization(self, name: str, description: str = "") -> Attributes:
        """Add a quality to the organization"""
        if not self.organization:
            raise ValueError("Organization must be created first")
        self.organization.add_quality(name, description)
        return self.organization.qualities[-1]
    
    def add_constraint_to_organization(self, name: str, description: str = "") -> Attributes:
        """Add a constraint to the organization"""
        if not self.organization:
            raise ValueError("Organization must be created first")
        self.organization.add_constraint(name, description)
        return self.organization.constraints[-1]
    
    def create_member(self, name: str, role: str, available_hours: int = 0,
                     qualities: List[str] = None, constraints: List[str] = None) -> Member:
        """
        Create a new member and add to organization.
        Qualities and constraints should be names that exist in the organization.
        """
        if not self.organization:
            raise ValueError("Organization must be created first")
        
        member = Member(name, role, qualities or [], constraints or [], available_hours)
        self.organization.add_member(member)
        return member
    
    def create_project(self, name: str, duration_weeks: Optional[int] = None) -> Project:
        """Create a new project and add to organization"""
        if not self.organization:
            raise ValueError("Organization must be created first")
        
        project = Project(name, duration_weeks)
        self.organization.add_project(project)
        return project
    
    def get_organization(self) -> Optional[Organization]:
        """Get the current organization"""
        return self.organization
    
    def get_organization_info(self) -> dict:
        """Get detailed information about the organization"""
        if not self.organization:
            return {}
        
        return {
            "name": self.organization.name,
            "qualities": [f"{q.name} - {q.description}" for q in self.organization.qualities],
            "constraints": [f"{c.name} - {c.description}" for c in self.organization.constraints],
            "members_count": len(self.organization.members),
            "projects_count": len(self.organization.projects),
        }
    
    def get_projects(self) -> List[Project]:
        """Get all projects in the organization"""
        if not self.organization:
            return []
        return self.organization.projects
    
    def get_members(self) -> List[Member]:
        """Get all members in the organization"""
        if not self.organization:
            return []
        return self.organization.members
    
    def add_task_to_project(self, project: Project, title: str, hours: int, 
                           deadline: str, required_qualities: List[str] = None,
                           required_constraints: List[str] = None) -> Task:
        """Create and add a task to a project"""
        task = Task(title, hours, deadline, required_qualities or [], 
                   required_constraints or [])
        project.add_task(task)
        return task
    
    def assign_member_to_project(self, project: Project, member: Member) -> None:
        """Assign a member to a project"""
        project.add_member(member)
    
    def get_compatible_members(self, project: Project, task: Task) -> List[Member]:
        """
        Get members who have all required qualities for a task.
        Returns list of members that match the task requirements.
        """
        compatible = []
        for member in project.members:
            # Check if member has all required qualities
            if all(quality in member.qualities for quality in task.required_qualities):
                # Check if member doesn't have any conflicting constraints
                if not any(constraint in member.constraints for constraint in task.required_constraints):
                    compatible.append(member)
        return compatible
    
    def find_available_member(self, project: Project, task: Task) -> Optional[Member]:
        """
        Find an available member who can take on a task.
        Considers member availability and task requirements.
        """
        compatible = self.get_compatible_members(project, task)
        
        # Sort by available hours (descending)
        compatible.sort(key=lambda m: m.available_hours, reverse=True)
        
        for member in compatible:
            if member.available_hours >= task.hours:
                return member
        
        return None
    
    def assign_task_to_member(self, task: Task, member: Member) -> None:
        """Assign a task to a member and update their available hours"""
        if task.hours > member.available_hours:
            raise TaskAssignmentError(
                f"{member.name} doesn't have enough available hours. "
                f"Required: {task.hours}, Available: {member.available_hours}"
            )
        member.available_hours -= task.hours
        task.assigned_to = member
        task.status = "assigned"
    
    def get_project_summary(self, project: Project) -> dict:
        """Get a summary of a project"""
        return {
            "name": project.name,
            "duration_weeks": project.duration_weeks,
            "tasks_count": len(project.tasks),
            "members_count": len(project.members),
            "tasks": [{"title": t.title, "hours": t.hours, "deadline": t.deadline, 
                      "status": t.status} for t in project.tasks],
        }
