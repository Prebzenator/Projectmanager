import os
from flask import Flask, request, jsonify, send_from_directory
from backend.tables.organization import Organization
from backend.features.create_member import create_member
from backend.tables.project import Project
from backend.features.create_task import create_task
from backend.features.create_organization import (
    create_organization,
    add_quality_to_org,
    add_constraint_to_org
)
from backend.features.create_project import create_project
from backend.features.generate_plan import generate_project_plan


# Help the application find the right files (API)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Backend folder
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

# Initialize Flask application and configure static file serving.
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")


# Get method to send the start of the application to index.html
@app.get("/")
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, "index.html")


# Simple endpoint used to verify that the backend is running.
@app.get("/health")
def health_check():
    return {"status": "ok"}


# In-memory state
org = None
default_project = None


# Feature: Create member
@app.post("/member")
def api_create_member():
    global org

    if org is None:
        return jsonify({"error": "Create an organization first"}), 400

    data = request.json

    name = data.get("name")
    role = data.get("role")
    qualities = data.get("qualities", [])
    constraints = data.get("constraints", [])
    available_hours = data.get("available_hours", 0)

    if not name or not role:
        return jsonify({"error": "Name and role are required"}), 400

    member = create_member(
        org=org,
        name=name,
        role=role,
        qualities=qualities,
        constraints=constraints,
        available_hours=available_hours
    )

    return jsonify({
        "message": "Member created",
        "member": member.to_dict()
    }), 201


# Feature: Create task
@app.post("/tasks")
def api_create_task():
    global default_project

    if org is None:
        return jsonify({"error": "Create an organization first"}), 400

    # Create default project only once
    if default_project is None:
        default_project = Project("Main Project", duration_weeks=12, members=[])
        org.add_project(default_project)

    data = request.json

    name = data.get("name")
    hours = data.get("hours")
    deadline = data.get("deadline")
    priority = data.get("priority", 1)
    dependencies = data.get("dependencies", [])

    # NEW: read qualities and constraints from the request
    required_qualities = data.get("required_qualities", [])
    required_constraints = data.get("required_constraints", [])

    # Validation
    if not name or hours is None or not deadline:
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(priority, int) or priority < 1 or priority > 5:
        return jsonify({"error": "Priority must be an integer between 1 and 5"}), 400

    # Create task — now passes qualities and constraints too
    task = create_task(
        project=default_project,
        name=name,
        hours=hours,
        deadline=deadline,
        priority=priority,
        required_qualities=required_qualities,      # NEW
        required_constraints=required_constraints   # NEW
    )

    # Resolve dependencies (if any)
    dependency_tasks = [
        t for t in default_project.tasks if t.id in dependencies
    ]
    for dep in dependency_tasks:
        task.add_dependency(dep)

    return jsonify({
        "message": "Task created",
        "task": task.to_dict()
    }), 201


# Feature: Create Organization
@app.post("/organization")
def api_create_organization():
    global org
    data = request.json

    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    org = create_organization(name, description)
    return jsonify({"message": f"Organization '{name}' created"}), 201


@app.get("/organization")
def api_get_organization():
    if org is None:
        return jsonify({"error": "No organization created yet"}), 404

    return jsonify(org.to_dict())


@app.post("/organization/qualities")
def api_add_quality():
    if org is None:
        return jsonify({"error": "Create an organization first"}), 400

    data = request.json
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    add_quality_to_org(org, name, description)
    return jsonify({"message": f"Quality '{name}' added"}), 201


@app.post("/organization/constraints")
def api_add_constraint():
    if org is None:
        return jsonify({"error": "Create an organization first"}), 400

    data = request.json
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    add_constraint_to_org(org, name, description)
    return jsonify({"message": f"Constraint '{name}' added"}), 201


# Get all qualities
@app.get("/qualities")
def api_get_qualities():
    if org is None:
        return jsonify([])
    return jsonify([q.to_dict() for q in org.qualities])


# Get all constraints
@app.get("/constraints")
def api_get_constraints():
    if org is None:
        return jsonify([])
    return jsonify([c.to_dict() for c in org.constraints])


# Feature: Create project
@app.post("/projects")
def api_create_project():
    global org

    if org is None:
        return jsonify({"error": "Create an organization first"}), 400

    data = request.json

    name = data.get("name")
    duration = data.get("duration_weeks")
    members = data.get("members", [])

    if not name:
        return jsonify({"error": "Project name is required"}), 400

    if duration is None or not isinstance(duration, int) or duration <= 0:
        return jsonify({"error": "Duration must be a positive integer"}), 400

    project = create_project(name, duration, members)
    org.add_project(project)

    return jsonify({
        "message": "Project created",
        "project": project.to_dict()
    }), 201


# Get all tasks
@app.get("/tasks")
def api_get_tasks():
    if default_project is None:
        return jsonify([])
    return jsonify([t.to_dict() for t in default_project.tasks])


# Get all members
@app.get("/members")
def api_get_members():
    if org is None:
        return jsonify([])
    return jsonify([m.to_dict() for m in org.members])



# Generate plan
@app.post("/generate_plan")
def api_generate_plan():
    global default_project

    if default_project is None:
        return jsonify({"error": "No project exists"}), 400

    data = request.json or {}
    mode = data.get("mode", "fastest")

    plan = generate_project_plan(default_project, mode=mode)

    return jsonify({
        "message": "Plan generated",
        "plan": plan
    }), 200


if __name__ == "__main__":
    app.run(debug=True)