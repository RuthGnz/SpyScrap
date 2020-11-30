<template>
  <v-container>
    <br>
    <v-row>
      <v-col
        v-for="n in columns"
        :key="n.name"
        cols="4"
      ><router-link :to="n.to">
        <v-card height="200">
        <v-img
          :src= n.img
          height="140"
        ></v-img>
        <v-card-title>
          {{n.name}}
        </v-card-title>

        </v-card>
      </router-link>
      </v-col>
    </v-row>
  </v-container>

</template>

<script>

  export default {
    name: 'Home',
    data: () => ({
      columns: [{name:'Google',img:require('@/assets/google.jpg'),to:"/google"},
      {name:'Tinder',img:require('@/assets/tinder.png'),to:"/tinder"},
      {name:'Facebook',img:require('@/assets/facebook.png'),to:"/facebook"},
      {name:'Twitter',img:require('@/assets/twitter.png'),to:"/twitter"},
      {name:'Yandex',img:require('@/assets/yandex.png'),to:"/yandex"}
      ,{name:'Instagram',img:require('@/assets/instagram.jpg'),to:"/instagram"}
      ,{name:'Boe',img:require('@/assets/boe.jpg'),to:"/boe"},
      {name:'Global',img:require('@/assets/logos.png'),to:"/score"}]
      ,
      //
    }),
    components: {
    },
    methods:{
    }
  }
</script>
