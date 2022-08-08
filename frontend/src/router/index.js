import { createRouter, createWebHistory } from "vue-router";
import store from "../store";

const routes = [

     {
        path:'/',
        name:"home",
        component: () => import('../views/Home/HomeView.vue')
    },
    {
        path: '/', component: () => import('../views/auth/Layout.vue'),
            children:[
                {path: 'login', component: () => import('../views/auth/Login.vue')},
                {path: 'registration', component: () => import('../views/auth/Registration.vue')},
                {path: 'forget-password', component: () => import('../views/auth/ForgetPassword.vue')},
                {path: 'reset-password', component: () => import('../views/auth/ResetPassword.vue')}
            ],
        meta: {
            guest: true
        }
    },

    {
        path:'/profile/:uuid',
        name:"profile",
        component:()=> import('../views/profile/Profile.vue')
    },
    {
        path:'/room/:roomid',
        name:'room',
        component:()=> import('../views/room/RoomView.vue'),
    },
    {
        path: '/chat', component: () => import('../views/app/Layout.vue'),
        children: [
            {path: '', component: () => import('../views/app/chat-app/ChatApp.vue')},
            {
                path: "/call-view", component: () => import('../views/app/call-app/BaseCallView.vue'),
                children: [
                    {
                        path: 'sender/:username/:receiver',
                        name: 'callerView',
                        component: () => import('../views/app/call-app/Sender.vue')
                    },
                    {
                        path: 'receiver/:username/:sender',
                        name: 'receiverView',
                        component: () => import('../views/app/call-app/Receiver.vue')
                    },
                ]
            },
        ],
        meta: {
            auth: true
        }
    },
    {
        path: '/:pathMatch(.*)*',
        name:"PageNotFound",
        component:()=> import('../views/PageNotFound.vue')
    },
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    window.scrollTo(0, 0)
    if (to.matched.some(record => record.meta.auth)) {
        if (store.state.token == null) {
            next({
                path: '/',
                params: {nextUrl: to.fullPath}
            })
        } else { 
            next()
        }
    } else if (to.matched.some(record => record.meta.guest)) {
        if (store.state.token == null) {
            next()
        } else {
            next({
                path: '/', //app
                params: {nextUrl: to.fullPath}
            })
        }
    } else {
        next()
    }
})

export default router