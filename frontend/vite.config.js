import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/chat': 'https://todo-199jiuq4.b4a.run',
      '/tasks': 'https://todo-199jiuq4.b4a.run',
    },
  },
})
