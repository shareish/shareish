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
            loginForbidden: true,
            layout: 'default'
        }
    },
    {
        path: "/log-in",
        name: 'login',
        component: TheLoginView,
        meta: {
            loginForbidden: true,
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
            loginForbidden: true,
            layout: 'default'
        }
    },
    {
        path: "/map",
        name: 'map',
        component: TheMapView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/account",
        name: 'account',
        component: TheAccountView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/profile/:id",
        name: 'profile',
        component: TheProfileView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/items",
        name: 'items',
        component: TheItemsView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/items/:id",
        name: 'item',
        component: TheItemView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/add-item",
        name: 'addItem',
        component: TheAddItemView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/add-item/from/:id",
        name: 'addItemFrom',
        component: TheAddItemView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/add-item/from-recurrents",
        name: 'addItemFromRecurrents',
        component: TheAddItemFromRecurrentsView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/edit-item/:id",
        name: 'editItem',
        component: TheEditItemView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/conversations",
        name: 'conversations',
        component: TheConversationsView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/conversations/:id",
        name: 'conversation',
        component: TheConversationsView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/settings",
        name: 'settings',
        component: TheSettingsView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },
    {
        path: "/settings/:tab",
        name: 'settingsTab',
        component: TheSettingsView,
        meta: {
            requireLogin: true,
            layout: 'default'
        }
    },

    // Redirects for old urls
    {path: "/dashboard", redirect: "/map"},
    {path: "/dashboard/items", redirect: "/items"},
    {path: "/dashboard/items/:id", redirect: "/items/:id"},
    {path: "/dashboard/items/add", redirect: "/add-item"}
]

// Create router instance
const router = new VueRouter({
    mode: 'history',
    routes: routes,
    linkActiveClass: 'is-active'
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
        next("/log-in")
    } else if (to.matched.some(record => record.meta.loginForbidden) && store.state.isAuthenticated) {
        next("/")
    } else {
        next()
    }

    i18n.locale = localStorage.getItem('language') || 'en'
});

export default router;
