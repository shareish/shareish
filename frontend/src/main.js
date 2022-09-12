const PROD_URL = 'https://shareish.montefiore.uliege.be';
const DEV_URL = 'http://localhost:8000';

import axios from 'axios';
axios.defaults.baseURL = (process.env.NODE_ENV === "production") ? PROD_URL : DEV_URL;

import Vue from 'vue';

import VueRouter from 'vue-router';
import router from './router';
Vue.use(VueRouter);

import i18n from './i18n';

import store from './store';

import App from './App.vue';
Vue.config.productionTip = false;

new Vue({
  render: h => h(App),
  router,
  store,
  i18n
}).$mount('#app');
