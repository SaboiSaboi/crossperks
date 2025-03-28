export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  app: {
    head: {
      title: "CrossPerks",
      meta: [
        {
          name: "description",
          content: "Earn a Surprise Perk.",
        },
      ],
      link: [{ rel: "icon", type: "image/svg+xml", href: "/favicon.svg" }],
    },
  },
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
  build: {
    transpile: ["vue-chart-3"],
  },
});
