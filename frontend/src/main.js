import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import i18n from './i18n'

// Modify this baseURL and give it the name of your host
axios.defaults.baseURL = (process.env.NODE_ENV === "production") ? 'https://shareish.montefiore.uliege.be' : 'http://localhost:8000'

createApp(App).use(i18n).use(store).use(router, axios).mount('#app')