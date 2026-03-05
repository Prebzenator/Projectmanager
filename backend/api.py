import os
from flask import Flask, request, jsonify, send_from_directory
from backend.tables.organization import Organization
from backend.tables.project import Project
from backend.features.create_task import create_task
from backend.features.create_organization import (
    create_organization,
    add_quality_to_org,
    add_constraint_to_org
)

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


# Seeding data to have an organization implemented from start.
org = None
default_project = None


# Feature: Create task. Creates API for creating a task in the application
@app.post("/tasks")
def api_create_task():
    global default_project

    if org is None:
        return jsonify({"error": "Create an organization first"}), 400

    # Create default project only once
    if default_project is None:
        default_project = Project("Hovedprosjekt")
        org.add_project(default_project)

    data = request.json

    name = data.get("name")
    hours = data.get("hours")
    deadline = data.get("deadline")
    priority = data.get("priority", 1)
    dependencies = data.get("dependencies", [])

    # Validation for required field, and right input
    if not name or not hours or not deadline:
        return jsonify({"error": "Missing required fields"}), 400
    
    if not isinstance(priority, int) or priority < 1 or priority > 5:
        return jsonify({"error": "Priority must be an integer between 1 and 5"}), 400

    # Use the feature-layer function to create task.
    task = create_task(
        project=default_project,
        name=name,
        hours=hours,
        deadline=deadline,
        priority=priority
    )

    # Resolve dependencies (if any)
    dependency_tasks = [
        t for t in default_project.tasks if t.id in dependencies
    ]

    for dep in dependency_tasks:
        task.add_dependency(dep)

    # Build response
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


# Get all tasks
@app.get("/tasks")
def api_get_tasks():
    if default_project is None:
        return jsonify([])
    return jsonify([t.to_dict() for t in default_project.tasks])
