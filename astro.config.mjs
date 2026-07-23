import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";

// GitHub Pages (project repo): https://username.github.io/MyPortfolio
// GitHub Pages (user site):   set base to "/" and site to https://username.github.io
// Custom domain:              set site below + add your domain to public/CNAME
export default defineConfig({
  site: "https://ganeshcmohan.github.io",
  base: "/MyPortfolio",
  integrations: [tailwind()],
});
