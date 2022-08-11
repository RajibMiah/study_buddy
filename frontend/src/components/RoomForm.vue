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
                  <span class="material-symbols-outlined"> arrow_back </span>
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
