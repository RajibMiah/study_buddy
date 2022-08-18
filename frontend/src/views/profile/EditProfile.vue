<template>
  <div class="profile_update_container">
    <div>
      <div class="header__NyBc snipcss0-0-0-1 snipcss-tI5yo">
        <div class="bg-wrapper__teZt snipcss0-1-1-2">
          <div class="background__26YF snipcss0-2-2-3"></div>
        </div>
        <div class="container__28Ei container snipcss0-1-1-4">
          <div class="avatar-base__19M6 snipcss0-2-4-5">
            <div class="avatar-upload">
              <div class="avatar-edit">
                <input
                  type="file"
                  id="file"
                  ref="file"
                  v-on:change="handleFileUpload()"
                  accept=".png, .jpg, .jpeg"
                />
                <label for="file"></label>
              </div>
              <!-- <div class="avatar-preview">
                <div
                  id="imagePreview"
                  style="background-image: url(http://i.pravatar.cc/500?img=7)"
                ></div>
              </div> -->
            </div>
            <a class="snipcss0-3-5-6 snip-a">
              <img
                class="avatar__2sMj snipcss0-4-6-7 snip-img"
                :src="profile_url"
                alt="md_rajib's avatar"
            /></a>
          </div>
          <div class="user-info__2aLr snipcss0-2-4-8">
            <div class="name__3EWH snipcss0-3-8-9">
              <div class="left-side__1lmO snipcss0-4-9-10"></div>
              <div class="container__1Mii snipcss0-4-9-11">
                <a>
                  <span class="name-text__1-NA snipcss0-5-11-12">{{
                    user_profile.username
                  }}</span>
                </a>
              </div>
              <div class="right-side__3zuc snipcss0-4-9-13">
                <a class="public__2p3C snipcss0-5-13-14 snip-a">
                  <i class="fa fa-external-link snipcss0-6-14-15"></i>
                </a>
              </div>
            </div>
            <div class="leetcodeId__13b9 snipcss0-3-8-16">
              Profile UUID : {{ user_profile.uuid }}
            </div>
          </div>
        </div>
      </div>
      <div class="container nav-toggled__2eeW nav__29df snipcss-i9Id5">
        <div class="side__2nDe snipcss-9xJIr">
          <div class="sidebar-base__2RIZ">
            <ul class="snip-ul">
              <li>
                <a
                  aria-current="page"
                  class="active__1IwF snip-a"
                  href="/profile/"
                >
                  <i class="fa fa-address-card"> </i>
                  &nbsp; Basic Info
                </a>
              </li>
              <li>
                <a href="/profile/points/" class="snip-a">
                  <i class="fa fa-database"> </i>
                  &nbsp; Points
                </a>
              </li>
              <li>
                <a href="/profile/account/" class="snip-a">
                  <i class="fa fa-cog"> </i>
                  &nbsp; Account
                </a>
              </li>
              <li>
                <a href="/profile/lab" class="snip-a">
                  <i class="fa fa-user-secret"> </i>
                  &nbsp; Lab
                </a>
              </li>
              <li>
                <a href="/profile/privacy/" class="snip-a">
                  <i class="fa fa-shield"> </i>
                  &nbsp; Privacy
                </a>
              </li>
              <li>
                <a href="/profile/notifications/" class="snip-a">
                  <i class="fa fa-bell"> </i>
                  &nbsp; Notifications
                </a>
              </li>
              <li>
                <a href="/subscription/" target="_blank" class="snip-a">
                  <i class="fa fa-credit-card"> </i>
                  &nbsp; Billing &nbsp;
                  <i class="fa fa-external-link external-link__3zeB"> </i>
                </a>
              </li>
              <li>
                <a href="/store/orders/" target="_blank" class="snip-a">
                  <i class="fa fa-paper-plane"> </i>
                  &nbsp; Orders &nbsp;
                  <i class="fa fa-external-link external-link__3zeB"> </i>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div class="content-toggled__1u8I content__equW">
          <div class="container__2Jyj">
            <div class="container-header">
              <div class="toggle-arrow__3ZiC">
                <i class="fa fa-angle-left"></i>
              </div>
              <div class="container header__3sy_">
                <span class="toggle-menu__1Iw2">
                  <i class="fa fa-list-ul"></i>
                </span>
                <i class="fa fa-angle-right"></i>
                Basic Info
              </div>
            </div>
            <div class="section__2T0q">
              <div class="title__3Mve">Basic Info</div>
              <div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="content__9cJ2">
                      <div class="title__14re">Name</div>
                      <div class="desc__2m9Y">{{ user_profile.name }}</div>
                      <div class="right-wrapper__3rVj">
                        <span class="text-disabled">
                          <span title="+2 LeetCode">
                            <i class="fa fa-database"></i>
                            +2
                          </span>
                        </span>
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="content__9cJ2">
                      <div class="title__14re">Gender</div>
                      <input
                        class="desc__2m9Y"
                        v-model="user_profile.gender"
                        :disabled="input_boolean.is_gender"
                      />

                      <div class="right-wrapper__3rVj" @click="">
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="placeholder__18ft content__9cJ2">
                      <div class="title__14re">Designation</div>
                      <div class="desc__2m9Y">
                        {{ user_profile.designation }}
                      </div>
                      <div class="right-wrapper__3rVj">
                        <span class="text-disabled">
                          <span title="+2 LeetCode">
                            <i class="fa fa-database"></i>
                            +2
                          </span>
                        </span>
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="placeholder__18ft content__9cJ2">
                      <div class="title__14re">Location</div>
                      <div class="desc__2m9Y">{{ user_profile.location }}</div>
                      <div class="right-wrapper__3rVj">
                        <span class="text-disabled">
                          <span title="+2 LeetCode">
                            <i class="fa fa-database"></i>
                            +2
                          </span>
                        </span>
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="content__9cJ2">
                      <div class="title__14re">Birthday</div>
                      <div class="desc__2m9Y">
                        <div>{{ user_profile.birthday }}</div>
                      </div>
                      <div class="right-wrapper__3rVj">
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="placeholder__18ft content__9cJ2">
                      <div class="title__14re">Summary</div>
                      <div class="desc__2m9Y">
                        {{ user_profile.summary }}
                      </div>
                      <div class="right-wrapper__3rVj">
                        <span class="text-disabled">
                          <span title="+2 LeetCode">
                            <i class="fa fa-database"></i>
                            +2
                          </span>
                        </span>
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="content__9cJ2">
                      <div class="title__14re">Website</div>
                      <div class="desc__2m9Y">
                        <div>
                          <div class="website__1VxW">
                            <div class="title__3AT2">
                              <a
                                href="https://www.linkedin.com/in/rajib-miah-680021149/"
                                class="snip-a"
                              >
                                https://www.linkedin.com/in/rajib-miah-680021149/
                              </a>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="right-wrapper__3rVj">
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="content__9cJ2">
                      <div class="title__14re">Github</div>
                      <div class="desc__2m9Y">{{ user_profile.github }}</div>
                      <div class="right-wrapper__3rVj">
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="content__9cJ2">
                      <div class="title__14re">LinkedIn</div>
                      <div class="desc__2m9Y">
                        {{ user_profile.linkedin }}
                      </div>
                      <div class="right-wrapper__3rVj">
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="placeholder__18ft content__9cJ2">
                      <div class="title__14re">Twitter</div>
                      <div class="desc__2m9Y">Your Twitter username or url</div>
                      <div class="right-wrapper__3rVj">
                        <span class="text-disabled">
                          <span title="+2 LeetCode">
                            <i class="fa fa-database"></i>
                            +2
                          </span>
                        </span>
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="section__2T0q">
              <div class="title__3Mve">Experience</div>
              <div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="content__9cJ2">
                      <div class="title__14re">Work</div>
                      <div class="desc__2m9Y">
                        <div>
                          <div class="experience__3za5">
                            <div class="title__MC_o">
                              Inverse.AI - softwere engineer
                            </div>
                            <div class="time__3FUK">04/2021 - 09/2021</div>
                          </div>
                          <div class="experience__3za5">
                            <div class="title__MC_o">
                              Console-IT - softwere developer
                            </div>
                            <div class="time__3FUK">06/2019 - 04/2021</div>
                          </div>
                        </div>
                      </div>
                      <div class="right-wrapper__3rVj">
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="placeholder__18ft content__9cJ2">
                      <div class="title__14re">Education</div>
                      <div class="desc__2m9Y">Add a school</div>
                      <div class="right-wrapper__3rVj">
                        <span class="text-disabled">
                          <span title="+2 LeetCode">
                            <i class="fa fa-database"></i>
                            +2
                          </span>
                        </span>
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="section__2T0q">
              <div class="title__3Mve">Skills</div>
              <div>
                <div class="row-wrapper__1dH2">
                  <div class="row__3ftQ">
                    <div class="content__9cJ2">
                      <div class="title__14re">Technical Skills</div>
                      <div class="desc__2m9Y" style="display: flex">
                        <div
                          v-for="skill in user_profile.skills"
                          :key="skill.id"
                          class="tags-block"
                        >
                          <span class="tags__3AYs"> {{ skill.name }}</span>
                        </div>
                      </div>
                      <div class="right-wrapper__3rVj">
                        <span class="edit__J5pK"> Edit </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../../axios";
export default {
  data: function () {
    return {
      is_loading: false,
      user_profile: [],
      profile_url: "",
      file: "",
      input_boolean: {
        is_gender: true,
      },
    };
  },
  methods: {
    fetchProfileData() {
      this.is_loading = true;
      axios.get(`/api/edit-profile/${this.$route.params.uuid}/`).then((res) => {
        this.user_profile = res.data;
        this.profile_url = res.data.avator;
        this.is_loading = false;
      });
    },

    async handleFileUpload() {
      this.file = this.$refs.file.files[0];
      this.profile_url = URL.createObjectURL(this.file);
      let formData = new FormData();
      formData.append("avator", this.file);
      await axios
        .patch(`api/profile/${this.$store.state.activeUser.uuid}/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          window.alert("Profile uploaded successfully!.");
        })
        .catch((err) => {
          console.log("error", err);
        });
    },
  },
  async mounted() {
    await this.fetchProfileData();
  },
};
</script>

<style scoped>
* {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}
body {
  background: whitesmoke;
  font-family: "Open Sans", sans-serif;
}
.container {
  max-width: 960px;
  margin: 30px auto;
  padding: 20px;
}
h1 {
  font-size: 20px;
  text-align: center;
  margin: 20px 0 20px;
}
h1 small {
  display: block;
  font-size: 15px;
  padding-top: 8px;
  color: gray;
}
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
}

.container {
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

@media (min-width: 768px) {
  .container {
    width: 750px;
  }
}

@media (min-width: 992px) {
  .container {
    width: 970px;
  }
}

@media (min-width: 1200px) {
  .container {
    width: 1170px;
  }
}

@media (min-width: 768px) {
  .container {
    position: relative;
  }
}

.nav__29df {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  -ms-flex-direction: row;
  flex-direction: row;
  position: relative;
}

.profile-app__KJyN {
  -webkit-font-smoothing: antialiased;
}

.content-wrapper {
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  min-height: 100%;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial,
    sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
  font-size: 14px;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.65);
  background-color: #fff;
  min-width: 320px;
  overflow-y: scroll;
  height: 100%;
  width: 100%;
  font-variant: tabular-nums;
  -webkit-font-feature-settings: "tnum";
  font-feature-settings: "tnum";
}

html {
  font-family: sans-serif;
  -webkit-text-size-adjust: 100%;
  -ms-text-size-adjust: 100%;
  font-size: 10px;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  height: 100%;
  width: 100%;
  line-height: 1.15;
  -ms-overflow-style: scrollbar;
}

.side__2nDe {
  width: 25%;
  min-height: 600px;
}

:after,
:before {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

*,
:before,
:after {
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
}

:selection {
  color: #fff;
  background: #1890ff;
}

ul {
  margin-top: 0;
  margin-bottom: 1em;
}

.sidebar-base__2RIZ ul {
  margin-top: 100px;
  -webkit-padding-start: 0;
}

.sidebar-base__2RIZ ul li {
  list-style: none;
  padding-right: 20px;
}

a {
  background-color: transparent;
  color: #1890ff;
  text-decoration: none;
  outline: none;
  cursor: pointer;
  -webkit-transition: color 0.3s;
  -o-transition: color 0.3s;
  transition: color 0.3s;
  -webkit-text-decoration-skip: objects;
  -ms-touch-action: manipulation;
  touch-action: manipulation;
}

.active__1IwF {
  background-color: #64b9f9;
  color: white !important;
}

.sidebar-base__2RIZ ul li > a {
  display: block;
  color: #5a5a5a;
  padding: 15px 20px;
  border-radius: 5px;
  text-decoration: none;
}

a:active,
a:hover {
  outline: 0;
}

a:hover {
  color: #40a9ff;
  text-decoration: underline;
}

a:active,
a:hover {
  text-decoration: none;
  outline: 0;
}

.fa {
  display: inline-block;
  font: normal normal normal 14px/1 FontAwesome;
  font-size: inherit;
  text-rendering: auto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.fa-database:before {
  content: "\f1c0";
}

.fa-gear:before,
.fa-cog:before {
  content: "\f013";
}

.fa-user-secret:before {
  content: "\f21b";
}

.fa-shield:before {
  content: "\f132";
}

.fa-bell:before {
  content: "\f0f3";
}

.fa-credit-card:before {
  content: "\f09d";
}

.external-link__3zeB {
  color: #0088cc;
}

.fa-external-link:before {
  content: "\f08e";
}

.fa-send:before,
.fa-paper-plane:before {
  content: "\f1d8";
}
</style>
