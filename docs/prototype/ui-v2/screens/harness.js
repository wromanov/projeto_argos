// DESIGN_SYSTEM_VERSION = 2.2.0; OWNER = ROOT.
// PROTOTYPE_ONLY: resolve deterministic UI variants; no domain or network behavior.
(() => {
  const states = new Set(["default", "empty", "loading", "error"]);
  const fixtures = new Set(["default", "long"]);
  const query = new URLSearchParams(window.location.search);
  const requestedState = query.get("state");
  const requestedFixture = query.get("fixture");
  const state = states.has(requestedState) ? requestedState : "default";
  const fixture = fixtures.has(requestedFixture) ? requestedFixture : "default";

  document.documentElement.dataset.argosPrototypeState = state;
  document.documentElement.dataset.argosPrototypeFixture = fixture;

  document.querySelectorAll("[data-argos-state-variant]").forEach((variant) => {
    variant.hidden = variant.dataset.argosStateVariant !== state;
  });
  document.querySelectorAll("[data-argos-fixture-variant]").forEach((variant) => {
    variant.hidden = variant.dataset.argosFixtureVariant !== fixture;
  });
})();
