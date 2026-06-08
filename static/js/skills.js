// Skills UI: user profiles (variant 2) and projects (variant 3)
(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("skills-container");
    if (!container) return;

    const userId = container.dataset.userId;
    const projectId = container.dataset.projectId;
    const isUserProfile = Boolean(userId);

    const addBtn = document.getElementById("add-skill-btn");
    const inputWrapper = document.getElementById("skill-input-wrapper");
    const input = document.getElementById("skill-input");
    const suggestions = document.getElementById("skill-suggestions");

    if (!addBtn || !inputWrapper || !input || !suggestions) return;

    const autocompleteUrl = isUserProfile ? "/users/skills/" : "/projects/skills/";
    const addUrl = isUserProfile
      ? `/users/${userId}/skills/add/`
      : `/projects/${projectId}/skills/add/`;
    const removeUrl = (skillId) =>
      isUserProfile
        ? `/users/${userId}/skills/${skillId}/remove/`
        : `/projects/${projectId}/skills/${skillId}/remove/`;

    addBtn.addEventListener("click", () => {
      addBtn.classList.add("hidden");
      inputWrapper.classList.remove("hidden");
      input.value = "";
      suggestions.innerHTML = "";
      suggestions.classList.add("hidden");
      input.focus();
    });

    let debounceTimer = null;
    input.addEventListener("input", () => {
      const query = input.value.trim();
      clearTimeout(debounceTimer);

      if (query.length < 2) {
        suggestions.classList.add("hidden");
        suggestions.innerHTML = "";
        return;
      }

      debounceTimer = setTimeout(async () => {
        const response = await fetch(
          `${autocompleteUrl}?q=${encodeURIComponent(query)}`
        );
        if (!response.ok) return;

        const data = await response.json();
        suggestions.innerHTML = "";

        data.forEach((skill) => {
          const item = document.createElement("li");
          item.textContent = skill.name;
          item.dataset.id = skill.id;
          item.className = "suggestion-item";
          suggestions.appendChild(item);
        });

        const hasExactMatch = data.some(
          (skill) => skill.name.toLowerCase() === query.toLowerCase()
        );
        if (!hasExactMatch) {
          const createItem = document.createElement("li");
          createItem.textContent = `Создать «${query}»`;
          createItem.dataset.name = query;
          createItem.className = "create-new";
          suggestions.appendChild(createItem);
        }

        suggestions.classList.remove("hidden");
      }, 200);
    });

    suggestions.addEventListener("mousedown", async (event) => {
      const item = event.target.closest("li");
      if (!item) return;

      if (item.classList.contains("create-new")) {
        await addSkillByName(item.dataset.name);
      } else if (item.dataset.id) {
        await addSkillById(item.dataset.id, item.textContent);
      }
      hideInput();
    });

    input.addEventListener("keydown", async (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        const query = input.value.trim();
        if (!query) return;

        const firstItem = suggestions.querySelector("li");
        if (firstItem && firstItem.dataset.id) {
          await addSkillById(firstItem.dataset.id, firstItem.textContent);
        } else {
          await addSkillByName(query);
        }
        hideInput();
      }
      if (event.key === "Escape") {
        hideInput();
      }
    });

    input.addEventListener("blur", () => setTimeout(hideInput, 120));

    function hideInput() {
      inputWrapper.classList.add("hidden");
      suggestions.classList.add("hidden");
      addBtn.classList.remove("hidden");
    }

    container.addEventListener("click", async (event) => {
      if (!event.target.classList.contains("remove-skill-btn")) return;

      const chip = event.target.closest(".skill-chip");
      const skillId = chip.dataset.id;
      const response = await fetch(removeUrl(skillId), {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
      });

      if (response.ok) {
        chip.remove();
        showEmptyStateIfNeeded();
      }
    });

    async function addSkillById(skillId, skillName) {
      const response = await fetch(addUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ skill_id: skillId }),
      });

      if (!response.ok) return;

      const data = await response.json();
      if (data.added === false) return;

      appendChip(data.id || data.skill_id, data.name || skillName);
    }

    async function addSkillByName(name) {
      const response = await fetch(addUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ name }),
      });

      if (!response.ok) return;

      const data = await response.json();
      if (data.added === false) return;

      appendChip(data.id || data.skill_id, data.name || name);
    }

    function appendChip(id, name) {
      if (container.querySelector(`.skill-chip[data-id="${id}"]`)) return;

      const chip = document.createElement("span");
      chip.className = "skill-chip";
      chip.dataset.id = id;
      chip.innerHTML = `${name} <button type="button" class="remove-skill-btn" aria-label="Удалить" title="Удалить">×</button>`;

      container.insertBefore(chip, addBtn);

      const empty = container.querySelector(".skill-empty");
      if (empty) empty.remove();
    }

    function showEmptyStateIfNeeded() {
      if (container.querySelector(".skill-chip")) return;
      if (container.querySelector(".skill-empty")) return;

      const empty = document.createElement("p");
      empty.className = "skill-empty no-skills";
      empty.textContent = "Навыки не добавлены";
      container.insertBefore(empty, addBtn);
    }

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
})();
