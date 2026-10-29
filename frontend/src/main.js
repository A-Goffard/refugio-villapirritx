import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

// --- AQUÍ ESTÁ LA CLAVE ---
import './assets/main.css' 
// --------------------------

// Django protege los POST/PATCH/DELETE con un token CSRF que guarda en esta cookie
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')