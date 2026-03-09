# backend/features/create_project.py

from backend.tables.project import Project

def create_project(name: str, duration_weeks: int, members: list[str]):
    return Project(name=name, duration_weeks=duration_weeks, members=members)
