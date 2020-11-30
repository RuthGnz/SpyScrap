<template>
  <v-container>
          <h1>
            Yandex
          </h1>
          <br />
          <p>
            You must provide an url of an image. If you have the image locally
            you can upload it and provide an Imgur token.
          </p>
          <v-form>
            <v-container>
              <v-row>

                <v-col
                  cols="12"
                  md="5"
                >
                  <v-text-field
                    v-model="token"
                    label="Imgur"
                  ></v-text-field>
                </v-col>
                <v-col
                  cols="12"
                  md="5"
                >
                  <v-text-field
                    v-model="url"
                    label="Url"
                  ></v-text-field>
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
                @click="searchYandex()"
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
  </v-container>
</template>

<script>
const URL_BASE = "http://0.0.0.0:5000/osint/api/v1";
export default {
  data() {
    return {
      dropFiles: [],
      url: "",
      token: "",
      userData: [],
      checkbox: false,
      data: [],
      isLoading:false,
      isAlert:false,
      msg: ""
    };
  },
  methods: {
    searchYandex() {
      //todo check empty
      this.isLoading=true
      this.isAlert=false


      if (this.url === "" && this.token === "" && this.dropFiles.length == 0) {
        this.isAlert=true;
        this.isLoading=false;
        this.msg = "At least an url or an image and a token must be provided"
      } else if (
        this.url === "" &&
        (this.token === "" || this.dropFiles.length == 0)
      ) {
        this.isAlert=true;
        this.isLoading=false;
        this.msg = "At least an url or an image and a token must be provided"
      } else {
        const data = new FormData();
        data.append("url", this.url);
        data.append("token", this.token);
        for (var i = 0; i < this.dropFiles.length; i++) {
          let file = this.dropFiles[i];
          data.append("files[" + i + "]", file);
        }
        this.$http.post(`${URL_BASE}/yandex`, data, { timeout: 12000000 }).then(
          response => {
            this.isLoading=false;
            const responseData = response.data;
            this.userData = responseData.msg;
          },
          response => {
            this.isLoading=false;
            this.alert = true;
            this.msg = "Internal Server error"
            return response

          }
        );
      }
    }

  }
};
</script>
