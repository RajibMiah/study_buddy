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
    e.preventDefault()
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
  chatLog.scrollTop = chatLog.scrollHeight;
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
      case "LOAD_CHAT_MSG":
        console.log('Group message loadded' , data.message)
        break;
      case "NEW_MSG":
        console.log("new message", data.message);
        $("#room-chat-list").append(createRoomNewMessage(data.message));
        break;
      default:
        console.error("Unknown message type!");
        break;
    }

    // scroll 'chatLog' to the bottom
    chatLog.scrollTop = chatLog.scrollHeight;
    console.log("chat log" ,chatLog)
  };

  chatSocket.onerror = function (err) {
    console.log("WebSocket encountered an error: " + err.message);
    console.log("Closing the socket.");
    chatSocket.close();
  };
}

// $(document).ready(function (e) {
//   console.log("ready on it");
//   var tab = document.getElementsByClassName("scroll");
//   tab.scrollTop = tab.scrollHeight;
// });

const createRoomNewMessage = (data) => {
  return `<div class="thread">
          <div class="thread__top">
              <div class="thread__author">
                  <a href="#" class="thread__authorInfo">
                      <div class="avatar avatar--small">
                          <img src=${data.avator}/>
                      </div>
                      <span>${data.username}</span>
                  </a>
                  <span class="thread__date"> 20 seconds
                      ago</span>
              </div>
                  <a href="#">
                      <div class="thread__delete">
                          <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
                              <title>remove</title>
                              <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
                          </svg>
                      </div>
                  </a>
          </div>
          <div class="thread__details" id="chatLog">
              ${data.body}
          </div>
      </div>`;
};

connect();
