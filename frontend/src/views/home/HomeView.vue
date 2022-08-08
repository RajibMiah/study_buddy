<template>
  <main class="layout layout--3">
    <div class="container">
      <!-- Topics Start -->
      <TopicComponentVue />
      <!-- Topics End -->

      <div class="roomList">
        <div class="mobile-menu">
          <form action="#" method="GET" class="header__search">
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
          </form>
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
            <svg
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              width="32"
              height="32"
              viewBox="0 0 32 32"
            >
              <title>add</title>
              <path
                d="M16.943 0.943h-1.885v14.115h-14.115v1.885h14.115v14.115h1.885v-14.115h14.115v-1.885h-14.115v-14.115z"
              ></path>
            </svg>
            Create Room
          </a>
        </div>
        <!-- START POPUP COMPONENT -->

        <!-- Modal -->
        <div
          class="modal fade"
          id="exampleModalCenter"
          tabindex="-1"
          role="dialog"
          aria-labelledby="exampleModalCenterTitle"
          aria-hidden="true"
        >
          <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLongTitle">
                  Modal title
                </h5>
                <button
                  type="button"
                  class="close"
                  data-dismiss="modal"
                  aria-label="Close"
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">...</div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-dismiss="modal"
                >
                  Close
                </button>
                <button type="button" class="btn btn-primary">
                  Save changes
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- <pre>{{ is_loading }}</pre> -->

        <div
          v-show="!is_loading"
          v-for="feeditem in feed_room_data"
          :key="feeditem.id"
        >
          <FeedComponentVue :data="feeditem" />
        </div>
      </div>

      <!-- Activities Start -->
      <div>
        <activity-component-vue />
      </div>
      <!-- Activities End -->
    </div>
  </main>
</template>

<script>
import axios from "../../axios";
import ActivityComponentVue from "../../components/ActivityComponent.vue";
import FeedComponentVue from "../../components/FeedComponent.vue";
import TopicComponentVue from "../../components/TopicComponent.vue";
export default {
  name: "home",
  components: {
    TopicComponentVue,
    FeedComponentVue,
    ActivityComponentVue,
  },
  data() {
    return {
      is_loading: false,
      available_study_room: 0,
      feed_room_data: [],
    };
  },

  // Methods are functions that mutate state and trigger updates.
  // They can be bound as event listeners in templates.
  methods: {
    featchFeedCardData() {
      this.is_loading = true;
      axios.get("room/").then((res) => {
        console.log("response", res);
        this.feed_room_data = res.data;
        this.available_study_room = res.data.length;
        this.is_loading = false;
      });
    },
  },

  // Lifecycle hooks are called at different stages
  // of a component's lifecycle.
  // This function will be called when the component is mounted.
  async mounted() {
    await this.featchFeedCardData();
  },
};
</script>

<style scoped></style>
