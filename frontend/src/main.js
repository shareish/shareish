import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import i18n from './i18n'

axios.defaults.baseURL = 'http://localhost:8000'

createApp(App).use(i18n).use(store).use(router, axios).mount('#app')