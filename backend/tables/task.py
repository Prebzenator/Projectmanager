import uuid

class Task:
    def __init__(self, name, hours, deadline, priority=1, required_qualities=None, required_constraints=None):
        # Unique identifier for referencing tasks
        self.id = str(uuid.uuid4())

        # Core task fields
        self.name = name
        self.hours = hours
        self.deadline = deadline
        self.priority = priority

        # Optional requirement fields
        self.required_qualities = required_qualities or []
        self.required_constraints = required_constraints or []

        # Dependencies: list of other Task objects
        self.dependencies = []

        # Status can later be used for scheduling or progress tracking
        self.status = "pending"

    def add_dependency(self, task):
        """Adds another task that must be completed before this one."""
        if task not in self.dependencies:
            self.dependencies.append(task)

    def to_dict(self):
        """Converts the task into a JSON‑friendly dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "hours": self.hours,
            "deadline": self.deadline,
            "priority": self.priority,
            "status": self.status,
            "dependencies": [d.id for d in self.dependencies]
        }

    def __repr__(self):
        return f"<Task {self.name} ({self.id})>"
