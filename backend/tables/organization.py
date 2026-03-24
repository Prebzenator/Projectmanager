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

    def add_member(self, member: Member):   # FIXED: was add_members (typo)
        self.members.append(member)

    def get_members(self):
        return [m.to_dict() for m in self.members]

    def get_projects(self):
        return [p.to_dict() for p in self.projects]

    def get_qualities(self):
        return [q.to_dict() for q in self.qualities]

    def get_constraints(self):
        return [c.to_dict() for c in self.constraints]



    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "projects": [p.to_dict() for p in self.projects],
            "qualities": [q.to_dict() for q in self.qualities],
            "constraints": [c.to_dict() for c in self.constraints],
            "members": [m.to_dict() for m in self.members]
        }
    