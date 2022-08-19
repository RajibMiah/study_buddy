<template>
  <!-- <pre>{{ user_profile }}</pre> -->
  <section class="companies-info snipcss-pWLv8 snip-section">
    <div class="container snip-div">
      <div class="company-title snip-div">
        <h3 class="snip-h3">All Top Profiles</h3>
      </div>
      <div class="companies-list snip-div">
        <div class="row snip-div">
          <div
            class="col-lg-3 col-md-4 col-sm-6 col-12 snip-div"
            v-for="user in user_profile"
            :key="user.id"
          >
            <div class="company_profile_info snip-div">
              <div class="company-up-info snip-div">
                <img :src="user.avator" alt="" class="snip-img" />
                <h3 class="snip-h3">{{ user.username }}</h3>
                <h4 class="snip-h4">{{ user.designation }}</h4>
                <ul class="snip-ul">
                  <li class="snip-li">
                    <a
                      href="#"
                      title=""
                      class="follow snip-a"
                      @click="followBtn(user.id)"
                    >
                      Follow
                    </a>
                  </li>
                  <li class="snip-li">
                    <router-link to="/chat" title="" class="message-us snip-a">
                      <i class="fa fa-envelope"> </i>
                    </router-link>
                  </li>
                  <!-- <li class="snip-li">
                    <a href="#" title="" class="hire-us snip-a"> Hire </a>
                  </li> -->
                </ul>
              </div>
              <router-link
                href="user-profile.html"
                title=""
                class="view-more-pro snip-a"
                :to="{
                  name: 'profile',
                  params: { uuid: user.uuid },
                }"
              >
                View Profile
              </router-link>
            </div>
          </div>
        </div>
      </div>
      <div class="process-comm snip-div">
        <div class="spinner snip-div">
          <div class="bounce1 snip-div"></div>
          <div class="bounce2 snip-div"></div>
          <div class="bounce3 snip-div"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "../../axios";
export default {
  name: "all-top-rank-profiles",
  components: {},
  data: function () {
    return {
      is_loading: false,
      user_profile: [],
      room_paticipants: [],
    };
  },
  methods: {
    fetchAllTopfollowerPersons() {
      this.is_loading = true;
      axios.get("api/top-profiles/").then((res) => {
        console.log("picked profile details data", res.data);
        this.user_profile = res.data;
        this.is_loading = false;
      });
    },
    async followBtn(user_id) {
      console.log("user id", user_id);
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

section {
  display: block;
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  float: left;
  width: 100%;
  position: relative;
}

.companies-info {
  padding: 60px 0;
}

*,
:after,
:before {
  box-sizing: border-box;
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

.company-title {
  float: left;
  width: 100%;
  margin-bottom: 20px;
  padding: 0 15px;
}

.companies-list {
  float: left;
  width: 100%;
  margin-bottom: -30px;
}

.process-comm {
  float: left;
  width: 100%;
  text-align: center;
  padding-top: 40px;
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

.company-title h3 {
  color: #000000;
  font-size: 20px;
  font-weight: 600;
  background-color: #fff;
  padding: 10px 15px;
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

.spinner {
  margin: 0 auto 0;
  width: 80px;
  text-align: center;
  height: 80px;
  border-radius: 100px;
  background-color: #fff;
  line-height: 80px;
  border: 1px solid #e1e1e1;
  cursor: pointer;
}

.col-12,
.col-lg-3,
.col-md-4,
.col-sm-6 {
  position: relative;
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
}

.col-12 {
  -ms-flex: 0 0 100%;
  flex: 0 0 100%;
  max-width: 100%;
}

@media (min-width: 576px) {
  .col-sm-6 {
    -ms-flex: 0 0 50%;
    flex: 0 0 50%;
    max-width: 50%;
  }
}

@media (min-width: 768px) {
  .col-md-4 {
    -ms-flex: 0 0 33.333333%;
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
  }
}

@media (min-width: 992px) {
  .col-lg-3 {
    -ms-flex: 0 0 25%;
    flex: 0 0 25%;
    max-width: 25%;
  }
}

.spinner > div {
  width: 15px;
  height: 15px;
  background-color: #b9b9b9;
  border-radius: 100%;
  display: inline-block;
  -webkit-animation: sk-bouncedelay 1.4s infinite ease-in-out both;
  animation: sk-bouncedelay 1.4s infinite ease-in-out both;
}

.spinner .bounce1 {
  -webkit-animation-delay: -0.32s;
  animation-delay: -0.32s;
}

.spinner .bounce2 {
  -webkit-animation-delay: -0.16s;
  animation-delay: -0.16s;
}

.company_profile_info {
  float: left;
  width: 100%;
  background-color: #fff;
  text-align: center;
  border-left: 1px solid #e4e4e4;
  border-right: 1px solid #e4e4e4;
  border-bottom: 1px solid #e4e4e4;
  margin-bottom: 30px;
}

.company-up-info {
  float: left;
  width: 100%;
  padding: 30px 0;
  border-bottom: 1px solid #e5e5e5;
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

.company_profile_info > a {
  display: inline-block;
  color: #000000;
  font-size: 16px;
  font-weight: 500;
  padding: 18px 0;
}

a:hover {
  color: initial;
  text-decoration: none;
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

.company-up-info img {
  float: none;
  margin-bottom: 10px;
  -webkit-border-radius: 100px;
  -moz-border-radius: 100px;
  -ms-border-radius: 100px;
  -o-border-radius: 100px;
  border-radius: 100px;
  height: 90px;
  object-fit: cover;
}

.company-up-info h3 {
  color: #000000;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 10px;
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

.company-up-info h4 {
  color: #686868;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 21px;
}

ul {
  margin-top: 0;
  margin-bottom: 1rem;
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
  list-style: none;
}

.company-up-info ul {
  float: left;
  width: 100%;
}

li {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

.company-up-info ul li {
  display: inline-block;
  margin-right: 6px;
}

.follow {
  background-color: #53d690;
}

.company-up-info ul li a {
  -webkit-border-radius: 4px;
  -moz-border-radius: 4px;
  -ms-border-radius: 4px;
  -o-border-radius: 4px;
  border-radius: 3px;
  display: inline-block;
  padding: 0 12px;
  color: #fff;
  height: 35px;
  line-height: 35px;
}

.message-us {
  background-color: #e44d3a;
}

.hire-us {
  background-color: #51a5fb;
}

i {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

.fa {
  display: inline-block;
  font: normal normal normal 14px/1 FontAwesome;
  font-size: inherit;
  text-decoration: inherit;
  text-rendering: auto;
  text-transform: none;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  font-style: normal;
  font-variant: normal;
  line-height: 1;
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
}

.company-up-info ul li a i {
  font-size: 24px;
  position: relative;
  top: 3px;
}

.fa-envelope:before {
  content: "\f0e0";
}

@keyframes sk-bouncedelay {
  0%,
  80%,
  100% {
    -webkit-transform: scale(0);
    transform: scale(0);
    transform: scale(0);
  }
  40% {
    -webkit-transform: scale(1);
    transform: scale(1);
    transform: scale(1);
  }
}
</style>
