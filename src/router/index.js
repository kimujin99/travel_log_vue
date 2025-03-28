import { createRouter, createWebHistory } from 'vue-router';
import Main from '../components/Main.vue';
import Login from '../components/Login.vue';
import Regist from '../components/Regist.vue';
import TravleRegist from '../components/TravleRegist.vue';

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/regist',
    name: 'Regist',
    component: Regist
  },
  {
    path: '/regist',
    name: 'Regist',
    component: Regist
  },
  {
    path: '/travle/regist',
    name: 'TravleRegist',
    component: TravleRegist
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;