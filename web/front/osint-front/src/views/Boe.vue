<template>
  <v-container>
          <h1>
            Boe
          </h1>
          <br />
          <p>
            You must provide at least the name field.
          </p>
          <v-form>
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                  md="5"
                >
                  <v-text-field
                    v-model="text"
                    :counter="30"
                    label="Text to search"
                    required
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="4">
                  <v-checkbox
                  v-model="checkbox"
                  :label="`Search By words: ${checkbox.toString()}`"
                ></v-checkbox>
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
              </v-row>
            </v-container>
            <v-btn
                depressed
                color="primary"
                @click="searchBoe()"
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

               <div class="grey--text ml-4">
                  <a :href="n.url" target="_blank">  {{n.url}}</a>
              </div>
              <v-btn
                 color="primary"
                 class="ma-2"
                 dark
                 @click="openDialog(n)"
               >More Info </v-btn>
             </v-card>
              </v-col>
            </v-row>
          </v-container>
          <v-row justify="center">
              <v-dialog v-model="isCardModalActive" width="600px">

                <v-card>

                  <v-card-text v-if="boeText.length>0">{{boeText}}</v-card-text>
                  <v-simple-table v-if="boteTable.length>0">
                    {{boteTable}}
                    <template v-slot:default v-for="(table,index) in boteTable">
                      <tbody :key="index">
                        <tr v-for="item in table.table" :key="item.name">
                          <td v-for="value in item" :key="value">{{ value }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-card>
              </v-dialog>
            </v-row>

  </v-container>
</template>
<script>
const URL_BASE = "http://0.0.0.0:5000/osint/api/v1";
export default {
  data() {
    return {
      text: "",
      checkbox: false,
      userData: [],
      isCardModalActive: false,
      number: 1,
      isLoading:false,
      isAlert:false,
      msg: "",
      boeText:"",
      boteTable:""

    };
  },
  methods: {
    openDialog(info){
      this.isCardModalActive = true;
      this.boteTable = info.datatables;
      this.boeText = info.texto;
      console.log(info.datatables)
    },
    searchBoe() {
      //todo check empty
      this.isLoading=true;
      this.alert=false;
      if (this.text === "") {
        this.isLoading=false;
        this.isAlert=true
        this.msg="You must provide at least the text to search."
      } else {
        const data = new FormData();
        data.append("text", this.text);
        data.append("explicit", !this.checkbox);
        data.append("pages", this.number);

        this.$http.post(`${URL_BASE}/boe`, data, { timeout: 12000000 }).then(
          response => {
            this.isLoading=false;
            const responseData = response.data;
            this.userData = responseData.msg;
          },
          response => {
            this.isLoading=false;
            this.alert=true;
            this.msg= "Internal Server error";
            return response
          }
        );
      }
    }
  }
};
</script>
