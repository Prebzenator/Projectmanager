/* ============================================================================
   PROJECT PLANNER - FRONTEND JAVASCRIPT
   ============================================================================ */

const API_URL = 'http://localhost:5000/api';
let currentProject = null;

// ============================================================================
// TAB NAVIGATION
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    // Initial load
    updateOrganizationInfo();
    loadMembers();
    loadProjects();
});

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active from all buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Activate button
    event.target.classList.add('active');

    // Refresh data when opening tabs
    if (tabName === 'organization') {
        loadMembers();
        updateQualityCheckboxes();
        updateConstraintCheckboxes();
    } else if (tabName === 'projects') {
        loadProjects();
    }
}

// ============================================================================
// ORGANIZATION
// ============================================================================

async function createOrganization() {
    const name = document.getElementById('orgName').value.trim();
    
    if (!name) {
        showStatus('orgStatus', 'error', 'Please enter organization name');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/organization/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });

        const data = await response.json();

        if (response.ok) {
            showStatus('orgStatus', 'success', `✓ Organization "${name}" created!`);
            document.getElementById('orgName').value = '';
            updateOrganizationInfo();
            loadProjects();
        } else {
            showStatus('orgStatus', 'error', data.error);
        }
    } catch (error) {
        showStatus('orgStatus', 'error', 'Error creating organization');
        console.error(error);
    }
}

async function updateOrganizationInfo() {
    try {
        const response = await fetch(`${API_URL}/organization/info`);
        const data = await response.json();
        console.log('Organization info:', data);
    } catch (error) {
        console.error('Error loading organization info:', error);
    }
}

// ============================================================================
// QUALITIES & CONSTRAINTS
// ============================================================================

async function addQuality() {
    const name = document.getElementById('qualityName').value.trim();
    const description = document.getElementById('qualityDesc').value.trim();

    if (!name) {
        alert('Please enter quality name');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/qualities/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description })
        });

        if (response.ok) {
            showStatus('orgStatus', 'success', `✓ Quality "${name}" added!`);
            document.getElementById('qualityName').value = '';
            document.getElementById('qualityDesc').value = '';
            updateQualityCheckboxes();
        }
    } catch (error) {
        console.error('Error adding quality:', error);
        alert('Error adding quality');
    }
}

async function addConstraint() {
    const name = document.getElementById('constraintName').value.trim();
    const description = document.getElementById('constraintDesc').value.trim();

    if (!name) {
        alert('Please enter constraint name');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/constraints/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description })
        });

        if (response.ok) {
            showStatus('orgStatus', 'success', `✓ Constraint "${name}" added!`);
            document.getElementById('constraintName').value = '';
            document.getElementById('constraintDesc').value = '';
            updateConstraintCheckboxes();
        }
    } catch (error) {
        console.error('Error adding constraint:', error);
        alert('Error adding constraint');
    }
}

async function updateQualityCheckboxes() {
    try {
        const response = await fetch(`${API_URL}/qualities`);
        const data = await response.json();

        let html = '';
        data.qualities.forEach(quality => {
            html += `
                <div class="checkbox-wrapper">
                    <input type="checkbox" id="qual_${quality.name}" value="${quality.name}">
                    <label for="qual_${quality.name}">${quality.name}</label>
                </div>
            `;
        });

        document.getElementById('qualityCheckboxes').innerHTML = html;
        document.getElementById('taskQualityCheckboxes').innerHTML = html;
    } catch (error) {
        console.error('Error loading qualities:', error);
    }
}

async function updateConstraintCheckboxes() {
    try {
        const response = await fetch(`${API_URL}/constraints`);
        const data = await response.json();

        let html = '';
        data.constraints.forEach(constraint => {
            html += `
                <div class="checkbox-wrapper">
                    <input type="checkbox" id="const_${constraint.name}" value="${constraint.name}">
                    <label for="const_${constraint.name}">${constraint.name}</label>
                </div>
            `;
        });

        document.getElementById('constraintCheckboxes').innerHTML = html;
    } catch (error) {
        console.error('Error loading constraints:', error);
    }
}

// ============================================================================
// MEMBERS
// ============================================================================

async function createMember() {
    const name = document.getElementById('memberName').value.trim();
    const role = document.getElementById('memberRole').value.trim();
    const available_hours = parseInt(document.getElementById('memberHours').value) || 0;

    if (!name || !role) {
        showStatus('memberStatus', 'error', 'Please enter name and role');
        return;
    }

    // Get selected qualities
    const qualities = Array.from(document.querySelectorAll('#qualityCheckboxes input:checked'))
        .map(cb => cb.value);

    // Get selected constraints
    const constraints = Array.from(document.querySelectorAll('#constraintCheckboxes input:checked'))
        .map(cb => cb.value);

    try {
        const response = await fetch(`${API_URL}/members/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, role, available_hours, qualities, constraints })
        });

        const data = await response.json();

        if (response.ok) {
            showStatus('memberStatus', 'success', `✓ Member "${name}" added!`);
            document.getElementById('memberName').value = '';
            document.getElementById('memberRole').value = '';
            document.getElementById('memberHours').value = '0';
            document.querySelectorAll('#qualityCheckboxes input').forEach(cb => cb.checked = false);
            document.querySelectorAll('#constraintCheckboxes input').forEach(cb => cb.checked = false);
            loadMembers();
        } else {
            showStatus('memberStatus', 'error', data.error);
        }
    } catch (error) {
        showStatus('memberStatus', 'error', 'Error creating member');
        console.error(error);
    }
}

async function loadMembers() {
    try {
        const response = await fetch(`${API_URL}/members`);
        const data = await response.json();

        // Update project members select
        let selectHtml = '<option value="">Select member...</option>';
        data.members.forEach(member => {
            selectHtml += `<option value="${member.name}">${member.name} (${member.role})</option>`;
        });
        document.getElementById('membersToAdd').innerHTML = selectHtml;

        // Update members list
        let listHtml = '';
        if (data.members.length === 0) {
            listHtml = '<div class="empty-state">No members yet. Add one in the Organization tab.</div>';
        } else {
            data.members.forEach(member => {
                listHtml += `
                    <div class="card">
                        <div class="card-title">${member.name}</div>
                        <div class="card-subtitle">${member.role}</div>
                        <div class="card-content">
                            <p><strong>Available Hours:</strong> ${member.available_hours}</p>
                            ${member.qualities.length > 0 ? `
                                <p><strong>Qualities:</strong>
                                ${member.qualities.map(q => `<span class="badge badge-quality">${q}</span>`).join('')}
                                </p>
                            ` : ''}
                            ${member.constraints.length > 0 ? `
                                <p><strong>Constraints:</strong>
                                ${member.constraints.map(c => `<span class="badge badge-constraint">${c}</span>`).join('')}
                                </p>
                            ` : ''}
                        </div>
                    </div>
                `;
            });
        }

        document.getElementById('membersList').innerHTML = listHtml;
    } catch (error) {
        console.error('Error loading members:', error);
    }
}

// ============================================================================
// PROJECTS
// ============================================================================

async function createProject() {
    const name = document.getElementById('projectName').value.trim();
    const duration_weeks = parseInt(document.getElementById('projectDuration').value) || null;

    if (!name) {
        showStatus('projectStatus', 'error', 'Please enter project name');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/projects/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, duration_weeks })
        });

        const data = await response.json();

        if (response.ok) {
            showStatus('projectStatus', 'success', `✓ Project "${name}" created!`);
            document.getElementById('projectName').value = '';
            document.getElementById('projectDuration').value = '0';
            loadProjects();
        } else {
            showStatus('projectStatus', 'error', data.error);
        }
    } catch (error) {
        showStatus('projectStatus', 'error', 'Error creating project');
        console.error(error);
    }
}

async function loadProjects() {
    try {
        const response = await fetch(`${API_URL}/projects`);
        const data = await response.json();

        let listHtml = '';
        if (data.projects.length === 0) {
            listHtml = '<div class="empty-state">No projects yet. Create one above.</div>';
        } else {
            data.projects.forEach(project => {
                listHtml += `
                    <div class="card">
                        <div class="card-title">${project.name}</div>
                        <div class="card-content">
                            ${project.duration_weeks ? `<p><strong>Duration:</strong> ${project.duration_weeks} weeks</p>` : ''}
                            <p><strong>Tasks:</strong> ${project.tasks_count} | <strong>Members:</strong> ${project.members_count}</p>
                        </div>
                        <div class="card-actions">
                            <button onclick="openProject('${project.name}')" class="btn btn-primary">Manage</button>
                        </div>
                    </div>
                `;
            });
        }

        document.getElementById('projectsList').innerHTML = listHtml;
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

async function openProject(projectName) {
    currentProject = projectName;

    try {
        const response = await fetch(`${API_URL}/projects/${projectName}`);
        const project = await response.json();

        document.getElementById('projectTitle').textContent = `Project: ${projectName}`;
        document.getElementById('projectDetailsSection').style.display = 'block';

        // Load project members
        let membersHtml = '';
        project.members.forEach(member => {
            membersHtml += `
                <div class="badge badge-quality">${member.name} (${member.role}) - ${member.available_hours}h available</div>
            `;
        });
        document.getElementById('projectMembersList').innerHTML = membersHtml || '<p class="text-muted">No members assigned</p>';

        // Load project tasks
        let tasksHtml = '';
        project.tasks.forEach(task => {
            const statusClass = task.status === 'pending' ? 'pending' : (task.status === 'in_progress' ? 'in_progress' : '');
            tasksHtml += `
                <div class="card">
                    <div class="card-title">${task.title}</div>
                    <div class="card-content">
                        <p><strong>Hours:</strong> ${task.hours} | <strong>Deadline:</strong> ${task.deadline}</p>
                        <p><strong>Status:</strong> <span class="badge badge-status ${statusClass}">${task.status}</span></p>
                        ${task.assigned_to ? `<p><strong>Assigned to:</strong> ${task.assigned_to}</p>` : '<p class="text-muted">Not assigned</p>'}
                        ${task.required_qualities.length > 0 ? `
                            <p><strong>Required:</strong> ${task.required_qualities.map(q => `<span class="badge badge-quality">${q}</span>`).join('')}</p>
                        ` : ''}
                    </div>
                    <div class="card-actions">
                        ${!task.assigned_to ? `<button onclick="assignTask('${task.title}')" class="btn btn-success">Assign</button>` : ''}
                        ${task.status !== 'completed' ? `<button onclick="updateTaskStatus('${task.title}', 'in_progress')" class="btn btn-secondary">In Progress</button>` : ''}
                        ${task.status !== 'completed' ? `<button onclick="updateTaskStatus('${task.title}', 'completed')" class="btn btn-secondary">Complete</button>` : ''}
                    </div>
                </div>
            `;
        });
        document.getElementById('projectTasksList').innerHTML = tasksHtml || '<p class="text-muted">No tasks added</p>';

        // Scroll to project details
        document.getElementById('projectDetailsSection').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error loading project:', error);
        alert('Error loading project details');
    }
}

async function addMemberToProject() {
    const member_name = document.getElementById('membersToAdd').value;

    if (!member_name || !currentProject) {
        alert('Please select a member');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/projects/${currentProject}/members/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ member_name })
        });

        const data = await response.json();

        if (response.ok) {
            alert(`✓ ${member_name} added to project!`);
            openProject(currentProject);
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error adding member:', error);
        alert('Error adding member');
    }
}

async function addTask() {
    const title = document.getElementById('taskTitle').value.trim();
    const hours = parseInt(document.getElementById('taskHours').value);
    const deadline = document.getElementById('taskDeadline').value;

    if (!title || !hours || !deadline) {
        alert('Please fill in all fields');
        return;
    }

    const required_qualities = Array.from(document.querySelectorAll('#taskQualityCheckboxes input:checked'))
        .map(cb => cb.value);

    try {
        const response = await fetch(`${API_URL}/tasks/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_name: currentProject,
                title,
                hours,
                deadline,
                required_qualities
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert(`✓ Task "${title}" added!`);
            document.getElementById('taskTitle').value = '';
            document.getElementById('taskHours').value = '0';
            document.getElementById('taskDeadline').value = '';
            document.querySelectorAll('#taskQualityCheckboxes input').forEach(cb => cb.checked = false);
            openProject(currentProject);
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error adding task:', error);
        alert('Error adding task');
    }
}

async function assignTask(taskTitle) {
    const project_name = currentProject;

    try {
        const response = await fetch(`${API_URL}/tasks/${project_name}/compatible_members`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task_title: taskTitle })
        });

        const data = await response.json();

        if (data.compatible_members.length === 0) {
            alert('No members with required skills available');
            return;
        }

        // Simple selection
        const memberNames = data.compatible_members.map(m => m.name);
        const memberHtml = memberNames.map((name, idx) => `${idx + 1}. ${name}`).join('\n');
        const selectedIdx = prompt(`Select member (enter number):\n${memberHtml}`);

        if (selectedIdx && selectedIdx >= 1 && selectedIdx <= memberNames.length) {
            const member_name = memberNames[selectedIdx - 1];

            const assignResp = await fetch(`${API_URL}/tasks/assign`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    project_name,
                    task_title: taskTitle,
                    member_name
                })
            });

            const assignData = await assignResp.json();

            if (assignResp.ok) {
                alert(`✓ Task assigned to ${member_name}!`);
                openProject(currentProject);
            } else {
                alert(assignData.error);
            }
        }
    } catch (error) {
        console.error('Error assigning task:', error);
        alert('Error assigning task');
    }
}

async function updateTaskStatus(taskTitle, status) {
    try {
        const response = await fetch(`${API_URL}/tasks/status/${currentProject}/${taskTitle}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });

        const data = await response.json();

        if (response.ok) {
            openProject(currentProject);
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error updating task:', error);
        alert('Error updating task');
    }
}

// ============================================================================
// UTILITIES
// ============================================================================

function showStatus(elementId, type, message) {
    const el = document.getElementById(elementId);
    el.className = `status-message ${type}`;
    el.textContent = message;

    setTimeout(() => {
        el.className = 'status-message';
    }, 5000);
}
