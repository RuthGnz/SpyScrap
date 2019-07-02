<template>
  <div id="app">
    <NavBar />
    <div class="container is-fullhd">
      <router-view></router-view>
    </div>
  </div>
</template>

<script type="text/javascript">
import NavBar from "@/components/NavBar.vue";
export default {
  name: "App",
  components: {
    NavBar
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
