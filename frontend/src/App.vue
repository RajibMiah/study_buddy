<template>
  <nav-bar v-if="this.$route.path !== '/chat'" />
  <router-view></router-view>
</template>
<script>
import NavBar from "./components/Navbar.vue";
export default {
  components: {
    "nav-bar": NavBar,
  },
  // watch: {
  //   "$route.name": function () {
  //     console.log(this.$route);
  //   },
  // },
};
</script>
