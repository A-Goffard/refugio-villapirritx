import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Tu Django local
        // false: Django tiene que ver el Host real (localhost:5173) o rechaza los POST por CSRF
        changeOrigin: false,
      },
      '/media': {
        target: 'http://127.0.0.1:8000', // Para las fotos
        changeOrigin: false,
      }
    }
  }
})
