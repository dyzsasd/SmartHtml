import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from 'vite-plugin-svgr'

import path from 'path';
import dotenv from 'dotenv';

const envPath = path.resolve(__dirname, '../.env');

dotenv.config({ path: envPath });

export default defineConfig(({}) => {
  if (!process.env.CLIENT_PORT || !process.env.web_app_host){
    new Error(`'CLIENT_PORT' and 'web_app_host' need to be configured in the ".env" file`)
  }

  const clientPort = Number(process.env.CLIENT_PORT)
  const serviceHost = process.env.web_app_host

  return {
    plugins: [
      react(),
      svgr({
        svgrOptions: {
          icon: true,
        },
      }),
    ],
    root: 'smart_html_client',
    server: {
      port: clientPort,
      proxy: {
        '/api': {
          target: serviceHost,
          changeOrigin: true
        }
      }
    }
  }
});