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
      <div class="modal-content">
        <div class="modal-header">
          <div class="layout__boxHeader">
            <div class="layout__boxTitle">
              <!-- <button
                type="button"
                class="close"
                data-dismiss="modal"
                aria-label="Close"
              >
                <span class="material-symbols-outlined"> arrow_back </span>
              </button> -->
              <div class="layout__header_content">
                <h3 style="color: black">Create/Update Study Room</h3>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-body">
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
              <div class="avatar-upload">
                <div class="avatar-edit">
                  <input
                    type="file"
                    id="imageUpload"
                    accept=".png, .jpg, .jpeg"
                  />
                  <label for="imageUpload"></label>
                </div>
                <div class="avatar-preview">
                  <div
                    id="imagePreview"
                    style="
                      background-image: url(http://i.pravatar.cc/500?img=7);
                    "
                  ></div>
                </div>
              </div>
            </form>
          </div>
        </div>
        <div class="modal-footer">
          <div class="form__action">
            <a
              class="btn btn--dark btn-danger"
              data-dismiss="modal"
              type="button"
              >Cancel</a
            >
            <button
              class="btn btn--main btn btn-secondary btn btn-primary"
              type="submit"
            >
              Submit
            </button>
          </div>
          <!-- <button type="button" class="btn btn-secondary" data-dismiss="modal">
            Close
          </button>
          <button type="button" class="btn btn-primary">Save changes</button> -->
        </div>
      </div>
    </div>
  </div>
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
          <div class="layout__box"></div>
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
      console.log("router========", $router.params);
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

<style scoped>
/* .avatar-upload {
  position: relative;
  max-width: 205px;
  margin: 50px auto;
}
.avatar-upload .avatar-edit {
  position: absolute;
  right: 12px;
  z-index: 1;
  top: 10px;
}
.avatar-upload .avatar-edit input {
  display: none;
}
.avatar-upload .avatar-edit input + label {
  display: inline-block;
  width: 34px;
  height: 34px;
  margin-bottom: 0;
  border-radius: 100%;
  background: #ffffff;
  border: 1px solid transparent;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.12);
  cursor: pointer;
  font-weight: normal;
  transition: all 0.2s ease-in-out;
}
.avatar-upload .avatar-edit input + label:hover {
  background: #f1f1f1;
  border-color: #d6d6d6;
}
.avatar-upload .avatar-edit input + label:after {
  content: "\f040";
  font-family: "FontAwesome";
  color: #757575;
  position: absolute;
  top: 10px;
  left: 0;
  right: 0;
  text-align: center;
  margin: auto;
}
.avatar-upload .avatar-preview {
  width: 192px;
  height: 192px;
  position: relative;
  border-radius: 100%;
  border: 6px solid #f8f8f8;
  box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.1);
}
.avatar-upload .avatar-preview > div {
  width: 100%;
  height: 100%;
  border-radius: 100%;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
} */
</style>
