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


# -----------------------------
# Helper: Find project by ID
# -----------------------------
def get_project_by_id(project_id):
    if org is None:
        return None
    for p in org.projects:
        if str(p.id) == str(project_id):
            return p
    return None


# -----------------------------
# Create member
# -----------------------------
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


# -----------------------------
# Create organization
# -----------------------------
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


# -----------------------------
# Add qualities + constraints
# -----------------------------
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


@app.get("/qualities")
def api_get_qualities():
    if org is None:
        return jsonify([])
    return jsonify([q.to_dict() for q in org.qualities])


@app.get("/constraints")
def api_get_constraints():
    if org is None:
        return jsonify([])
    return jsonify([c.to_dict() for c in org.constraints])


# -----------------------------
# Create project
# -----------------------------
@app.post("/projects")
def api_create_project():
    global org

    if org is None:
        return jsonify({"error": "Create an organization first"}), 400

    data = request.json

    name = data.get("name")
    duration = data.get("duration_weeks")
    members = data.get("members", [])  # ← LISTE MED NAVN (str)

    if not name:
        return jsonify({"error": "Project name is required"}), 400

    if duration is None or not isinstance(duration, int) or duration <= 0:
        return jsonify({"error": "Duration must be a positive integer"}), 400

    # create_project forventer liste med navn (str)
    project = create_project(org, name, duration, members)

    return jsonify({
        "message": "Project created",
        "project": project.to_dict()
    }), 201


# -----------------------------
# Members
# -----------------------------
@app.get("/members")
def api_get_members():
    if org is None:
        return jsonify([])
    return jsonify([m.to_dict() for m in org.members])


# -----------------------------
# Project-specific TASK routes
# -----------------------------
@app.get("/projects/<project_id>/tasks")
def api_get_project_tasks(project_id):
    project = get_project_by_id(project_id)
    if project is None:
        return jsonify({"error": "Project not found"}), 404

    return jsonify([t.to_dict() for t in project.tasks])


@app.post("/projects/<project_id>/tasks")
def api_create_project_task(project_id):
    project = get_project_by_id(project_id)
    if project is None:
        return jsonify({"error": "Project not found"}), 404

    data = request.json

    name = data.get("name")
    hours = data.get("hours")
    deadline = data.get("deadline")
    priority = data.get("priority", 1)
    dependencies = data.get("dependencies", [])
    required_qualities = data.get("required_qualities", [])
    required_constraints = data.get("required_constraints", [])

    if not name or hours is None or not deadline:
        return jsonify({"error": "Missing required fields"}), 400

    task = create_task(
        project=project,
        name=name,
        hours=hours,
        deadline=deadline,
        priority=priority,
        required_qualities=required_qualities,
        required_constraints=required_constraints
    )

    dependency_tasks = [t for t in project.tasks if t.id in dependencies]
    for dep in dependency_tasks:
        task.add_dependency(dep)

    return jsonify({
        "message": "Task created",
        "task": task.to_dict()
    }), 201


# -----------------------------
# Project-specific PLAN route
# -----------------------------
@app.post("/projects/<project_id>/generate_plan")
def api_generate_project_plan(project_id):
    project = get_project_by_id(project_id)
    if project is None:
        return jsonify({"error": "Project not found"}), 404

    data = request.json or {}
    mode = data.get("mode", "fastest")

    plan = generate_project_plan(project, mode=mode)

    return jsonify({
        "message": "Plan generated",
        "plan": plan
    }), 200


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
