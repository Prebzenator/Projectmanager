from .attributes import Attributes

class Organization:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.qualities = []
        self.constraints = []
        self.members = []
        self.projects = []
    
    def add_quality(self, name, description=""):
        self.qualities.append(Attributes(name, description))

    def add_constraint(self, name, description=""):
        self.constraints.append(Attributes(name, description))

    def add_member(self, member):
        self.members.append(member)

    def add_project(self, project):
        self.projects.append(project)
