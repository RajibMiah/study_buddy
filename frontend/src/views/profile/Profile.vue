<template>
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
                src="../assets/images/user.png"
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
                    <h3>root</h3>
                  </div>
                </div>
                <div>
                  <div class="profile-user-followers">
                    <h4>@root 10 followers</h4>
                  </div>

                  <div class="btn btn--main btn--pill" id="followers">
                    <a class="follow-span">Follow</a>
                  </div>
                </div>
              </div>
              <div>
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
            <p class="profile__bio">user bio info</p>
          </div>
        </div>
        <FeedComponentVue />
      </div>
      <ActivityComponentVue />
    </div>
  </main>
</template>

<script>
import ActivityComponentVue from "../components/ActivityComponent.vue";
import FeedComponentVue from "../components/FeedComponent.vue";
import TopicComponentVue from "../components/TopicComponent.vue";
export default {
  name: "Profile",
  components: {
    FeedComponentVue,
    ActivityComponentVue,
    TopicComponentVue,
  },
  data: function () {
    return {};
  },
  methods: {},
  computed: {},
};
</script>
<style scoped></style>
