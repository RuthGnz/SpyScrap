<template>
  <div class="container">
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            BOE
          </h1>
          <br />
          <h2 class="subtitle">
            You must provide at least the name field. If you provide a known
            image, it would filter the results using facial recognition.
          </h2>
        </div>
      </div>
    </section>
    <section>
      <div class="columns is-multiline">
        <div class="column is-two-third">
          <b-field label="Text to Search. Names, DNI, text...">
            <b-input value="Text" v-model="text"></b-input>
          </b-field>
          <b-field>
            <b-checkbox v-model="checkbox">Search by words</b-checkbox>
          </b-field>
          <b-button type="is-primary" @click="searchBoe()">Send</b-button>
        </div>
        <div class="column is-one-third">
          <b-field label="Number of pages to Search">
            <b-numberinput v-model="number"></b-numberinput>
          </b-field>
        </div>
      </div>
    </section>
    <div class="columns is-multiline">
      <div v-for="(user) in userData" :key="user.url" class="column is-one-fifth">
        <div class="card">
          <div class="card-content">
            <div class="content">
              <p class="subtitle is-6">
                Url: <a :href="user.url">{{ user.url }}</a>
              </p>
              <p class="subtitle is-6">
                Info:
                <a @click="loadModal(user.datatables, user.texto)">View More</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <section>
      <b-modal
        :active.sync="isCardModalActive"
        has-modal-card
        full-screen
        :can-cancel="true"
      >
        <div class="modal-card" style="width: auto">
          <header class="modal-card-head">
            <p class="modal-card-title">Boe Data</p>
          </header>
          <section class="modal-card-body">
            <div class="columns" v-for="t in tables" :key="t">
              <table class="table column">
                <thead>
                  <tr>
                    <th v-for="(column, index) in t.headings" :key="index">
                      {{ column }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in t.table" :key="index">
                    <td
                      v-for="(column, indexColumn) in t.headings"
                      :key="indexColumn"
                    >
                      {{ item[column] }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-for="t in text" :key="t">
              <p>{{ t }}</p>
            </div>
          </section>
          <footer class="modal-card-foot">
            <button
              class="button"
              type="button"
              @click="isCardModalActive = false"
            >
              Close
            </button>
          </footer>
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
      text: "",
      checkbox: false,
      userData: [],
      isCardModalActive: false,
      tables: [],
      number: 1
    };
  },
  methods: {
    loadModal(datatables, texto) {
      this.isCardModalActive = true;
      this.tables = datatables;
      this.text = texto;
    },
    searchBoe() {
      //todo check empty
      const loadingComponent = this.$loading.open();
      if (this.text === "") {
        loadingComponent.close();
        this.toast("You must provide the text");
      } else {
        const data = new FormData();
        data.append("text", this.text);
        data.append("explicit", !this.checkbox);
        data.append("pages", this.number);

        this.$http.post(`${URL_BASE}/boe`, data, { timeout: 12000000 }).then(
          response => {
            loadingComponent.close();
            const responseData = response.data;
            this.userData = responseData.msg;
          },
          response => {
            loadingComponent.close();
            this.toast("Internal Server error");
            return response
          }
        );
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
