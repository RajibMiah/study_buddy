<template>
  <!-- <pre>{{ user_profile }}</pre> -->
  <div class="widget suggestions full-width snipcss-YIPho snip-div">
    <div class="sd-title snip-div">
      <h3 class="snip-h3">Most Viewed People</h3>
    </div>
    <div class="suggestions-list snip-div">
      <div
        v-for="user in user_profile"
        :key="user.id"
        class="suggestion-usd snip-div"
      >
        <router-link :to="{ name: 'profile', params: { uuid: user.uuid } }">
          <img :src="user.avator" alt="" class="snip-img" />
          <div class="sgt-text snip-div">
            <h4 class="snip-h4">{{ user.username }}</h4>
            <span class="snip-span"> {{ user.designation }} </span>
          </div>
        </router-link>

        <span
          class="material-symbols-outlined follow-btn"
          @click="followBtn(user.id)"
        >
          Follow
        </span>
        <!-- <span
          class="material-symbols-outlined follow-btn"
          @click="followBtn(user.id)"
        >
          Unfollow
        </span> -->
      </div>

      <div class="view-more snip-div">
        <router-link
          :to="{
            name: 'top-profiles',
          }"
          title=""
          class="snip-a"
        >
          View More
        </router-link>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "../axios";
export default {
  name: "all-profile-side-menu",
  components: {},
  data: function () {
    return {
      is_loading: false,
      user_profile: [],
    };
  },
  methods: {
    async fetchAllTopfollowerPersons() {
      this.is_loading = true;
      await axios.get("api/top-profiles/").then((res) => {
        console.log("picked toprofile sidebar data", res.data);
        res.data.map((user) => {
          if (!user.is_followed) {
            this.user_profile.push(user);
          }
        });
        // this.user_profile = res.data;
        this.user_profile.sort((a, b) =>
          b.total_follower > a.total_follower
            ? 1
            : a.total_follower > b.total_follower
            ? -1
            : 0
        );
        console.log(this.user_profile);
        this.is_loading = false;
      });
    },
    async followBtn(user_id) {
      console.log(this.user_profile);

      let data = {
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
          console.log("response", res);
          this.user_profile = this.user_profile.filter(
            (user) => user.id !== res.data.user_id
          );
          this.user_profile.sort((a, b) =>
            a.total_follower > b.total_follower
              ? 1
              : b.total_follower > a.total_follower
              ? -1
              : 0
          );
        })
        .catch((err) => {
          console.log("error==>", err);
        });
    },
  },
  async mounted() {
    await this.fetchAllTopfollowerPersons();
  },
  computed: {},
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Poppins|Roboto");
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

div {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

.follow-btn {
  cursor: pointer;
  color: #e44d3a;
  font-weight: 700;
}
.right-sidebar {
  float: left;
  width: 100%;
}

.col-lg-3 {
  position: relative;
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
}

@media (min-width: 992px) {
  .col-lg-3 {
    -ms-flex: 0 0 25%;
    flex: 0 0 25%;
    max-width: 25%;
  }
}

.pd-right-none {
  padding-right: 0;
}

.row {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  margin-right: -15px;
  margin-left: -15px;
  margin: 0;
}

.main-section-data {
  float: left;
  width: 100%;
}

.container {
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
}

@media (min-width: 576px) {
  .container {
    max-width: 540px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 720px;
  }
}

@media (min-width: 992px) {
  .container {
    max-width: 960px;
  }
}

@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}

.main-section {
  float: left;
  width: 100%;
}

main {
  display: block;
  float: left;
  width: 100%;
  padding: 60px 0;
}

.wrapper {
  float: left;
  width: 100%;
  position: relative;
}

body {
  margin: 0;
  font-family: "Source Sans Pro", sans-serif;
  font-size: 100%;
  font-weight: 400;
  line-height: 1;
  color: #212529;
  text-align: left;
  background-color: #f2f2f2;
  padding: 0;
  border: 0;
  font: inherit;
  vertical-align: baseline;
  overflow-x: hidden;
}

html {
  font-family: sans-serif;
  line-height: 1.15;
  -webkit-text-size-adjust: 100%;
  -webkit-tap-highlight-color: transparent;
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

.full-width {
  float: left;
  width: 100%;
  background-color: #fff;
  margin-bottom: 20px;
  border-left: 1px solid #e5e5e5;
  border-right: 1px solid #e5e5e5;
  border-bottom: 1px solid #e5e5e5;
}

.widget {
  float: left;
  width: 100%;
  background-color: #fff;
  border-left: 1px solid #e4e4e4;
  border-right: 1px solid #e4e4e4;
  border-bottom: 1px solid #e4e4e4;
  margin-bottom: 20px;
  -webkit-box-shadow: 0px 2px #e4e4e4;
  -moz-box-shadow: 0px 2px #e4e4e4;
  -ms-box-shadow: 0px 2px #e4e4e4;
  -o-box-shadow: 0px 2px #e4e4e4;
  box-shadow: 0px 2px #e4e4e4;
}

*,
:after,
:before {
  box-sizing: border-box;
}

.sd-title {
  float: left;
  width: 100%;
  padding: 20px;
  border-bottom: 1px solid #e5e5e5;
  position: relative;
  display: grid;
}

.suggestions-list {
  float: left;
  width: 100%;
  padding: 13px 0 30px 0;
}

h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-weight: 500;
  line-height: 1.2;
  font-size: 100%;
  margin: 0;
  padding: 0;
  border: 0;
  font: inherit;
  vertical-align: baseline;
}

.sd-title h3 {
  color: #000000;
  font-size: 18px;
  font-weight: 600;
  float: left;
}

i {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

.la {
  display: inline-block;
  font: normal normal normal 16px/1 "LineAwesome";
  font-size: inherit;
  text-decoration: inherit;
  text-rendering: optimizeLegibility;
  text-transform: none;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
}

.sd-title i {
  float: right;
  color: #b7b7b7;
  font-size: 24px;
  position: absolute;
  right: 5px;
  top: 18px;
}

.la-ellipsis-v:before {
  content: "\f1c4";
}

.suggestion-usd {
  float: left;
  width: 100%;
  padding: 15px 20px;
}

.view-more {
  float: left;
  width: 100%;
  text-align: center;
  padding-top: 10px;
}

img {
  vertical-align: baseline;
  border-style: none;
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  float: left;
  max-width: 100%;
}

.suggestion-usd img {
  -webkit-border-radius: 100px;
  -moz-border-radius: 100px;
  -ms-border-radius: 100px;
  -o-border-radius: 100px;
  border-radius: 100px;
  width: 19%;
}

.sgt-text {
  float: left;
  padding-left: 10px;
}

span {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

.suggestion-usd > span {
  float: right;
  margin-top: 4px;
  position: relative;
}

a {
  color: #007bff;
  text-decoration: none;
  background-color: transparent;
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

.view-more > a {
  -webkit-transition: all 0.4s ease-in;
  -moz-transition: all 0.4s ease-in;
  -ms-transition: all 0.4s ease-in;
  -o-transition: all 0.4s ease-in;
  transition: all 0.4s ease-in;
  color: #e44d3a;
  font-size: 14px;
  font-weight: 700;
}

a:hover {
  color: initial;
  text-decoration: none;
}

.view-more > a:hover {
  color: #e44d3a;
}

h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-weight: 500;
  line-height: 1.2;
  font-size: 100%;
  margin: 0;
  padding: 0;
  border: 0;
  font: inherit;
  vertical-align: baseline;
}

.sgt-text h4 {
  color: #000000;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
}

.sgt-text span {
  color: #686868;
  font-size: 14px;
}

.suggestion-usd > span i {
  -webkit-transition: all 0.4s ease-in;
  -moz-transition: all 0.4s ease-in;
  -ms-transition: all 0.4s ease-in;
  -o-transition: all 0.4s ease-in;
  transition: all 0.4s ease-in;
  color: #b2b2b2;
  width: 30px;
  height: 30px;
  border-radius: 3px;
  border: 1px solid #e5e5e5;
  text-align: center;
  line-height: 30px;
  font-weight: 700;
  cursor: pointer;
}

.la-plus:before {
  content: "\f2c2";
}
</style>
