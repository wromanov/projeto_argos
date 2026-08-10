(() => {
  "use strict";

  const selector = "[data-filter-multiselect]";

  function updateSummary(details) {
    const summaryText = details.querySelector(
      "[data-filter-summary-text]"
    );

    if (!summaryText) {
      return;
    }

    const inputs = details.querySelectorAll(
      'input[type="checkbox"]'
    );

    const selectedCount = Array.from(inputs).filter(
      (input) => input.checked
    ).length;

    const emptyLabel =
      summaryText.dataset.emptyLabel || "Todos";

    if (selectedCount === 0) {
      summaryText.textContent = emptyLabel;
      return;
    }

    summaryText.textContent =
      selectedCount === 1
        ? "1 sele\u00e7\u00e3o"
        : `${selectedCount} sele\u00e7\u00f5es`;
  }

  function initializeMultiselect(details, allDetails) {
    updateSummary(details);

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
