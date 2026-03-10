from backend.tables.member import Member

def create_member(org, name, role, qualities=None, constraints=None, available_hours=0):
    member = Member(
        name=name,
        role=role,
        qualities=qualities or [],
        constraints=constraints or [],
        available_hours=available_hours
    )
    org.add_member(member)
    return member
