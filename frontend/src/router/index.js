import VueRouter from "vue-router";
import store from "../store"
import i18n from "@/i18n"

import TheHomeView from "@/views/TheHomeView.vue"
import TheSignUpView from "@/views/TheSignUpView.vue"
import TheLoginView from "@/views/TheLoginView.vue"
import TheResetPasswordView from "@/views/TheResetPasswordView.vue"
import TheResetPasswordConfirmView from "@/views/TheResetPasswordConfirmView.vue"
import TheActivateView from "@/views/TheActivateView.vue"
import TheAccountView from "@/views/TheAccountView.vue";
import TheProfileView from "@/views/TheProfileView.vue";
import TheSettingsView from "@/views/TheSettingsView.vue";
import TheItemsView from "@/views/TheItemsView.vue";
import TheItemView from "@/views/TheItemView.vue"
import TheMapView from "@/views/TheMapView.vue";
import TheAddItemView from "@/views/TheAddItemView.vue"
import TheAboutView from "@/views/TheAboutView.vue";
import TheAddItemFromRecurrentsView from "@/views/TheAddItemFromRecurrentsView.vue";
import TheEditItemView from "@/views/TheEditItemView.vue";
import TheConversationsView from "@/views/TheConversationsView.vue";
import TheRecoverAccountView from "@/views/TheRecoverAccountView.vue";
import TheError404View from "@/views/TheError404View.vue";
import TheStartAccountDeletionProcessView from "@/views/TheStartAccountDeletionProcessView.vue";
import ErrorHandler from "@/mixins/ErrorHandler";

const routes = [
    {
        path: "/",
        name: 'home',
        component: TheHomeView,
        meta: {
            layout: 'no-navbar'
        }
    },
    {
        path: "/about",
        name: 'about',
        component: TheAboutView,
        meta: {
            layout: 'default'
        }
    },
    {
        path: "/sign-up",
        name: 'signup',
        component: TheSignUpView,
        meta: {
            authForbidden: true,
            layout: 'default'
        }
    },
    {
        path: "/log-in",
        name: 'login',
        component: TheLoginView,
        meta: {
            authForbidden: true,
            layout: 'default'
        }
    },
    {
        path: "/reset-password",
        name: 'resetPassword',
        component: TheResetPasswordView,
        meta: {
            layout: 'default'
        }
    },
    {
        path: "/reset-password/confirm/:uid/:token",
        name: 'resetPasswordConfirm',
        component: TheResetPasswordConfirmView,
        meta: {
            layout: 'default'
        }
    },
    {
        path: "/activate/:uid/:token",
        name: 'activateEmailToken',
        component: TheActivateView,
        meta: {
            layout: 'default'
        }
    },
    {
        path: "/activate",
        name: 'activateEmail',
        component: TheActivateView,
        meta: {
            authForbidden: true,
            layout: 'default'
        }
    },
    {
        path: "/map",
        name: 'map',
        component: TheMapView,
        meta: {
            requiresAuth: false,
            layout: 'default'
        }
    },
    {
        path: "/map/pos/:lat/:lng",
        name: 'mapPos',
        component: TheMapView,
        beforeEnter: (to, from, next) => {
            const { lat, lng } = to.params;
            const floatRegex = /^\d+(\.\d+)?$/;
            if (floatRegex.test(lat) && floatRegex.test(lng)) {
                next();
            } else {
                ErrorHandler.methods.snackbarError({ key: "BAD_MAP_POSITION"});
                next({ name: 'map' });
            }
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/account",
        name: 'account',
        component: TheAccountView,
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/profile/:id",
        name: 'profile',
        component: TheProfileView,
        beforeEnter: (to, from, next) => {
            const { id } = to.params;
            const integerRegex = /^\d+$/;
            if (integerRegex.test(id) && id !== '0') {
                next();
            } else {
                ErrorHandler.methods.snackbarError({ key: "ACCOUNT_DOESNT_EXIST"});
                next({ name: 'error404' });
            }
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/items",
        name: 'items',
        component: TheItemsView,
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/items/:id",
        name: 'item',
        component: TheItemView,
        beforeEnter: (to, from, next) => {
            const { id } = to.params;
            const integerRegex = /^\d+$/;
            if (integerRegex.test(id) && id !== '0') {
                next();
            } else {
                ErrorHandler.methods.snackbarError({ key: "ITEM_DOESNT_EXIST"});
                next({ name: 'items' });
            }
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/add-item",
        name: 'addItem',
        component: TheAddItemView,
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/add-item/from/:id",
        name: 'addItemFrom',
        component: TheAddItemView,
        beforeEnter: (to, from, next) => {
            const { id } = to.params;
            const integerRegex = /^\d+$/;
            if (integerRegex.test(id) && id !== '0') {
                next();
            } else {
                ErrorHandler.methods.snackbarError({ key: "ITEM_DOESNT_EXIST"});
                next({ name: 'addItem' });
            }
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/add-item/pos/:lat/:lng/:type/:resource/:rid",
        name: 'addItemPos',
        component: TheAddItemView,
        beforeEnter: (to, from, next) => {
            const { lat, lng, type, resource, rid } = to.params;
            const floatRegex = /^\d+(\.\d+)?$/;
            if (floatRegex.test(lat) && floatRegex.test(lng)) {
                // TODO: add type, resource and rid verifications
                next();
                return;
            } else {
                ErrorHandler.methods.snackbarError({ key: "BAD_ITEM_POSITION"});
            }
            next({ name: 'addItem' });
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/add-item/from-recurrents",
        name: 'addItemFromRecurrents',
        component: TheAddItemFromRecurrentsView,
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/edit-item/:id",
        name: 'editItem',
        component: TheEditItemView,
        beforeEnter: (to, from, next) => {
            const { id } = to.params;
            const integerRegex = /^\d+$/;
            if (integerRegex.test(id) && id !== '0') {
                next();
            } else {
                ErrorHandler.methods.snackbarError({ key: "ITEM_DOESNT_EXIST"});
                next({ name: 'items' });
            }
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/conversations",
        name: 'conversations',
        component: TheConversationsView,
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/conversations/:id",
        name: 'conversation',
        component: TheConversationsView,
        beforeEnter: (to, from, next) => {
            const { id } = to.params;
            const integerRegex = /^\d+$/;
            if (integerRegex.test(id) && id !== '0') {
                next();
            } else {
                ErrorHandler.methods.snackbarError({ key: "CONVERSATION_DOESNT_EXIST"});
                next({ name: 'conversations' });
            }
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/settings",
        name: 'settings',
        redirect: {
            name: 'settingsTab',
            params: { tab: 'profile' }
        }
    },
    {
        path: "/settings/:tab",
        name: 'settingsTab',
        component: TheSettingsView,
        beforeEnter: (to, from, next) => {
            const { tab } = to.params;
            const existingTabs = ['profile', 'account', 'notifications'];
            if (existingTabs.includes(tab)) {
                next();
            } else {
                // No special message showed
                next({
                    name: 'settingsTab',
                    params: { tab: 'profile' }
                });
            }
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },
    {
        path: "/recover-account",
        name: 'recoverAccount',
        component: TheRecoverAccountView,
        meta: {
            layout: 'default'
        }
    },
    {
        path: "/recover-account/:token",
        name: 'recoverAccountToken',
        component: TheRecoverAccountView,
        beforeEnter: (to, from, next) => {
            const { token } = to.params;
            const tokenRegex = /^[a-zA-Z0-9\-_]+$/;
            if (tokenRegex.test(token)) {
                next();
            } else {
                ErrorHandler.methods.snackbarError({ key: "TOKEN_BAD_FORMAT"});
                next({ name: 'home' });
            }
        },
        meta: {
            layout: 'default'
        }
    },
    {
        path: "/delete-account/:token",
        name: 'startAccountDeletionProcess',
        component: TheStartAccountDeletionProcessView,
        beforeEnter: (to, from, next) => {
            const { token } = to.params;
            const tokenRegex = /^[a-zA-Z0-9\-_]+$/;
            if (tokenRegex.test(token)) {
                next();
            } else {
                ErrorHandler.methods.snackbarError({ key: "TOKEN_BAD_FORMAT"});
                next({ name: 'home' });
            }
        },
        meta: {
            requiresAuth: true,
            layout: 'default'
        }
    },

    // Redirects for old urls
    {path: "/dashboard", redirect: "/map"},
    {path: "/dashboard/items", redirect: "/items"},
    {path: "/dashboard/items/:id", redirect: "/items/:id"},
    {path: "/dashboard/items/add", redirect: "/add-item"},

    // Error 404 page
    {
        path: '*',
        name: 'error404',
        component: TheError404View,
        meta: {
            layout: 'default'
        }
    }
]

// Create router instance
const router = new VueRouter({
    mode: 'history',
    routes: routes,
    linkActiveClass: 'is-active'
});

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const authForbidden = to.matched.some(record => record.meta.authForbidden);
    const isAuthenticated = store.state.isAuthenticated;

    if (requiresAuth && !isAuthenticated) {
        next("/log-in")
    } else if (authForbidden && isAuthenticated) {
        next("/map")
    } else {
        next()
    }

    i18n.locale = localStorage.getItem('language') || 'en'
});

export default router;
