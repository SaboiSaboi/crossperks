<script setup lang="ts">
const { handleCheckAuth } = useAuthS();
const user = await handleCheckAuth();
const features = [
  {
    title: "Your Customers Get Rewarded",
    description:
      "When they shop with you, they unlock an exclusive surprise at a neighboring business.",
  },
  {
    title: "New Faces Walk Through Your Door",
    description:
      "Other businesses send their customers your way. No ads. No effort. Just foot traffic and business growth.",
  },
  {
    title: "Casual Shoppers Become Regulars",
    description:
      "A single perk turns into repeat visits, building a loyal customer base with zero extra work.",
  },
  {
    title: "Your Business Thrives",
    description:
      "More customers, more revenue—without changing a thing. Just let CrossPerks do the work.",
  },
];
</script>

<template>
  <div
    class="min-h-screen flex flex-col bg-black text-gray-100 font-sans w-full"
  >
    <HeaderDashboard />

    <section
      class="relative flex flex-col-reverse md:flex-row items-center justify-between px-6 md:px-10 py-24 md:py-32 max-w-7xl mx-auto animate-fade-in"
    >
      <div class="max-w-2xl text-center md:text-left">
        <h1
          class="text-5xl md:text-6xl font-extrabold text-white leading-tight"
        >
          More Customers. No Extra Work.
        </h1>
        <p class="text-lg text-gray-300 mt-6 text-balance">
          CrossPerks helps businesses like yours bring in new customers
          effortlessly. No ad spend. No complicated marketing. Just steady,
          organic growth through offering perks.
        </p>
        <div
          v-show="!user"
          class="mt-8 flex flex-col sm:flex-row items-center sm:space-x-4"
        >
          <NuxtLink
            class="text-xl px-8 py-4 bg-blue-400 text-[#333333] font-semibold rounded-full hover:bg-blue-500 transition shadow-lg"
            to="/signup"
          >
            Get Started for Free
          </NuxtLink>
        </div>
      </div>
      <NuxtImg
        src="https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg"
        alt="Business Growth"
        class="w-full md:w-1/2 max-w-lg rounded-lg shadow-lg animate-slide-up"
      />
    </section>

    <section class="px-6 md:px-10 py-24 bg-[] text-center animate-fade-in">
      <h2
        class="text-4xl md:text-5xl font-extrabold mb-8 text-blue-400 text-balance"
      >
        A New Way to Attract & Keep Customers
      </h2>
      <p class="text-lg text-gray-300 max-w-3xl mx-auto mb-12 text-balance">
        What if your best customers came from next door? CrossPerks turns casual
        shoppers into loyal fans—effortlessly.
      </p>
      <div class="grid md:grid-cols-2 gap-16 items-center text-left">
        <div class="flex justify-center">
          <NuxtImg
            src="https://images.pexels.com/photos/7163407/pexels-photo-7163407.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
            alt="Customer Engagement"
            class="w-full max-w-lg rounded-xl shadow-lg"
          />
        </div>
        <div class="flex flex-col space-y-10">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="flex items-start space-x-4"
          >
            <div>
              <h3 class="text-3xl font-semibold text-blue-400">
                {{ feature.title }}
              </h3>
              <p class="text-gray-300 mt-3 text-lg text-balance">
                {{ feature.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section
      class="py-24 bg-gradient-to-br from-blue-900 to-blue-950 text-white text-center animate-fade-in"
    >
      <h2 class="text-4xl font-bold mb-6">Let’s Grow Your Business Together</h2>
      <p v-show="!user" class="text-balance text-lg mb-8">
        Join CrossPerks today and start bringing in more customers—without
        lifting a finger.
      </p>
      <NuxtLink
        v-show="!user"
        to="/signup"
        class="bg-yellow-600 text-white px-10 py-4 rounded-full hover:bg-yellow-700 transition-transform transform hover:scale-105 shadow-lg"
      >
        Join for Free
      </NuxtLink>
    </section>

    <Footer />
  </div>
</template>
