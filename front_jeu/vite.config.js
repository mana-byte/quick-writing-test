import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['ec2-18-202-55-34.eu-west-1.compute.amazonaws.com'],
    port: 8080
  }
})
