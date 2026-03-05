class Project:
    def __init__(self, name, duration_weeks=None):
        self.name = name
        self.tasks = []
        self.members = []
        self.duration_weeks = duration_weeks
        self.options = {}

    def add_task(self, task, priority=1):
        self.tasks.append(task)

    def add_member(self, member):
        self.members.append(member)

    def set_options(self, **kwargs):
        self.options.update(kwargs)
