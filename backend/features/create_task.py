from backend.tables.task import Task

def create_task(project, name, hours, deadline, priority=1,
                required_qualities=None, required_constraints=None):
    """
    Creates a task and adds it to a project.
    Also accepts required qualities and constraints.
    """
    task = Task(
        name=name,
        hours=hours,
        deadline=deadline,
        priority=priority,
        required_qualities=required_qualities or [],
        required_constraints=required_constraints or []
    )
    project.add_task(task)
    return task