import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Toast ,{ POSITION } from "vue-toastification";
import "vue-toastification/dist/index.css";


import App from './App.vue'
import router from './router'
import './axios'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const toastOptions =  {
  position: "top-center",
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: false,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: "button",
  icon: true,
  rtl: false
}

app.use(Toast, toastOptions);

app.use(pinia)
app.use(router)

app.mount('#app')













