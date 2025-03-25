<script setup lang="ts">
import { ref, onMounted } from "vue";
import { z } from "zod";

const BusinessSchema = z.object({
  category: z.string(),
  city: z.string(),
  identifiers: z.array(z.string()),
  logo: z.string().nullable(),
  official_name: z.string(),
  phone: z.string(),
  state: z.string(),
  street_address: z.string(),
  website: z.string().url(),
  zip_code: z.string(),
});

type BusinessType = z.infer<typeof BusinessSchema>;

const businesses = ref<BusinessType[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchBusinesses = async () => {
  try {
    const response = await $fetch("http://127.0.0.1:8000/account/businesses/");
    const parsedResponse = z.array(BusinessSchema).safeParse(response);

    if (!parsedResponse.success) {
      console.error("Validation Error:", parsedResponse.error);
      error.value = "Invalid data format received.";
      return;
    }
    businesses.value = parsedResponse.data;
  } catch (err) {
    console.error("Error fetching businesses:", err);
    error.value = "Failed to load businesses.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchBusinesses);
</script>

<template>
  <div class="bg-black min-h-screen">
    <Header />

    <div class="max-w-6xl mx-auto px-4 my-16">
      <h1 class="text-4xl font-bold text-white text-center my-12">
        Discover Local Businesses
      </h1>

      <!-- Loading & Error Handling -->
      <div v-if="loading" class="text-center text-white">
        Loading businesses...
      </div>
      <div v-if="error" class="text-center text-red-500">
        Failed to load data.
      </div>

      <!-- Business Grid -->
      <div
        v-if="businesses.length"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
      >
        <NuxtLink
          v-for="business in businesses"
          :key="business.official_name"
          :to="`/${business.website}`"
          class="bg-white shadow-lg rounded-lg overflow-hidden border hover:shadow-xl transition-all duration-300"
        >
          <div
            class="relative w-full h-44 flex items-center justify-center bg-gray-100 rounded-t-lg"
          >
            <img
              v-if="business.logo"
              :src="business.logo"
              :alt="business.official_name"
              class="w-full h-full object-cover rounded-t-lg"
            />
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-20 h-20 text-green-600"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M13.5 21v-7.5a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 .75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349M3.75 21V9.349m0 0a3.001 3.001 0 0 0 3.75-.615A2.993 2.993 0 0 0 9.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 0 0 2.25 1.016c.896 0 1.7-.393 2.25-1.015a3.001 3.001 0 0 0 3.75.614m-16.5 0a3.004 3.004 0 0 1-.621-4.72l1.189-1.19A1.5 1.5 0 0 1 5.378 3h13.243a1.5 1.5 0 0 1 1.06.44l1.19 1.189a3 3 0 0 1-.621 4.72M6.75 18h3.75a.75.75 0 0 0 .75-.75V13.5a.75.75 0 0 0-.75-.75H6.75a.75.75 0 0 0-.75.75v3.75c0 .414.336.75.75.75Z"
              />
            </svg>
          </div>

          <!-- Business Details -->
          <div class="p-5 bg-white rounded-b-lg">
            <h2 class="text-lg font-semibold text-gray-900">
              {{ business.official_name }}
            </h2>
            <div class="flex flex-wrap gap-2 mt-3">
              <span
                v-for="tag in business.identifiers"
                :key="tag"
                class="text-sm font-medium px-3 py-1 rounded-full bg-blue-100 text-blue-700"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>
    </div>

    <Footer />
  </div>
</template>

<style scoped></style>
