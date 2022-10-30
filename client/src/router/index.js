import Vue from 'vue';
import Router from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';

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
  ],
});
