<template>
  <v-container>

  <h1>
    Scoring
  </h1>
  <br />
  <p>
    You must provide all the values. It can take a while to compute your
    public exposition.
  </p>
  <v-form>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          md="5"
        >
          <v-text-field
            v-model="name"
            :counter="30"
            label="Person to search"
            required
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          md="5"
        >
          <v-text-field
            v-model="token"
            :counter="30"
            label="Imgurl Token"
          ></v-text-field>
        </v-col>

        <v-col
          cols="12"
          md="10"
        >
        <v-slider
         v-model="number"
         color="blue"
         label="Twitter and Facebook pages"
         min="1"
         max="30"
         thumb-label
       ></v-slider>
       <v-slider
        v-model="gnumber"
        color="blue"
        label="Google number of images"
        min="1"
        max="100"
        thumb-label
      ></v-slider>
        </v-col>

        <v-col cols="12" md="4">
          <v-file-input
            accept="image/*"
            label="File input"
            v-model="dropFiles"
          ></v-file-input>

        </v-col>
      </v-row>
    </v-container>
    <v-btn
        depressed
        color="primary"
        @click="searchAll()"
      >
        Send
      </v-btn>
  </v-form>
  <div class="text-center">

    <v-progress-circular
          :size="200"
          :width="5"
          color="blue"
          indeterminate
          v-show="isLoading"
        ></v-progress-circular>
        <br>
        <v-alert
         border="right"
         color="blue-grey"
         dark
         v-show="isAlert"
       >
     {{msg}}
    </v-alert>
  </div>

<div>
  <v-tabs
   fixed-tabs
   background-color="blue"
   dark
 >
   <v-tab>
     Google
   </v-tab>
   <v-tab>
     Twitter
   </v-tab>
   <v-tab>
     Facebook
   </v-tab>
   <v-tab>
     Instagram
   </v-tab>
   <v-tab>
     Yandex
   </v-tab>
   <v-tab-item>
     <v-container fluid>
       google todo
     </v-container>
   </v-tab-item>
   <v-tab-item>
     <v-container fluid class="grey lighten-5">
         <v-row no-gutters>
           <v-col
             v-for="n in userData.twitter"
             :key="n.link"
             cols="12"
             sm="2"
           >
             <v-card
               class="pa-3"
               outlined
               tile
             >
             <a :href="n.link" target="_blank"><v-img
                   :src="n.image"
                   height="200px"
             ></v-img></a>
             <v-list-item-content>
               <v-list-item-title>{{n.name}}</v-list-item-title>
             </v-list-item-content>
            <v-card-actions>
              <v-btn
                color="blue lighten-2"
                text
              >
                More Info
              </v-btn>

              <v-spacer></v-spacer>

              <v-btn
                icon
                @click="showTwitter(n)"
              >
                <v-icon>{{ toShowTwitter == n.link ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-actions>

            <v-expand-transition>
              <div v-if="toShowTwitter == n.link">
                <v-divider></v-divider>
                <v-list-item-content>
                  <v-list-item-subtitle>Descripción: {{n.description}}</v-list-item-subtitle>
                  <v-list-item-subtitle>Nacimiento: {{n.born}}</v-list-item-subtitle>
                  <v-list-item-subtitle>Miembro desde: {{n.member_since}}</v-list-item-subtitle>
                  <v-list-item-subtitle>Localización: {{n.location}}</v-list-item-subtitle>
                </v-list-item-content>
              </div>
            </v-expand-transition>
          </v-card>
           </v-col>
         </v-row>
     </v-container>
   </v-tab-item>
   <v-tab-item>
     <v-container class="grey lighten-5" fluid>
       <v-row no-gutters>
         <v-col
           v-for="n in userData.facebook"
           :key="n.profile"
           cols="12"
           sm="2"
         >
           <a :href="n.profile" target="_blank"><v-card
             class="pa-3"
             outlined
             tile
           >
           <v-img
                 :src="n.image"
                 height="200px"
           ></v-img>
           <v-list-item-content>
             <v-list-item-title>{{n.name}}</v-list-item-title>
           </v-list-item-content>


        </v-card></a>
         </v-col>
       </v-row>
     </v-container>
   </v-tab-item>
   <v-tab-item>
       <v-container class="grey lighten-5" fluid>
         <v-row no-gutters>
           <v-col
             v-for="n in userData.instagram"
             :key="n.username"
             cols="12"
             sm="2"
           >
             <a :href="n.profile" target="_blank"><v-card
               class="pa-3"
               outlined
               tile
             >
             <v-img
                   :src="n.image"
                   height="200px"
             ></v-img>
             <v-card-title>
              {{n.full_name}}
            </v-card-title>
            <div class="grey--text ml-4">
                 {{n.usernane}}
           </div>
           <div class="my-4 subtitle-1">
                   Verified: {{n.is_verified}}
                 </div>
                 <div class="my-4 subtitle-1">
               Private: {{n.is_private}}
   </div>
          </v-card></a>
           </v-col>
         </v-row>
       </v-container>
   </v-tab-item>
   <v-tab-item>
       <v-container fluid class="grey lighten-5">
         <v-row no-gutters>
           <v-col
             v-for="n in userData.yandex"
             :key="n.url"
             cols="12"
             sm="2"
           >
             <v-card
               class="pa-3"
               outlined
               tile
             >
             <a :href="n.url" target="_blank"><v-img
                   :src="n.originUrl"
                   height="200px"
             ></v-img></a>
           <div class="my-4 subtitle-1">
                   {{n.domain}}
                 </div>
                 <div class="my-4 subtitle-2">
               {{n.title}}
   </div>
          </v-card>
           </v-col>
         </v-row>
     </v-container>
   </v-tab-item>
 </v-tabs>
</div>
</v-container>





</template>

<script>
const URL_BASE = "http://0.0.0.0:5000/osint/api/v1";
export default {
  data() {
    return {
      dropFiles: [],
      name: "",
      token: "",
      userData: {
        "facebook": [],
        "google": [],
        "instagram": [          {
                "full_name": "Ruth GN",
                "image": "data/instagram/2020-11-30 16:18:19_images/recognized/0-instagram.jpg",
                "is_private": true,
                "is_verified": false,
                "profile": "https://www.instagram.com/_ruthgnz",
                "username": "_ruthgnz"
            }],
        "score": 10,
        "twitter": [
            {
                "born": "None",
                "description": "Cybersecurity and cloud researcher at BBVA Next Technologies. Telecommunications engineer.\n\nhello@ruthgonzalez.es\n\nCrossfitter & Runner",
                "image": "https://pbs.twimg.com/profile_images/1172161923972030464/uWWN69uX_200x200.jpg",
                "link": "https://twitter.com/ruthgnz",
                "location": "Pamplona/Madrid",
                "member_since": "None",
                "name": "Ruth G.N",
                "storedImage": "data/twitter/2020-11-30 15:41:20_images/recognized/ruthgnz.jpg",
                "web": "ruthgonzalez.es"
            }
        ],
        "yandex": []
    },
      data: [],
      gnumber: 10,
      number: 2,
      chartData: [],
      isCardModalActive: false,
      isLoading:false,
      isAlert:false,
      msg: "",
      toShowTwitter: "",
      URL_IMG: "http://0.0.0.0:5000",
      chartOptions: {
        chart: {
          title: "Scoring Findings",
          subtitle: "Findings"
        }
      }
    };
  },
  methods: {
    showTwitter(n) {
      if (n.toShowTwitter == false){
        n.toShowTwitter = true
      } else if (n.toShowTwitter == true){
        n.toShowTwitter = false
      } else {
        n.toShowTwitter = true
      }
      if (n.toShowTwitter == true) {
        this.toShowTwitter = n.link
      } else {
        this.toShowTwitter = ""

      }
    },
    searchAll() {
      //todo check empty
      this.isLoading=true
      this.isAlert=false
      if (this.name === "" || this.token === "" || this.dropFiles.length == 0) {
        this.isLoading=false;
        this.isAlert=true
        this.msg ="You must provide all inputs";
      } else {
        const data = new FormData();
        data.append("name", this.name);
        data.append("token", this.token);
        data.append("number", this.number);
        data.append("gnumber", this.gnumber);
        console.log(this.dropFiles);
        for (var i = 0; i < this.dropFiles.length; i++) {
          let file = this.dropFiles[i];
          data.append("files[" + i + "]", file);
        }
        this.$http
          .post(`${URL_BASE}/scoring`, data, { timeout: 12000000 })
          .then(response => {
            this.isLoading=false;
            const responseData = response.data;
            this.userData = responseData.msg;
            console.log(this.userData);
            this.chartData = [
              ["Place", "Possible Findings"],
              ["Facebook", this.userData.facebook.length],
              ["Instagram", this.userData.instagram.length],
              ["Google", this.userData.google.length],
              ["yandex", this.userData.yandex.length],
              ["Twitter", this.userData.twitter.length]
            ];
          })
          .catch(error => {
            this.isLoading=false;
            this.isAlert=true
            this.msg="Error"
            return error
          });
      }
    },
  }
};
</script>
