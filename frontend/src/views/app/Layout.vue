<template>
  <router-view />
</template>

<script>
export default {
  name: "Layout",
};
</script>

<style scoped>
.chat-layout {
  display: flex;
  outline: none !important;
}
.chat-layout .chat-leftbar {
  width: 320px;
  height: 100vh;
  overflow: hidden;
  background-color: #fff;
}
.chat-layout .chat-leftbar .chat-left-headbar {
  padding: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.03);
  position: sticky;
  top: 0;
  background-color: #fff;
  z-index: 1;
}
.chat-layout .chat-leftbar .chat-left-headbar a {
  float: right;
  font-size: 20px;
  color: #4c595f;
}
.chat-layout .chat-leftbar .chat-left-headbar #img-icon {
  width: 29px;
  height: 29px;
  display: flex;
  align-items: center;
  justify-content: unset;
  margin: 7px;
}
.chat-layout .chat-leftbar .chat-left-search {
  padding: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.03);
  position: sticky;
  top: 0;
}
.chat-layout .chat-leftbar .chat-left-search input[type="search"] {
  background-color: rgba(129, 167, 205, 0.1);
  color: #8a98ac;
  font-size: 16px;
  padding-left: 20px;
  border: none;
  border-radius: 3px 0 0 3px;
}
.chat-layout .chat-leftbar .chat-left-search .input-group-append {
  margin-left: 0;
}
.chat-layout .chat-leftbar .chat-left-search .btn {
  background-color: rgba(129, 167, 205, 0.1);
  color: #8a98ac;
  font-size: 18px;
  border-radius: 0 3px 3px 0;
  box-shadow: none;
  z-index: 0;
}
.chat-layout .chat-leftbar .chat-left-search .btn img {
  height: 18px;
  color: #8a98ac;
}
.chat-layout .chat-leftbar .chat-left-body {
  padding-bottom: 109px;
  height: calc(100vh - 100px);
  overflow: auto;
}
.chat-layout .chat-leftbar .chat-left-body .chat-userlist .media {
  display: flex;
  align-items: flex-start;
}
.chat-layout .chat-leftbar .chat-left-body .chat-userlist .media .chat-timing {
  color: #8a98ac;
  float: right;
  font-size: 11px;
  font-weight: 400;
  margin-top: 3px;
}
.chat-layout .chat-leftbar .chat-left-body .chat-userlist .media .user-status {
  position: relative;
  left: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid #fff;
  background-color: #19a299;
}
.chat-layout
  .chat-leftbar
  .chat-left-body
  .chat-userlist
  .media
  .user-status
  ~ img {
  margin-left: -12px;
  height: 40px;
}
.chat-layout .chat-leftbar .chat-left-body .chat-userlist .media img {
  width: 40px;
  margin-right: 10px;
}
.chat-layout .chat-leftbar .chat-left-body .chat-userlist .media .media-body {
  word-break: break-word;
  flex: 1;
}
.chat-layout .chat-leftbar .chat-left-body .chat-userlist .media h5 {
  font-size: 15px;
  margin-bottom: 5px;
  font-weight: 600;
  color: #263a5b;
}
.chat-layout .chat-leftbar .chat-left-body .chat-userlist .media p {
  margin-bottom: 0;
  font-size: 14px;
}
.chat-layout .chat-leftbar .chat-left-body .nav-pills .nav-link {
  padding: 15px !important;
  border-bottom: none !important;
  cursor: pointer;
  color: #8a98ac;
  border-radius: 0;
}
.chat-layout .chat-leftbar .chat-left-body .nav-pills .nav-link .badge {
  font-weight: 600;
}
.chat-layout .chat-leftbar .chat-left-body .nav-pills .nav-link .badge-primary {
  background-color: #19a299;
}
.chat-layout .chat-leftbar .chat-left-body .nav-pills .nav-link:hover {
  background-color: #f1f3f4;
  border-right: 2px solid #19a299;
}
.chat-layout .chat-leftbar .chat-left-body .nav-pills .nav-link.active {
  background-color: #f1f3f4;
  border-right: 2px solid #19a299;
}
.chat-layout .chat-leftbar .chat-left-body .nav-pills .nav-link.active img {
  fill: #f1f3f4;
}
.chat-layout .chat-leftbar .chat-menu {
  background-color: #fff;
  padding: 0 15px;
  border-top: 1px solid rgba(0, 0, 0, 0.03);
  position: fixed;
  width: 320px;
  bottom: 0;
  z-index: 9;
}
.chat-layout .chat-leftbar .chat-menu .nav-pills .nav-link {
  border-radius: 0;
  padding: 18px 0;
}
.chat-layout .chat-leftbar .chat-menu .nav-pills .nav-link.active {
  background-color: #fff;
  border-bottom: 2px solid #19a299;
}
.chat-layout .chat-rightbar {
  flex: 1;
  height: 100vh;
  max-width: calc(100vw - 320px);
  overflow: hidden;
}
.chat-layout .chat-rightbar .chat-details {
  background-color: #fff;
  border-left: 1px solid rgba(0, 0, 0, 0.03);
  border-right: 1px solid rgba(0, 0, 0, 0.03);
  flex: 1;
}
.chat-layout .chat-rightbar .chat-details .chat-head {
  padding: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.03);
}
.chat-layout .chat-rightbar .chat-details .chat-head .user-status {
  position: relative;
  left: 12px;
  margin-left: -12px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid #fff;
  background-color: #19a299;
}
.chat-layout .chat-rightbar .chat-details .chat-head img {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 50%;
}
.chat-layout .chat-rightbar .chat-details .chat-head h5 {
  margin-bottom: 5px;
  font-size: 15px;
}
.chat-layout .chat-rightbar .chat-details .chat-head p {
  font-size: 13px;
  line-height: 1.3;
  margin-bottom: 0 !important;
  margin-top: 0 !important;
}
.chat-layout .chat-rightbar .chat-details .chat-head .list-inline li button {
  outline: none;
  border: 0;
  background-color: transparent;
}
.chat-layout
  .chat-rightbar
  .chat-details
  .chat-head
  .list-inline
  li
  button
  img {
  height: 20px;
}
.chat-layout .chat-rightbar .chat-details .chat-body {
  background-image: url("http://themesbox.in/admin-templates/gappa/html/light/assets/images/authentication-bg.jpg");
  padding: 30px 30px 41px;
  height: calc(100vh - 138px);
  overflow: auto;
}
.chat-layout .chat-rightbar .chat-details .chat-body .chat-message {
  margin-bottom: 15px;
}
.chat-layout .chat-rightbar .chat-details .chat-body .chat-message.right {
  text-align: right;
}
.chat-layout .chat-rightbar .chat-details .chat-body .chat-message.right .text {
  background-color: #19a299;
  color: #ffffff;
}
.chat-layout
  .chat-rightbar
  .chat-details
  .chat-body
  .chat-message.right
  .text:after {
  content: " ";
  position: absolute;
  width: 0;
  height: 0;
  left: auto;
  right: -10px;
  top: auto;
  bottom: 0;
  border: 6px solid #19a299;
  border-color: transparent transparent #19a299 #19a299;
}
.chat-layout .chat-rightbar .chat-details .chat-body .chat-message.left {
  text-align: left;
}
.chat-layout .chat-rightbar .chat-details .chat-body .chat-message.left .text {
  background-color: #ffffff;
}
.chat-layout
  .chat-rightbar
  .chat-details
  .chat-body
  .chat-message.left
  .text:after {
  content: " ";
  position: absolute;
  width: 0;
  height: 0;
  left: -10px;
  right: auto;
  top: auto;
  bottom: 0;
  border: 6px solid #ffffff;
  border-color: transparent #ffffff #ffffff transparent;
}
.chat-layout .chat-rightbar .chat-details .chat-body .chat-message .text {
  padding: 5px 10px;
  display: inline-block;
  border-radius: 3px;
  position: relative;
}
.chat-layout .chat-rightbar .chat-details .chat-body .chat-message .meta {
  margin-top: 5px;
  font-size: 13px;
  color: #4c595f;
}
.chat-layout .chat-rightbar .chat-details .chat-bottom {
  background-color: #ffffff;
  padding: 15px 30px;
  border-top: 1px solid rgba(0, 0, 0, 0.03);
  border-left: 1px solid rgba(0, 0, 0, 0.03);
  position: fixed;
  bottom: 0;
  left: 320px;
  right: 0;
}
.chat-layout
  .chat-rightbar
  .chat-details
  .chat-bottom
  .chat-messagebar
  input[type="text"] {
  background-color: transparent;
  color: #8a98ac;
  font-size: 16px;
  border: none;
  border-radius: 0;
}
li.media {
  display: flex;
  align-items: flex-start;
}
li.media .media-body {
  word-break: break-word;
  flex: 1;
}
.form-control:focus {
  box-shadow: none !important;
}
.pulse {
  height: 270px;
  width: 270px;
  background-color: #19a299 !important;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
.pulse img {
  border-radius: 50% !important;
  height: 250px;
  width: 250px;
}
.pulse:before {
  content: "";
  position: absolute;
  border: 1px solid #19a299;
  width: calc(100% + 40px);
  height: calc(100% + 40px);
  border-radius: 50%;
  animation: pulse 1s linear infinite;
}
.pulse:after {
  content: "";
  position: absolute;
  border: 1px solid #19a299;
  width: calc(100% + 40px);
  height: calc(100% + 40px);
  border-radius: 50%;
  animation: pulse 1s linear infinite;
  animation-delay: 0.3s;
}
@keyframes pulse {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  50% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}
#remoteVideo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  object-fit: contain;
  transform: rotateY(180deg);
}
#localVideo {
  position: fixed;
  transform: rotateY(180deg);
  right: 0;
  top: 0;
  width: 20vw;
  height: 20vh;
  object-fit: contain;
  z-index: 999;
}
.call-controls {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
}
</style>
