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
  const imageRecordedAt = dialog.querySelector("[data-quick-detail-image-recorded-at]");
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
  let documentScrollLock = null;

  const value = (item) => item === null || item === undefined || item === "" ? "—" : String(item);
  const date = (item) => {
    if (!item) return "—";
    const parsed = new Date(item);
    return Number.isNaN(parsed.getTime()) ? "—" : new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(parsed);
  };
  const statusLabelsElement = document.getElementById("monitoring-state-labels");
  const statusLabels = (statusLabelsElement ? JSON.parse(statusLabelsElement.textContent) : null) || {};
  const imageLabels = {
    NO_IMAGE_AVAILABLE: "Nenhuma imagem disponível",
    UNAVAILABLE: "Imagem temporariamente indisponível",
    ERROR: "Não foi possível exibir a imagem"
  };
  const imageSourceLabels = {
    CAPTURA_CAMERA: "Imagem capturada pela câmera",
    UPLOAD_MANUAL: "Imagem enviada manualmente"
  };

  function imageTimestamp(item) {
    if (!item) return "";
    const parsed = new Date(item);
    if (Number.isNaN(parsed.getTime())) return "";
    const parts = new Intl.DateTimeFormat("pt-BR", {
      timeZone: "America/Sao_Paulo", day: "2-digit", month: "2-digit",
      year: "numeric", hour: "2-digit", minute: "2-digit", hourCycle: "h23"
    }).formatToParts(parsed).reduce((result, part) => {
      result[part.type] = part.value;
      return result;
    }, {});
    return `Registrada em ${parts.day}/${parts.month}/${parts.year} às ${parts.hour}:${parts.minute}`;
  }

  function clearSelection() {
    if (selectedRow) selectedRow.classList.remove("camera-row--selected");
    selectedRow = null;
  }

  function acquireDocumentScrollLock() {
    const element = document.scrollingElement;
    if (!element || documentScrollLock) return;

    const computedOverflowY = window.getComputedStyle(element).overflowY;
    if (computedOverflowY === "hidden" || computedOverflowY === "clip") return;

    const style = element.style;
    const computedScrollbarGutter = window.getComputedStyle(element).scrollbarGutter;
    const reserveScrollbarGutter = window.innerWidth > element.clientWidth &&
      !computedScrollbarGutter.startsWith("stable");
    documentScrollLock = {
      element,
      overflow: style.getPropertyValue("overflow"),
      overflowPriority: style.getPropertyPriority("overflow"),
      scrollbarGutter: style.getPropertyValue("scrollbar-gutter"),
      scrollbarGutterPriority: style.getPropertyPriority("scrollbar-gutter"),
      reserveScrollbarGutter,
      scrollX: window.scrollX,
      scrollY: window.scrollY
    };
    if (reserveScrollbarGutter) style.setProperty("scrollbar-gutter", "stable", "important");
    style.setProperty("overflow", "hidden");
  }

  function restoreDocumentScrollLock() {
    const lock = documentScrollLock;
    if (!lock || dialog.open) return;

    const otherOpenDialogs = Array.from(document.querySelectorAll("dialog[open]"))
      .filter((otherDialog) => otherDialog !== dialog);
    if (otherOpenDialogs.length) {
      otherOpenDialogs.forEach((otherDialog) => {
        otherDialog.addEventListener("close", restoreDocumentScrollLock, { once: true });
      });
      return;
    }

    documentScrollLock = null;
    const style = lock.element.style;
    if (style.getPropertyValue("overflow") === "hidden" && !style.getPropertyPriority("overflow")) {
      if (lock.overflow) style.setProperty("overflow", lock.overflow, lock.overflowPriority);
      else style.removeProperty("overflow");
      if (lock.reserveScrollbarGutter && style.getPropertyValue("scrollbar-gutter") === "stable" &&
          style.getPropertyPriority("scrollbar-gutter") === "important") {
        if (lock.scrollbarGutter) {
          style.setProperty("scrollbar-gutter", lock.scrollbarGutter, lock.scrollbarGutterPriority);
        } else {
          style.removeProperty("scrollbar-gutter");
        }
      }
      window.requestAnimationFrame(() => {
        if (documentScrollLock || document.querySelector("dialog[open]")) return;
        const restoreStyle = lock.element.style;
        const scrollBehavior = restoreStyle.getPropertyValue("scroll-behavior");
        const scrollBehaviorPriority = restoreStyle.getPropertyPriority("scroll-behavior");
        restoreStyle.setProperty("scroll-behavior", "auto", "important");
        try {
          lock.element.scrollTo({ left: lock.scrollX, top: lock.scrollY, behavior: "auto" });
        } finally {
          if (scrollBehavior) {
            restoreStyle.setProperty("scroll-behavior", scrollBehavior, scrollBehaviorPriority);
          } else {
            restoreStyle.removeProperty("scroll-behavior");
          }
        }
      });
    }
  }

  function close() {
    requestId += 1;
    if (controller) controller.abort();
    controller = null;
    image.removeAttribute("src");
    image.dataset.previewUrl = "";
    image.hidden = true;
    clearSelection();
    if (dialog.open) dialog.close();
    restoreDocumentScrollLock();
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
    badge.textContent = Object.prototype.hasOwnProperty.call(statusLabels, state) ? statusLabels[state] : String(state);
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
    const sourceLabel = imageSourceLabels[data.image.source] || "Nenhuma imagem disponível";
    imageTitle.textContent = sourceLabel;
    image.alt = data.image.source === "NONE" ? "" : sourceLabel;
    const timestamp = data.image.source === "NONE" ? "" : imageTimestamp(data.image.recorded_at);
    imageRecordedAt.textContent = timestamp;
    imageRecordedAt.hidden = !timestamp;
    image.removeAttribute("src");
    image.dataset.previewUrl = "";
    if (data.image.state === "AVAILABLE" && data.image.preview_url) {
      imageState.textContent = "Carregando imagem…";
      imageFrame.dataset.imageState = "loading";
      image.dataset.previewUrl = new URL(data.image.preview_url, window.location.href).href;
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
      acquireDocumentScrollLock();
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
  image.addEventListener("load", () => {
    if (!dialog.open || content.hidden || !image.dataset.previewUrl || image.currentSrc !== image.dataset.previewUrl) return;
    image.hidden = false;
    imagePlaceholder.hidden = true;
    imageFrame.dataset.imageState = "available";
    imageState.textContent = "";
  });
  image.addEventListener("error", () => {
    if (!image.dataset.previewUrl || image.currentSrc !== image.dataset.previewUrl) return;
    image.hidden = true;
    imagePlaceholder.hidden = false;
    imageFrame.dataset.imageState = "unavailable";
    imageState.textContent = "Não foi possível carregar a imagem selecionada";
  });
});
