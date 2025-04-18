import { createRouter, createWebHistory } from 'vue-router';
import Main from '../components/Main.vue';
import Login from '../components/Login.vue';
import Regist from '../components/Regist.vue';
import TravelRegist from '../components/TravelRegist.vue';

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
    meta: { requiresAuth: true } // 🔐 로그인 필요한 페이지
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
    path: '/travel/regist',
    name: 'TravelRegist',
    component: TravelRegist,
    meta: { requiresAuth: true } // 🔐 로그인 필요
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// ✅ 로그인 체크 가드
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('authToken');

  if (to.path === '/login' && token) {
    // 로그인된 사용자가 로그인 페이지로 가려는 경우 → 홈으로 리디렉션
    next('/');
  } else if (to.meta.requiresAuth && !token) {
    // 로그인 필요한데 토큰 없으면 → 로그인 페이지로
    next('/login');
  } else {
    // 그 외는 통과
    next();
  }
});

export default router;