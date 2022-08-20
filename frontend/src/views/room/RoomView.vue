<template>
  <div v-if="is_loading"><h1>loading....</h1></div>
  <main v-else class="profile-page layout layout--2">
    <!-- <pre>{{ room_details }}</pre> -->
    <!-- <pre>{{ host }}</pre> -->
    <div class="container">
      <!-- Room Start -->
      <div class="room">
        <div class="room__top">
          <div class="room__topLeft">
            <a
              data-toggle="modal"
              data-target="#exampleModalCenter"
              @click="$router.go(-1)"
            >
              <svg
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 32 32"
              >
                <title>arrow-left</title>
                <path
                  d="M13.723 2.286l-13.723 13.714 13.719 13.714 1.616-1.611-10.96-10.96h27.625v-2.286h-27.625l10.965-10.965-1.616-1.607z"
                ></path>
              </svg>
            </a>
            <h3>Study Room</h3>
          </div>

          <div
            class="room__topRight"
            v-if="room_details?.room_host?.id == $store.state.activeUser.id"
          >
            <router-link
              :to="{
                name: 'update-room',
                params: { roomid: room_details.id },
              }"
            >
              <span class="material-symbols-outlined" style="color: white">
                edit_note
              </span>
            </router-link>
            <a href="#myModal" class="trigger-btn" data-toggle="modal">
              <span class="material-symbols-outlined" style="color: white">
                delete
              </span>
            </a>
          </div>
        </div>
        <div class="room__box scroll">
          <div class="room__header scroll">
            <div class="room__info">
              <h3>{{ room_details.name }}</h3>
              <span> {{ dateHumanize(room_details.created) }}</span>
            </div>
            <div class="room__hosted">
              <p>Hosted By</p>
              <router-link
                :to="{
                  name: 'profile',
                  params: { uuid: host?.uuid ? host.uuid : 222 },
                }"
                class="room__author"
              >
                <div class="avatar avatar--small">
                  <img
                    :src="
                      host?.avator
                        ? host.avator
                        : 'https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png'
                    "
                  />
                </div>
                <span>@{{ host.name }}</span>
              </router-link>
            </div>
            <div class="room__details" style="color: black">
              {{ room_details.description }}
            </div>
            <div class="image-card-container">
              <div class="card image-card">
                <img
                  class="card-img-top card-img"
                  :src="
                    room_details.room_image
                      ? room_details.room_image
                      : 'https://www.lighthouselabs.ca/uploads/post/open_graph_image/414/JavaScript-Uses-Cases-Programming-Language-.jpg'
                  "
                  alt="room_image"
                />
              </div>
            </div>
            <span class="room__topics">{{ room_details?.topic?.name }}</span>
          </div>

          <div class="room__conversation">
            <div class="threads scroll" id="room-chat-list">
              <div
                v-for="message in message_set"
                :key="message.id"
                class="thread"
                id="chatLog"
              >
                <div class="thread__top">
                  <div class="thread__author">
                    <router-link
                      :to="{
                        name: 'profile',
                        params: { uuid: $store.state.activeUser.uuid },
                      }"
                      class="thread__authorInfo"
                    >
                      <div class="avatar avatar--small">
                        <img :src="message.user.avator" alt="user_profile" />
                      </div>
                      <span>@{{ message?.user.username }}</span>
                    </router-link>
                    <span class="thread__date">{{
                      dateHumanize(message.created)
                    }}</span>
                  </div>

                  <a
                    v-if="message.user.id == $store.state.activeUser.id"
                    href="#myModal"
                    class="trigger-btn"
                    data-toggle="modal"
                  >
                    <div class="thread__delete">
                      <svg
                        version="1.1"
                        xmlns="http://www.w3.org/2000/svg"
                        width="32"
                        height="32"
                        viewBox="0 0 32 32"
                      >
                        <title>remove</title>
                        <path
                          d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"
                        ></path>
                      </svg>
                    </div>
                  </a>
                </div>
                <div class="thread__details">{{ message.body }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="room__message">
          <form action="" method="POST" class="room_message_form_control">
            <input
              name="body"
              id="chatMessageInput"
              placeholder="Write your message here..."
              v-model="message_input_value"
            />
            <div class="room_msg_input-group-append">
              <button
                @click="postMessageToWebSocket()"
                class="btn"
                id="chatMessageSend"
                type="button"
              >
                Send
              </button>
            </div>
          </form>
        </div>
      </div>
      <!-- Room End -->

      <!--   Start -->
      <div class="participants">
        <h3 class="participants__top">
          Participants
          <span>({{ room_participants.length }} Joined)</span>
        </h3>
        <!-- <pre>{{ room_details.participants }}</pre> -->
        <div
          v-for="participant in room_participants"
          :key="participant.id"
          id="participants_list"
        >
          <!-- <pre>{{ participant }}</pre> -->
          <div class="participants__list scroll" id="participants_list">
            <router-link
              :to="{
                name: 'profile',
                params: { uuid: participant.uuid },
              }"
              class="participant"
            >
              <div class="avatar avatar--medium">
                <img
                  :src="
                    participant.avator
                      ? participant?.avator
                      : 'https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png'
                  "
                />
              </div>
              <p>
                {{ participant.name }}
                <span>@{{ participant.name }}</span>
              </p>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <ConfirmationComponentVue />
    <!-- <room-from-model /> -->
  </main>
</template>
<script>
import $ from "jquery";
import moment from "moment";
import axios from "../../axios";
import ConfirmationComponentVue from "../../components/ConfirmationComponent.vue";
import RoomFormVue from "../../components/RoomForm.vue";
export default {
  name: "RoomView",
  components: {
    "room-form-model": RoomFormVue,
    ConfirmationComponentVue,
  },
  data() {
    return {
      is_loading: false,
      room_details: [],
      room_participants: [],
      host: [],
      message_set: [],
      connection: null,
      message_connection: null,
      message_input_value: "",
    };
  },

  methods: {
    dateHumanize(date) {
      return moment(date).fromNow();
    },
    fetchRoomDetails() {
      this.is_loading = true;
      axios.get(`/api/room/${this.$route.params.roomid}/`).then((res) => {
        console.log("picked room details data", res.data);
        this.room_details = res.data;
        this.room_participants = res.data.participants;
        this.host = res.data.room_host;
        this.message_set = res.data.messages.message_set;
        this.is_loading = false;
      });
    },
    async createRoomNewMessage(data) {
      await axios
        .post("/api/room-message/", data, {
          headers: {
            //application json
          },
        })
        .then((res) => {
          console.log("New Room Message reponse", res.data);
        });
      // return `<div class="thread">
      //         <div class="thread__top">
      //             <div class="thread__author">
      //                 <a href="#" class="thread__authorInfo">
      //                     <div class="avatar avatar--small">
      //                         <img src=${data.avator}/>
      //                     </div>
      //                     <span>${data.username}</span>
      //                 </a>
      //                 <span class="thread__date">${data.created}|timesince ago</span>
      //             </div>
      //                 <a href="{% url 'delete-message' ${data.message_id} %}">
      //                     <div class="thread__delete">
      //                         <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
      //                             <title>remove</title>
      //                             <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
      //                         </svg>
      //                     </div>
      //                 </a>
      //         </div>
      //         <div class="thread__details" id = "chatLog" >
      //             ${data.body}
      //         </div>
      //     </div>`;
    },
    postMessageToWebSocket() {
      if (this.message_input_value === 0) return;
      this.connection.send(
        JSON.stringify({
          command: "NEW_MSG",
          message: this.message_input_value,
          userid: this.$store.state.activeUser.id,
          username: this.$store.state.activeUser.username,
          roomid: this.$route.params.roomid,
        })
      );
    },
  },
  async mounted() {
    await this.fetchRoomDetails();
  },
  created() {
    // this.connection = new WebSocket(
    //   `${import.meta.env.VITE_WS_ENDPOINT}ws/notification/`
    // );
    this.connection = new WebSocket(
      `${import.meta.env.VITE_WS_ENDPOINT}ws/room/${this.$route.params.roomid}/`
    );

    this.connection.onopen = (event) => {
      console.log("Successfully connected to the WebSocket.");
    };
    this.connection.onclose = (event) => {
      console.log(
        "WebSocket connection closed unexpectedly. Trying to reconnect in 2s..."
      );
      setTimeout(function () {
        console.log("Reconnecting...");
        this.created();
      }, 2000);
    };

    this.connection.onmessage = (e) => {
      console.log("on message");
      const data = JSON.parse(e.data);
      console.log("group channel data===>", data);
      switch (data["command"]) {
        case "LOAD_CHAT_MSG":
          console.log("Group message loadded", data.message);
          break;
        case "NEW_MSG":
          console.log("new message", data.message);
          this.createRoomNewMessage(data);
          // $("#room-chat-list").append(createRoomNewMessage(data.message));

          break;
        case "PARTICIPANTS_ADDED":
          console.log("participants added ", data.message);
          $("#participants_list").append(createParticipants(data.message));
          break;
        default:
          console.error("Unknown message type!");
          break;
      }

      // // scroll 'chatLog' to the bottom
      // chatLog.scrollTop = chatLog.scrollHeight;
      // console.log("chat log", chatLog);
    };
  },
};
</script>
<style></style>
