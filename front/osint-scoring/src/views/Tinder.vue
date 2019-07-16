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
      <div  v-for="user,index in userData" class="column is-one-fifth">
        <a @click="openModelUser(user.photos)">
        <div class="card">
          <div class="card-image">
            <div class="slide">
              <figure class="image is-4by3">
                <img  :src="user.photos[0]" @error="removeUrlUser(index,user.photos[0])">
              </figure>
            </div>
          </div>
          <div class="card-content">
             <div class="content">
                  <p class="title is-4">{{user.user.name}}</p>
                  <p class="subtitle is-6">Location: {{user.user.location}}</p>
                  <p class="subtitle is-6">Birth: {{user.user.birth.split('T')[0]}}</p>

                  <p v-if="user.user.job !== ''"><span v-if="user.user.job.company !== undefined">{{user.user.job.company.name}}</span> &nbsp;<span v-if="user.user.job.title !== undefined">{{user.user.job.title.name}}</span></p>
            </div>
          </div>
        </div>
      </a>
      </div>

    </div>
    <section>


    </section>

    <section>
      
        <b-modal :active.sync="isCardModalActive" :width="640" scroll="keep">
            <div class="card">
                <div class="card-content">
           <carousel :per-page="1" :navigate-to="someLocalProperty" :mouse-drag="true" :centerMode="true" :navigationEnabled="true">
              <slide v-for="photo in userSelectedPhotos">
               <figure class="image is-1000x1000">
                  <img :src="photo" @error="removeUrl(photo)">
                </figure>
              </slide>
            </carousel>
                </div>
            </div>
        </b-modal>
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
      isCardModalActive: false,
      userSelectedPhotos: [],
    };
  },
  methods: {
    deleteDropFile(index) {
      this.dropFiles.splice(index, 1);
    },
    removeUrl(photo) {
      var index = this.userSelectedPhotos.indexOf(photo);
        if (index > -1) {
          this.userSelectedPhotos.splice(index, 1);
        }
    },
    removeUrlUser(index,photo) {
      var index2 = this.userData[index].photos.indexOf(photo);
        if (index2 > -1) {
          this.userData[index].photos.splice(index2, 1);
        }
    },
    openModelUser(photos) {
      this.userSelectedPhotos = photos;
      this.isCardModalActive=true;
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
        console.log(this.dropFiles);
        for( var i = 0; i < this.dropFiles.length; i++ ){
          let file = this.dropFiles[i];
          data.append('files[' + i + ']', file);
        }
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
