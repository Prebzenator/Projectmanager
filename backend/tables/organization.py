from backend.tables.attributes import Quality, Constraint
from backend.tables.member import Member

class Organization:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.projects = []
        self.qualities = []
        self.constraints = []
        self.members = []

    def add_project(self, project):
        self.projects.append(project)

    def add_quality(self, name, description=""):
        self.qualities.append(Quality(name, description))

    def add_constraint(self, name, description=""):
        self.constraints.append(Constraint(name, description))

    def add_members(self, member: Member):
        self.members.append(member)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "qualities": [q.to_dict() for q in self.qualities],
            "constraints": [c.to_dict() for c in self.constraints]
        }
