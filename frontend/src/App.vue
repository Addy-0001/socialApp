<template>
  <div class="app-container">
    <Header v-if="!isAdminRoute" />
    <router-view />
    <Footer v-if="!isAdminRoute" />
  </div>
</template>
  
  <script>
import Header from "./components/layout/Header.vue";
import Footer from "./components/layout/Footer.vue";

export default {
  name: "App",
  components: {
    Header,
    Footer,
  },
  computed: {
    isAdminRoute() {
      return this.$route.path.startsWith("/admin");
    },
  },
};
</script>
  
<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
  