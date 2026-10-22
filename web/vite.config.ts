import { defineConfig } from 'vite';

export default defineConfig({
  // Served under shell same-origin proxy /demo-proxy/*
  base: '/demo-proxy/',
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8766',
      '/media': 'http://127.0.0.1:8766',
      '/references': 'http://127.0.0.1:8766',
    },
  },
});
