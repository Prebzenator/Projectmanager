class Member:
    def __init__(self, name, role, qualities=None, constraints=None, available_hours=0):
        self.name = name
        self.role = role
        self.qualities = qualities or []
        self.constraints = constraints or []
        self.available_hours = available_hours

    def __repr__(self):
        return f"<Member {self.name} ({self.role})>"

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "qualities": self.qualities,
            "constraints": self.constraints,
            "available_hours": self.available_hours
        }
