import {defineConfig} from "vite";
import tailwindcss from '@tailwindcss/vite'
import {resolve} from "path";
export default defineConfig({
  base: "/static/",
  plugins: [
    tailwindcss(),
  ],
  build: {
    manifest: 'manifest.json',
    outDir: resolve("./assets"),
    assetsDir: "build",
    rollupOptions: {
      input: {
        main: resolve("./static/src/js/main.js"),
      }
    }
  }
})