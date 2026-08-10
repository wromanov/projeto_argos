(() => {
  "use strict";

  const selector = "[data-filter-multiselect]";

  function selectedInputs(details) {
    return Array.from(
      details.querySelectorAll('input[type="checkbox"]')
    ).filter((input) => input.checked);
  }

  function optionLabel(input) {
    const option = input.closest(".filter-multiselect__option");
    const label = option ? option.querySelector("span") : null;
    return label ? label.textContent.trim() : input.value;
  }

  function updateSummary(details) {
    const summaryText = details.querySelector(
      "[data-filter-summary-text]"
    );

    if (!summaryText) {
      return;
    }

    const selected = selectedInputs(details);
    const emptyLabel = summaryText.dataset.emptyLabel || "Todos";

    if (selected.length === 0) {
      summaryText.textContent = emptyLabel;
      return;
    }

    if (selected.length === 1) {
      summaryText.textContent = optionLabel(selected[0]);
      return;
    }

    summaryText.textContent = `${selected.length} seleções`;
  }

  function initializeMultiselect(details, allDetails) {

    details.addEventListener("change", (event) => {
      if (event.target.matches('input[type="checkbox"]')) {
        updateSummary(details);
      }
    });

    details.addEventListener("toggle", () => {
      if (!details.open) {
        return;
      }

      allDetails.forEach((other) => {
        if (other !== details) {
          other.open = false;
        }
      });
    });

    details.addEventListener("keydown", (event) => {
      if (event.key !== "Escape" || !details.open) {
        return;
      }

      details.open = false;

      const summary = details.querySelector("summary");
      if (summary) {
        summary.focus();
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    const allDetails = Array.from(
      document.querySelectorAll(selector)
    );

    allDetails.forEach((details) => {
      initializeMultiselect(details, allDetails);
    });

    document.addEventListener("click", (event) => {
      allDetails.forEach((details) => {
        if (
          details.open &&
          !details.contains(event.target)
        ) {
          details.open = false;
        }
      });
    });
  });
})();
