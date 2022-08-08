<template>
  <div class="chat-left-headbar">
    <div class="row align-items-center">
      <div class="col-9">
        <ul class="list-unstyled mb-0">
          <li class="media">
            <router-link
              :to="{
                name: 'profile',
                params: { uuid: $store.state.activeUser.uuid },
              }"
              class="chat-user-name-container"
            >
              <img
                class="align-self-center mr-2 chat-user-profile"
                :src="
                  $store.state.activeUser.avator
                    ? $store.state.activeUser.avator
                    : 'https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg'
                "
                alt="Generic placeholder image"
              />
              <div class="media-body chat-user-name-container">
                <h5 class="mb-0 mt-2 chat-user-text">
                  @{{ $store.state.activeUser.name }}
                </h5>
              </div>
            </router-link>
          </li>
        </ul>
      </div>
      <div class="col-3">
        <a
          @click.prevent="logout"
          href="chat/logout"
          data-toggle="tooltip"
          data-placement="right"
          title=""
          data-original-title="Logout"
        >
          <img src="/src/assets/icons/log-out.svg" alt="" />
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../../../../../axios";

export default {
  name: "Header",
  methods: {
    async logout() {
      await axios
        .post("chat/logout/")
        .then((response) => {
          this.$store.dispatch("clearState");
          this.$router.push("/");
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.chat-user-profile {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 50%;
}
.chat-user-name-container {
  display: flex;
  height: 40px;
  padding: 4px;
}
.chat-user-text {
  font-size: small;
}
</style>
