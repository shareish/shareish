import { createStore } from 'vuex'

export default createStore({
    state: {
        user: {
            email: '',
            id: ''
        },
        isAuthenticated: false,
        token: '',
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