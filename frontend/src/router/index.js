import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CampaignDetailView from '@/views/Campaign/CampaignDetailView.vue'
import CampaignListView from '@/views/Campaign/CampaignListView.vue'
import SignupView from '@/views/Auth/SignupView.vue'
import LoginView from '@/views/Auth/LoginView.vue'
import MyDonations from '@/views/Auth/MyDonations.vue'

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
      path: '/campaigns/:id/donate',
      name: 'campaign-donate',
      component: () => import('@/views/Campaign/CreateDonation.vue'),
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      meta: {
        requiresAnon: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/Auth/Profile.vue'),
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/my-campaigns',
      name: 'my-campaigns',
      component: () => import('@/views/Auth/MyCampaignsView.vue'),
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/campaigns/create',
      name: 'create-campaign',
      component: () => import("@/views/Auth/CreateCampaign.vue"),
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/donations',
      name: 'donations',
      component: () => import("@/views/Auth/MyDonations.vue"),
      meta: {
        requiresAuth: true,
      }
    }
  ],
})


// loginRequired and anonRequired for handling route protectors
const loginRequired = (to, from, next) => {
  const token = localStorage.getItem('accessToken');
  const user = localStorage.getItem('user');
  if (token && user) {
    next();
  } else {
    next({ name: 'login' })
  }
}

const anonRequired = (to, from, next) => {
  const token = localStorage.getItem('accessToken');
  const user = localStorage.getItem('user');
  if (token && user) {
    next({ name: 'home' })
  } else {
    next();
  }
}

// Apply Route Gaurds
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    loginRequired(to, from, next);
  } else if (to.matched.some(record => record.meta.requiresAnon)) {
    anonRequired(to, from, next);
  } else {
    next();
  }
});


export default router
