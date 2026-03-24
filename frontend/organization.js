document.addEventListener("DOMContentLoaded", () => {
    loadOrganization();

    document.getElementById("create-project-btn").onclick = () => {
        const name = prompt("Project name:");
        const duration = prompt("Duration in weeks:");
        if (name && duration) {
            createProject(name, duration);
        }
    };

    document.getElementById("add-member-btn").onclick = () => {
        const name = prompt("Member name:");
        const role = prompt("Role:");
        if (name && role) {
            createMember(name, role);
        }
    };

    document.getElementById("add-quality-btn").onclick = () => {
        const name = prompt("Quality name:");
        const description = prompt("Description:");
        if (name) {
            createQuality(name, description);
        }
    };

    document.getElementById("add-constraint-btn").onclick = () => {
        const name = prompt("Constraint name:");
        const description = prompt("Description:");
        if (name) {
            createConstraint(name, description);
        }
    };
});

async function loadOrganization() {
    const response = await fetch("/api/organization");
    const org = await response.json();

    document.getElementById("org-name").textContent = org.name;
    renderProjects(org.projects);
    renderMembers(org.members);
    renderQualities(org.qualities);
    renderConstraints(org.constraints);
}
function renderMembers(members) {
    const container = document.getElementById("members-list");
    container.innerHTML = "";
    members.forEach(member => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <strong>${member.name}</strong> (${member.role})<br>
            Qualities: ${member.qualities.join(", ")}<br>
            Constraints: ${member.constraints.join(", ")}<br>
            <button class="edit-member-btn">Edit</button>
        `;
        card.querySelector(".edit-member-btn").onclick = () => editMember(member);
        container.appendChild(card);
    });
}

function renderQualities(qualities) {
    const container = document.getElementById("qualities-list");
    container.innerHTML = "";
    qualities.forEach(q => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<strong>${q.name}</strong><br>${q.description}`;
        container.appendChild(card);
    });
}

function renderConstraints(constraints) {
    const container = document.getElementById("constraints-list");
    container.innerHTML = "";
    constraints.forEach(c => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<strong>${c.name}</strong><br>${c.description}`;
        container.appendChild(card);
    });
}

async function createMember(name, role) {
    await fetch("/api/member", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, role})
    });
    loadOrganization();
}

async function createQuality(name, description) {
    await fetch("/api/organization/qualities", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, description})
    });
    loadOrganization();
}

async function createConstraint(name, description) {
    await fetch("/api/organization/constraints", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, description})
    });
    loadOrganization();
}

function editMember(member) {
    const newName = prompt("Edit name:", member.name);
    const newRole = prompt("Edit role:", member.role);
    // For enkelhet: bare navn og rolle, kan utvides med qualities/constraints
    if (newName && newRole && (newName !== member.name || newRole !== member.role)) {
        // TODO: Implementer API for å oppdatere medlem hvis ønskelig
        alert("Edit member API not implemented");
    }
}

function renderProjects(projects) {
    const container = document.getElementById("projects-list");
    container.innerHTML = "";

    projects.forEach(project => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <strong>${project.name}</strong><br>
            Duration: ${project.duration_weeks} weeks<br>
            Members: ${project.members.length}
        `;
        card.onclick = () => openProject(project.id);
        container.appendChild(card);
    });
}

async function createProject(name, duration_weeks) {
    await fetch("/api/projects", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, duration_weeks})
    });

    loadOrganization();
}

function openProject(id) {
    window.location.href = `/project.html?id=${id}`;
}



