from backend.tables.organization import Organization

def create_organization(name, description=""):
    """
    Creates and returns a new Organization.
    """
    return Organization(name, description)

def add_quality(org, name, description=""):
    """
    Adds a quality to the organization's pool.
    """
    if not name:
        raise ValueError("Name is required")
    org.add_quality(name, description)

def add_constraint(org, name, description=""):
    """
    Adds a constraint to the organization's pool.
    """
    if not name:
        raise ValueError("Name is required")
    org.add_constraint(name, description)