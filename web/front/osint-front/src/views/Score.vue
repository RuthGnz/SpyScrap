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
            v-model="imgurl"
            label="Image URL for Yandex"
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
        label="Google number of pages"
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

  <div class="text-center">
    <p>Score</p>
    <v-progress-circular
       :rotate="360"
       :size="100"
       :width="15"
       :value="value"
       color="blue"
     >
       {{ value }}
     </v-progress-circular>

  </div>
<br>
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
     <v-container class="grey lighten-5" fluid>
       <v-row no-gutters>
         <v-col
           v-for="n in userData.google"
           :key="n.from_url"
           cols="12"
           sm="2"
         >
           <v-card
             class="pa-3"
             outlined
             tile
           >
           <a :href="n.from_url" target="_blank"><v-img
                 :src="n.photos"
                 height="200px"
           ></v-img></a>
           <v-list-item-content>
             <v-list-item-title>{{n.info}}</v-list-item-title>
           </v-list-item-content>
          <v-card-actions>
            <v-btn
              color="blue lighten-2"
              text
              @click="showGoogle(n)"
            >
              More Info
            </v-btn>

            <v-spacer></v-spacer>

          </v-card-actions>

        </v-card>
         </v-col>
       </v-row>
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
                 :src="'/'+n.image"
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
             <v-card
               class="pa-3"
               outlined
               tile
             >
             <a :href="n.profile" target="_blank"><v-img
                   :src="'/'+n.image"
                   height="200px"
             ></v-img></a>
             <v-list two-line>
               <v-list-item>

                 <v-list-item-content>
                     <v-list-item-title>{{n.full_name}}</v-list-item-title>
                   <v-list-item-subtitle>Verified: {{n.is_verified}}</v-list-item-subtitle>
                   <v-list-item-subtitle>Private: {{n.is_private}}</v-list-item-subtitle>
                 </v-list-item-content>

               </v-list-item>
             </v-list>
          </v-card>
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
<v-row justify="center">
    <v-dialog v-model="isCardModalActive" width="600px" scrollable>

      <v-card>

        <v-list-item-content v-for="(word,index) in loc" :key="index">
          <v-list-item-subtitle>{{word}}</v-list-item-subtitle>

        </v-list-item-content>

      </v-card>
    </v-dialog>
  </v-row>
</v-container>





</template>

<script>
const URL_BASE = "/osint/api/v1";
export default {
  data() {
    return {
      value: 0,
      dropFiles: [],
      name: "",
      imgurl: "",
      userData: {},
      data: [],
      gnumber: 10,
      number: 2,
      isCardModalActive: false,
      isLoading:false,
      isAlert:false,
      msg: "",
      toShowTwitter: "",
      loc:[],
      chartOptions: {
        chart: {
          title: "Scoring Findings",
          subtitle: "Findings"
        }
      }
    };
  },
  methods: {
    showGoogle(n) {
      console.log(n.LOC_LIST)
      this.isCardModalActive = true;
      this.loc = n.LOC_LIST
    },
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
      if (this.name === "" || this.imgurl === "" || this.dropFiles.length == 0) {
        this.isLoading=false;
        this.isAlert=true
        this.msg ="You must provide all inputs";
      } else {
        const data = new FormData();
        data.append("name", this.name);
        data.append("imgurl", this.imgurl);
        data.append("number", this.number);
        data.append("gnumber", this.gnumber);
        data.append("files[0]", this.dropFiles);

        this.$http
          .post(`${URL_BASE}/scoring`, data, { timeout: 12000000 })
          .then(response => {
            this.isLoading=false;
            const responseData = response.data;
            this.userData = responseData.msg;
            this.value = this.userData.score
          })
          .catch(error => {
            this.isLoading=false;
            this.isAlert=true
            this.msg="Error"
            console.log(error)
            return error
          });
      }
    },
  }
};
</script>
