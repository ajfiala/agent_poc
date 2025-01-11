import path from "path";
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc'
import svgr from "vite-plugin-svgr"

export default defineConfig({
  plugins: [react(), svgr({include: "**/*.svg",})],
  base: "/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173
  }
})