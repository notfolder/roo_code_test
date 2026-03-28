/**
 * Vue.jsアプリケーションエントリーポイント
 * Vue / Vuetify / Pinia / Vue Router を初期化して起動する
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import App from './App.vue'
import router from './router'

// Vuetifyを初期化する
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: 'light',
  },
})

// Vueアプリケーションを生成してプラグインを登録し、DOMにマウントする
createApp(App)
  .use(createPinia())
  .use(router)
  .use(vuetify)
  .mount('#app')
