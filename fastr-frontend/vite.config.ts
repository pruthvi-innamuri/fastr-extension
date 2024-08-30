import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        background: 'src/background.ts',
        content: 'src/content.ts',
        options: 'options.html'
      },
      output: {
        entryFileNames: '[name].js',
      },
    },
  },
})