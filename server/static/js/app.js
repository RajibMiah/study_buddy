/* Study Buddy — UI behaviour: theming, menus, toasts. */
(function () {
  "use strict";

  /* ---------------------------- Theme ---------------------------- */
  var STORE_KEY = "sb-theme";
  var root = document.documentElement;

  function stored() {
    try { return localStorage.getItem(STORE_KEY); } catch (e) { return null; }
  }
  function resolved() {
    var t = stored();
    if (t === "light" || t === "dark") return t;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function apply(theme, persist) {
    root.setAttribute("data-theme", theme);
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(theme === "dark"));
      var label = btn.querySelector("[data-theme-label]");
      if (label) label.textContent = theme === "dark" ? "Dark" : "Light";
    });
    if (persist) { try { localStorage.setItem(STORE_KEY, theme); } catch (e) {} }
  }

  apply(resolved(), false);
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if (!stored()) apply(resolved(), false);
  });

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-theme-toggle]");
    if (toggle) {
      apply(root.getAttribute("data-theme") === "dark" ? "light" : "dark", true);
    }
  });

  /* --------------------------- Menus ---------------------------- */
  document.addEventListener("click", function (e) {
    var trigger = e.target.closest("[data-menu-trigger]");
    var openMenus = document.querySelectorAll(".menu.is-open");
    openMenus.forEach(function (m) {
      if (!trigger || !m.contains(trigger)) m.classList.remove("is-open");
    });
    if (trigger) {
      var menu = trigger.closest(".menu");
      if (menu) menu.classList.toggle("is-open");
    }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll(".menu.is-open").forEach(function (m) { m.classList.remove("is-open"); });
    }
  });

  /* -------------------------- Mobile nav ------------------------ */
  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-nav-toggle]")) {
      document.body.classList.toggle("nav-open");
    }
  });

  /* --------------------------- Toasts -------------------------- */
  var ICONS = {
    success: '<path d="M20 6 9 17l-5-5"/>',
    error: '<path d="M18 6 6 18M6 6l12 12"/>',
    warning: '<path d="M12 9v4m0 4h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
    info: '<path d="M12 16v-4m0-4h.01M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0z"/>'
  };

  function dismiss(el) {
    el.classList.add("is-leaving");
    el.addEventListener("animationend", function () { el.remove(); }, { once: true });
  }

  window.sbToast = function (message, level) {
    level = level || "info";
    var tray = document.querySelector(".toast-tray");
    if (!tray) {
      tray = document.createElement("div");
      tray.className = "toast-tray";
      tray.setAttribute("aria-live", "polite");
      document.body.appendChild(tray);
    }
    var el = document.createElement("div");
    el.className = "toast toast--" + level;
    el.setAttribute("role", "status");
    el.innerHTML =
      '<svg class="toast__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' + (ICONS[level] || ICONS.info) + "</svg>" +
      '<div class="toast__msg"></div>' +
      '<button class="toast__close" aria-label="Dismiss">&times;</button>';
    el.querySelector(".toast__msg").textContent = message;
    el.querySelector(".toast__close").addEventListener("click", function () { dismiss(el); });
    tray.appendChild(el);
    setTimeout(function () { if (el.isConnected) dismiss(el); }, 5200);
  };

  // Promote server-rendered Django messages into toasts.
  document.querySelectorAll("[data-toast]").forEach(function (node) {
    window.sbToast(node.dataset.toast, node.dataset.level || "info");
    node.remove();
  });

  /* ---------------------- Skeleton removal --------------------- */
  window.addEventListener("load", function () {
    document.querySelectorAll("[data-skeleton]").forEach(function (s) { s.remove(); });
    document.querySelectorAll("[data-defer]").forEach(function (d) { d.hidden = false; });
  });
})();
