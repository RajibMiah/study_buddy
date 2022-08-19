<template>
  <div class="activities__container">
    <div class="activities__header">
      <h2>Room Activities</h2>
    </div>
    <div
      v-if="this.$route.params.uuid == this.$store.state.activeUser.uuid"
      class="activities__container__inner"
    >
      <!-- <pre>{{ data }}</pre> -->
      <div class="activities" v-for="data in room_activity">
        <div class="activities__box">
          <div class="activities__boxHeader roomListRoom__header">
            <router-link
              :to="{
                name: 'profile',
                params: { uuid: data.user.uuid },
              }"
              class="roomListRoom__author"
            >
              <div class="avatar avatar--small">
                <img :src="data.user.avator" />
              </div>
              <p>
                {{ data.user.username }}
                <span>{{ dateHumanize(data.created) }}</span>
              </p>
            </router-link>
            <div class="roomListRoom__actions">
              <a href="#myModal" class="trigger-btn" data-toggle="modal">
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
          <div class="activities__boxContent">
            <p>
              replied to post “<router-link
                :to="{
                  name: 'room',
                  params: { roomid: data.room.id },
                }"
              >
                {{ data.room.name }}</router-link
              >
            </p>
            <div class="activities__boxRoomContent">{{ data.body }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="scroll-marker"></div>
  </div>
  <ConfirmationComponentVue />
</template>
<script>
import moment from "moment";
import ConfirmationComponentVue from "./ConfirmationComponent.vue";

export default {
  name: "ActivityComponent",
  props: ["room_activity"],
  components: {
    ConfirmationComponentVue,
  },
  methods: {
    dateHumanize(date) {
      return moment(date).fromNow();
    },
  },
};
</script>
