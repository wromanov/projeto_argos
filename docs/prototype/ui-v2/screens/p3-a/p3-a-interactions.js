// P3-A only: deterministic fixture rendering and local prototype interactions.
(() => {
  const screenId = document.querySelector('meta[name="argos-screen-id"]')?.content;
  const state = document.documentElement.dataset.argosPrototypeState || "default";
  const fixtureName = document.documentElement.dataset.argosPrototypeFixture || "default";
  if (!screenId || screenId === "SCR-PORTAL-001") return;

  const fixtureUrl = new URL("../../fixtures/p3-a-camera-inventory.json", document.baseURI);
  const escapeText = (value) => String(value ?? "");
  const element = (tag, className, value) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = escapeText(value);
    return node;
  };
  const badgeClass = (kind) => `argos-status-badge argos-status-badge--${kind}`;
  const monitoringKind = (camera) => {
    if (camera.monitoring_state === "ONLINE") return "success";
    if (camera.monitoring_state === "OFFLINE") return "danger";
    return "neutral";
  };
  const completenessLabel = (camera) => camera.completeness === "COMPLETE" ? "Completo" : "Incompleto";

  fetch(fixtureUrl, { headers: { Accept: "application/json" } })
    .then((response) => {
      if (!response.ok) throw new Error("Fixture indisponível");
      return response.json();
    })
    .then((data) => {
      if (screenId === "SCR-DASH-001") renderDashboard(data);
      if (screenId === "SCR-INV-001") renderInventory(data);
      if (screenId === "SCR-CAM-DETAIL-001") renderCameraDetail(data);
    })
    .catch(() => {
      const feedback = document.querySelector("[data-filter-feedback]");
      if (feedback) feedback.textContent = "Fixture local indisponível; filtros demonstrativos não foram carregados.";
      const summary = document.querySelector("[data-results-summary]");
      if (summary && state === "default") summary.textContent = "Não foi possível carregar a fixture local.";
      const featured = document.querySelector("[data-dashboard-featured-camera]");
      if (featured) featured.replaceChildren(element("p", "", "Não foi possível carregar os dados demonstrativos."));
    });

  function renderDashboard(data) {
    const metrics = fixtureName === "long" ? data.dashboard_long : data.dashboard;
    if (!metrics) return;
    document.querySelectorAll("[data-metric]").forEach((node) => {
      const value = metrics[node.dataset.metric];
      if (value !== undefined) node.textContent = String(value);
    });

    const activities = document.querySelector("[data-dashboard-activities]");
    if (activities) {
      const activityItems = fixtureName === "long" ? [] : data.activities;
      activities.replaceChildren(...activityItems.map((activity) => {
        const item = element("li");
        const link = element("a", "", activity.title);
        link.href = `scr-cam-detail-001.html#${encodeURIComponent(activity.camera_id)}`;
        link.setAttribute("aria-label", `${activity.title}; câmera ${activity.camera_id}`);
        item.append(link, element("span", "", ` — ${activity.camera_id} · ${activity.occurred_at}`));
        return item;
      }));
      if (!activityItems.length) activities.append(element("li", "", "Nenhuma atividade registrada nesta fixture."));
    }

    const camera = fixtureName === "long" ? data.long_camera : data.cameras.find((item) => item.id === "CAM-DEMO-0103");
    const featured = document.querySelector("[data-dashboard-featured-camera]");
    if (camera && featured) {
      const link = element("a", "", camera.name);
      link.href = `scr-cam-detail-001.html#${encodeURIComponent(camera.id)}`;
      const detail = element("p", "", `${camera.manufacturer} · ${camera.model}`);
      const location = element("p", "", `${camera.terminal} · ${camera.sector}`);
      const monitoring = element("span", badgeClass(monitoringKind(camera)), camera.monitoring_label);
      const operation = element("span", "argos-badge argos-badge--neutral", camera.operational_label);
      const freshness = camera.freshness === "STALE"
        ? element("span", "argos-status-badge argos-status-badge--warning", "Dados desatualizados")
        : null;
      featured.replaceChildren(link, detail, location, element("div", "argos-inline"));
      const labels = featured.lastElementChild;
      labels.append(operation, monitoring);
      if (freshness) labels.append(freshness);
    }
  }

  function renderInventory(data) {
    const filters = [...document.querySelectorAll("[data-filter]")];
    const optionSource = fixtureName === "long" ? [...data.cameras, data.long_camera] : data.cameras;
    const rowsBody = document.querySelector("[data-inventory-rows]");
    const summary = document.querySelector("[data-results-summary]");
    const pagination = document.querySelector("[data-pagination]");
    const tableRegion = document.querySelector('[data-argos-state-variant="default"].argos-table-region');
    const filterEmpty = document.querySelector("[data-filter-empty]");
    const results = document.querySelector("#inventory-results");
    const feedback = document.querySelector("[data-filter-feedback]");
    const activeFilters = document.querySelector("[data-active-filters]");
    const selectionStatus = document.querySelector("[data-selection-status]");
    const pageSize = 3;
    let currentPage = 1;
    let cameras = optionSource;

    const dynamicOptions = {
      terminal: "Todos",
      manufacturer: "Todos",
      vlan: "Todas",
      farm: "Todas",
    };
    Object.entries(dynamicOptions).forEach(([key, firstLabel]) => {
      const select = filters.find((control) => control.dataset.filter === key);
      if (!select) return;
      const firstOption = select.options[0];
      firstOption.textContent = firstLabel;
      const uniqueValues = [...new Set(optionSource.map((camera) => camera[key]).filter(Boolean))]
        .sort((a, b) => a.localeCompare(b, "pt-BR"));
      uniqueValues.forEach((value) => {
        const option = element("option", "", value);
        option.value = value;
        select.append(option);
      });
    });

    function currentValues() {
      return Object.fromEntries(filters.map((control) => [control.dataset.filter, control.value.trim()]));
    }

    function filteredCameras() {
      const values = currentValues();
      const searchable = (camera) => [
        camera.name, camera.identifier, camera.model, camera.manufacturer, camera.terminal,
        camera.floor, camera.sector, camera.environment, camera.description,
        camera.reference_point, camera.type, camera.vlan, camera.farm,
      ].join(" ").toLocaleLowerCase("pt-BR");
      return cameras.filter((camera) => {
        const searchMatch = !values.search || searchable(camera).includes(values.search.toLocaleLowerCase("pt-BR"));
        const completenessMatch = !values.completeness || camera.completeness === values.completeness;
        return searchMatch
          && completenessMatch
          && (!values.operational_label || camera.operational_label === values.operational_label)
          && (!values.monitoring_label || camera.monitoring_label === values.monitoring_label)
          && (!values.terminal || camera.terminal === values.terminal)
          && (!values.type || camera.type === values.type)
          && (!values.manufacturer || camera.manufacturer === values.manufacturer)
          && (!values.vlan || camera.vlan === values.vlan)
          && (!values.farm || camera.farm === values.farm);
      });
    }

    function refreshActiveFilters(values) {
      if (!activeFilters) return;
      const labels = {
        search: "Busca", operational_label: "Situação", monitoring_label: "Monitoramento",
        completeness: "Completude", terminal: "Terminal", type: "Tipo", manufacturer: "Fabricante",
        vlan: "VLAN", farm: "Fazenda",
      };
      const nodes = Object.entries(values).filter(([, value]) => value).map(([key, value]) =>
        element("span", "argos-badge argos-badge--info", `${labels[key]}: ${value === "COMPLETE" ? "Completo" : value === "INCOMPLETE" ? "Incompleto" : value}`));
      activeFilters.replaceChildren(...nodes);
      if (!nodes.length) activeFilters.setAttribute("aria-label", "Nenhum filtro ativo");
      else activeFilters.setAttribute("aria-label", "Filtros ativos");
    }

    function makeBadge(text, kind, status = true) {
      return element("span", status ? badgeClass(kind) : `argos-badge argos-badge--${kind}`, text);
    }

    function renderRows() {
      const matches = filteredCameras();
      const pageCount = Math.max(1, Math.ceil(matches.length / pageSize));
      currentPage = Math.min(currentPage, pageCount);
      const start = (currentPage - 1) * pageSize;
      const visible = matches.slice(start, start + pageSize);
      refreshActiveFilters(currentValues());
      rowsBody.replaceChildren(...visible.map((camera) => {
        const row = element("tr");
        row.dataset.rowCameraId = camera.id;
        row.tabIndex = 0;
        row.setAttribute("aria-selected", "false");

        const nameCell = element("td");
        const detailLink = element("a", "", camera.name);
        detailLink.href = `scr-cam-detail-001.html#${encodeURIComponent(camera.id)}`;
        detailLink.setAttribute("aria-label", `Abrir detalhe da câmera ${camera.name}`);
        nameCell.append(detailLink, element("div", "", camera.identifier));

        const imageCell = element("td");
        imageCell.append(makeBadge("Imagem não disponível", "neutral", false));

        const operationCell = element("td");
        operationCell.append(makeBadge(camera.operational_label, "neutral", true));

        const monitoringCell = element("td");
        monitoringCell.append(makeBadge(camera.monitoring_label, monitoringKind(camera), true));
        if (camera.freshness === "STALE") monitoringCell.append(element("div", "", "Dados desatualizados"));

        const completenessCell = element("td");
        completenessCell.append(makeBadge(completenessLabel(camera), camera.completeness === "COMPLETE" ? "success" : "warning", true));

        const modelCell = element("td");
        modelCell.append(element("div", "", camera.manufacturer), element("div", "", camera.model));

        const locationCell = element("td");
        locationCell.append(element("div", "", camera.terminal), element("div", "", camera.sector));

        const actionsCell = element("td");
        const actions = element("div", "argos-stack");
        const quickLink = element("a", "argos-button argos-button--secondary argos-button--compact", "Quick Detail");
        quickLink.href = "../index.html#screen-scr-cam-quick-001";
        quickLink.setAttribute("aria-label", `Quick Detail protegido da câmera ${camera.identifier}`);
        const fullLink = element("a", "argos-button argos-button--secondary argos-button--compact", "Detalhe");
        fullLink.href = `scr-cam-detail-001.html#${encodeURIComponent(camera.id)}`;
        fullLink.setAttribute("aria-label", `Abrir detalhe completo da câmera ${camera.identifier}`);
        actions.append(quickLink, fullLink);
        actionsCell.append(actions);

        row.append(nameCell, imageCell, operationCell, monitoringCell, completenessCell, modelCell, locationCell, actionsCell);
        return row;
      }));
      if (selectionStatus) selectionStatus.textContent = "Nenhuma câmera selecionada.";

      if (summary) summary.textContent = state === "empty"
        ? "Nenhum resultado neste estado demonstrativo"
        : state === "loading"
          ? "Carregando fixture demonstrativa"
          : state === "error"
            ? "Fixture não carregada neste estado demonstrativo"
            : matches.length
              ? `Exibindo ${start + 1}–${start + visible.length} de ${matches.length} câmeras demonstrativas`
              : "0 câmeras demonstrativas encontradas";
      if (tableRegion) tableRegion.hidden = state !== "default" || matches.length === 0;
      if (filterEmpty) filterEmpty.hidden = state !== "default" || matches.length !== 0;
      if (pagination) pagination.hidden = state !== "default" || matches.length <= pageSize;
      if (results) results.setAttribute("aria-busy", state === "loading" ? "true" : "false");
      renderPagination(pageCount);
      if (feedback) feedback.textContent = `${matches.length} ${matches.length === 1 ? "resultado" : "resultados"} na fixture local.`;
    }

    function renderPagination(pageCount) {
      if (!pagination) return;
      const links = [];
      if (currentPage > 1) links.push(pageLink("Anterior", currentPage - 1));
      else links.push(element("span", "", "Anterior"));
      for (let page = 1; page <= pageCount; page += 1) {
        const link = pageLink(String(page), page);
        if (page === currentPage) link.setAttribute("aria-current", "page");
        link.setAttribute("aria-label", `Página ${page}`);
        links.push(link);
      }
      if (currentPage < pageCount) links.push(pageLink("Próxima", currentPage + 1));
      else links.push(element("span", "", "Próxima"));
      pagination.replaceChildren(...links);
    }

    function pageLink(label, page) {
      const link = element("a", "", label);
      link.href = `#inventory-page-${page}`;
      link.dataset.page = String(page);
      link.addEventListener("click", (event) => {
        event.preventDefault();
        currentPage = page;
        renderRows();
      });
      return link;
    }

    filters.forEach((control) => control.addEventListener(control.type === "search" ? "input" : "change", () => {
      currentPage = 1;
      renderRows();
    }));
    document.querySelectorAll("[data-clear-filters]").forEach((button) => button.addEventListener("click", () => {
      filters.forEach((control) => { control.value = ""; });
      currentPage = 1;
      renderRows();
      filters.find((control) => control.dataset.filter === "search")?.focus();
    }));
    rowsBody.addEventListener("click", (event) => {
      if (event.target.closest("a, button, input, select")) return;
      const row = event.target.closest("tr[data-row-camera-id]");
      if (row) selectRow(row);
    });
    rowsBody.addEventListener("keydown", (event) => {
      const row = event.target.closest("tr[data-row-camera-id]");
      if (!row || event.target.closest("a, button, input, select")) return;
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectRow(row);
      }
    });

    function selectRow(row) {
      const wasSelected = row.getAttribute("aria-selected") === "true";
      rowsBody.querySelectorAll("tr[aria-selected='true']").forEach((selected) => selected.setAttribute("aria-selected", "false"));
      row.setAttribute("aria-selected", wasSelected ? "false" : "true");
      if (selectionStatus) selectionStatus.textContent = wasSelected
        ? "Seleção removida."
        : `Câmera ${row.dataset.rowCameraId} selecionada.`;
    }

    renderRows();
  }

  function renderCameraDetail(data) {
    const hashId = decodeURIComponent(window.location.hash.slice(1));
    const camera = fixtureName === "long"
      ? data.long_camera
      : data.cameras.find((item) => item.id === hashId) || data.cameras.find((item) => item.id === "CAM-DEMO-0103");
    if (!camera) return;

    document.querySelectorAll("[data-camera-field]").forEach((node) => {
      const value = camera[node.dataset.cameraField];
      if (value !== undefined) node.textContent = escapeText(value);
    });
    document.querySelectorAll("[data-camera-network]").forEach((node) => {
      const value = camera.network?.[node.dataset.cameraNetwork];
      node.textContent = value || "Não informado na fixture";
    });
    const operational = document.querySelector("[data-camera-operational]");
    const monitoring = document.querySelector("[data-camera-monitoring]");
    const completeness = document.querySelector("[data-camera-completeness]");
    const staleBadge = document.querySelector("[data-camera-stale]");
    const staleAlert = document.querySelector("[data-camera-stale-alert]");
    const imageState = document.querySelector("[data-camera-image-state]");
    const historyContent = document.querySelector("[data-camera-history-content]");
    if (historyContent) historyContent.hidden = state === "empty";
    if (operational) operational.textContent = camera.operational_label;
    if (monitoring) {
      monitoring.textContent = camera.monitoring_label;
      monitoring.className = badgeClass(monitoringKind(camera));
    }
    if (completeness) {
      completeness.textContent = `Cadastro ${completenessLabel(camera).toLocaleLowerCase("pt-BR")}`;
      completeness.className = badgeClass(camera.completeness === "COMPLETE" ? "success" : "warning");
    }
    const isStale = camera.freshness === "STALE";
    if (staleBadge) staleBadge.hidden = !isStale;
    if (staleAlert) staleAlert.hidden = !isStale;
    if (imageState) imageState.textContent = camera.image_state === "NO_IMAGE_AVAILABLE"
      ? "Imagem não disponível nesta fixture"
      : camera.image_state;

    Object.entries(camera.history || {}).forEach(([historyType, entries]) => {
      const list = document.querySelector(`[data-history="${historyType}"]`);
      if (!list) return;
      const content = entries.map((entry) => {
        const item = element("li");
        const title = entry.title || (historyType === "outages" ? `Indisponibilidade ${entry.opened_at} · ${entry.duration}` : entry.id);
        item.append(element("strong", "", title));
        const details = [entry.occurred_at, entry.origin, entry.close_reason].filter(Boolean).join(" · ");
        if (details) item.append(element("span", "", ` — ${details}`));
        return item;
      });
      if (!content.length) content.push(element("li", "", "Nenhum registro relacionado nesta fixture."));
      list.replaceChildren(...content);
    });
  }
})();
