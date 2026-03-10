document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
    populateDependenciesDropdown();

    document.getElementById("organization-form")
        .addEventListener("submit", handleCreateOrganization);

    document.getElementById("quality-form")
        .addEventListener("submit", handleAddQuality);

    document.getElementById("constraint-form")
        .addEventListener("submit", handleAddConstraint);

    document.getElementById("task-form")
        .addEventListener("submit", handleCreateTask);

    // Create Member – nå uten checkboxes
    document.getElementById("member-form")
        .addEventListener("submit", handleCreateMember);
});


// ---------------------------------------------------------
// Create Organization
// ---------------------------------------------------------
async function handleCreateOrganization(event) {
    event.preventDefault();

    const name = document.getElementById("org-name").value;
    const description = document.getElementById("org-description").value;

    const res = await fetch("/organization", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });

    const result = await res.json();
    const box = document.getElementById("org-response");

    if (res.status === 201) {
        box.textContent = "Organization created!";
        box.style.color = "green";
        document.getElementById("organization-form").reset();
    } else {
        box.textContent = result.error;
        box.style.color = "red";
    }
}


// ---------------------------------------------------------
// Add Quality
// ---------------------------------------------------------
async function handleAddQuality(event) {
    event.preventDefault();

    const name = document.getElementById("quality-name").value;
    const description = document.getElementById("quality-description").value;

    const res = await fetch("/organization/qualities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });

    const result = await res.json();
    const box = document.getElementById("quality-response");

    if (res.status === 201) {
        box.textContent = "Quality added!";
        box.style.color = "green";
        document.getElementById("quality-form").reset();
    } else {
        box.textContent = result.error;
        box.style.color = "red";
    }
}


// ---------------------------------------------------------
// Add Constraint
// ---------------------------------------------------------
async function handleAddConstraint(event) {
    event.preventDefault();

    const name = document.getElementById("constraint-name").value;
    const description = document.getElementById("constraint-description").value;

    const res = await fetch("/organization/constraints", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });

    const result = await res.json();
    const box = document.getElementById("constraint-response");

    if (res.status === 201) {
        box.textContent = "Constraint added!";
        box.style.color = "green";
        document.getElementById("constraint-form").reset();
    } else {
        box.textContent = result.error;
        box.style.color = "red";
    }
}



// ---------------------------------------------------------
// Create Member 
// ---------------------------------------------------------
async function handleCreateMember(event) {
    event.preventDefault();

    const name = document.getElementById("member-name").value;
    const role = document.getElementById("member-role").value;
    const available_hours = parseInt(document.getElementById("member-hours").value);

    // Hent tekst fra textarea og gjør om til lister
    const qualities = document.getElementById("member-qualities").value
        .split("\n")
        .map(q => q.trim())
        .filter(q => q !== "");

    const constraints = document.getElementById("member-constraints").value
        .split("\n")
        .map(c => c.trim())
        .filter(c => c !== "");

    const res = await fetch("/member", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name,
            role,
            available_hours,
            qualities,
            constraints
        })
    });

    const result = await res.json();
    const box = document.getElementById("member-response");

    if (res.status === 201) {
        box.textContent = "Member created!";
        box.style.color = "green";

        document.getElementById("member-form").reset();
        addMemberToList(result.member);
    } else {
        box.textContent = result.error;
        box.style.color = "red";
    }
}


// ---------------------------------------------------------
// Show members
// ---------------------------------------------------------
function addMemberToList(member) {
    const list = document.getElementById("member-list");
    const li = document.createElement("li");
    li.textContent = `${member.name} – ${member.role} (${member.available_hours}h)`;
    list.appendChild(li);
}



// ---------------------------------------------------------
// Load Tasks
// ---------------------------------------------------------
async function loadTasks() {
    const res = await fetch("/tasks");
    const tasks = await res.json();
    renderTasks(tasks);
}

function renderTasks(tasks) {
    const container = document.getElementById("task-list");
    container.innerHTML = "";

    if (tasks.length === 0) {
        container.innerHTML = "<p>No tasks created yet.</p>";
        return;
    }

    tasks.forEach(task => {
        const div = document.createElement("div");
        div.className = "task-card";

        div.innerHTML = `
            <h3>${task.name}</h3>
            <p><strong>Hours:</strong> ${task.hours}</p>
            <p><strong>Deadline:</strong> ${task.deadline}</p>
            <p><strong>Priority:</strong> ${task.priority}</p>
            <p><strong>Dependencies:</strong> 
                ${task.dependencies.length > 0 ? task.dependencies.join(", ") : "None"}
            </p>
        `;

        container.appendChild(div);
    });
}


// ---------------------------------------------------------
// Populate Dependencies Dropdown
// ---------------------------------------------------------
async function populateDependenciesDropdown() {
    const res = await fetch("/tasks");
    const tasks = await res.json();

    const select = document.getElementById("task-dependencies");
    select.innerHTML = "";

    tasks.forEach(task => {
        const option = document.createElement("option");
        option.value = task.id;
        option.textContent = task.name;
        select.appendChild(option);
    });
}


// ---------------------------------------------------------
// Create Task
// ---------------------------------------------------------
async function handleCreateTask(event) {
    event.preventDefault();

    const name = document.getElementById("task-name").value;
    const hours = parseInt(document.getElementById("task-hours").value);
    const deadline = document.getElementById("task-deadline").value;
    const priority = parseInt(document.getElementById("task-priority").value);

    const dependencies = Array.from(
        document.getElementById("task-dependencies").selectedOptions
    ).map(opt => opt.value);

    const res = await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name,
            hours,
            deadline,
            priority,
            dependencies
        })
    });

    const result = await res.json();
    const box = document.getElementById("task-response");

    if (res.status === 201) {
        box.textContent = "Task created!";
        box.style.color = "green";

        document.getElementById("task-form").reset();
        loadTasks();
        populateDependenciesDropdown();
    } else {
        box.textContent = result.error;
        box.style.color = "red";
    }
}
