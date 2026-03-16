from backend.tables.task import Task

def create_task(project, name, hours, deadline, priority=1):
    """
    Oppretter en task og legger den til et prosjekt.
    """
    task = Task(name, hours, deadline, priority=priority)
    project.add_task(task)
    return task
