class Task:
    def __init__(self, title, hours, deadline, required_qualities=None, required_constraints=None):
        self.title = title
        self.hours = hours
        self.deadline = deadline
        self.required_qualities = required_qualities or []
        self.required_constraints = required_constraints or []
        self.dependencies = []
        self.status = "pending"
        self.assigned_to = None

    def add_dependency(self, task):
        self.dependencies.append(task)
    
    def add_required_quality(self, quality):
        """Add a required quality for this task"""
        if quality not in self.required_qualities:
            self.required_qualities.append(quality)
    
    def add_required_constraint(self, constraint):
        """Add a required constraint for this task"""
        if constraint not in self.required_constraints:
            self.required_constraints.append(constraint)
    
    def mark_complete(self):
        """Mark task as completed"""
        self.status = "completed"
    
    def mark_in_progress(self):
        """Mark task as in progress"""
        self.status = "in_progress"

    def __repr__(self):
        return f"<Task {self.title} ({self.status})>"
