// Load tasks when the page loads
document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
    populateDependenciesDropdown();

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
