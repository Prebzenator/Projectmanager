class Member:
    def __init__(self, name, role, qualities=None, constraints=None, available_hours=0):
        self.name = name
        self.role = role
        self.qualities = qualities or []
        self.constraints = constraints or []
        self.available_hours = available_hours

    def __repr__(self):
        return f"<Member {self.name} ({self.role})>"
