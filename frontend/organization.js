document.addEventListener("DOMContentLoaded", () => {
    loadOrganization();
    loadMemberAttributes();

    document.getElementById("project-form").addEventListener("submit", handleCreateProject);
    document.getElementById("member-form").addEventListener("submit", handleCreateMember);
    document.getElementById("quality-form").addEventListener("submit", handleCreateQuality);
    document.getElementById("constraint-form").addEventListener("submit", handleCreateConstraint);
});


// ------------------------------
// Load organization
// ------------------------------
async function loadOrganization() {
    const res = await fetch("/organization");

    if (!res.ok) {
        alert("No organization exists. Go back and create one.");
        window.location.href = "index.html";
        return;
    }

    const org = await res.json();

    document.getElementById("org-name").textContent = org.name;

    renderProjects(org.projects);
    renderMembers(org.members);
    renderQualities(org.qualities);
    renderConstraints(org.constraints);
    renderProjectMembersCheckboxes(org.members);
}


// ------------------------------
// Load qualities + constraints for member form
// ------------------------------
async function loadMemberAttributes() {
    const qRes = await fetch("/qualities");
    const qualities = await qRes.json();

    const cRes = await fetch("/constraints");
    const constraints = await cRes.json();

    const qBox = document.getElementById("member-qualities-box");
    const cBox = document.getElementById("member-constraints-box");

    qBox.innerHTML = "";
    cBox.innerHTML = "";

    qualities.forEach(q => {
        const wrapper = document.createElement("label");
        wrapper.className = "checkbox-item";

        wrapper.innerHTML = `
            <input type="checkbox" value="${q.name}">
            ${q.name}
        `;

        qBox.appendChild(wrapper);
    });

    constraints.forEach(c => {
        const wrapper = document.createElement("label");
        wrapper.className = "checkbox-item";

        wrapper.innerHTML = `
            <input type="checkbox" value="${c.name}">
            ${c.name}
        `;

        cBox.appendChild(wrapper);
    });
}


// ------------------------------
// Render functions
// ------------------------------
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
        card.onclick = () => window.location.href = `project.html?project=${project.id}`;
        container.appendChild(card);
    });
}

function renderMembers(members) {
    const container = document.getElementById("members-list");
    container.innerHTML = "";

    members.forEach((member, index) => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <strong>${member.name}</strong> (${member.role})<br>
            Qualities: ${member.qualities.length ? member.qualities.join(", ") : "None"}<br>
            Constraints: ${member.constraints.length ? member.constraints.join(", ") : "None"}
        `;

        container.appendChild(card);
    });
}

function renderQualities(qualities) {
    const container = document.getElementById("qualities-list");
    container.innerHTML = "";

    qualities.forEach(q => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<strong>${q.name}</strong><br>${q.description || ""}`;
        container.appendChild(card);
    });
}

function renderConstraints(constraints) {
    const container = document.getElementById("constraints-list");
    container.innerHTML = "";

    constraints.forEach(c => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<strong>${c.name}</strong><br>${c.description || ""}`;
        container.appendChild(card);
    });
}

function renderProjectMembersCheckboxes(members) {
    const box = document.getElementById("project-members-box");
    if (!box) return;

    box.innerHTML = "";

    members.forEach(m => {
        const wrapper = document.createElement("label");
        wrapper.className = "checkbox-item";

        // Viktig: bruk navn som value
        wrapper.innerHTML = `
            <input type="checkbox" value="${m.name}">
            ${m.name} (${m.role})
        `;

        box.appendChild(wrapper);
    });
}


// ------------------------------
// Create functions
// ------------------------------
async function handleCreateProject(e) {
    e.preventDefault();

    const name = document.getElementById("project-name").value;
    const duration_weeks = parseInt(document.getElementById("project-duration").value);

    const members = Array.from(
        document.querySelectorAll("#project-members-box input[type='checkbox']:checked")
    ).map(cb => cb.value); // navn

    await fetch("/projects", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, duration_weeks, members })
    });

    e.target.reset();
    loadOrganization();
}

async function handleCreateMember(e) {
    e.preventDefault();

    const name = document.getElementById("member-name").value;
    const role = document.getElementById("member-role").value;

    const qualities = Array.from(
        document.querySelectorAll("#member-qualities-box input[type='checkbox']:checked")
    ).map(cb => cb.value);

    const constraints = Array.from(
        document.querySelectorAll("#member-constraints-box input[type='checkbox']:checked")
    ).map(cb => cb.value);

    await fetch("/member", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name,
            role,
            qualities,
            constraints,
            available_hours: 40
        })
    });

    e.target.reset();
    await loadOrganization();
    await loadMemberAttributes();
}

async function handleCreateQuality(e) {
    e.preventDefault();

    const name = document.getElementById("quality-name").value;
    const description = document.getElementById("quality-description").value;

    await fetch("/organization/qualities", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, description })
    });

    e.target.reset();
    await loadOrganization();
    await loadMemberAttributes();
}

async function handleCreateConstraint(e) {
    e.preventDefault();

    const name = document.getElementById("constraint-name").value;
    const description = document.getElementById("constraint-description").value;

    await fetch("/organization/constraints", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, description })
    });

    e.target.reset();
    await loadOrganization();
    await loadMemberAttributes();
}
