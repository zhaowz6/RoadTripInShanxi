import Vue from 'vue';
import Router from 'vue-router';
import Layout from '@/layouts/Layout';

// 引入页面组件
import Dashboard from '@/views/Dashboard';
import Users from '@/views/Users';

Vue.use(Router);

const routes = [
    {
        path: '/',
        component: Layout,
        redirect: '/dashboard',
        children: [
            {
                path: 'dashboard',
                component: Dashboard,
                name: 'Dashboard'
            },
            {
                path: 'users',
                component: Users,
                name: 'Users'
            }
            // 其他子路由
        ]
    },
    // 其他路由
];

const router = new Router({
    mode: 'history',
    routes
});

export default router;

