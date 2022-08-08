<template>
  <nav-bar />
  <router-view></router-view>
</template>
<script>
import NavBar from "./components/Navbar.vue";
export default {
  components: {
    "nav-bar": NavBar,
  },
};
</script>
