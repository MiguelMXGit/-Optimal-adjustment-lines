import Vue from 'vue';
import Router from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import axiosAuth from '@/api/axios-auth';

Vue.use(Router);

const routes = [
  {
    path: '/',
    component: Login,
  },
  {
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
  },
];

const router = new Router({
  routes: routes,
});

router.beforeEach((to, from, next) => {
  let token = localStorage.getItem('token');
  let requireAuth = to.matched.some(record => record.meta.requiresAuth);

  if (!requireAuth) {
    next();
  }

  if (requireAuth && token == '') {
    next('/');
  }

  if (to.path === '/') {
    if (token) {
      axiosAuth
        .post('/verify-token')
        .then(() => {
          next('/dashboard');
        })
        .catch(() => {
          next();
        });
    } else {
      next();
    }
  }

  if (requireAuth && token) {
    axiosAuth
      .post('/verify-token')
      .then(() => {
        next();
      })
      .catch(() => {
        next('/');
      });
  }
});

export default router;
