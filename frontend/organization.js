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
}


// ------------------------------
// Load qualities + constraints for member form
// ------------------------------
async function loadMemberAttributes() {
    const qRes = await fetch("/qualities");
    const qualities = await qRes.json();

    const cRes = await fetch("/constraints");
    const constraints = await cRes.json();

    const qSelect = document.getElementById("member-qualities");
    const cSelect = document.getElementById("member-constraints");

    qSelect.innerHTML = "";
    cSelect.innerHTML = "";

    qualities.forEach(q => {
        const opt = document.createElement("option");
        opt.value = q.name;
        opt.textContent = q.name;
        qSelect.appendChild(opt);
    });

    constraints.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c.name;
        opt.textContent = c.name;
        cSelect.appendChild(opt);
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
        card.onclick = () => window.location.href = "project.html";
        container.appendChild(card);
    });
}

function renderMembers(members) {
    const container = document.getElementById("members-list");
    container.innerHTML = "";

    members.forEach(member => {
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


// ------------------------------
// Create functions
// ------------------------------
async function handleCreateProject(e) {
    e.preventDefault();

    const name = document.getElementById("project-name").value;
    const duration_weeks = parseInt(document.getElementById("project-duration").value);

    await fetch("/projects", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, duration_weeks })
    });

    e.target.reset();
    loadOrganization();
}

async function handleCreateMember(e) {
    e.preventDefault();

    const name = document.getElementById("member-name").value;
    const role = document.getElementById("member-role").value;

    const qualities = Array.from(
        document.getElementById("member-qualities").selectedOptions
    ).map(o => o.value);

    const constraints = Array.from(
        document.getElementById("member-constraints").selectedOptions
    ).map(o => o.value);

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
    loadOrganization();
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
    await loadMemberAttributes();  // VIKTIG: oppdater member-select
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
    await loadMemberAttributes();  // VIKTIG: oppdater member-select
}
