import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import router from './router'
import App from './App.vue'
import { useAuthStore } from './stores/auth'

const pinia = createPinia()
const vuetify = createVuetify({
  components,
  directives,
  icons: { defaultSet: 'mdi', aliases, sets: { mdi } },
})

const app = createApp(App)
app.use(pinia)
app.use(vuetify)
app.use(router)

const authStore = useAuthStore()
authStore.restoreFromStorage()

app.mount('#app')
