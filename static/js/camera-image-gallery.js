(() => {
  const dialog = document.getElementById("camera-image-gallery");
  if (!dialog || typeof dialog.showModal !== "function") return;

  const openers = [...document.querySelectorAll("[data-gallery-open]")];
  const closeButtons = [...dialog.querySelectorAll("[data-gallery-close], [data-gallery-close-footer]")];
  const thumbnails = [...dialog.querySelectorAll("[data-gallery-image]")];
  const grid = dialog.querySelector("[data-gallery-grid]");
  const detail = dialog.querySelector("[data-gallery-detail]");
  const title = dialog.querySelector("[data-gallery-selected-title]");
  const origin = dialog.querySelector("[data-gallery-selected-origin]");
  const time = dialog.querySelector("[data-gallery-selected-time]");
  const preview = dialog.querySelector("[data-gallery-preview]");
  const backButtons = [...dialog.querySelectorAll("[data-gallery-back]")];
  let opener = null;
  let selectedThumbnail = null;

  const returnToGrid = () => {
    if (!detail || detail.hidden) return false;
    detail.hidden = true;
    if (grid) grid.hidden = false;
    if (preview) preview.replaceChildren();
    selectedThumbnail?.focus();
    return true;
  };

  const showImage = (button) => {
    selectedThumbnail = button;
    if (grid) grid.hidden = true;
    if (!detail) return;
    detail.hidden = false;
    title.textContent = button.dataset.imageLabel || "Imagem selecionada";
    origin.textContent = button.dataset.imageOrigin || "";
    time.textContent = button.dataset.imageTime || "";
    preview.replaceChildren();

    if (button.dataset.imageState !== "AVAILABLE" || !button.dataset.imageFull) {
      const message = document.createElement("p");
      message.setAttribute("role", "status");
      message.textContent = "Imagem indisponível no momento.";
      preview.append(message);
    } else {
      const image = document.createElement("img");
      image.alt = button.dataset.imageLabel || "Imagem da câmera";
      image.src = button.dataset.imageFull;
      image.addEventListener("error", () => {
        const message = document.createElement("p");
        message.setAttribute("role", "status");
        message.textContent = "Imagem indisponível no momento.";
        preview.replaceChildren(message);
      }, { once: true });
      preview.append(image);
    }
    dialog.querySelector("[data-gallery-back]")?.focus();
  };

  openers.forEach((button) => button.addEventListener("click", () => {
    opener = button;
    selectedThumbnail = null;
    if (grid) grid.hidden = false;
    if (detail) detail.hidden = true;
    dialog.showModal();
  }));

  thumbnails.forEach((button, index) => {
    button.addEventListener("click", () => showImage(button));
    button.addEventListener("keydown", (event) => {
      if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
      event.preventDefault();
      const step = event.key === "ArrowRight" ? 1 : -1;
      thumbnails[(index + step + thumbnails.length) % thumbnails.length]?.focus();
    });
  });

  closeButtons.forEach((button) => button.addEventListener("click", () => dialog.close()));
  backButtons.forEach((button) => button.addEventListener("click", returnToGrid));
  document.addEventListener("keydown", (event) => {
    if (!dialog.open || event.key !== "Tab") return;
    const focusable = [...dialog.querySelectorAll(
      'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
    )].filter((element) => !element.hidden && element.getClientRects().length > 0);
    if (!focusable.length) {
      event.preventDefault();
      dialog.focus();
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    const activeIsOutside = !dialog.contains(document.activeElement);
    if ((event.shiftKey && (document.activeElement === first || activeIsOutside))
      || (!event.shiftKey && (document.activeElement === last || activeIsOutside))) {
      event.preventDefault();
      (event.shiftKey ? last : first).focus();
    }
  });
  dialog.addEventListener("cancel", (event) => {
    if (returnToGrid()) event.preventDefault();
  });
  dialog.addEventListener("close", () => {
    if (grid) grid.hidden = false;
    if (detail) detail.hidden = true;
    if (preview) preview.replaceChildren();
    const target = opener;
    opener = null;
    selectedThumbnail = null;
    target?.focus();
  });
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
})();
