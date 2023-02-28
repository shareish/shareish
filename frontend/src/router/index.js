import VueRouter from 'vue-router';
import store from '../store'
import i18n from '@/i18n'

import HomeView from '@/components/HomeView.vue'
import ItemsMap from '@/components/pages/ItemsMap';
import SignUp from '@/components/user-management/SignUpView.vue'
import Login from '@/components/user-management/LoginView.vue'
import ItemDetails from '@/components/pages/ItemDetails'
import AddItem from '@/components/pages/AddItem'
import Conversations from '@/components/pages/Conversations'
import ConversationDetail from '@/components/pages/ConversationDetails'
import ResetPassword from '@/components/user-management/ResetPassword.vue'
import ResetPasswordConfirm from '@/components/user-management/ResetPasswordConfirm.vue'
import ActivateEmail from '@/components/user-management/ActivateEmail.vue'
import ItemsList from '@/components/pages/ItemsList';
import Account from '@/components/pages/Account';
import UserProfile from '@/components/pages/UserProfile';
import Settings from "@/components/pages/Settings.vue";

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import ( /* webpackChunkName: "about" */ '@/components/AboutView.vue')
    },
    {
        path: '/sign-up',
        name: 'signup',
        component: SignUp,
        meta: {
            loginForbidden: true
        }
    },
    {
        path: '/log-in',
        name: 'login',
        component: Login,
        meta: {
            loginForbidden: true
        }
    },
    {
        path: '/reset-password',
        name: 'resetPassword',
        component: ResetPassword
    },
    {
        path: '/password/reset/confirm/:uid/:token',
        name: 'resetPasswordConfirm',
        component: ResetPasswordConfirm
    },
    {
        path: '/activate/:uid/:token',
        name: 'activateEmail',
        component: ActivateEmail
    },
    {
        path: '/map',
        name: 'itemsMap',
        component: ItemsMap,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/profile',
        name: 'myaccount',
        component: Account,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/profile/:id',
        name: 'userDetails',
        component: UserProfile,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/items',
        name: 'items',
        component: ItemsList,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/items/:id',
        name: 'itemDetail',
        component: ItemDetails,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/add-item',
        name: 'addItem',
        component: AddItem,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/conversations',
        name: 'conversations',
        component: Conversations,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/conversations/:id',
        name: 'conversationDetail',
        component: ConversationDetail,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/settings',
        name: 'settings',
        component: Settings,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/settings/:page',
        name: 'settingsPage',
        component: Settings,
        meta: {
            requireLogin: true
        }
    },

    // Redirects for old urls
    {path: '/dashboard', redirect: '/map'},
    {path: '/dashboard/items', redirect: '/items'},
    {path: '/dashboard/items/:id', redirect: '/items/:id'},
    {path: '/dashboard/items/add', redirect: '/add-item'}
]

// Create router instance
const router = new VueRouter({
    mode: 'history',
    routes: routes,
    linkActiveClass: 'is-active'
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
        next('/log-in')
    } else if (to.matched.some(record => record.meta.loginForbidden) && store.state.isAuthenticated) {
        next('/')
    } else {
        next()
    }

    i18n.locale = localStorage.getItem('language') || 'en'
});

export default router;
