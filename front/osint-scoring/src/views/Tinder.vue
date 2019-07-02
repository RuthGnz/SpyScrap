<template>
  <div class="container">
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            Tinder
          </h1>
          <br />
          <h2 class="subtitle">
            You must provide at least one field.
          </h2>
        </div>
      </div>
    </section>
    <section>
      <div class="columns is-multiline">
         <div class="column is-one-quarter"></div>
        <div class="column is-one-quarter">
          <b-field label="Name">
            <b-input value="Name" v-model="name"></b-input>
          </b-field>
        </div>
        <div class="column is-one-quarter">
           <b-field label="Company">
            <b-input value="Company" v-model="company"> </b-input>
          </b-field>         
        </div>
         
          <div class="column is-one-quarter"></div>
           <div class="column is-one-quarter"></div>
          <div class="column is-one-quarter">
            <b-button type="is-primary" @click="searchTinder()">Send</b-button>
          </div>
        <div class="column is-one-quarter">
            <b-field>
              <b-upload v-model="dropFiles" multiple drag-drop>
                <section class="section">
                  <div class="content has-text-centered">
                    <p>
                      <b-icon pack="fas" icon="upload" size="is-large"> </b-icon>
                    </p>
                    <p>Drop your files here or click to upload</p>
                  </div>
                </section>
              </b-upload>
            </b-field> 
                  <div>
                <span
                  v-for="(file, index) in dropFiles"
                  :key="index"
                  class="tag is-primary"
                >
                        {{ file.name }}
                <button
                  class="delete is-small"
                  type="button"
                  @click="deleteDropFile(index)"
                ></button>
                </span>
              </div>         
        </div>

      </div>






    </section>
    <div class="columns is-multiline">
      <div  v-for="user in userData" class="column is-one-fifth">  
        <div class="card">
          <div class="card-image">
            <figure class="image is-4by3">
              <img  :src="user.photos[0]">
            </figure>
          </div>
          <div class="card-content">
            <div class="content">

                <p>{{user.user.name}}</p>
                <p>{{user.user.birth}}</p>
                <p>{{user.user.location}}</p>
                <p>{{user.user.job}}</p>
            </div>
          </div>
        </div>
      </div>

    </div>
    <section>


    </section>
  </div>
</template>

<script>
const URL_BASE = "http://0.0.0.0:5000/osint/api/v1";
export default {
  name: "Tinder",
  data() {
    return {
      dropFiles: [],
      name: "",
      company: "",
      userData: [],
    };
  },
  methods: {
    deleteDropFile(index) {
      this.dropFiles.splice(index, 1);
    },
    searchTinder() {
      //todo check empty
      if (
        this.name === "" &&
        this.company === "" &&
        this.dropFiles.length == 0
      ) {
        this.toast("You must provide at least one input");
      } else {
        const data = new FormData();
        data.append("name", this.name);
        data.append("company", this.company);
        data.append("files", this.dropFiles);
        this.$http
          .post(`${URL_BASE}/tinder`, data, { timeout: 12000000 })
          .then(response => {
            const responseData = response.data;
            this.userData = responseData.msg
          });
      }
    },
    toast(msg) {
      this.$toast.open({
        duration: 5000,
        message: msg,
        position: "is-bottom",
        type: "is-danger"
      });
    }
  }
};
</script>
