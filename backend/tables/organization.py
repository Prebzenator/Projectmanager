from backend.tables.attributes import Quality, Constraint

class Organization:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.projects = []
        self.qualities = []
        self.constraints = []

    def add_project(self, project):
        self.projects.append(project)

    def add_quality(self, name, description=""):
        self.qualities.append(Quality(name, description))

    def add_constraint(self, name, description=""):
        self.constraints.append(Constraint(name, description))

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "projects": [p.to_dict() for p in self.projects],
            "qualities": [q.to_dict() for q in self.qualities],
            "constraints": [c.to_dict() for c in self.constraints]
        }
