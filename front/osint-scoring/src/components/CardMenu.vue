<template>
  <div class="container">
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            Choose the Scraping type
          </h1>
          <br />
          <h2 class="subtitle">
            Depending on wich type you select you might have to provide a photo
            or a name. Happy Scraping!
          </h2>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="columns">
        <div class="column">
          <a href="/tinder">
            <div class="card">
              <div class="card-image">
                <figure class="image is-4by3">
                  <img src="@/assets/tinder.png" alt="Placeholder image" />
                </figure>
              </div>
              <div class="card-content">
                <div class="content">
                  With this module you can check if someone is on Tinder. You
                  can provide a Photo, a company name.
                  <br />
                </div>
              </div>
            </div>
          </a>
        </div>
        <div class="column">
          <a href="/google">
            <div class="card">
              <div class="card-image">
                <figure class="image is-4by3">
                  <img src="@/assets/google.jpg" alt="Placeholder image" />
                </figure>
              </div>
              <div class="card-content">
                <div class="content">
                  With this module you can get images of a user given a name and a known image.
                  <br />
                </div>
              </div>
            </div>
          </a>
        </div>
        <div class="column">
          Third column
        </div>
        <div class="column">
          Fourth column
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "CardMenu",
  data() {
    return {};
  },
  methods: {}
};
</script>
