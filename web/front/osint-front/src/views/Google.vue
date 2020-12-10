<template>
  <v-container>
          <h1>
            Google
          </h1>
          <br />
          <p>
            You must provide at least the name field. If you provide a known
            image, it would filter the results using facial recognition.
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
                    v-model="place"
                    :counter="30"
                    label="Where you whan to search"
                  ></v-text-field>
                </v-col>

                <v-col
                  cols="12"
                  md="10"
                >
                <v-slider
                 v-model="number"
                 color="blue"
                 label="Number of pages"
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
                  <v-checkbox
                  v-model="checkbox"
                  :label="`Download images: ${checkbox.toString()}`"
                ></v-checkbox>
                </v-col>
              </v-row>
            </v-container>
            <v-btn
                depressed
                color="primary"
                @click="searchGoogle()"
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

                    <v-container class="grey lighten-5">
                      <v-row no-gutters>
                        <v-col
                          v-for="n in userData"
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
      dropFiles: [],
      name: "",
      place: "",
      userData: [],
      checkbox: false,
      data: [],
      isCardModalActive: false,
      number: 10,
      isLoading:false,
      isAlert:false,
      msg: "",
      loc:[]
    };
  },
  methods: {
    showGoogle(n) {
      console.log(n.LOC_LIST)
      this.isCardModalActive = true;
      this.loc = n.LOC_LIST
    },
    searchGoogle() {
      //todo check empty
      this.isLoading=true
      this.isAlert=false
      if (this.name == "" && this.place =="" && this.dropFiles.length==0){
        this.isLoading=false;
        this.isAlert=true
        this.msg="You must provide at least the name of the person to search."
      }else {

        const data = new FormData();
        data.append("name", this.name);
        data.append("place", this.place);
        data.append("download", this.checkbox);
        data.append("number", this.number);
        if (this.name == "") {
          this.isAlert=true
          this.msg="Name is compulsory";
          this.isLoading=false;
        } else {
          if (this.dropFiles.length != 0 ) {
            data.append("files[0]", this.dropFiles);
          }
          this.$http.post(`${URL_BASE}/google`, data, { timeout: 12000000 }).then(
            response => {
              this.isLoading=false;
              const responseData = response.data;
              this.userData = responseData.msg;
            },
            response => {
              this.isLoading=false;
              this.isAlert=false;
              this.msg="Internal Error";
              return response
            }
          );
        }
      }

    }

  }
};
</script>
