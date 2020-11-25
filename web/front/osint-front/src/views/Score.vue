<template>
  <div class="container">
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            ¡Scoring!
          </h1>
          <br />
          <h2 class="subtitle">
            You must provide all the values. It can take a while to compute your
            public exposition
          </h2>
        </div>
      </div>
    </section>
    <section>
      <div class="columns is-multiline">
        <div class="column is-one-quarter"></div>
        <div class="column is-one-quarter">
          <b-field label="Name and Surnames">
            <b-input value="Name" v-model="name"></b-input>
          </b-field>
          <b-field label="Imgurl Token">
            <b-input value="Token" v-model="token"></b-input>
          </b-field>
        </div>
        <div class="column is-one-quarter">
          <b-field label="Twitter and Facebook pages">
            <b-numberinput v-model="number"></b-numberinput>
          </b-field>
          <b-field label="Google number of images">
            <b-numberinput v-model="gnumber"></b-numberinput>
          </b-field>
        </div>

        <div class="column is-one-quarter"></div>
        <div class="column is-one-quarter"></div>
        <div class="column is-one-quarter">
          <b-button type="is-primary" @click="searchAll()">Send</b-button>
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

    <section>
      <br />
      <div v-if="Object.keys(userData).length > 0">
        <h1><b>TOTAL SCORE</b></h1>
        <div>
          <span class="tag is-warning is-large">{{ userData.score }}</span>
        </div>
      </div>
      <br />
      <div v-if="chartData.length > 0">
        <GChart type="ColumnChart" :data="chartData" :options="chartOptions" />
      </div>
      <br />
    </section>

    <section v-if="Object.keys(userData).length > 0">
      <div
        class="is-divider"
        v-if="userData.facebook.length > 0"
        data-content="Facebook"
      ></div>
      <div class="columns is-multiline">
        <div
          v-for="(user) in userData.facebook.length" :key="user.profile"> 0"
          class="column is-one-fifth"
        >
          <div class="card">
            <div class="card-image">
              <div class="slide">
                <figure class="image is-4by3">
                  <img :src="URL_IMG + '/' + user.image" />
                </figure>
              </div>
            </div>
            <div class="card-content">
              <div class="content">
                <p class="title is-4">{{ user.name }}</p>
                <p class="subtitle is-6">
                  Profile URL: <a :href="user.profile">{{ user.profile }}</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        class="is-divider"
        v-if="userData.instagram.length > 0"
        data-content="Instagram"
      ></div>
      <div class="columns is-multiline">
        <div
          v-for="(user) in userData.instagram" :key="user.username"
          class="column is-one-fifth"
        >
          <div class="card">
            <div class="card-image">
              <div class="slide">
                <figure class="image is-4by3">
                  <img :src="URL_IMG + '/' + user.image" />
                </figure>
              </div>
            </div>
            <div class="card-content">
              <div class="content">
                <p class="title is-4">{{ user.full_name }}</p>
                <p class="subtitle is-6">UserName: {{ user.username }}</p>
                <p class="subtitle is-6">Is Private: {{ user.is_private }}</p>
                <p class="subtitle is-6">Is Verified: {{ user.is_verified }}</p>
                <p class="subtitle is-6">
                  Profile URL: <a :href="user.profile">{{ user.profile }}</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        class="is-divider"
        v-if="userData.google.length > 0"
        data-content="Google"
      ></div>
      <div class="columns is-multiline">
        <div
          v-for="(user, index) in userData.google" :key="index"
          class="column is-one-fifth"
        >
          <div class="card">
            <div class="card-image">
              <div class="slide">
                <figure class="image is-4by3">
                  <img :src="user.photos" />
                </figure>
              </div>
            </div>
            <div class="card-content">
              <div class="content">
                <p class="subtitle is-6">
                  URL: <a :href="user.from_url">{{ user.from_url }}</a>
                </p>
                <p class="subtitle is-6">Info: {{ user.info }}</p>
                <p v-if="user.LOC_LIST.length > 0" class="subtitle is-6">
                  Words In Site:
                  <a @click="showModal(user.LOC_LIST)">View More</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        class="is-divider"
        v-if="userData.twitter.length > 0"
        data-content="Twitter"
      ></div>
      <div class="columns is-multiline">
        <div
          v-for="(user, index) in userData.twitter" :key="index"
          class="column is-one-fifth"
        >
          <a :href="'https://twitter.com/' + user.link">
            <div class="card">
              <div class="card-image">
                <div class="slide">
                  <figure class="image is-4by3">
                    <img :src="user.image" />
                  </figure>
                </div>
              </div>

              <div class="card-content">
                <div class="content">
                  <p class="title is-4">{{ user.name }}</p>
                  <p class="subtitle is-6">{{ user.member_since }}</p>
                  <p class="subtitle is-6">{{ user.activity }}</p>
                  <p class="subtitle is-6">{{ user.location }}</p>
                </div>
              </div>
            </div>
          </a>
        </div>
      </div>

      <div
        class="is-divider"
        v-if="userData.yandex.length > 0"
        data-content="Yandex"
      ></div>
      <div class="columns is-multiline">
        <div
          v-for="(user, index) in userData.yandex" :key="index"
          class="column is-one-fifth"
        >
          <div class="card">
            <div class="card-image">
              <div class="slide">
                <figure class="image is-4by3">
                  <img :src="user.originUrl" />
                </figure>
              </div>
            </div>
            <div class="card-content">
              <div class="content">
                <p class="subtitle is-6">Domain: {{ user.domain }}</p>
                <p class="subtitle is-6">Text: {{ user.text }}</p>
                <p class="subtitle is-6">Title: {{ user.title }}</p>
                <p class="subtitle is-6">
                  URL: <a :href="user.url">{{ user.url }}</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section>
      <b-modal :active.sync="isCardModalActive" :width="640" scroll="keep">
        <div class="card">
          <div class="card-content">
            <ul v-for="e in data" :key="e">
              <li>{{ e }}</li>
            </ul>
          </div>
        </div>
      </b-modal>
    </section>
  </div>
</template>

<script>
const URL_BASE = "http://0.0.0.0:5000/osint/api/v1";
export default {
  data() {
    return {
      dropFiles: [],
      name: "",
      token: "",
      userData: {},
      data: [],
      gnumber: 100,
      number: 10,
      chartData: [],
      isCardModalActive: false,
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
    deleteDropFile(index) {
      this.dropFiles.splice(index, 1);
    },
    showModal(data) {
      this.isCardModalActive = true;
      this.data = data;
    },
    searchAll() {
      //todo check empty
      const loadingComponent = this.$loading.open();
      if (this.name === "" && this.token === "" && this.dropFiles.length == 0) {
        loadingComponent.close();
        this.toast("You must provide all inputs");
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
            loadingComponent.close();
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
            loadingComponent.close();
            this.toast("Error");
            return error
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
