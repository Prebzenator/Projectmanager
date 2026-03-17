document.addEventListener("DOMContentLoaded", () => {
    renderPlan();
});


function renderPlan() {
    const container = document.getElementById("timeline-container");
    const info = document.getElementById("plan-info");

    // Read the plan saved by project.js when "Generate Plan" was clicked
    const raw = localStorage.getItem("generatedPlan");

    if (!raw) {
        container.innerHTML = "<p>No plan found. Go back and generate one first.</p>";
        return;
    }

    const plan = JSON.parse(raw);

    if (plan.length === 0) {
        container.innerHTML = "<p>The plan is empty — add some tasks first.</p>";
        return;
    }

    // Find the total duration so we can scale all bars to percentages
    const totalHours = plan[plan.length - 1].end;

    info.textContent = `${plan.length} task${plan.length > 1 ? "s" : ""} · Total: ${totalHours} hours`;

    // Draw hour markers across the top
    const header = document.createElement("div");
    header.className = "timeline-header";

    const markerCount = 5; // show 5 evenly spaced hour markers
    for (let i = 0; i <= markerCount; i++) {
        const hours = Math.round((totalHours / markerCount) * i);
        const marker = document.createElement("span");
        marker.className = "hour-marker";
        marker.style.left = `${(i / markerCount) * 100}%`;
        marker.textContent = `${hours}h`;
        header.appendChild(marker);
    }

    container.appendChild(header);

    // Draw one row per task
    const colors = ["color-1", "color-2", "color-3", "color-4", "color-5"];

    plan.forEach((item, index) => {
        const row = document.createElement("div");
        row.className = "timeline-row";

        // Left label
        const label = document.createElement("div");
        label.className = "task-label";
        label.textContent = item.task_name;
        label.title = item.task_name; // tooltip for long names

        // Track (grey background)
        const track = document.createElement("div");
        track.className = "task-track";

        // Calculate the bar's left offset and width as percentages
        const leftPercent = (item.start / totalHours) * 100;
        const widthPercent = ((item.end - item.start) / totalHours) * 100;

        // Coloured bar
        const bar = document.createElement("div");
        bar.className = `task-bar ${colors[index % colors.length]}`;
        bar.style.left = `${leftPercent}%`;
        bar.style.width = `${widthPercent}%`;
        bar.textContent = `${item.start}h – ${item.end}h`;
        bar.title = `${item.task_name}: ${item.start}h to ${item.end}h`;

        track.appendChild(bar);
        row.appendChild(label);
        row.appendChild(track);
        container.appendChild(row);
    });
}