<template>
  <v-container>
          <h1>
            Yandex
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
                 max="20"
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


  </v-container>
</template>

<script>
const URL_BASE = "http://0.0.0.0:5000/osint/api/v1";
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
      number: 100,
      isLoading:false,
      isAlert:false,
      msg: ""
    };
  },
  methods: {
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
          for (var i = 0; i < this.dropFiles.length; i++) {
            let file = this.dropFiles[i];
            data.append("files[" + i + "]", file);
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
