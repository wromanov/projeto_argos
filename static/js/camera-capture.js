(() => {
  "use strict";

  const panel = document.querySelector("[data-camera-capture]");
  if (!panel) return;

  const feedback = panel.querySelector("[data-capture-feedback]");
  const jobId = panel.dataset.jobId;
  const initialState = panel.dataset.jobState;
  if (!jobId || !["QUEUED", "RUNNING"].includes(initialState)) return;

  const statusUrl = panel.dataset.statusUrl.replace(
    "00000000-0000-0000-0000-000000000000",
    encodeURIComponent(jobId),
  );
  const messages = {
    QUEUED: "Captura solicitada; aguardando processamento.",
    RUNNING: "Captura em processamento.",
    SUCCEEDED: "Captura concluída.",
    FAILED: "Não foi possível concluir a captura. Tente novamente mais tarde.",
    CANCELLED: "Captura cancelada.",
  };
  let timer = null;
  let inFlight = false;
  let stopped = false;

  const stop = () => {
    stopped = true;
    if (timer !== null) window.clearTimeout(timer);
    timer = null;
  };

  const poll = async () => {
    if (stopped || inFlight) return;
    inFlight = true;
    try {
      const response = await fetch(statusUrl, {
        method: "GET",
        credentials: "same-origin",
        headers: { Accept: "application/json" },
        cache: "no-store",
      });
      if (!response.ok) {
        stop();
        return;
      }
      const result = await response.json();
      const state = typeof result.state === "string" ? result.state : "";
      if (feedback && messages[state] && feedback.textContent.trim() !== messages[state]) {
        feedback.textContent = messages[state];
      }
      if (result.terminal || ["SUCCEEDED", "FAILED", "CANCELLED"].includes(state)) {
        stop();
        return;
      }
    } catch (_) {
      // Uma falha transitória de rede mantém o estado SSR e permite nova consulta.
    } finally {
      inFlight = false;
      if (!stopped) timer = window.setTimeout(poll, 2000);
    }
  };

  window.addEventListener("beforeunload", stop, { once: true });
  timer = window.setTimeout(poll, 2000);
})();
