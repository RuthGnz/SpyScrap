<template>
    <v-app id="inspire">
      <v-app-bar
        app
        shrink-on-scroll
        dark
        src="https://i.picsum.photos/id/435/1920/1080.jpg?hmac=0OhtYvw86ilta9_RqWMpabY3T8_ElTOQJutsYbSRQUY"
      >
        <v-toolbar-title>SpyScrap</v-toolbar-title>

        <v-spacer></v-spacer>
        <v-btn icon href="/">
      <v-icon>mdi-home</v-icon>
    </v-btn>
      </v-app-bar>

      <v-main>
        <router-view/>
      </v-main>
      <v-footer padless>
  <v-col
    class="text-center"
    cols="12"
  >
    {{ new Date().getFullYear() }} — <strong>@RuthGnz @MiguelHzBz</strong>
  </v-col>
</v-footer>
    </v-app>
  </template>

<script>

export default {
  name: 'App',

  data: () => ({

    //
  }),
};
</script>
