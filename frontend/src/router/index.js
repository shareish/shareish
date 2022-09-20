import VueRouter from 'vue-router';
import HomeView from '../views/HomeView.vue'
import ItemsMap from '@/components/pages/ItemsMap';
import SignUp from '../views/SignUpView.vue'
import Login from '../views/LoginView.vue'
import MyAccount from '../views/dashboard/MyAccountView.vue'
import Items from '../views/dashboard/ItemListView.vue'
import ItemDetail from '../views/dashboard/ItemDetailView.vue'
// import AddItem from '../views/dashboard/AddItemView.vue'
import AddItem from '@/components/pages/AddItem'
// import Conversations from '../views/dashboard/ConversationsView.vue'
import Conversations from '@/components/pages/Conversations'
import ConversationDetail from '../views/dashboard/ConversationDetailView.vue'
import Recurrents from '../views/dashboard/RecurrentsListView.vue'
import UserDetail from '../views/dashboard/UserDetailView.vue'
import ResultsSearch from '../views/dashboard/ResultsSearchView.vue'
import Autocomplete from '../views/dashboard/AutocompleteView.vue'
import ResetPassword from '../views/ResetPassword.vue'
import ResetPasswordConfirm from '../views/ResetPasswordConfirm.vue'
import ActivateEmail from '../views/ActivateEmail.vue'

import store from '../store'
import i18n from '@/i18n'
import ItemsList from '@/components/pages/ItemsList';
import Account from '@/components/pages/Account';

const routes = [{
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
            import ( /* webpackChunkName: "about" */ '../views/AboutView.vue')
    },
    {
        path: '/sign-up',
        name: 'signup',
        component: SignUp
    },
    {
        path: '/log-in',
        name: 'login',
        component: Login
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
        component: ItemDetail,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/results',
        name: 'resultsSearch',
        component: ResultsSearch,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/users/:id',
        name: 'userDetail',
        component: UserDetail,
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
        path: '/dashboard/recurrents',
        name: 'recurrents',
        component: Recurrents,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/autocomplete',
        name: 'autocomplete',
        component: Autocomplete,
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

    // Redirects for old urls
    {path: '/dashboard', redirect: '/map'},
    {path: '/dashboard/items', redirect: '/items'},
    {path: '/dashboard/items/:id', redirect: '/items/:id'},
    {path: '/dashboard/items/add', redirect: '/add-item'},
]

// Create router instance
const router = new VueRouter({
    mode: 'history',
    routes: routes,
    linkActiveClass: 'is-active'
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
        i18n.locale = localStorage.getItem('language') || 'en'
        next('/')
    }
 else {
        next()
    }
})

export default router;