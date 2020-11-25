import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";

Vue.use(Router)

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/tinder",
      name: "tinder",
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Tinder.vue")
    },
    {
      path: "/google",
      name: "google",
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Google.vue")
    },
    {
      path: "/yandex",
      name: "yandex",
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Yandex.vue")
    },
    {
      path: "/boe",
      name: "boe",
      component: () => import(/* webpackChunkName: "about" */ "./views/Boe.vue")
    },
    {
      path: "/instagram",
      name: "instagram",
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Instagram.vue")
    },
    {
      path: "/facebook",
      name: "facebook",
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Facebook.vue")
    },
    {
      path: "/twitter",
      name: "twitter",
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Twitter.vue")
    },
    {
      path: "/score",
      name: "score",
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Score.vue")
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue")
    }
  ]
});
