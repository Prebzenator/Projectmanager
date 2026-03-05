"""
Project Planner Web Application
Flask Backend API
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from features.planner import Planner, TaskAssignmentError
import os

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
CORS(app)

# Global planner instance
planner = Planner()

# ============================================================================
# ORGANIZATION ENDPOINTS
# ============================================================================

@app.route('/api/organization/create', methods=['POST'])
def create_organization():
    """Create a new organization"""
    try:
        data = request.json
        name = data.get('name')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        org = planner.create_organization(name)
        return jsonify({
            'success': True,
            'organization': {
                'name': org.name,
                'members': len(org.members),
                'projects': len(org.projects)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/organization/info', methods=['GET'])
def get_organization_info():
    """Get organization information"""
    try:
        info = planner.get_organization_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================================
# QUALITIES & CONSTRAINTS ENDPOINTS
# ============================================================================

@app.route('/api/qualities/add', methods=['POST'])
def add_quality():
    """Add quality to organization"""
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        quality = planner.add_quality_to_organization(name, description)
        return jsonify({
            'success': True,
            'quality': {'name': quality.name, 'description': quality.description}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/constraints/add', methods=['POST'])
def add_constraint():
    """Add constraint to organization"""
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        constraint = planner.add_constraint_to_organization(name, description)
        return jsonify({
            'success': True,
            'constraint': {'name': constraint.name, 'description': constraint.description}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/qualities', methods=['GET'])
def get_qualities():
    """Get all qualities"""
    try:
        org = planner.get_organization()
        if not org:
            return jsonify({'qualities': []}), 200
        
        qualities = [{'name': q.name, 'description': q.description} for q in org.qualities]
        return jsonify({'qualities': qualities})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/constraints', methods=['GET'])
def get_constraints():
    """Get all constraints"""
    try:
        org = planner.get_organization()
        if not org:
            return jsonify({'constraints': []}), 200
        
        constraints = [{'name': c.name, 'description': c.description} for c in org.constraints]
        return jsonify({'constraints': constraints})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================================
# MEMBER ENDPOINTS
# ============================================================================

@app.route('/api/members/create', methods=['POST'])
def create_member():
    """Create a new member"""
    try:
        data = request.json
        name = data.get('name')
        role = data.get('role')
        available_hours = data.get('available_hours', 0)
        qualities = data.get('qualities', [])
        constraints = data.get('constraints', [])
        
        if not name or not role:
            return jsonify({'error': 'Name and role are required'}), 400
        
        member = planner.create_member(name, role, available_hours, qualities, constraints)
        return jsonify({
            'success': True,
            'member': {
                'name': member.name,
                'role': member.role,
                'available_hours': member.available_hours,
                'qualities': member.qualities,
                'constraints': member.constraints
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/members', methods=['GET'])
def get_members():
    """Get all members"""
    try:
        members = planner.get_members()
        members_list = [{
            'name': m.name,
            'role': m.role,
            'available_hours': m.available_hours,
            'qualities': m.qualities,
            'constraints': m.constraints
        } for m in members]
        return jsonify({'members': members_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@app.route('/api/projects/create', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.json
        name = data.get('name')
        duration_weeks = data.get('duration_weeks')
        
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        project = planner.create_project(name, duration_weeks)
        return jsonify({
            'success': True,
            'project': {
                'name': project.name,
                'duration_weeks': project.duration_weeks,
                'tasks': len(project.tasks),
                'members': len(project.members)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    try:
        projects = planner.get_projects()
        projects_list = [{
            'name': p.name,
            'duration_weeks': p.duration_weeks,
            'tasks_count': len(p.tasks),
            'members_count': len(p.members)
        } for p in projects]
        return jsonify({'projects': projects_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/projects/<project_name>', methods=['GET'])
def get_project(project_name):
    """Get project details"""
    try:
        projects = planner.get_projects()
        project = next((p for p in projects if p.name == project_name), None)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        tasks = [{
            'title': t.title,
            'hours': t.hours,
            'deadline': t.deadline,
            'status': t.status,
            'assigned_to': t.assigned_to.name if t.assigned_to else None,
            'required_qualities': t.required_qualities
        } for t in project.tasks]
        
        members = [{'name': m.name, 'role': m.role, 'available_hours': m.available_hours} for m in project.members]
        
        return jsonify({
            'name': project.name,
            'duration_weeks': project.duration_weeks,
            'tasks': tasks,
            'members': members
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/projects/<project_name>/members/add', methods=['POST'])
def add_member_to_project(project_name):
    """Add member to project"""
    try:
        data = request.json
        member_name = data.get('member_name')
        
        projects = planner.get_projects()
        project = next((p for p in projects if p.name == project_name), None)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        members = planner.get_members()
        member = next((m for m in members if m.name == member_name), None)
        
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        
        if member in project.members:
            return jsonify({'error': 'Member already in project'}), 400
        
        planner.assign_member_to_project(project, member)
        return jsonify({'success': True, 'message': f'{member_name} added to project'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================================
# TASK ENDPOINTS
# ============================================================================

@app.route('/api/tasks/add', methods=['POST'])
def add_task():
    """Add task to project"""
    try:
        data = request.json
        project_name = data.get('project_name')
        title = data.get('title')
        hours = data.get('hours')
        deadline = data.get('deadline')
        required_qualities = data.get('required_qualities', [])
        required_constraints = data.get('required_constraints', [])
        
        if not all([title, hours, deadline]):
            return jsonify({'error': 'Title, hours, and deadline are required'}), 400
        
        projects = planner.get_projects()
        project = next((p for p in projects if p.name == project_name), None)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        task = planner.add_task_to_project(project, title, hours, deadline, required_qualities, required_constraints)
        return jsonify({
            'success': True,
            'task': {
                'title': task.title,
                'hours': task.hours,
                'deadline': task.deadline,
                'status': task.status
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/tasks/<project_name>/compatible_members', methods=['POST'])
def get_compatible_members_for_task(project_name):
    """Get compatible members for a task"""
    try:
        data = request.json
        task_title = data.get('task_title')
        
        projects = planner.get_projects()
        project = next((p for p in projects if p.name == project_name), None)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        task = next((t for t in project.tasks if t.title == task_title), None)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        compatible = planner.get_compatible_members(project, task)
        members_list = [{
            'name': m.name,
            'role': m.role,
            'available_hours': m.available_hours,
            'qualities': m.qualities
        } for m in compatible]
        
        return jsonify({'compatible_members': members_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/tasks/assign', methods=['POST'])
def assign_task():
    """Assign task to member"""
    try:
        data = request.json
        project_name = data.get('project_name')
        task_title = data.get('task_title')
        member_name = data.get('member_name')
        
        projects = planner.get_projects()
        project = next((p for p in projects if p.name == project_name), None)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        task = next((t for t in project.tasks if t.title == task_title), None)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        members = planner.get_members()
        member = next((m for m in members if m.name == member_name), None)
        
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        
        planner.assign_task_to_member(task, member)
        return jsonify({'success': True, 'message': f'Task assigned to {member_name}'})
    except TaskAssignmentError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/tasks/status/<project_name>/<task_title>', methods=['PUT'])
def update_task_status(project_name, task_title):
    """Update task status"""
    try:
        data = request.json
        status = data.get('status')
        
        if status not in ['pending', 'assigned', 'in_progress', 'completed']:
            return jsonify({'error': 'Invalid status'}), 400
        
        projects = planner.get_projects()
        project = next((p for p in projects if p.name == project_name), None)
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        task = next((t for t in project.tasks if t.title == task_title), None)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        task.status = status
        
        if status == 'completed':
            task.mark_complete()
        elif status == 'in_progress':
            task.mark_in_progress()
        
        return jsonify({'success': True, 'message': 'Task status updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================================
# SERVE FRONTEND
# ============================================================================

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
