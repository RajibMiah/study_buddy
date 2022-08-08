<template>
  <!-- <pre>{{ user_profile }}</pre> -->
  <main class="profile-page layout layout--3">
    <div class="container">
      <div>
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
                    <h4>@{{ user_profile.name }} 10 followers</h4>
                  </div>

                  <div
                    v-if="$route.params.uuid !== $store.state.activeUser.uuid"
                    class="btn btn--main btn--pill"
                    id="followers"
                  >
                    <a class="follow-span">Follow</a>
                  </div>
                </div>
              </div>
              <div class="profile-contact-conatiner">
                <a href="#">
                  <div class="header__user">
                    <button type="button" class="icon-button">
                      <span class="material-symbols-outlined">chat</span>
                    </button>
                  </div>
                </a>
                <a href="#" target="_blank">
                  <div class="header__user">
                    <button type="button" class="icon-button">
                      <span class="material-symbols-outlined">
                        storefront
                      </span>
                    </button>
                  </div>
                </a>
              </div>
              <!-- <p>@{{ user.username }}</p> -->
            </div>

            <!-- <a href="#" class="btn btn--main btn--pill"
              >Edit Profile</a
            >
           -->
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
          <FeedComponentVue :data="feeditem" />
        </div>
      </div>
      <ActivityComponentVue />
    </div>
  </main>
</template>

<script>
import axios from "../../axios";
import ActivityComponentVue from "../../components/ActivityComponent.vue";
import FeedComponentVue from "../../components/FeedComponent.vue";
import TopicComponentVue from "../../components/TopicComponent.vue";
export default {
  name: "Profile",
  components: {
    FeedComponentVue,
    ActivityComponentVue,
    TopicComponentVue,
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
        // this.room_paticipants = res.data.participants;
        this.is_loading = false;
      });
    },
  },
  async mounted() {
    await this.fetchProfileData();
  },
  computed: {},
};
</script>
<style scoped>
.profile-contact-conatiner {
  display: flex;
  text-align: center;
  justify-content: center;
}
</style>
