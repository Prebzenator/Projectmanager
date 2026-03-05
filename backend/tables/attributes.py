class Quality:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description
        }


class Constraint:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description
        }
