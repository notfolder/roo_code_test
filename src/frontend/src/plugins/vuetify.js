import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#0f766e',
          secondary: '#155e75',
          accent: '#f59e0b',
          background: '#f8fafc'
        }
      }
    }
  }
})

export default vuetify
