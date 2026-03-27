document.addEventListener("DOMContentLoaded", () => {
    checkOrganization();
    document.getElementById("organization-form")
        .addEventListener("submit", handleCreateOrganization);
});

// Check if organization exists
async function checkOrganization() {
    const section = document.getElementById("organization-entry");
    const card = document.getElementById("org-card");

    try {
        const res = await fetch("/organization");

        if (!res.ok) {
            section.style.display = "none";
            return;
        }

        const org = await res.json();
        section.style.display = "block";

        card.innerHTML = `
            <div class="organization-card">
                <h3>${org.name}</h3>
                <p>${org.description || "No description"}</p>
            </div>
        `;

        document.getElementById("open-org-btn").onclick = () => {
            window.location.href = "organization.html";
        };

    } catch (err) {
        console.error("Failed to load organization:", err);
    }
}

// Create organization
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
        checkOrganization();
    } else {
        box.textContent = result.error;
        box.style.color = "red";
    }
}
