import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CampaignDetailView from '@/views/Campaign/CampaignDetailView.vue'
import CampaignListView from '@/views/Campaign/CampaignListView.vue'
import SignupView from '@/views/Auth/SignupView.vue'
import LoginView from '@/views/Auth/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/campaigns',
      name: 'campaigns',
      component: CampaignListView,
    },
    {
      path: '/campaigns/:id',
      name: 'campaign',
      component: CampaignDetailView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/Auth/Profile.vue')
    },
    {
      path: '/my-campaigns',
      name: 'my-campaigns',
      component: () => import('@/views/Auth/MyCampaignsView.vue')
    },
    {
      path: '/campaigns/create',
      name: 'create-campaign',
      component: () => import("@/views/Auth/CreateCampaign.vue")
    }
  ],
})

export default router
