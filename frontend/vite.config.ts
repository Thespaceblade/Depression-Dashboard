import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Strip dead Railway hosts from VITE_API_URL at build time so they never
 * appear in the production JS bundle (defense in depth for #13/#19).
 * Prefer same-origin Vercel `/api` when unset or Railway.
 */
function sanitizeViteApiUrl(raw: string | undefined): string {
  const value = String(raw ?? '').trim().replace(/\/$/, '')
  if (!value) return ''
  if (/railway\.app/i.test(value)) {
    console.warn(
      '[vite] Stripping Railway VITE_API_URL from build; using same-origin /api',
    )
    return ''
  }
  return value
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiUrl = sanitizeViteApiUrl(env.VITE_API_URL ?? process.env.VITE_API_URL)

  return {
    plugins: [react()],
    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(apiUrl),
    },
    server: {
      port: 3000,
      proxy: {
        '/api': {
          // Local Flask backend. Production uses same-origin Vercel /api routes.
          target: process.env.VITE_DEV_API_PROXY || 'http://localhost:5001',
          changeOrigin: true,
        },
      },
    },
  }
})
