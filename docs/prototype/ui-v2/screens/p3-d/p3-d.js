// Prototype-only interactions for P3-D. No network, POST, persistence, or domain rules.
(() => {
  const root = document.documentElement;
  const state = root.dataset.argosPrototypeState || "default";
  const fixture = root.dataset.argosPrototypeFixture || "default";
  const setHidden = (element, hidden) => {
    element.hidden = hidden;
  };

  document.querySelectorAll("[data-argos-state-variant]").forEach((element) => {
    setHidden(element, element.dataset.argosStateVariant !== state);
  });

  document.querySelectorAll("[data-fixture-default][data-fixture-long]").forEach((element) => {
    const value = element.dataset[`fixture${fixture === "long" ? "Long" : "Default"}`];
    if ("value" in element) element.value = value;
    else element.textContent = value;
  });

  document.querySelectorAll("[data-invalid-in-error]").forEach((element) => {
    if (state === "error") {
      element.setAttribute("aria-invalid", "true");
      if ("value" in element) element.value = "";
    } else element.removeAttribute("aria-invalid");
  });

  if (state === "error") {
    document.querySelectorAll("[data-error-select]").forEach((select) => {
      select.value = "__PERSONALIZADO__";
    });
  }

  const syncConditional = (select, focusOnReveal = false) => {
    const target = document.getElementById(select.dataset.conditionalTarget);
    if (!target) return;
    const visible = select.value === "__PERSONALIZADO__";
    setHidden(target, !visible);
    const input = target.querySelector("input");
    if (input) input.required = visible;
    if (visible && focusOnReveal) target.querySelector("input")?.focus();
  };

  document.querySelectorAll("[data-conditional-target]").forEach((select) => {
    syncConditional(select);
    select.addEventListener("change", () => syncConditional(select, true));
  });

  document.querySelectorAll("[data-demo-submit]").forEach((button) => {
    button.addEventListener("click", () => {
      const feedback = document.getElementById(button.dataset.demoSubmit);
      if (!feedback) return;
      setHidden(feedback, false);
      feedback.textContent = button.dataset.demoMessage || "Prévia de sucesso: nenhuma alteração foi persistida.";
      feedback.focus();
    });
  });

  if (state === "focus") {
    document.querySelector("[data-focus-target]")?.focus({ preventScroll: true });
  }
})();
