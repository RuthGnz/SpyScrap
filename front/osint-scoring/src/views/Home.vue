<template>
  <div class="home">
    <CardMenu />
  </div>
</template>

<script>
// @ is an alias to /src
import CardMenu from "@/components/CardMenu.vue";

export default {
  name: "Home",
  components: {
    CardMenu
  }
};
</script>
