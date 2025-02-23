<template>
  <section>
    <div class="relative max-w-6xl mx-auto px-4 sm:px-6">
      <!-- Background Particles Animation Placeholder -->
      <div class="absolute inset-0 max-w-6xl mx-auto px-4 sm:px-6"></div>

      <div class="py-12 md:py-16">
        <div class="overflow-hidden">
          <div
            class="inline-flex w-full flex-nowrap overflow-hidden relative [mask-image:_linear-gradient(to_right,transparent_0,_black_128px,_black_calc(100%-128px),transparent_100%)]"
          >
            <!-- Main Scrolling List -->
            <ul
              class="flex animate-infinite-scroll items-center justify-center md:justify-start [&_img]:max-w-none [&_li]:mx-8"
            >
              <li
                v-for="(client, index) in clients"
                :key="index"
                class="flex flex-col items-center"
              >
                <span class="text-base text-white w-24 flex text-center">{{
                  client.name
                }}</span>
              </li>
            </ul>

            <ul
              class="flex animate-infinite-scroll items-center justify-center md:justify-start [&_img]:max-w-none [&_li]:mx-8"
              aria-hidden="true"
            >
              <li
                v-for="(client, index) in clients"
                :key="`duplicate-${index}`"
                class="flex flex-col items-center"
              >
                <span class="text-base text-white w-24 text-center">{{
                  client.name
                }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const clients = [
  { name: "Momo Coffee", image: "/images/momo-coffee.svg" },
  { name: "Greenleaf Market", image: "/images/greenleaf-market.svg" },
  { name: "Urban Books", image: "/images/urban-books.svg" },
  { name: "Sunny Side Bakery", image: "/images/sunny-side-bakery.svg" },
  { name: "The Local Diner", image: "/images/local-diner.svg" },
  { name: "City Gym", image: "/images/city-gym.svg" },
  { name: "Glow Spa", image: "/images/glow-spa.svg" },
  { name: "Bloom Florist", image: "/images/bloom-florist.svg" },
  { name: "Tech Hub", image: "/images/tech-hub.svg" },
];
</script>
