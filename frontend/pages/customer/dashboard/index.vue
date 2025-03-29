<script setup lang="ts">
import { ref, onMounted } from "vue";

const { handleCheckAuth } = useAuthS();

const userName = ref("");
const currentPerk = ref<any | null>(null);
const recentPerks = ref<any>([]);

const userData: any = await handleCheckAuth();
userName.value = userData.user.name || "User";

const fetchPerks = async () => {
  try {
    const response: any = await $fetch(
      "http://localhost:8000/customer/perks/",
      {
        method: "GET",
        headers: {
          Authorization: `Token ${getToken()}`,
        },
      }
    );

    currentPerk.value = response.current_perk;
    recentPerks.value = response.recent_perks;
  } catch (error) {
    console.error("Failed to fetch perks:", error);
  }
};

const getToken = () => {
  const match = document.cookie.match(new RegExp("(^| )auth_token=([^;]+)"));
  return match ? match[2] : null;
};

onMounted(fetchPerks);
</script>
<template>
  <div>
    <div class="bg-gray-950"><Header /></div>
    <div
      class="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-10"
    >
      <!-- Header -->
      <h2 class="text-4xl font-bold mb-6 text-slate-900">
        Welcome, {{ userName }} 🎉
      </h2>
      <p v-if="currentPerk" class="text-lg text-gray-600 mb-10">
        Here is your surprise perk.
      </p>

      <!-- Current Perk Section -->
      <div
        class="w-full max-w-lg bg-white p-8 rounded-2xl shadow-lg text-center border border-gray-200"
      >
        <div v-if="currentPerk">
          <h3 class="text-2xl font-semibold mb-4 text-slate-900">
            Your Current Perk
          </h3>
          <p class="text-lg text-gray-700 font-medium">
            {{ currentPerk.business }}
          </p>
          <p class="text-3xl font-bold text-green-600 my-3">
            {{ currentPerk.discount }}
          </p>
          <p class="text-sm text-gray-500">Expires: {{ currentPerk.expiry }}</p>
        </div>
        <div v-else>
          <h3 class="text-2xl font-semibold text-gray-500">No Active Perk</h3>
          <p class="text-lg text-gray-700 mt-2 text-balance">
            Shop at

            <NuxtLink
              to="/businesses"
              class="underline text-blue-800 hover:text-blue-700"
            >
              participating businesses
            </NuxtLink>

            to earn a surprise perk.
          </p>
        </div>
      </div>

      <!-- Recent Perks Section -->
      <div
        class="w-full max-w-lg mt-10 bg-white p-8 rounded-2xl shadow-lg border border-gray-200"
      >
        <h3
          class="text-2xl font-semibold mb-4 text-slate-900 flex justify-center"
        >
          Recent Perks
        </h3>
        <ul v-if="recentPerks.length" class="divide-y divide-gray-200">
          <li v-for="perk in recentPerks" :key="perk.id" class="py-3">
            <p class="text-lg font-medium text-slate-700">
              {{ perk.business }} -
              <span class="text-green-600">{{ perk.discount }}</span>
            </p>
          </li>
        </ul>
        <p v-else class="text-gray-500 flex justify-center">
          No recent perks yet.
        </p>
      </div>
    </div>
  </div>
</template>

<style>
html {
  scroll-behavior: smooth;
}
</style>
