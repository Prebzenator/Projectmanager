// Load tasks when the page loads
document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
    populateDependenciesDropdown()
    loadOrganization;

    const form = document.getElementById("task-form");
    form.addEventListener("submit", handleCreateTask);
});


// ---------------------------------------------------------
// Fetch and display all tasks
// ---------------------------------------------------------
async function loadTasks() {
    const res = await fetch("/tasks");
    const tasks = await res.json();
    renderTasks(tasks);
}


// Render tasks into the task list section
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
// Populate dependency dropdown with existing tasks
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
// Handle Create Task form submission
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

    const taskData = {
        name,
        hours,
        deadline,
        priority,
        dependencies
    };

    const res = await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(taskData)
    });

    const result = await res.json();
    const responseBox = document.getElementById("response");

    if (res.status === 201) {
        responseBox.textContent = "Task created successfully!";
        responseBox.style.color = "green";

        // Refresh UI
        loadTasks();
        populateDependenciesDropdown();

        // Reset form
        document.getElementById("task-form").reset();
    } else {
        responseBox.textContent = result.error || "Error creating task.";
        responseBox.style.color = "red";
    }
}

// create organization and load it
async function createOrganization() {
    const name = document.getElementById("org-name").value.trim();
    const description = document.getElementById("org-description").value.trim();
    const responseEl = document.getElementById("org-response");

    if (!name) {
        responseEl.textContent = "Please enter a name.";
        responseEl.style.color = "red";
        return;
    }

    const res = await fetch("/organization", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });

    const result = await res.json();

    if (res.status === 201) {
        responseEl.textContent = `Organization "${name}" created!`;
        responseEl.style.color = "green";
        loadOrganization();
    } else {
        responseEl.textContent = result.error;
        responseEl.style.color = "red";
    }
}

async function loadOrganization() {
    const res = await fetch("/organization");
    if (!res.ok) return;

    const org = await res.json();

    document.getElementById("org-status").innerHTML = `
        <p><strong>Organization:</strong> ${org.name}</p>
        <p><strong>Description:</strong> ${org.description || "None"}</p>
        <p><strong>Qualities:</strong> ${org.qualities.map(q => q.name).join(", ") || "None"}</p>
        <p><strong>Constraints:</strong> ${org.constraints.map(c => c.name).join(", ") || "None"}</p>
    `;
}

async function addQuality() {
    const name = document.getElementById("quality-name").value.trim();
    const description = document.getElementById("quality-desc").value.trim();

    if (!name) return alert("Please enter a quality name");

    const res = await fetch("/organization/qualities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });

    if (res.ok) {
        document.getElementById("quality-name").value = "";
        document.getElementById("quality-desc").value = "";
        loadOrganization();
    } else {
        const result = await res.json();
        alert(result.error);
    }
}

async function addConstraint() {
    const name = document.getElementById("constraint-name").value.trim();
    const description = document.getElementById("constraint-desc").value.trim();

    if (!name) return alert("Please enter a constraint name");

    const res = await fetch("/organization/constraints", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });

    if (res.ok) {
        document.getElementById("constraint-name").value = "";
        document.getElementById("constraint-desc").value = "";
        loadOrganization();
    } else {
        const result = await res.json();
        alert(result.error);
    }
}