# backend/features/create_project.py

from backend.tables.project import Project


def validate_project_members(org, members):
    org_member_names = {m.name for m in org.members}
    return [m for m in members if m in org_member_names]


def create_project(org, name: str, duration_weeks: int, members: list[str]):
    # Validate members BEFORE creating project
    valid_members = validate_project_members(org, members)

    project = Project(
        name=name,
        duration_weeks=duration_weeks,
        members=valid_members
    )

    org.add_project(project)
    return project
