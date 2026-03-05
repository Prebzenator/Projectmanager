from backend.tables.task import Task

def create_task(project, name, hours, deadline, priority=1):
    """
    Oppretter en task og legger den til et prosjekt.
    """
    task = Task(name, hours, deadline)
    project.add_task(task, priority=priority)
    return task
