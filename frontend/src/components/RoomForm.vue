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
              <div class="layout__header_content">
                <h3 style="color: black">Create/Update Study Room</h3>
              </div>
            </div>
          </div>
        </div>
        <form v-on:submit.prevent="submitForm">
          <div class="modal-body">
            <div class="layout__body">
              <form class="form" action="" method="POST">
                <div class="form__group">
                  <label for="room_topic">Enter topic tags</label>
                  <input
                    required
                    type="text"
                    name="topic"
                    list="topic-list"
                    v-model="form.tags"
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
                  <input
                    required
                    type="text"
                    name="name"
                    list="topic-list"
                    v-model="form.name"
                  />
                </div>
                <div class="form__group">
                  <!-- <label for="room_topic">Topic</label>
                  <input
                    required
                    type="text"
                    name="topic"
                    id="topic"
                    list="topic-list"
                    v-model="form.topic"
                  /> -->
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
                  <QuillEditor
                    theme="snow"
                    name="description"
                    list="topic-list"
                    v-model="form.description"
                    :value="form.description"
                  />
                  <!-- <input
                    required
                    type="text"
                    name="description"
                    list="topic-list"
                    v-model="form.description"
                  /> -->
                </div>
                <div class="avatar-upload">
                  <div class="avatar-edit">
                    <input
                      type="file"
                      id="file"
                      ref="file"
                      accept=".png, .jpg, .jpeg"
                      v-on:change="handleFileUpload()"
                    />
                    <label for="imageUpload"></label>
                  </div>
                  <div class="avatar-preview">
                    <img
                      v-if="url"
                      :src="url"
                      style="width: inherit; padding: 15px"
                    />
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
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

// OR | AND
import "@vueup/vue-quill/dist/vue-quill.bubble.css";
import axios from "../axios";
export default {
  name: "room-form-model",
  components: {
    QuillEditor,
  },
  data() {
    return {
      form: {
        tags: "",
        name: "",
        description: "this is description",
      },
      file: "",
      url: null,
    };
  },

  created() {},

  methods: {
    featchRoomData() {},
    submitForm() {
      let formData = new FormData();
      formData.append("tags", this.form.tags);
      formData.append("name", this.form.name);
      formData.append("description", this.form.description);
      formData.append("room_image", this.file);
      axios
        .post("api/room/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log("response", res);
          window.location.reload();
        })
        .catch((err) => {
          console.log("error", err);
        });
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
      this.url = URL.createObjectURL(this.file);
    },
    closeModal() {},
  },
  async mounted() {},
};
</script>

<style scoped>
.avatar-preview {
  width: 17rem;
  text-align: center;
  justify-content: center;
  display: flex;
  align-items: center;
}
/* 
.avatar-upload {
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
