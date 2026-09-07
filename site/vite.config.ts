import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/postcss';
import path from 'node:path';

// 개인 사이트(yerim-accounting) 아래 /vasp-map/ 경로에 정적으로 올린다.
export default defineConfig({
  base: '/vasp-map/',
  plugins: [react()],
  css: { postcss: { plugins: [tailwindcss()] } },
  resolve: { alias: [{ find: '@/data', replacement: path.resolve(__dirname, '../data') }, { find: '@', replacement: path.resolve(__dirname, '.') }] },
  build: { outDir: 'dist', emptyOutDir: true, chunkSizeWarningLimit: 2500 },
});
