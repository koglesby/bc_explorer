import Vue from 'vue';
import Router from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import Dashboard from '../components/Dashboard.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeComponent,
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
    }
  ],
});
