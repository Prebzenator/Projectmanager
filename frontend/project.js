// -------------------------------
// Load tasks on page load
// -------------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
    setupCreateTaskForm();
    setupGeneratePlanButton();
});


// -------------------------------
// Fetch and display tasks
// -------------------------------
async function loadTasks() {
    const taskListDiv = document.getElementById("task-list");
    const dependenciesSelect = document.getElementById("task-dependencies");

    taskListDiv.innerHTML = "Loading tasks...";

    try {
        const res = await fetch("/tasks");
        const tasks = await res.json();

        // Display tasks
        taskListDiv.innerHTML = "";
        tasks.forEach(task => {
            const div = document.createElement("div");
            div.className = "task-item";
            div.innerHTML = `
                <strong>${task.name}</strong><br>
                Hours: ${task.hours}<br>
                Deadline: ${task.deadline}<br>
                Priority: ${task.priority}<br>
                Dependencies: ${task.dependencies.join(", ") || "None"}
            `;
            taskListDiv.appendChild(div);
        });

        // Populate dependencies dropdown
        dependenciesSelect.innerHTML = "";
        tasks.forEach(task => {
            const option = document.createElement("option");
            option.value = task.id;
            option.textContent = task.name;
            dependenciesSelect.appendChild(option);
        });

    } catch (err) {
        taskListDiv.innerHTML = "Failed to load tasks.";
        console.error(err);
    }
}


// -------------------------------
// Create Task
// -------------------------------
function setupCreateTaskForm() {
    const form = document.getElementById("task-form");
    const responseP = document.getElementById("task-response");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("task-name").value;
        const hours = parseInt(document.getElementById("task-hours").value);
        const deadline = document.getElementById("task-deadline").value;
        const priority = parseInt(document.getElementById("task-priority").value);

        const dependenciesSelect = document.getElementById("task-dependencies");
        const dependencies = Array.from(dependenciesSelect.selectedOptions).map(opt => opt.value);

        const payload = {
            name,
            hours,
            deadline,
            priority,
            dependencies
        };

        try {
            const res = await fetch("/tasks", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            responseP.textContent = data.message || "Task created.";

            // Reload tasks
            loadTasks();
            form.reset();

        } catch (err) {
            responseP.textContent = "Failed to create task.";
            console.error(err);
        }
    });
}


// -------------------------------
// Generate Plan
// -------------------------------
function setupGeneratePlanButton() {
    const btn = document.getElementById("generate-plan-btn");
    const responseP = document.getElementById("plan-response");

    btn.addEventListener("click", async () => {
        const mode = document.getElementById("plan-mode").value;

        try {
            const res = await fetch("/generate_plan", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mode })
            });

            const data = await res.json();

            if (data.plan) {
                // Save plan so plan.html can read it
                localStorage.setItem("generatedPlan", JSON.stringify(data.plan));
            }

            responseP.textContent = data.message || "Plan generated.";

        } catch (err) {
            responseP.textContent = "Failed to generate plan.";
            console.error(err);
        }
    });
}
