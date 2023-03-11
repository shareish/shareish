import VueRouter from "vue-router";
import store from "../store"
import i18n from "@/i18n"

import TheHomeView from "@/components/pages/TheHomeView.vue"
import TheSignUpView from "@/components/user-management/TheSignUpView.vue"
import TheLoginView from "@/components/user-management/TheLoginView.vue"
import TheResetPasswordView from "@/components/user-management/TheResetPasswordView.vue"
import TheResetPasswordConfirmView from "@/components/user-management/TheResetPasswordConfirmView.vue"
import TheActivateView from "@/components/user-management/TheActivateView.vue"
import TheAccountView from "@/components/pages/TheAccountView.vue";
import TheProfileView from "@/components/pages/TheProfileView.vue";
import TheSettingsView from "@/components/pages/TheSettingsView.vue";
import TheItemsView from "@/components/pages/TheItemsView.vue";
import TheItemView from "@/components/pages/TheItemView.vue"
import TheMapView from "@/components/pages/TheMapView.vue";
import TheAddItemView from "@/components/pages/TheAddItemView.vue"
import TheConversationsView from "@/components/pages/TheConversationsView.vue"
import TheConversationView from "@/components/pages/TheConversationView.vue"
import TheAboutView from "@/components/pages/TheAboutView.vue";
import TheAddItemFromRecurrentsView from "@/components/pages/TheAddItemFromRecurrentsView.vue";

const routes = [
    {
        path: "/",
        name: 'home',
        component: TheHomeView
    },
    {
        path: "/about",
        name: 'about',
        component: TheAboutView
    },
    {
        path: "/sign-up",
        name: 'signup',
        component: TheSignUpView,
        meta: {
            loginForbidden: true
        }
    },
    {
        path: "/log-in",
        name: 'login',
        component: TheLoginView,
        meta: {
            loginForbidden: true
        }
    },
    {
        path: "/reset-password",
        name: 'resetPassword',
        component: TheResetPasswordView
    },
    {
        path: "/reset-password/confirm/:uid/:token",
        name: 'resetPasswordConfirm',
        component: TheResetPasswordConfirmView
    },
    {
        path: "/activate/:uid/:token",
        name: 'activateEmailToken',
        component: TheActivateView
    },
    {
        path: "/activate",
        name: 'activateEmail',
        component: TheActivateView,
        meta: {
            loginForbidden: true
        }
    },
    {
        path: "/map",
        name: 'itemsMap',
        component: TheMapView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/profile",
        name: 'myaccount',
        component: TheAccountView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/profile/:id",
        name: 'userDetails',
        component: TheProfileView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/items",
        name: 'items',
        component: TheItemsView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/items/:id",
        name: 'itemDetail',
        component: TheItemView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/add-item",
        name: 'addItem',
        component: TheAddItemView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/add-item/from/:id",
        name: 'addItemFrom',
        component: TheAddItemView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/add-item/from-recurrents",
        name: 'addItemFromRecurrents',
        component: TheAddItemFromRecurrentsView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/conversations",
        name: 'conversations',
        component: TheConversationsView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/conversations/:id",
        name: 'conversationDetail',
        component: TheConversationView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/settings",
        name: 'settings',
        component: TheSettingsView,
        meta: {
            requireLogin: true
        }
    },
    {
        path: "/settings/:page",
        name: 'settingsPage',
        component: TheSettingsView,
        meta: {
            requireLogin: true
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
