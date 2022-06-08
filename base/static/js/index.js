
// console.log("Sanity check from index.js.");

// // focus 'roomInput' when user opens the page
// document.querySelector("#chatMessageInput").focus();

// // submit if the user presses the enter key
// document.querySelector("#chatMessageInput").onkeyup = function(e) {
//     if (e.keyCode === 13) {  // enter key
//         document.querySelector("#roomConnect").click();
//     }
// };

// // redirect to '/room/<roomInput>/'
// document.querySelector("#chatMessageInput").onclick = function() {
//     let roomName = document.querySelector("#roomInput").value;
//     window.location.pathname = "ws/room/" + roomId + "/";
//     console.log(window.location.pathname)
// }

// // redirect to '/room/<roomSelect>/'
// document.querySelector("#roomSelect").onchange = function() {
//     let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
//     window.location.pathname = "room/" + roomId + "/";
//     console.log(window.location.pathname)
// }