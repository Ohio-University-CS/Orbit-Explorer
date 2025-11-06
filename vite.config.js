import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    // point to the setup file that lives with your frontend app
    setupFiles: './frontendeng/frontend/src/setupTests.js',
  },
});
