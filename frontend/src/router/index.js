import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CampaignsView from '@/views/CampaignsView.vue'
import CampaignDetailView from '@/views/Campaign/CampaignDetailView.vue'
import CampaignListView from '@/views/Campaign/CampaignListView.vue'

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
    }
  ],
})

export default router
