from backend.tables.member import Member
from backend.tables.organization import Organization


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


def assign_member_attributes(org: Organization, member: Member, qualities, constraints):
    valid_quality_names = {q.name for q in org.qualities}
    valid_constraint_names = {c.name for c in org.constraints}

    member.qualities = [q for q in qualities if q in valid_quality_names]
    member.constraints = [c for c in constraints if c in valid_constraint_names]


def update_member(member: Member, name=None, role=None, available_hours=None):
    if name is not None:
        member.name = name
    if role is not None:
        member.role = role
    if available_hours is not None:
        member.available_hours = available_hours


def update_member_attributes(org: Organization, member: Member, qualities=None, constraints=None):
    if qualities is not None:
        assign_member_attributes(org, member, qualities, member.constraints)

    if constraints is not None:
        assign_member_attributes(org, member, member.qualities, constraints)
