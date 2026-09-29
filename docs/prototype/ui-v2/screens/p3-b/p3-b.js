(() => {
  "use strict";
  const params = new URLSearchParams(window.location.search);
  const state = document.documentElement.dataset.argosPrototypeState || "default";
  const fixtureName = document.documentElement.dataset.argosPrototypeFixture || "default";
  const screenId = document.querySelector('meta[name="argos-screen-id"]')?.content;
  const setText = (key, value) => {
    const node = document.querySelector('[data-bind="' + key + '"]');
    if (node) node.textContent = value == null ? "" : String(value);
  };
  const setTime = (key, value) => {
    const node = document.querySelector('[data-bind="' + key + '"]');
    if (!node) return;
    node.dateTime = value || "";
    node.textContent = formatDate(value);
  };
  const formatDate = (value) => {
    if (!value) return "—";
    const match = String(value).match(/^(\d{4})-(\d{2})-(\d{2})T?(\d{2})?:?(\d{2})?/);
    return match ? match[3] + "/" + match[2] + "/" + match[1] + (match[4] ? " · " + match[4] + ":" + (match[5] || "00") : "") : String(value);
  };
  const cell = (row, value) => {
    const td = document.createElement("td");
    td.textContent = value == null || value === "" ? "—" : String(value);
    row.append(td);
    return td;
  };
  const appendBadge = (td, label, variant) => {
    const badge = document.createElement("span");
    badge.className = "argos-status-badge argos-status-badge--" + variant;
    badge.textContent = label;
    td.replaceChildren(badge);
  };
  const makeLink = (href, label) => {
    const anchor = document.createElement("a");
    anchor.href = href;
    anchor.textContent = label;
    return anchor;
  };
  const queryHref = (updates) => {
    const next = new URLSearchParams(window.location.search);
    for (const [key, value] of Object.entries(updates)) {
      if (value == null || value === "") next.delete(key);
      else next.set(key, value);
    }
    return window.location.pathname + (next.toString() ? "?" + next.toString() : "");
  };
  const addPagination = (container, current, total, label) => {
    if (!container) return;
    const pagination = container.querySelector("nav");
    if (!pagination) return;
    pagination.replaceChildren();
    container.hidden = total < 2;
    if (total < 2) return;
    const previous = current > 1 ? makeLink(queryHref({ page: String(current - 1) }), "Anterior") : document.createElement("span");
    if (current === 1) { previous.textContent = "Anterior"; previous.setAttribute("aria-disabled", "true"); }
    pagination.append(previous);
    for (let page = 1; page <= total; page += 1) {
      const item = page === current ? document.createElement("span") : makeLink(queryHref({ page: String(page) }), String(page));
      if (page === current) { item.textContent = String(page); item.setAttribute("aria-current", "page"); }
      pagination.append(item);
    }
    const next = current < total ? makeLink(queryHref({ page: String(current + 1) }), "Próxima") : document.createElement("span");
    if (current === total) { next.textContent = "Próxima"; next.setAttribute("aria-disabled", "true"); }
    pagination.append(next);
    pagination.setAttribute("aria-label", label);
  };
  const load = async () => {
    const response = await fetch("../../fixtures/p3-b.json");
    if (!response.ok) throw new Error("Não foi possível carregar as fixtures locais.");
    return response.json();
  };
  const renderMonitoring = (data) => {
    const item = data.monitoring[fixtureName] || data.monitoring.default;
    setText("monitor-camera-id", item.camera.id);
    setText("monitor-camera-name", item.camera.name);
    setText("monitor-camera-location", item.camera.location);
    const substitutionsLink = document.querySelector('[data-bind="monitor-substitutions-link"]');
    substitutionsLink.href = "scr-sub-camera-001.html?camera=" + encodeURIComponent(item.camera.id) + "&fixture=" + encodeURIComponent(fixtureName);
    const stale = params.get("freshness") === "stale";
    const staleNotice = document.querySelector('[data-bind="monitor-stale"]');
    const status = document.querySelector('[data-bind="monitor-status"]');
    const stable = document.querySelector('[data-bind="monitor-stable-status"]');
    if (stale) {
      staleNotice.hidden = false;
      status.className = "argos-status-badge argos-status-badge--neutral";
      status.textContent = "Desconhecido";
      stable.hidden = false;
      setText("monitor-stable-inline", item.stableState);
      setTime("monitor-evidence", item.evidenceAt);
    }
    const empty = state === "empty";
    setText("monitor-count", (empty ? 0 : item.outages.length) + " registros");
    document.querySelector('[data-bind="monitor-empty"]').hidden = !empty;
    document.querySelector('[data-bind="monitor-table-region"]').hidden = empty;
    document.querySelector('[data-bind="monitor-pagination"]').hidden = empty;
    if (empty) return;
    const body = document.querySelector('[data-bind="monitor-rows"]');
    const pageSize = 5;
    const totalPages = Math.max(2, Math.ceil(item.outages.length / pageSize));
    const page = Math.min(Math.max(1, Number(params.get("page") || 1)), totalPages);
    for (const outage of item.outages.slice((page - 1) * pageSize, page * pageSize)) {
      const tr = document.createElement("tr");
      cell(tr, formatDate(outage.startedAt));
      cell(tr, formatDate(outage.closedAt));
      cell(tr, outage.duration);
      const originCell = cell(tr, "");
      appendBadge(originCell, outage.originLabel, "neutral");
      const statusCell = cell(tr, "");
      appendBadge(statusCell, outage.closedAt ? "Fechada" : "Aberta", outage.closedAt ? "success" : "warning");
      cell(tr, outage.closeReasonLabel || "—");
      body.append(tr);
    }
    addPagination(document.querySelector('[data-bind="monitor-pagination"]'), page, totalPages, "Paginação do histórico de monitoramento");
  };
  const renderSubList = (data) => {
    const all = data.substitutions[fixtureName] || data.substitutions.default;
    const q = (params.get("q") || "").trim();
    const from = params.get("data_inicial") || "";
    const to = params.get("data_final") || "";
    const invalid = state === "error" || (from && to && from > to);
    const search = document.querySelector('[data-bind="sub-search"]');
    const start = document.querySelector('[data-bind="sub-date-start"]');
    const end = document.querySelector('[data-bind="sub-date-end"]');
    search.value = q;
    start.value = from;
    end.value = to;
    document.querySelector('[data-bind="sub-fixture"]').value = fixtureName;
    const error = document.querySelector('[data-bind="sub-filter-error"]');
    error.hidden = !invalid;
    if (invalid) {
      start.setAttribute("aria-invalid", "true");
      end.setAttribute("aria-invalid", "true");
      start.setAttribute("aria-describedby", "period-error-copy");
      end.setAttribute("aria-describedby", "period-error-copy");
    }
    const chips = document.querySelector('[data-bind="sub-active-filters"]');
    chips.replaceChildren();
    for (const [label, value] of [["Busca", q], ["A partir de", from], ["Até", to]]) {
      if (!value) continue;
      const chip = document.createElement("span");
      chip.className = "argos-badge argos-badge--info";
      chip.textContent = label + ": " + value;
      chips.append(chip);
    }
    document.querySelector('[data-bind="sub-active-filters-shell"]').hidden = chips.childElementCount === 0;
    const filtered = all.filter((entry) => {
      const searchable = [entry.previous.id, entry.previous.name, entry.replacement.id, entry.replacement.name, entry.operationalName, entry.motive].join(" ").toLocaleLowerCase("pt-BR");
      return (!q || searchable.includes(q.toLocaleLowerCase("pt-BR"))) && (!from || entry.occurredAt.slice(0, 10) >= from) && (!to || entry.occurredAt.slice(0, 10) <= to);
    });
    const empty = state === "empty" || (!invalid && filtered.length === 0);
    document.querySelector('[data-bind="sub-empty"]').hidden = !empty;
    document.querySelector('[data-bind="sub-table-region"]').hidden = empty || invalid;
    const summary = invalid ? "Ajuste o intervalo informado para consultar o histórico." : empty ? "0 registros para a consulta atual." : filtered.length + " registros nesta página de demonstração.";
    setText("sub-result-summary", summary);
    const pagination = document.querySelector('[data-bind="sub-pagination"]');
    pagination.hidden = empty || invalid;
    if (empty || invalid) return;
    const rows = document.querySelector('[data-bind="sub-rows"]');
    const pageSize = 4;
    const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
    const page = Math.min(Math.max(1, Number(params.get("page") || 1)), totalPages);
    for (const entry of filtered.slice((page - 1) * pageSize, page * pageSize)) {
      const tr = document.createElement("tr");
      cell(tr, formatDate(entry.occurredAt));
      cell(tr, entry.previous.id + " · " + entry.previous.name);
      cell(tr, entry.replacement.id + " · " + entry.replacement.name);
      cell(tr, entry.operationalName);
      cell(tr, entry.motive);
      const action = cell(tr, "");
      const detailLink = makeLink("scr-sub-detail-001.html?id=" + encodeURIComponent(entry.id) + "&fixture=" + encodeURIComponent(fixtureName), "Ver registro");
      detailLink.className = "argos-button argos-button--secondary";
      action.append(detailLink);
      rows.append(tr);
    }
    addPagination(pagination, page, totalPages, "Paginação do histórico global");
  };
  const renderSubDetail = (data) => {
    const entries = data.substitutions[fixtureName] || data.substitutions.default;
    const entry = entries.find((candidate) => candidate.id === params.get("id")) || entries.find((candidate) => candidate.id === data.substitutions.selectedDetailId) || entries[0];
    setText("detail-id", entry.id);
    setText("detail-id-copy", entry.id);
    setTime("detail-occurred", entry.occurredAt);
    setTime("detail-created", entry.createdAt);
    setText("detail-registered-name", entry.registeredName);
    setText("detail-registered-user", entry.registeredBy);
    setText("previous-id", entry.previous.id);
    setText("previous-name", entry.previous.name);
    setText("previous-location", entry.previous.location);
    setText("replacement-id", entry.replacement.id);
    setText("replacement-name", entry.replacement.name);
    setText("replacement-location", entry.replacement.location);
    setText("detail-operational-name", entry.operationalName);
    setText("detail-motive", entry.motive);
    setText("detail-observations", entry.observations);
  };
  const renderSubCamera = (data) => {
    const all = data.substitutions[fixtureName] || data.substitutions.default;
    const cameraId = params.get("camera") || data.substitutions.scopedCameraId;
    const related = all.filter((entry) => entry.previous.id.includes(cameraId) || entry.replacement.id.includes(cameraId));
    const sample = related[0] || all[0];
    const cameraIsPrevious = sample ? sample.previous.id.includes(cameraId) : true;
    setText("scoped-camera-id", cameraId);
    setText("scoped-camera-name", cameraIsPrevious ? sample?.previous.name || "Câmera da fixture" : sample?.replacement.name || "Câmera da fixture");
    const empty = state === "empty" || related.length === 0;
    setText("scoped-count", (empty ? 0 : related.length) + " registros");
    document.querySelector('[data-bind="scoped-empty"]').hidden = !empty;
    document.querySelector('[data-bind="scoped-table-region"]').hidden = empty;
    document.querySelector('[data-bind="scoped-pagination"]').hidden = empty;
    if (empty) return;
    const rows = document.querySelector('[data-bind="scoped-rows"]');
    const pageSize = 2;
    const totalPages = Math.max(1, Math.ceil(related.length / pageSize));
    const page = Math.min(Math.max(1, Number(params.get("page") || 1)), totalPages);
    for (const entry of related.slice((page - 1) * pageSize, page * pageSize)) {
      const isPrevious = entry.previous.id.includes(cameraId);
      const relatedCamera = isPrevious ? entry.replacement : entry.previous;
      const tr = document.createElement("tr");
      cell(tr, formatDate(entry.occurredAt));
      const roleCell = cell(tr, "");
      appendBadge(roleCell, isPrevious ? "Foi substituída" : "Entrou como substituta", isPrevious ? "warning" : "info");
      cell(tr, relatedCamera.id + " · " + relatedCamera.name);
      cell(tr, entry.operationalName);
      cell(tr, entry.motive);
      const action = cell(tr, "");
      const detailLink = makeLink("scr-sub-detail-001.html?id=" + encodeURIComponent(entry.id) + "&fixture=" + encodeURIComponent(fixtureName), "Ver registro");
      detailLink.className = "argos-button argos-button--secondary";
      action.append(detailLink);
      rows.append(tr);
    }
    addPagination(document.querySelector('[data-bind="scoped-pagination"]'), page, totalPages, "Paginação das substituições da câmera");
  };
  load().then((data) => {
    if (screenId === "SCR-MON-HISTORY-001") renderMonitoring(data);
    if (screenId === "SCR-SUB-LIST-001") renderSubList(data);
    if (screenId === "SCR-SUB-DETAIL-001") renderSubDetail(data);
    if (screenId === "SCR-SUB-CAMERA-001") renderSubCamera(data);
  }).catch((error) => {
    const notice = document.createElement("aside");
    notice.className = "argos-alert argos-alert--danger";
    notice.setAttribute("role", "alert");
    const content = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = "A pr\u00e9via n\u00e3o p\u00f4de ser renderizada";
    const message = document.createElement("p");
    message.textContent = "Confira o carregamento dos dados de demonstra\u00e7\u00e3o e recarregue a p\u00e1gina.";
    content.append(title, message);
    notice.append(content);
    document.querySelector("main").prepend(notice);
    console.error(error);
  });
})();
