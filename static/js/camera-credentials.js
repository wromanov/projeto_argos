(() => {
  "use strict";

  const card = document.getElementById("camera-credential-card");
  const cameraForm = document.getElementById("camera-form");
  if (!card || !cameraForm) return;

  const dialogs = {
    replace: document.getElementById("credential-replace-dialog"),
    revoke: document.getElementById("credential-revoke-dialog"),
    reveal: document.getElementById("credential-reveal-dialog"),
    dirty: document.getElementById("credential-dirty-dialog"),
  };
  const buttons = [...card.querySelectorAll("[data-open-credential]")];
  const formState = () => [...cameraForm.elements].filter((el) => el.name).map((el) => {
    if (el.type === "checkbox" || el.type === "radio") return `${el.name}:${el.value}:${el.checked}`;
    return `${el.name}:${el.value}`;
  });
  const initialState = formState();
  let pendingOperation = null;
  let pendingForm = null;
  let returnFocus = null;

  const isDirty = () => {
    const current = formState();
    return current.length !== initialState.length || current.some((value, index) => value !== initialState[index]);
  };

  const closeDialog = (dialog) => {
    if (dialog?.open) dialog.close();
  };

  const clearCredentialInputs = () => {
    ["credential-username", "credential-password", "credential-current-password"].forEach((id) => {
      const input = document.getElementById(id);
      if (input) input.value = "";
    });
    const revealStatus = document.querySelector("[data-reveal-status]");
    const secretOutput = document.querySelector("[data-revealed-secret]");
    if (revealStatus) {
      revealStatus.hidden = true;
      revealStatus.textContent = "";
    }
    if (secretOutput) {
      secretOutput.hidden = true;
      secretOutput.replaceChildren();
    }
  };

  const openDialog = (name, source = document.activeElement) => {
    const dialog = dialogs[name];
    if (!dialog || typeof dialog.showModal !== "function") return;
    returnFocus = source;
    dialog.showModal();
    const first = dialog.querySelector("input:not([type=hidden]), button:not([data-close-dialog])");
    if (first) first.focus();
  };

  const startOperation = (name, source) => {
    if (isDirty()) {
      pendingOperation = name;
      returnFocus = source;
      openDialog("dirty", source);
      return;
    }
    openDialog(name, source);
  };

  buttons.forEach((button) => {
    button.hidden = false;
    button.addEventListener("click", () => startOperation(button.dataset.openCredential, button));
  });

  document.querySelectorAll("[data-close-dialog]").forEach((button) => {
    button.addEventListener("click", () => closeDialog(button.closest("dialog")));
  });

  Object.values(dialogs).filter(Boolean).forEach((dialog) => {
    dialog.addEventListener("close", () => {
      if (dialog === dialogs.replace || dialog === dialogs.reveal) clearCredentialInputs();
      if (returnFocus?.isConnected) returnFocus.focus();
    });
  });

  const replaceForm = dialogs.replace?.querySelector("form");
  const revokeForm = dialogs.revoke?.querySelector("form");
  [replaceForm, revokeForm].filter(Boolean).forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!isDirty()) return;
      event.preventDefault();
      pendingForm = form;
      pendingOperation = null;
      returnFocus = document.activeElement;
      closeDialog(form.closest("dialog"));
      openDialog("dirty", returnFocus);
    });
  });

  document.querySelector("[data-keep-camera-edits]")?.addEventListener("click", () => {
    pendingForm = null;
    pendingOperation = null;
    closeDialog(dialogs.dirty);
    document.querySelector("#camera-form button[type=submit]")?.focus();
  });

  document.querySelector("[data-discard-camera-edits]")?.addEventListener("click", () => {
    cameraForm.reset();
    const operation = pendingOperation;
    const form = pendingForm;
    pendingOperation = null;
    pendingForm = null;
    closeDialog(dialogs.dirty);
    window.setTimeout(() => {
      if (form) form.requestSubmit();
      else if (operation) openDialog(operation);
    }, 0);
  });

  const revealForm = document.getElementById("credential-reveal-form");
  revealForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (isDirty()) {
      pendingForm = revealForm;
      pendingOperation = null;
      returnFocus = document.activeElement;
      closeDialog(dialogs.reveal);
      openDialog("dirty", returnFocus);
      return;
    }
    const submit = revealForm.querySelector("button[type=submit]");
    const password = revealForm.elements.current_password;
    const status = revealForm.querySelector("[data-reveal-status]");
    const output = revealForm.querySelector("[data-revealed-secret]");
    status.hidden = true;
    status.textContent = "";
    output.hidden = true;
    output.replaceChildren();
    submit.disabled = true;
    try {
      const response = await fetch(revealForm.action, {
        method: "POST",
        body: new FormData(revealForm),
        credentials: "same-origin",
        cache: "no-store",
        headers: { Accept: "application/json" },
      });
      const data = await response.json();
      password.value = "";
      if (!response.ok || typeof data.username !== "string" || typeof data.password !== "string") {
        status.textContent = response.status === 403 ? "Acesso ou reautenticação negada." : "Não foi possível revelar a credencial.";
        status.hidden = false;
        return;
      }
      const usernameLabel = document.createElement("strong");
      usernameLabel.textContent = "Usuário";
      const usernameValue = document.createElement("p");
      usernameValue.textContent = data.username;
      const passwordLabel = document.createElement("strong");
      passwordLabel.textContent = "Senha";
      const passwordValue = document.createElement("p");
      passwordValue.textContent = data.password;
      output.append(usernameLabel, usernameValue, passwordLabel, passwordValue);
      output.hidden = false;
      status.textContent = "Credencial revelada temporariamente. Feche o diálogo para limpar os dados.";
      status.hidden = false;
    } catch {
      password.value = "";
      status.textContent = "Não foi possível concluir a solicitação.";
      status.hidden = false;
    } finally {
      submit.disabled = false;
    }
  });

  window.addEventListener("pagehide", clearCredentialInputs, { once: true });
})();
