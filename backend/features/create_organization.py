from backend.tables.organization import Organization

def create_organization(name, description=""):
    return Organization(name, description)


def add_quality_to_org(org, name, description=""):
    org.add_quality(name, description)
    return org


def add_constraint_to_org(org, name, description=""):
    org.add_constraint(name, description)
    return org
