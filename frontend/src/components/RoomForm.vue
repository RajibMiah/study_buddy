<template>
  <div
    class="modal fade"
    id="exampleModalCenter"
    tabindex="-1"
    role="dialog"
    aria-labelledby="exampleModalCenterTitle"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div>
        <div class="container">
          <div class="layout__box">
            <div class="layout__boxHeader">
              <div class="layout__boxTitle">
                <button
                  type="button"
                  class="close"
                  data-dismiss="modal"
                  aria-label="Close"
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
                </button>
                <h3>Create/Update Study Room</h3>
              </div>
            </div>
            <div class="layout__body">
              <form class="form" action="" method="POST">
                <div class="form__group">
                  <label for="room_topic">Enter a Topic</label>
                  <input
                    required
                    type="text"
                    value=""
                    name="topic"
                    list="topic-list"
                  />
                  <datalist id="topic-list">
                    <select id="room_topic">
                      <option value="">
                        <!-- {{ topic.name }} -->
                      </option>
                    </select>
                  </datalist>
                </div>

                <div class="form__group">
                  <label for="room_name">Room Name</label>
                  <!-- {{ form.name }} -->
                  <input
                    required
                    type="text"
                    value=""
                    name="topic"
                    list="topic-list"
                  />
                </div>
                <div class="form__group">
                  <label for="room_topic">Topic</label>
                  <input
                    required
                    type="text"
                    name="topic"
                    id="room_topic"
                    list="topic-list"
                  />
                  <datalist id="topic-list">
                    <select id="room_topic">
                      <option value="">Select your topic</option>
                      <option value="Python">Python</option>
                      <option value="Django">Django</option>
                    </select>
                  </datalist>
                </div>
                <div class="form__group">
                  <label for="room_description">Room Description</label>
                  <!-- {{ form.description }} -->
                  <input
                    required
                    type="text"
                    value=""
                    name="topic"
                    list="topic-list"
                  />
                </div>

                <div class="form__action">
                  <a class="btn btn--dark" data-dismiss="modal" type="button"
                    >Cancel</a
                  >
                  <button
                    class="btn btn--main btn btn-secondary btn btn-primary"
                    type="submit"
                  >
                    Submit
                  </button>
                  <!-- <div class="modal-footer">
                          <button class="">Close</button>
                          <button type="button">Save changes</button>
                        </div> -->
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "room-form-model",
  components: {},
  data() {
    return {};
  },

  created() {},

  // Methods are functions that mutate state and trigger updates.
  // They can be bound as event listeners in templates.
  methods: {
    featchFeedCardData() {
      this.is_loading = true;
      console.log("router========", this.$router);
      axios.get("api/room/").then((res) => {
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

    // console.log("router q value is", this.$route.params.q);
  },
};
</script>

<style scoped></style>
