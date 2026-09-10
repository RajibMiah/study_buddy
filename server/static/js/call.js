/* Study Buddy — WebRTC mesh video call for a study room. */
(function () {
  "use strict";

  var root = document.getElementById("call");
  if (!root) return;

  var roomId = root.dataset.roomId;
  var iceServers;
  try { iceServers = JSON.parse(root.dataset.ice || "[]"); } catch (e) { iceServers = []; }

  var startBtn = document.getElementById("call-start");
  var leaveBtn = document.getElementById("call-leave");
  var micBtn = document.getElementById("call-mic");
  var camBtn = document.getElementById("call-cam");
  var stage = document.getElementById("call-stage");
  var statusEl = document.getElementById("call-status");

  var socket = null;
  var myId = null;
  var localStream = null;
  var peers = {}; // peer_id -> { pc, name }

  function setStatus(text) { if (statusEl) statusEl.textContent = text; }

  function tile(id, label, muted) {
    var el = document.getElementById("tile-" + id);
    if (el) return el.querySelector("video");
    el = document.createElement("figure");
    el.className = "call-tile";
    el.id = "tile-" + id;
    el.innerHTML = '<video autoplay playsinline' + (muted ? " muted" : "") + '></video><figcaption></figcaption>';
    el.querySelector("figcaption").textContent = label;
    stage.appendChild(el);
    return el.querySelector("video");
  }

  function dropTile(id) {
    var el = document.getElementById("tile-" + id);
    if (el) el.remove();
  }

  function send(obj) {
    if (socket && socket.readyState === WebSocket.OPEN) socket.send(JSON.stringify(obj));
  }

  function makeConnection(peerId, name, initiator) {
    if (peers[peerId]) return peers[peerId].pc;
    var pc = new RTCPeerConnection({ iceServers: iceServers });
    peers[peerId] = { pc: pc, name: name || "Guest" };

    localStream.getTracks().forEach(function (t) { pc.addTrack(t, localStream); });

    pc.onicecandidate = function (e) {
      if (e.candidate) send({ type: "signal", target: peerId, data: { candidate: e.candidate } });
    };
    pc.ontrack = function (e) {
      tile(peerId, peers[peerId].name, false).srcObject = e.streams[0];
      setStatus(Object.keys(peers).length + " connected");
    };
    pc.onconnectionstatechange = function () {
      if (pc.connectionState === "failed" || pc.connectionState === "closed") teardownPeer(peerId);
    };

    if (initiator) {
      pc.createOffer()
        .then(function (o) { return pc.setLocalDescription(o); })
        .then(function () { send({ type: "signal", target: peerId, data: { description: pc.localDescription } }); });
    }
    return pc;
  }

  function teardownPeer(peerId) {
    var entry = peers[peerId];
    if (!entry) return;
    try { entry.pc.close(); } catch (e) {}
    delete peers[peerId];
    dropTile(peerId);
    setStatus(Object.keys(peers).length ? Object.keys(peers).length + " connected" : "Waiting for others…");
  }

  function onSignal(from, name, data) {
    var pc = peers[from] ? peers[from].pc : makeConnection(from, name, false);
    if (data.description) {
      pc.setRemoteDescription(data.description).then(function () {
        if (data.description.type === "offer") {
          return pc.createAnswer()
            .then(function (a) { return pc.setLocalDescription(a); })
            .then(function () { send({ type: "signal", target: from, data: { description: pc.localDescription } }); });
        }
      }).catch(function (e) { console.warn("signal error", e); });
    } else if (data.candidate) {
      pc.addIceCandidate(data.candidate).catch(function () {});
    }
  }

  function connect() {
    var scheme = location.protocol === "https:" ? "wss" : "ws";
    socket = new WebSocket(scheme + "://" + location.host + "/ws/call/" + roomId + "/");

    socket.onmessage = function (e) {
      var m = JSON.parse(e.data);
      if (m.type === "welcome") { myId = m.peer_id; send({ type: "join" }); setStatus("Waiting for others…"); }
      else if (m.type === "peer-join") { makeConnection(m.peer_id, m.name, true); }
      else if (m.type === "signal") { onSignal(m.peer_id, m.name, m.data || {}); }
      else if (m.type === "peer-leave") { teardownPeer(m.peer_id); }
    };
    socket.onclose = function (e) {
      if (e.code === 4401 && window.sbToast) window.sbToast("Sign in to start a call.", "warning");
    };
  }

  function start() {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then(function (stream) {
        localStream = stream;
        tile("local", "You", true).srcObject = stream;
        root.classList.add("is-live");
        startBtn.hidden = true;
        leaveBtn.hidden = micBtn.hidden = camBtn.hidden = false;
        connect();
      })
      .catch(function () {
        if (window.sbToast) window.sbToast("Camera and microphone access is required.", "error");
      });
  }

  function leave() {
    send({ type: "leave" });
    Object.keys(peers).forEach(teardownPeer);
    if (localStream) localStream.getTracks().forEach(function (t) { t.stop(); });
    if (socket) socket.close();
    localStream = socket = null;
    stage.innerHTML = "";
    root.classList.remove("is-live");
    startBtn.hidden = false;
    leaveBtn.hidden = micBtn.hidden = camBtn.hidden = true;
    setStatus("");
  }

  function toggleTrack(kind, btn) {
    if (!localStream) return;
    var track = kind === "audio" ? localStream.getAudioTracks()[0] : localStream.getVideoTracks()[0];
    if (!track) return;
    track.enabled = !track.enabled;
    btn.classList.toggle("is-off", !track.enabled);
    btn.setAttribute("aria-pressed", String(!track.enabled));
  }

  startBtn && startBtn.addEventListener("click", start);
  leaveBtn && leaveBtn.addEventListener("click", leave);
  micBtn && micBtn.addEventListener("click", function () { toggleTrack("audio", micBtn); });
  camBtn && camBtn.addEventListener("click", function () { toggleTrack("video", camBtn); });
  window.addEventListener("beforeunload", function () { if (socket) leave(); });
})();
