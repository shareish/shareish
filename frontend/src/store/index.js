import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: {
            email: null,
            id: null
        },
        isAuthenticated: false,
        token: '',
        notifications: 0,
    },
    getters: {},
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
            } else {
                state.token = ''
                state.isAuthenticated = false
            }
            if (localStorage.getItem('user_id')) {
                state.user.id = Number(localStorage.getItem('user_id'));
            } else {
                state.user.id = null
            }
        },

        setToken(state, token) {
            state.token = token
            state.isAuthenticated = true
        },

        removeToken(state) {
            state.token = ''
            state.isAuthenticated = false
        },

        setUserID(state, id) {
            state.user.id = id
        },

        removeUserID(state) {
            state.user.id = ''
        },
    },
    actions: {},
    modules: {}
})