<template>
  <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <img
          src="https://bulma.io/images/bulma-logo.png"
          alt="Bulma: Free, open source, & modern CSS framework based on Flexbox"
          width="112"
          height="28"
        />
      </a>

      <a
        role="button"
        class="navbar-burger"
        aria-label="menu"
        aria-expanded="false"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar"
};
</script>
