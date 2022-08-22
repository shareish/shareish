import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import i18n from './i18n'

// Modify this baseURL and give it the name of your host
axios.defaults.baseURL = 'http://www.shareish.montefiore.uliege.be'

createApp(App).use(i18n).use(store).use(router, axios).mount('#app')