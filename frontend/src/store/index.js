import Vuex from "vuex";
import Vue from "vue";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        user: {
            email: null,
            id: null
        },
        isAuthenticated: false,
        itemsFilters: {},
        token: null,
        notifications: 0,
    },
    getters: {},
    mutations: {
        initializeStore(state) {
            this.commit('setToken', localStorage.getItem('token'));
            this.commit('setUserID', localStorage.getItem('user_id'));
        },
        setToken(state, token) {
            if (token) {
                state.token = token;
                state.isAuthenticated = true;
            } else {
                this.commit('removeToken');
            }
        },
        removeToken(state) {
            state.token = null;
            state.isAuthenticated = false;
        },
        setUserID(state, id) {
            state.user.id = id;
        },
        removeUserID(state) {
            state.user.id = null;
        },
        setItemsFilters(state, itemsFilters) {
            for (const [key, value] of Object.entries(itemsFilters))
                state.itemsFilters[key] = value;
        }
    },
    actions: {},
    modules: {}
});
