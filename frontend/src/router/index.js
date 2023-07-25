import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SigninView from '../views/SigninView.vue'
import AboutView from '../views/AboutView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import TheatreView from '../views/TheatreView.vue'
import Four04View from '../views/Four04View.vue'
import AdminView from '../views/AdminView.vue'
import { useUserStore } from '../stores/users';
import { useToast } from 'vue-toastification';




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signin',
      name: 'signin',
      component: SigninView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      beforeEnter: (to, from, next) => {
      const userStore = useUserStore()
      const toast = useToast();
        if (userStore.isUser()) {
          next();
        } else {
          toast.warning("Please login to Access ...redirecting !")
          next('/signin');
        }
      },

    },
    {
      path:"/theatre/:id",
      component: TheatreView,
      name:"theatre"
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    beforeEnter: (to, from, next) => {
      const userStore = useUserStore()
      const toast = useToast();
      
      if (userStore.isAdmin()) {
        next();
      } else {
        toast.error("Error : Restricted....redirecting !")
        next('/');
      }
    },
  },
  {
      path:"/:catchall(.*)*",
      component: Four04View,
      name:"404"
  },
  ]
})

export default router
