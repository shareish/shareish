var PROD_URL = "https://shareish.org";
var DEV_URL = "http://localhost:8000";

import axios from "axios";
axios.defaults.baseURL = (process.env.NODE_ENV === 'production') ? PROD_URL : DEV_URL;

import Vue from "vue";
import './registerServiceWorker';
import Buefy from "buefy";
import "buefy/dist/buefy.css";
Vue.use(Buefy, {
  defaultIconPack: 'fas',
});

import VueRouter from "vue-router";
import router from "./router";
Vue.use(VueRouter);

import i18n from "./i18n";

import VeeValidate from "vee-validate";
Vue.use(VeeValidate, {
  i18nRootKey: 'validations',
  i18n,
  inject: false
});

import store from "./store";

import App from "./App.vue";
Vue.config.productionTip = false;

Vue.prototype.$DEV_URL = DEV_URL;

new Vue({
  render: h => h(App),
  router,
  store,
  i18n
}).$mount("#app");
