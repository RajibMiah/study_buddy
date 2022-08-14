<template>
  <main class="layout layout--3">
    <div class="container">
      <!-- Topics Start -->
      <TopicComponentVue />
      <!-- Topics End -->

      <div class="roomList">
        <div class="mobile-menu">
          <!-- <form action="#" method="GET" class="header__search">
            <label>
              <svg
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 32 32"
              >
                <title>search</title>
                <path
                  d="M32 30.586l-10.845-10.845c1.771-2.092 2.845-4.791 2.845-7.741 0-6.617-5.383-12-12-12s-12 5.383-12 12c0 6.617 5.383 12 12 12 2.949 0 5.649-1.074 7.741-2.845l10.845 10.845 1.414-1.414zM12 22c-5.514 0-10-4.486-10-10s4.486-10 10-10c5.514 0 10 4.486 10 10s-4.486 10-10 10z"
                ></path>
              </svg>
              <input name="q" placeholder="Search for posts" />
            </label>
          </form> -->
          <div class="mobile-menuItems">
            <a class="btn btn--main btn--pill" href="{% url 'topics' %}"
              >Browse Topics</a
            >
            <a class="btn btn--main btn--pill" href="{% url 'activity' %}"
              >Recent Activities</a
            >
          </div>
        </div>

        <div class="roomList__header">
          <div>
            <h2>Study Rooms</h2>
            <p>{{ available_study_room }} Rooms available</p>
          </div>

          <a
            class="btn btn--main"
            data-toggle="modal"
            data-target="#exampleModalCenter"
          >
            <span class="material-symbols-outlined"> add </span>
            Create Room
          </a>
        </div>
        <!-- START POPUP COMPONENT -->

        <!-- <pre>{{ is_loading }}</pre> -->

        <div
          v-show="!is_loading"
          v-for="feeditem in feed_room_data"
          :key="feeditem.id"
        >
          <FeedComponentVue :data="feeditem" />
        </div>
      </div>

      <div class="top-rated-profile-container">
        <top-profile-component />
        <!-- <activity-component-vue /> -->
      </div>
    </div>
    <room-from-model />
  </main>
</template>

<script>
import axios from "../../axios";
import ActivityComponentVue from "../../components/ActivityComponent.vue";
import FeedComponentVue from "../../components/FeedComponent.vue";
import TopicComponentVue from "../../components/TopicComponent.vue";
import RoomFormVue from "../../components/RoomForm.vue";
import TopProfileComponetVue from "../../components/TopProfileComponet.vue";

export default {
  name: "home",
  components: {
    TopicComponentVue,
    FeedComponentVue,
    ActivityComponentVue,
    "room-from-model": RoomFormVue,
    "top-profile-component": TopProfileComponetVue,
  },
  data() {
    return {
      is_loading: false,
      available_study_room: 0,
      feed_room_data: [],
      router: this.$route.params,
    };
  },

  methods: {
    featchFeedCardData() {
      this.is_loading = true;
      axios.get("api/room/").then((res) => {
        console.log("response", res);
        this.feed_room_data = res.data;
        this.available_study_room = res.data.length;
        this.is_loading = false;
      });
    },
    featchQueryData(query) {
      // console.log("fetached function called with", query);
      this.is_loading = true;
      axios.get("api/room/", { params: { q: query.q } }).then((res) => {
        console.log("response", res);
        this.feed_room_data = res.data;
        this.available_study_room = res.data.length;
        this.is_loading = false;
      });
    },
  },
  watch: {
    $route: async function () {
      if (this.$route.query.q) {
        // console.log("home router has query ", this.$route.query);
        await this.featchQueryData(this.$route.query);
      } else {
        await this.featchFeedCardData();
      }
    },
  },
  // computed: {
  //   route() {
  //     console.log(this.route);
  //   },
  // },

  async mounted() {
    await this.featchFeedCardData();
  },
};
</script>

<style scoped>
.top-rated-profile-container {
  position: sticky;
  height: 95vh;
  top: 13px;
}
</style>
