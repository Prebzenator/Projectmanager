class Task:
    def __init__(self, title, hours, deadline, required_qualities=None, required_constraints=None):
        self.title = title
        self.hours = hours
        self.deadline = deadline
        self.required_qualities = required_qualities or []
        self.required_constraints = required_constraints or []
        self.dependencies = []
        self.status = "pending"

    def add_dependency(self, task):
        self.dependencies.append(task)

    def __repr__(self):
        return f"<Task {self.title}>"
