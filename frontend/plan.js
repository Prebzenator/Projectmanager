document.addEventListener("DOMContentLoaded", () => {
    renderPlan();
});

function renderPlan() {
    const container = document.getElementById("timeline-container");
    const info = document.getElementById("plan-info");

    const raw = localStorage.getItem("generatedPlan");

    if (!raw) {
        container.innerHTML = "<p>No plan found. Generate a plan first.</p>";
        return;
    }

    const plan = JSON.parse(raw);

    if (!Array.isArray(plan) || plan.length === 0) {
        container.innerHTML = "<p>The plan is empty — add tasks first.</p>";
        return;
    }

    // Total hours = end time of last task
    const totalHours = plan[plan.length - 1].end;
    info.textContent = `${plan.length} tasks · Total: ${totalHours} hours`;

    // Header markers
    const header = document.createElement("div");
    header.className = "timeline-header";

    const markerCount = 5;
    for (let i = 0; i <= markerCount; i++) {
        const hours = Math.round((totalHours / markerCount) * i);
        const marker = document.createElement("span");
        marker.className = "hour-marker";
        marker.style.left = `${(i / markerCount) * 100}%`;
        marker.textContent = `${hours}h`;
        header.appendChild(marker);
    }

    container.appendChild(header);

    // Rows
    const colors = ["color-1", "color-2", "color-3", "color-4", "color-5"];

    plan.forEach((item, index) => {
        const row = document.createElement("div");
        row.className = "timeline-row";

        const label = document.createElement("div");
        label.className = "task-label";
        label.textContent = item.task_name;

        const track = document.createElement("div");
        track.className = "task-track";

        const leftPercent = (item.start / totalHours) * 100;
        const widthPercent = ((item.end - item.start) / totalHours) * 100;

        const bar = document.createElement("div");
        bar.className = `task-bar ${colors[index % colors.length]}`;
        bar.style.left = `${leftPercent}%`;
        bar.style.width = `${widthPercent}%`;
        bar.textContent = `${item.start}h – ${item.end}h`;

        track.appendChild(bar);
        row.appendChild(label);
        row.appendChild(track);
        container.appendChild(row);
    });
}
