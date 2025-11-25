import { reactRouter } from "@react-router/dev/vite";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";
import dotenv from "dotenv";

dotenv.config({ path: `.env.${process.env.NODE_ENV}` });

console.log("VITE_BACKEND_REST_URL:", process.env.VITE_BACKEND_REST_URL);
console.log("VITE_BACKEND_GRAPHQL_URL:", process.env.VITE_BACKEND_GRAPHQL_URL);

export default defineConfig({
  plugins: [tailwindcss(), reactRouter(), tsconfigPaths()],
  server: {
    proxy: {
      "/graphql": {
        target: process.env.VITE_BACKEND_GRAPHQL_URL,
        changeOrigin: true,
        secure: false,
      },
      "/auth": {
        target: process.env.VITE_BACKEND_REST_URL,
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/auth/, ''),
      },
    }
  }
});
