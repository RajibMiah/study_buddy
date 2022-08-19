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
              <span> {{ dateHumanize(room_details.created) }} ago</span>
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
            />
            <div class="room_msg_input-group-append">
              <button class="btn" id="chatMessageSend" type="button">
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
  },
  async mounted() {
    await this.fetchRoomDetails();
  },
};
</script>
<style></style>
