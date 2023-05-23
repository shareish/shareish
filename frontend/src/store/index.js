import Vuex from "vuex";
import Vue from "vue";
import createPersistedState from "vuex-persistedstate";
import {isDict, isInt} from "@/functions";

Vue.use(Vuex);

export default new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        user: {
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
            this.commit('setUserID', Number(localStorage.getItem('user_id')));
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
            state.user.id = (isInt(id)) ? id : null;
        },
        removeUserID(state) {
            state.user.id = null;
        },
        setItemsFilters(state, {builtURLParams, keysToKeep = []}) {
            if (isDict(state.itemsFilters)) {
                const toKeep = {};
                for (const key of keysToKeep) {
                    if (key in state.itemsFilters)
                        toKeep[key] = state.itemsFilters[key];
                }
                state.itemsFilters = builtURLParams;
                for (const [key, value] of Object.entries(toKeep))
                    state.itemsFilters[key] = value;
            } else {
                state.itemsFilters = builtURLParams;
            }
        }
    },
    actions: {},
    modules: {}
});
