# backend/tables/project.py

class Project:
    _id_counter = 1

    def __init__(self, name: str, duration_weeks: int, members: list[str]):
        self.id = Project._id_counter
        Project._id_counter += 1

        self.name = name
        self.duration_weeks = duration_weeks
        self.members = members
        self.tasks = []  # slik at create_task kan bruke prosjektet

    def add_member(self, member_name: str):
        self.members.append(member_name)

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration_weeks": self.duration_weeks,
            "members": self.members,
            "tasks": [t.to_dict() for t in self.tasks]
        }
