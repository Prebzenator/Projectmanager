// -------------------------------
// Load on page load
// -------------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
    loadQualitiesAndConstraints(); // NEW: fill quality/constraint dropdowns
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

        if (tasks.length === 0) {
            taskListDiv.innerHTML = "<p>No tasks yet.</p>";
        }

        tasks.forEach(task => {
            const div = document.createElement("div");
            div.className = "task-item";
            div.innerHTML = `
                <strong>${task.name}</strong><br>
                Hours: ${task.hours}<br>
                Deadline: ${task.deadline}<br>
                Priority: ${task.priority}<br>
                Required Qualities: ${task.required_qualities.join(", ") || "None"}<br>
                Required Constraints: ${task.required_constraints.join(", ") || "None"}<br>
                Dependencies: ${task.dependency_names.join(", ") || "None"}
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
// NEW: Load qualities and constraints from the org
// and populate the two dropdowns in the task form
// -------------------------------
async function loadQualitiesAndConstraints() {
    try {
        // Qualities
        const qualRes = await fetch("/qualities");
        const qualities = await qualRes.json();

        const qualSelect = document.getElementById("task-qualities");
        qualSelect.innerHTML = "";

        if (qualities.length === 0) {
            qualSelect.innerHTML = "<option disabled>No qualities added yet</option>";
        } else {
            qualities.forEach(q => {
                const option = document.createElement("option");
                option.value = q.name;
                option.textContent = q.name;
                qualSelect.appendChild(option);
            });
        }

        // Constraints
        const conRes = await fetch("/constraints");
        const constraints = await conRes.json();

        const conSelect = document.getElementById("task-constraints");
        conSelect.innerHTML = "";

        if (constraints.length === 0) {
            conSelect.innerHTML = "<option disabled>No constraints added yet</option>";
        } else {
            constraints.forEach(c => {
                const option = document.createElement("option");
                option.value = c.name;
                option.textContent = c.name;
                conSelect.appendChild(option);
            });
        }

    } catch (err) {
        console.error("Failed to load qualities/constraints:", err);
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

        // Dependencies
        const dependenciesSelect = document.getElementById("task-dependencies");
        const dependencies = Array.from(dependenciesSelect.selectedOptions).map(opt => opt.value);

        // NEW: selected qualities and constraints
        const qualSelect = document.getElementById("task-qualities");
        const required_qualities = Array.from(qualSelect.selectedOptions).map(opt => opt.value);

        const conSelect = document.getElementById("task-constraints");
        const required_constraints = Array.from(conSelect.selectedOptions).map(opt => opt.value);

        const payload = {
            name,
            hours,
            deadline,
            priority,
            dependencies,
            required_qualities,     // NEW
            required_constraints    // NEW
        };

        try {
            const res = await fetch("/tasks", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            responseP.textContent = data.message || "Task created.";

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