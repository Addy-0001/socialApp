import { createApp } from 'vue'
import { createPinia } from 'pinia'
import "./assets/css/main.css"


import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia()

app.use(pinia)


import { useAuthStore } from './stores/auth';
const authStore = useAuthStore(pinia);

// Initialize auth state immediately
authStore.initAuth();

app.use(router)

app.mount('#app')
