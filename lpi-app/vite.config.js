import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,json,svg,png}'],
        runtimeCaching: [
          {
            urlPattern: /^https?:\/\/localhost/,
            handler: 'NetworkFirst',
            options: { cacheName: 'api-cache' }
          }
        ]
      },
      manifest: {
        name: 'LPI Linux Essentials Study',
        short_name: 'LPI Study',
        start_url: '/',
        display: 'standalone',
        theme_color: '#6366f1',
        background_color: '#f8fafc',
        icons: [
          { src: '/icon-192.svg', sizes: '192x192', type: 'image/svg+xml' },
          { src: '/icon-512.svg', sizes: '512x512', type: 'image/svg+xml' },
        ]
      }
    })
  ],
})
