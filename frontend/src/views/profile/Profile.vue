<template>
  <!-- <pre>{{ user_profile }}</pre> -->
  <div v-if="is_loading">..</div>
  <main v-else class="profile-page layout layout--3">
    <div class="container">
      <div class="top-rated-profile-container">
        <TopicComponentVue />
      </div>

      <div class="roomList">
        <div class="profile">
          <div class="profile__avatar">
            <div class="avatar avatar--large active">
              <img
                id="profile-img"
                :src="
                  user_profile.avator
                    ? user_profile.avator
                    : 'https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png'
                "
                class="online"
                alt=""
              />
            </div>
          </div>
          <div class="profile__info">
            <div class="profile_info_container">
              <div>
                <div>
                  <div>
                    <h3>{{ user_profile.username }}</h3>
                  </div>
                </div>
                <div>
                  <div class="profile-user-followers">
                    <h4>
                      @{{ user_profile.name }}
                      {{ user_profile?.follows_list?.total_followers }}
                      followers
                    </h4>
                  </div>
                  <div style="display: flex; justify-content: center">
                    <div
                      v-if="
                        $route.params.uuid !== $store.state.activeUser.uuid &&
                        !user_profile?.follows_list?.is_followed
                      "
                      class="btn btn--main btn--pill"
                      id="followers"
                      @click="
                        followingBtn(
                          (user_id = user_profile?.id),
                          null,
                          user_profile?.follows_list?.is_followed
                        )
                      "
                    >
                      <a class="follow-span">Follow</a>
                    </div>
                    <div
                      v-else-if="user_profile?.follows_list?.is_followed"
                      class="btn btn--main btn--pill"
                      id="followers"
                      @click="
                        followingBtn(
                          (user_id = user_profile?.id),
                          user_profile?.follows_list?.follows,
                          user_profile?.follows_list?.is_followed
                        )
                      "
                    >
                      <a class="follow-span">Unfollow</a>
                    </div>
                    <div
                      v-else
                      class="btn btn--main btn--pill"
                      id="edit-profile"
                    >
                      <router-link
                        :to="{
                          name: 'edit-profile',
                          params: { uuid: $store.state.activeUser.uuid },
                        }"
                        class="follow-span"
                        >Edit Profile</router-link
                      >
                    </div>
                    <div
                      v-if="$route.params.uuid !== $store.state.activeUser.uuid"
                      class="profile-contact-conatiner"
                    >
                      <a href="#">
                        <div class="header__user">
                          <button type="button" class="icon-button">
                            <span class="material-symbols-outlined">chat</span>
                          </button>
                        </div>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="profile__about">
            <h3>About</h3>
            <p class="profile__bio">{{ user_profile.bio }}</p>
          </div>
        </div>
        <div
          v-for="feeditem in user_profile?.user_created_rooms"
          :key="feeditem.id"
        >
          <!-- <pre>{{ feeditem }}</pre> -->
          <FeedComponentVue
            :data="feeditem"
            :thumbUpMethod="thumbUpMethod"
            :thumbDownMethod="thumbDownMethod"
          />
        </div>
      </div>
      <div v-if="this.$route.params.uuid == this.$store.state.activeUser.uuid">
        <ActivityComponentVue :room_activity="user_profile.room_activity" />
      </div>
      <div v-else class="top-rated-profile-container">
        <TopProfileComponetVue />
      </div>
    </div>
  </main>
</template>

<script>
import axios from "../../axios";
import ActivityComponentVue from "../../components/ActivityComponent.vue";
import FeedComponentVue from "../../components/FeedComponent.vue";
import TopicComponentVue from "../../components/TopicComponent.vue";
import TopProfileComponetVue from "../../components/TopProfileComponet.vue";
export default {
  name: "Profile",
  components: {
    FeedComponentVue,
    ActivityComponentVue,
    TopicComponentVue,
    TopProfileComponetVue,
  },
  data: function () {
    return {
      is_loading: false,
      user_profile: [],
      room_paticipants: [],
    };
  },
  methods: {
    fetchProfileData() {
      this.is_loading = true;
      axios.get(`/api/profile/${this.$route.params.uuid}/`).then((res) => {
        console.log("picked profile details data", res.data);
        this.user_profile = res.data;
        this.is_loading = false;
      });
    },
    async thumbUpMethod(data) {
      console.log("thumb up length", data?.is_votted.length);
      console.log("data ===>", data);
      if (data?.is_votted.length > 0) {
        await axios
          .delete(`api/votes/${data.is_votted[0].id}/`, {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((res) => {
            console.log("deleted", res.data);
            data.is_votted = [];
            data.vote.upvote = data.vote.upvote - 1;
          });
      } else {
        let thumb_data = {
          upvote: 1,
          upvote_boolean: true,
          user: this.$store.state.activeUser.id,
          room: data.id,
        };
        await axios
          .post("api/votes/", JSON.stringify(thumb_data), {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((res) => {
            data.is_votted.push(res.data);
            data.vote.upvote = data.vote.upvote + 1;
            console.log("data crated ", data);
          });
      }

      console.log("not called");
    },
    async thumbDownMethod(data) {
      if (data?.is_votted.length > 0) {
        await axios
          .delete(`api/votes/${data.is_votted[0].id}/`, {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((res) => {
            console.log("deleted", res.data);
            data.is_votted = [];
            data.vote.downvote = data.vote.downvote - 1;
          });
      } else {
        let thumb_data = {
          downvote: 1,
          downvote_boolean: true,
          user: this.$store.state.activeUser.id,
          room: data.id,
        };
        await axios
          .post("api/votes/", JSON.stringify(thumb_data), {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((res) => {
            data.is_votted.push(res.data);
            data.vote.downvote = data.vote.downvote + 1;
            console.log("data crated ", data);
          });
      }
    },
    async followingBtn(user_id, follows_data, is_followed) {
      if (is_followed) {
        let get_Following_pk;
        follows_data.map((data) => {
          if (data.following_user_id === this.$store.state.activeUser.id) {
            get_Following_pk = data.id;
          }
        });
        await axios
          .delete(`/api/userfollowing/${get_Following_pk}/`)
          .then((res) => {
            console.log(" delete response", res);
            this.user_profile.follows_list.follows =
              this.user_profile.follows_list.follows.filter(
                (data) =>
                  data.following_user_id != this.$store.state.activeUser.id
              );

            this.user_profile.follows_list.is_followed = false;
            this.user_profile.follows_list.total_followers =
              this.user_profile.follows_list.total_followers - 1;
          });
      } else {
        const data = {
          user_id: user_id,
          following_user_id: this.$store.state.activeUser.id,
        };
        await axios
          .post("/api/userfollowing/", JSON.stringify(data), {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((res) => {
            console.log(" create response response", res);
            // this.$forceUpdate();
            this.user_profile.follows_list.follows.push(res.data);
            this.user_profile.follows_list.is_followed = true;
            this.user_profile.follows_list.total_followers =
              this.user_profile.follows_list.total_followers + 1;
          });
      }
    },
  },
  async mounted() {
    console.log("mount is call");
    await this.fetchProfileData();
  },

  computed: {},
};
</script>
<style scoped>
.top-rated-profile-container {
  position: sticky;
  height: 95vh;
  top: 13px;
}
.profile-contact-conatiner {
  display: flex;
  text-align: center;
  justify-content: center;
}
</style>
