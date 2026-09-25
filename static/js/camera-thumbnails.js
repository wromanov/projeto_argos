"use strict";

// Storage pode mudar entre o HTML e o request lazy; preserve o placeholder.
document.addEventListener("error", (event) => {
  const image = event.target;
  if (!(image instanceof HTMLImageElement) || !image.classList.contains("camera-thumbnail__image")) return;
  image.hidden = true;
  const thumbnail = image.closest(".camera-thumbnail");
  if (thumbnail) thumbnail.dataset.thumbnailState = "UNAVAILABLE";
}, true);
