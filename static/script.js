const form = document.querySelector("#recommendation-form");
const interestButtons = document.querySelectorAll(".interest-chip");
const selectedCount = document.querySelector("#selected-count");
const formMessage = document.querySelector("#form-message");
const resetButton = document.querySelector("#reset-button");
const resultsList = document.querySelector("#results-list");
const emptyState = document.querySelector("#empty-state");
const resultsSummary = document.querySelector("#results-summary");

const selectedInterests = new Set();

function updateSelectedCount() {
    const count = selectedInterests.size;
    selectedCount.textContent = count === 1 ? "1 selected" : `${count} selected`;
}

function showMessage(message, type = "error") {
    formMessage.textContent = message;
    formMessage.className = `form-message ${type}`;
}

function clearMessage() {
    formMessage.textContent = "";
    formMessage.className = "form-message";
}

function resetResults() {
    resultsList.innerHTML = "";
    resultsSummary.innerHTML = "";
    resultsSummary.classList.add("hidden");
    emptyState.textContent = "Select a few interests to see your best course matches here.";
    emptyState.classList.remove("hidden");
}

interestButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const interest = button.dataset.interest;

        if (selectedInterests.has(interest)) {
            selectedInterests.delete(interest);
            button.classList.remove("selected");
        } else {
            selectedInterests.add(interest);
            button.classList.add("selected");
        }

        clearMessage();
        updateSelectedCount();
    });
});

function validateForm(formData) {
    if (!formData.name.trim()) {
        return "Please enter your name.";
    }

    if (!formData.username.trim()) {
        return "Please enter your username.";
    }

    if (!formData.age || Number(formData.age) <= 0) {
        return "Please enter a valid age.";
    }

    if (selectedInterests.size === 0) {
        return "Please choose at least one interest.";
    }

    return "";
}

function escapeHtml(text) {
    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function createInterestTags(interests) {
    return interests.map((interest) => `<span>${escapeHtml(interest)}</span>`).join("");
}

function createResultsSummary(user, interests) {
    resultsSummary.innerHTML = `
        <p>Hi ${escapeHtml(user.name)}! Based on your interests, here are your recommended courses.</p>
        <div class="selected-interests-block">
            <span class="summary-label">Your interests</span>
            <div class="selected-interest-tags">
                ${createInterestTags(interests)}
            </div>
        </div>
    `;
    resultsSummary.classList.remove("hidden");
}

function displayRecommendations(recommendations, user, interests) {
    resultsList.innerHTML = "";

    if (recommendations.length === 0) {
        resultsSummary.innerHTML = "";
        resultsSummary.classList.add("hidden");
        emptyState.textContent = "No recommendations found yet. Try choosing different interests.";
        emptyState.classList.remove("hidden");
        return;
    }

    emptyState.classList.add("hidden");
    createResultsSummary(user, interests);

    recommendations.forEach((course) => {
        const card = document.createElement("article");
        card.className = course.is_top_pick ? "course-card top-pick" : "course-card";
        const matchText = course.matching_interests.length === 1
            ? "Matched 1 interest"
            : `Matched ${course.matching_interests.length} interests`;

        card.innerHTML = `
            <div class="card-header">
                <div>
                    <p class="card-label">${course.is_top_pick ? "Best match" : "Good match"}</p>
                    <h3>${escapeHtml(course.course_name)}</h3>
                </div>
                <strong>${course.score_percent}%</strong>
            </div>
            <div class="progress-track" aria-label="Match score">
                <span style="width: ${course.score_percent}%"></span>
            </div>
            <p class="match-count">${matchText}</p>
            <div class="matching-tags">
                ${createInterestTags(course.matching_interests)}
            </div>
        `;

        resultsList.appendChild(card);
    });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearMessage();

    const formData = {
        name: document.querySelector("#name").value,
        username: document.querySelector("#username").value,
        age: document.querySelector("#age").value,
        interests: Array.from(selectedInterests),
    };

    const validationError = validateForm(formData);
    if (validationError) {
        showMessage(validationError);
        return;
    }

    showMessage("Finding your best course matches...", "info");

    try {
        const response = await fetch("/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage(data.errors ? data.errors.join(" ") : "Something went wrong.");
            return;
        }

        displayRecommendations(data.recommendations, data.user, formData.interests);
        clearMessage();
    } catch (error) {
        showMessage("Could not reach the Python backend. Make sure Flask is running.");
    }
});

resetButton.addEventListener("click", () => {
    form.reset();
    selectedInterests.clear();
    interestButtons.forEach((button) => button.classList.remove("selected"));
    updateSelectedCount();
    clearMessage();
    resetResults();
});
