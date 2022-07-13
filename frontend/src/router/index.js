import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Dashboard from '../views/dashboard/DashboardView.vue'
import SignUp from '../views/SignUpView.vue'
import Login from '../views/LoginView.vue'
import MyAccount from '../views/dashboard/MyAccountView.vue'
import Items from '../views/dashboard/ItemListView.vue'
import ItemDetail from '../views/dashboard/ItemDetailView.vue'
import AddItem from '../views/dashboard/AddItemView.vue'

import store from '../store'
import i18n from '@/i18n'

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
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/my-account',
        name: 'myaccount',
        component: MyAccount,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/items',
        name: 'items',
        component: Items,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/items/:id',
        name: 'itemDetail',
        component: ItemDetail,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/items/add',
        name: 'addItem',
        component: AddItem,
        meta: {
            requireLogin: true
        }
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
        i18n.locale = localStorage.getItem('language') || 'en'
        next('/log-in')
    } else {
        next()
    }
})

export default router