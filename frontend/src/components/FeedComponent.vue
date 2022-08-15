<template>
  <!-- <pre>{{ data }}</pre> -->
  <div class="roomListRoom">
    <router-link
      :to="{ name: 'room', params: { roomid: data.id } }"
      class="room-list-link"
    >
      <div>
        <div class="roomListRoom__header">
          <div class="room_detail_container">
            <router-link
              :to="{ name: 'profile', params: { uuid: data.room_host?.uuid } }"
              class="roomListRoom__author"
            >
              <div class="avatar avatar--small">
                <img
                  :src="
                    data.room_host?.avator
                      ? data.room_host?.avator
                      : 'https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png'
                  "
                />
              </div>
              <span>@{{ data.room_host?.name }}</span>
            </router-link>
            <div class="roomListRoom__actions">
              <span>{{ dateHumanize(data.created) }}</span>
            </div>
          </div>
        </div>

        <div class="roomListRoom__content">
          <a href="#">{{ data.name }}</a>
        </div>
      </div>
    </router-link>
    <div class="image-card-container">
      <div class="card image-card">
        <img
          class="card-img-top card-img"
          :src="
            data.room_image
              ? data.room_image
              : 'https://www.lighthouselabs.ca/uploads/post/open_graph_image/414/JavaScript-Uses-Cases-Programming-Language-.jpg'
          "
          alt="room_image"
        />
      </div>
    </div>
    <div class="roomListRoom__meta">
      <!-- up and down vote section -->
      <!-- {{ data?.is_votted[0].upvote_boolean }} -->

      <div class="vote-section">
        <div clsss="vote-btn-section">
          <div type="buton" class="vote-btn" @click="thumb_up_func(data)">
            <span
              class="material-symbols-outlined"
              :class="[
                data?.is_votted[0]?.upvote_boolean ? 'vote-style ' : null,
              ]"
            >
              thumb_up
            </span>
            <span class="vote-span">{{
              data.vote?.upvote > 0 && data.vote?.upvote !== null
                ? data.vote?.upvote
                : 0
            }}</span>
          </div>
        </div>
        <div class="vote-btn-section">
          <div type="button" class="vote-btn" @click="thumb_down_func(data)">
            <span
              class="material-symbols-outlined"
              :class="[
                data?.is_votted[0]?.downvote_boolean ? 'vote-style ' : null,
              ]"
            >
              thumb_down_off
            </span>
            <span class="vote-span">{{
              data.vote?.downvote > 0 && data.vote?.downvote !== null
                ? data.vote?.downvote
                : 0
            }}</span>
          </div>
        </div>
      </div>
      <div class="room_participation_container">
        <div class="room_commects_container">
          <span class="material-symbols-outlined"> comment </span>
          <span>{{ data.total_messages }} comments</span>
        </div>
      </div>

      <div class="roomListRoom__joined">
        <span class="material-symbols-outlined"> group </span>
        {{ data.participants.length }} Joined
      </div>
      <div class="roomListRoom__joined">
        <p class="roomListRoom__topic">{{ data.topic?.name }}</p>
      </div>
    </div>
  </div>
</template>
<script>
import moment from "moment";
import axios from "../axios";
export default {
  name: "FeedComponent",
  props: ["data"],
  data() {
    return {
      is_loading: false,
      _upvote: 0,
      _downvote: 0,
      thumb_value: {
        upvote: 0,
        downvote: 0,
        user: 0,
        room: 0,
      },
    };
  },
  methods: {
    dateHumanize(date) {
      return moment(date).fromNow();
    },
    thumb_up_func(data, upvote) {
      if (
        data?.is_votted.length > 0 &&
        (data?.is_votted[0].upvote_boolean ||
          data?.is_votted[0].downvote_boolean)
      ) {
        axios
          .delete(`api/votes/${data.is_votted[0].id}`, {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((res) => {
            console.log("data is delted", res);
          });
      } else {
        console.log("pass data", data);
        const vote_data = {
          upvote: 1,
          upvote_boolean: true,
          user: data.room_host.id,
          room: data.id,
        };
        console.log("vote_data", vote_data);
        axios
          .post("api/votes/", JSON.stringify(vote_data), {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((res) => {
            console.log("response", res);
          });
      }
    },
    thumb_down_func(id) {
      console.log("thumb down id", id);
    },
  },
  async mounted() {},
};
</script>

<style scoped>
.room-list-link {
  width: 100%;
}
.vote-section {
  display: flex;
}
.vote-btn-section {
  padding: 0px 7px 0px 7px;
}
.vote-btn {
  display: flex;
  cursor: pointer;
}
.vote-span {
  padding-left: 7px;
}
.room_commects_container {
  justify-content: center;
  color: var(--color-dark-medium);
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.4rem;
  font-weight: 500;
}
.room_participation_container {
  display: flex;
}
.room_detail_container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}
.image-card-container {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 0px 7px 7px 0px;
}
.image-card {
  /* height: 23rem; */
  width: 100%;
}
.card-img {
  height: inherit;
}
.vote-style {
  color: orange;
}
</style>
