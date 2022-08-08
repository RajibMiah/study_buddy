<template>
  <div v-if="is_loading"><h1>loading....</h1></div>
  <main v-else class="profile-page layout layout--2">
    <pre>{{ room_details }}</pre>
    <div class="container">
      <!-- Room Start -->
      <div class="room">
        <div class="room__top">
          <div class="room__topLeft">
            <a>
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

          <div class="room__topRight">
            <a>
              <svg
                enable-background="new 0 0 24 24"
                height="32"
                viewBox="0 0 24 24"
                width="32"
                xmlns="http://www.w3.org/2000/svg"
              >
                <title>edit</title>
                <g>
                  <path
                    d="m23.5 22h-15c-.276 0-.5-.224-.5-.5s.224-.5.5-.5h15c.276 0 .5.224.5.5s-.224.5-.5.5z"
                  />
                </g>
                <g>
                  <g>
                    <path
                      d="m2.5 22c-.131 0-.259-.052-.354-.146-.123-.123-.173-.3-.133-.468l1.09-4.625c.021-.09.067-.173.133-.239l14.143-14.143c.565-.566 1.554-.566 2.121 0l2.121 2.121c.283.283.439.66.439 1.061s-.156.778-.439 1.061l-14.142 14.141c-.065.066-.148.112-.239.133l-4.625 1.09c-.038.01-.077.014-.115.014zm1.544-4.873-.872 3.7 3.7-.872 14.042-14.041c.095-.095.146-.22.146-.354 0-.133-.052-.259-.146-.354l-2.121-2.121c-.19-.189-.518-.189-.707 0zm3.081 3.283h.01z"
                    />
                  </g>
                  <g>
                    <path
                      d="m17.889 10.146c-.128 0-.256-.049-.354-.146l-3.535-3.536c-.195-.195-.195-.512 0-.707s.512-.195.707 0l3.536 3.536c.195.195.195.512 0 .707-.098.098-.226.146-.354.146z"
                    />
                  </g>
                </g>
              </svg>
            </a>
            <a>
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
            </a>
          </div>
        </div>
        <div class="room__box scroll">
          <div class="room__header scroll">
            <div class="room__info">
              <h3>{{ room_details.name }}</h3>
              <span> {{ room_details.created }} ago</span>
            </div>
            <div class="room__hosted">
              <p>Hosted By</p>
              <router-link
                :to="{
                  name: 'profile',
                  params: { uuid: 'uiijasdjif-0021sf-2121 ' },
                }"
                class="room__author"
              >
                <div class="avatar avatar--small">
                  <img
                    :src="
                      room_details.room_host.avator
                        ? room_details.room_host?.avator
                        : 'https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png'
                    "
                  />
                </div>
                <span>@{{ room_details?.room_host?.name }}</span>
              </router-link>
            </div>
            <div class="room__details" style="color: black">
              {{ room_details.description }}
            </div>
            <span class="room__topics">{{ room_details?.topic?.name }}</span>
          </div>

          <div class="room__conversation">
            <div class="threads scroll" id="room-chat-list">
              <div class="thread" id="chatLog">
                <div class="thread__top">
                  <div class="thread__author">
                    <a href="#" class="thread__authorInfo">
                      <div class="avatar avatar--small">
                        <img src="../assets/images/user.png" />
                      </div>
                      <span>@Rajib</span>
                    </a>
                    <span class="thread__date">20 minite ago</span>
                  </div>

                  <a href="#">
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
                <div class="thread__details">message</div>
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
          <span>({{ room_paticipants.length }} Joined)</span>
        </h3>
        <!-- <pre>{{ room_paticipants }}</pre> -->
        <div
          v-for="participant in room_paticipants"
          :key="participant.id"
          class="participants__list scroll"
          id="participants_list"
        >
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
        <!-- <div class="col-12 col-md-4">
          <label for="onlineUsers">Online users</label>
          <select
            multiple
            class="form-control"
            id="onlineUsersSelector"
          ></select>
        </div> -->
      </div>

      <!--  End -->
    </div>
    <!-- <script src="script.js"></script> -->
  </main>
</template>
<script>
import axios from "../../axios";
export default {
  name: "RoomView",
  data() {
    return {
      is_loading: false,
      room_details: [],
      room_paticipants: [],
    };
  },

  // Methods are functions that mutate state and trigger updates.
  // They can be bound as event listeners in templates.
  methods: {
    fetchRoomDetails() {
      this.is_loading = true;
      axios.get(`room/${this.$route.params.roomid}`).then((res) => {
        console.log("picked room details data", res.data);
        this.room_details = res.data;
        this.room_paticipants = res.data.participants;
        this.is_loading = false;
      });
    },
  },

  // Lifecycle hooks are called at different stages
  // of a component's lifecycle.
  // This function will be called when the component is mounted.
  async mounted() {
    await this.fetchRoomDetails();
  },
};
</script>
<style></style>
