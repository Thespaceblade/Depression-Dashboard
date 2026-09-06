import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        // Local Flask backend. Production uses same-origin Vercel /api routes.
        target: process.env.VITE_DEV_API_PROXY || 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
})

