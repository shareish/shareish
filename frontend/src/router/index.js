import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Dashboard from '../views/dashboard/DashboardView.vue'
import SignUp from '../views/SignUpView.vue'
import Login from '../views/LoginView.vue'
import MyAccount from '../views/dashboard/MyAccountView.vue'
import Barters from '../views/dashboard/BarterListView.vue'
import BarterDetail from '../views/dashboard/BarterDetailView.vue'
import AddBarter from '../views/dashboard/AddBarterView.vue'

import store from '../store'

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
        path: '/dashboard/barters',
        name: 'barters',
        component: Barters,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/barters/:id',
        name: 'barterDetail',
        component: BarterDetail,
        meta: {
            requireLogin: true
        }
    },
    {
        path: '/dashboard/barters/add',
        name: 'addBarter',
        component: AddBarter,
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
        next('/log-in')
    } else {
        next()
    }
})

export default router