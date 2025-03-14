export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  css: ["@/assets/css/tailwind.css"],
  devtools: { enabled: true },
  modules: [
    "pinia-plugin-persistedstate/nuxt",
    "@pinia/nuxt",
    "shadcn-nuxt",
    "@nuxtjs/tailwindcss",
    "@nuxt/image",
    "@vueuse/nuxt",
  ],
  shadcn: {
    prefix: "",
    componentDir: "./components/ui",
  },
});
