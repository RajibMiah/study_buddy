/* Study Buddy — realtime room chat client. */
(function () {
  "use strict";

  var mount = document.getElementById("chat-scroll");
  if (!mount) return;

  var roomId = mount.dataset.roomId;
  var currentUserId = mount.dataset.userId || "";
  var form = document.getElementById("chat-form");
  var input = document.getElementById("chat-input");
  var scheme = location.protocol === "https:" ? "wss" : "ws";
  var socket = null;
  var retry = 0;

  function scrollToEnd() { mount.scrollTop = mount.scrollHeight; }
  scrollToEnd();

  function render(msg) {
    var mine = String(msg.user_id) === String(currentUserId);
    var wrap = document.createElement("div");
    wrap.className = "msg" + (mine ? " is-me" : "");
    var avatar = msg.avatar
      ? '<img class="avatar avatar--sm" src="' + msg.avatar + '" alt="">'
      : '<span class="avatar avatar--sm"></span>';
    wrap.innerHTML =
      avatar +
      '<div><div class="msg__meta"><b></b><time></time></div>' +
      '<div class="msg__bubble"><div class="msg__body"></div></div></div>';
    wrap.querySelector("b").textContent = "@" + msg.username;
    wrap.querySelector("time").textContent = msg.created || "just now";
    wrap.querySelector(".msg__body").textContent = msg.body;
    mount.appendChild(wrap);
    scrollToEnd();
  }

  function connect() {
    socket = new WebSocket(scheme + "://" + location.host + "/ws/room/" + roomId + "/");

    socket.onopen = function () { retry = 0; if (input) input.disabled = false; };
    socket.onmessage = function (e) {
      try { render(JSON.parse(e.data)); } catch (err) {}
    };
    socket.onclose = function (e) {
      if (input) input.disabled = true;
      if (e.code === 4401) {
        if (window.sbToast) window.sbToast("Sign in to join the conversation.", "warning");
        return;
      }
      retry += 1;
      if (retry <= 5) setTimeout(connect, Math.min(1000 * retry, 5000));
    };
  }
  connect();

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var body = (input.value || "").trim();
      if (!body || !socket || socket.readyState !== WebSocket.OPEN) return;
      socket.send(JSON.stringify({ command: "NEW_MESSAGE", body: body }));
      input.value = "";
      input.focus();
    });
  }
})();
