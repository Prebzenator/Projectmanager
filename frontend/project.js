// PROJECT_ID kommer fra project.html
const PROJECT_ID = window.PROJECT_ID;

document.addEventListener("DOMContentLoaded", () => {
    loadTasks();
    loadQualitiesAndConstraints();
    setupCreateTaskForm();
    setupGeneratePlanButton();

    document.getElementById("view-plan-btn").onclick = () => {
        window.location.href = "plan.html";
    };
});


// ------------------------------
// Load tasks
// ------------------------------
async function loadTasks() {
    const container = document.getElementById("task-list");
    const depSelect = document.getElementById("task-dependencies");

    container.innerHTML = "Loading tasks...";

    try {
        const res = await fetch(`/projects/${PROJECT_ID}/tasks`);
        const tasks = await res.json();

        container.innerHTML = "";
        depSelect.innerHTML = "";

        if (!Array.isArray(tasks) || tasks.length === 0) {
            container.innerHTML = "<p>No tasks yet.</p>";
            return;
        }

        tasks.forEach(task => {
            const card = document.createElement("div");
            card.className = "card";

            card.innerHTML = `
                <strong>${task.name}</strong><br>
                Hours: ${task.hours}<br>
                Deadline: ${task.deadline}<br>
                Priority: ${task.priority}<br>
                Required Qualities: ${task.required_qualities?.join(", ") || "None"}<br>
                Required Constraints: ${task.required_constraints?.join(", ") || "None"}<br>
                Dependencies: ${task.dependency_names?.join(", ") || "None"}
            `;

            container.appendChild(card);

            const opt = document.createElement("option");
            opt.value = task.id;
            opt.textContent = task.name;
            depSelect.appendChild(opt);
        });

    } catch (err) {
        container.innerHTML = "Failed to load tasks.";
        console.error(err);
    }
}


// ------------------------------
// Load qualities + constraints
// ------------------------------
async function loadQualitiesAndConstraints() {
    try {
        const qRes = await fetch("/qualities");
        const qualities = await qRes.json();

        const qSelect = document.getElementById("task-qualities");
        qSelect.innerHTML = "";

        qualities.forEach(q => {
            const opt = document.createElement("option");
            opt.value = q.name;
            opt.textContent = q.name;
            qSelect.appendChild(opt);
        });

        const cRes = await fetch("/constraints");
        const constraints = await cRes.json();

        const cSelect = document.getElementById("task-constraints");
        cSelect.innerHTML = "";

        constraints.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c.name;
            opt.textContent = c.name;
            cSelect.appendChild(opt);
        });

    } catch (err) {
        console.error("Failed to load qualities/constraints:", err);
    }
}


// ------------------------------
// Create task
// ------------------------------
function setupCreateTaskForm() {
    const form = document.getElementById("task-form");
    const response = document.getElementById("task-response");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            name: document.getElementById("task-name").value,
            hours: parseInt(document.getElementById("task-hours").value),
            deadline: document.getElementById("task-deadline").value,
            priority: parseInt(document.getElementById("task-priority").value),
            dependencies: Array.from(document.getElementById("task-dependencies").selectedOptions).map(o => o.value),
            required_qualities: Array.from(document.getElementById("task-qualities").selectedOptions).map(o => o.value),
            required_constraints: Array.from(document.getElementById("task-constraints").selectedOptions).map(o => o.value)
        };

        try {
            const res = await fetch(`/projects/${PROJECT_ID}/tasks`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            response.textContent = data.message || "Task created.";

            form.reset();
            loadTasks();

        } catch (err) {
            response.textContent = "Failed to create task.";
            console.error(err);
        }
    });
}


// ------------------------------
// Generate plan
// ------------------------------
function setupGeneratePlanButton() {
    const btn = document.getElementById("generate-plan-btn");
    const response = document.getElementById("plan-response");

    btn.addEventListener("click", async () => {
        const mode = document.getElementById("plan-mode").value;

        try {
            const res = await fetch(`/projects/${PROJECT_ID}/generate_plan`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mode })
            });

            const data = await res.json();

            if (data.plan) {
                localStorage.setItem("generatedPlan", JSON.stringify(data.plan));
            }

            response.textContent = data.message || "Plan generated.";

        } catch (err) {
            response.textContent = "Failed to generate plan.";
            console.error(err);
        }
    });
}
