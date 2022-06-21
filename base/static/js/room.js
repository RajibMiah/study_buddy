// chat/static/room.js

console.log("Sanity check from room.js.");

const roomId = JSON.parse(document.getElementById("roomId").textContent);
let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

chatMessageInput.focus();

chatMessageInput.onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter key
    chatMessageSend.click();
  }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function () {
  if (chatMessageInput.value.length === 0) return;

  chatSocket.send(
    JSON.stringify({
      command: "NEW_MSG",
      message: chatMessageInput.value,
    })
  );

  chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {
  chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/room/" + roomId + "/"
  );

  chatSocket.onopen = function (e) {
    console.log("Successfully connected to the WebSocket.");
  };

  chatSocket.onclose = function (e) {
    console.log(
      "WebSocket connection closed unexpectedly. Trying to reconnect in 2s..."
    );
    setTimeout(function () {
      console.log("Reconnecting...");
      connect();
    }, 2000);
  };

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    switch (data["command"]) {
      case "chat_message":
        chatLog.value += data.user + ": " + data.message + "\n"; // new
        break;
      case "NEW_MSG":
        console.log("new message", data.message);
        break;
      default:
        console.error("Unknown message type!");
        break;
    }

    // scroll 'chatLog' to the bottom
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  chatSocket.onerror = function (err) {
    console.log("WebSocket encountered an error: " + err.message);
    console.log("Closing the socket.");
    chatSocket.close();
  };
}
connect();
