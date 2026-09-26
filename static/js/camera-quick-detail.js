"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const dialog = document.querySelector("[data-quick-detail-dialog]");
  if (!dialog) return;
  const closeButton = dialog.querySelector("[data-quick-detail-close]");
  const message = dialog.querySelector("[data-quick-detail-message]");
  const content = dialog.querySelector("[data-quick-detail-content]");
  const image = dialog.querySelector("[data-quick-detail-image]");
  const imageState = dialog.querySelector("[data-quick-detail-image-state]");
  const imageFrame = dialog.querySelector("[data-quick-detail-image-frame]");
  const imagePlaceholder = dialog.querySelector("[data-quick-detail-image-placeholder]");
  const imageTitle = dialog.querySelector("[data-quick-detail-image-title]");
  const footer = dialog.querySelector("[data-quick-detail-footer]");
  const editLink = dialog.querySelector("[data-quick-detail-edit-link]");
  const headerSubtitle = dialog.querySelector("[data-quick-detail-header-subtitle]");
  const rows = Array.from(document.querySelectorAll("[data-quick-detail-row]"));
  const previousButton = dialog.querySelector("[data-quick-detail-previous]");
  const nextButton = dialog.querySelector("[data-quick-detail-next]");
  let controller = null;
  let requestId = 0;
  let selectedRow = null;
  let opener = null;

  const value = (item) => item === null || item === undefined || item === "" ? "—" : String(item);
  const date = (item) => {
    if (!item) return "—";
    const parsed = new Date(item);
    return Number.isNaN(parsed.getTime()) ? "—" : new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(parsed);
  };
  const statusLabels = { ONLINE: "Online", OFFLINE: "Offline", UNKNOWN: "Desconhecido", OUT_OF_SCOPE: "Não monitorada" };
  const imageLabels = {
    NO_IMAGE_AVAILABLE: "Nenhuma imagem disponível",
    UNAVAILABLE: "Imagem indisponível",
    ERROR: "Erro na imagem registrada"
  };

  function clearSelection() {
    if (selectedRow) selectedRow.classList.remove("camera-row--selected");
    selectedRow = null;
  }

  function close() {
    requestId += 1;
    if (controller) controller.abort();
    controller = null;
    image.removeAttribute("src");
    image.hidden = true;
    clearSelection();
    if (dialog.open) dialog.close();
    if (opener && opener.isConnected) opener.focus({ preventScroll: true });
    opener = null;
  }

  function render(data) {
    dialog.querySelectorAll("[data-quick-detail-value]").forEach((node) => {
      const [group, field] = node.dataset.quickDetailValue.split(".");
      node.textContent = value(data[group]?.[field]);
    });
    const state = data.monitoring.state;
    headerSubtitle.textContent = [value(data.camera.patrimonio), value(data.camera.nome)].filter((part) => part !== "—").join(" · ") || "Inventário de câmeras";
    const badge = dialog.querySelector("[data-quick-detail-status]");
    badge.textContent = statusLabels[state] || "Desconhecido";
    badge.className = `badge badge--${["ONLINE", "OFFLINE", "UNKNOWN", "OUT_OF_SCOPE"].includes(state) ? state.toLowerCase() : "unknown"}`;
    dialog.querySelector('[data-quick-detail-monitoring="state"]').textContent = badge.textContent;
    dialog.querySelector('[data-quick-detail-monitoring="evidence"]').textContent = date(data.monitoring.evidence_at);
    dialog.querySelector('[data-quick-detail-monitoring="freshness"]').textContent = data.monitoring.freshness === "stale" ? "Dados desatualizados" : `Evidência: ${date(data.monitoring.evidence_at)}`;
    dialog.querySelector("[data-quick-detail-full-link]").href = data.links.full_detail_url;
    if (editLink) editLink.href = selectedRow.dataset.quickDetailEditUrl;
    content.hidden = false;
    footer.hidden = false;
    message.hidden = true;
    image.hidden = true;
    imagePlaceholder.hidden = false;
    imageFrame.dataset.imageState = data.image.state.toLowerCase();
    const sourceLabel = data.image.source === "CAPTURA_CAMERA" ? "Última captura registrada" :
      data.image.source === "UPLOAD_MANUAL" ? "Imagem enviada manualmente" : "Nenhuma imagem disponível";
    imageTitle.textContent = sourceLabel;
    image.alt = sourceLabel === "Nenhuma imagem disponível" ? "" : `${sourceLabel} da câmera`;
    image.removeAttribute("src");
    if (data.image.state === "AVAILABLE" && data.image.preview_url) {
      imageState.textContent = "Carregando imagem…";
      imageFrame.dataset.imageState = "loading";
      image.src = data.image.preview_url;
    } else {
      imageState.textContent = imageLabels[data.image.state] || "Imagem indisponível";
    }
  }

  async function open(row, trigger) {
    if (controller) controller.abort();
    requestId += 1;
    const identity = requestId;
    controller = new AbortController();
    if (!dialog.open) {
      opener = trigger;
      dialog.showModal();
    }
    clearSelection();
    selectedRow = row;
    row.classList.add("camera-row--selected");
    const rowIndex = rows.indexOf(row);
    previousButton.disabled = rowIndex <= 0;
    nextButton.disabled = rowIndex >= rows.length - 1;
    content.hidden = true;
    footer.hidden = true;
    headerSubtitle.textContent = "Inventário de câmeras";
    message.hidden = false;
    message.textContent = "Carregando detalhes…";
    image.hidden = true;
    image.removeAttribute("src");
    closeButton.focus({ preventScroll: true });
    try {
      const response = await fetch(row.dataset.quickDetailUrl, {
        credentials: "same-origin", headers: { Accept: "application/json" }, signal: controller.signal
      });
      if (identity !== requestId || selectedRow !== row || !dialog.open) return;
      if (!response.ok) {
        message.textContent = response.status === 404 ? "Câmera não encontrada." :
          response.status === 401 || response.status === 403 ? "Acesso não autorizado." : "Erro ao carregar os detalhes.";
        return;
      }
      const data = await response.json();
      if (identity !== requestId || selectedRow !== row || !dialog.open) return;
      render(data);
    } catch (error) {
      if (identity !== requestId || error.name === "AbortError") return;
      message.textContent = "Falha de rede ao carregar os detalhes.";
    }
  }

  rows.forEach((row) => {
    const trigger = row.querySelector("[data-quick-detail-trigger]");
    trigger.addEventListener("click", () => open(row, trigger));
    row.addEventListener("click", (event) => {
      if (event.target.closest("a, button, input, select, textarea, summary")) return;
      open(row, trigger);
    });
  });
  closeButton.addEventListener("click", close);
  previousButton.addEventListener("click", () => { const index = rows.indexOf(selectedRow); if (index > 0) open(rows[index - 1], opener); });
  nextButton.addEventListener("click", () => { const index = rows.indexOf(selectedRow); if (index >= 0 && index < rows.length - 1) open(rows[index + 1], opener); });
  dialog.addEventListener("cancel", (event) => { event.preventDefault(); close(); });
  dialog.addEventListener("close", () => { if (opener) close(); });
  dialog.addEventListener("click", (event) => { if (event.target === dialog) close(); });
  image.addEventListener("load", () => { if (dialog.open && !content.hidden) { image.hidden = false; imagePlaceholder.hidden = true; imageFrame.dataset.imageState = "available"; imageState.textContent = ""; } });
  image.addEventListener("error", () => { image.hidden = true; imagePlaceholder.hidden = false; imageFrame.dataset.imageState = "unavailable"; imageState.textContent = "Imagem indisponível"; });
});
