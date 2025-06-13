import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: '主页',
    component: () => import('../layout/index.vue'),
    redirect: '/index',//重定向到index路径，因为根路径/下没有直接组件，所以访问根时跳转到/index路径
    children: [
      {
        path: '/index',
        name: '首页',
        component: () => import('../views/index/index.vue')
      },
      {
        path: '/sys/user',
        name: '用户管理',
        component: () => import('../views/sys/user/index.vue')
      },
      {
        path: '/sys/role',
        name: '角色管理',
        component: () => import('../views/sys/role/index.vue')
      },
      {
        path: '/sys/menu',
        name: '菜单管理',
        component: () => import('../views/sys/menu/index.vue')
      },
      {
        path: '/bsns/department',
        name: '部门管理',
        component: () => import('../views/bsns/Department')
      },
      {
        path: '/bsns/post',
        name: '岗位管理',
        component: () => import('../views/bsns/Post')
      },
      {
        path: '/userCenter',
        name: '个人中心',
        component: () => import('../views/userCenter/index.vue')
      },
      {
        path: '/bsns/data',
        name: '数据管理',
        component: () => import('../views/bsns/Data')
      },
      {
        path: '/bsns/face',
        name: '人脸管理',
        component: () => import('../views/bsns/Face')
      },
      {
        path: '/bsns/ai',
        name: 'AI对话',
        component: () => import('../views/bsns/Ai')
      },
      {
        path: '/bsns/recording',
        name: '人脸录入',
        component: () => import('../views/bsns/Recording')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
