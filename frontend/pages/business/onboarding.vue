<script setup lang="ts">
import { useRouter } from "vue-router";
import { ref } from "vue";

const { handleCheckAuth } = useAuthS();

const { data: business } = await useAsyncData("business", async () => {
  try {
    const businessData = await handleCheckAuth();
    return businessData;
  } catch (error) {
    console.error("Error fetching business data");
    return null;
  }
});
watchEffect(() => {
  if (business.value) {
    console.log(business.value);
    // officialName.value = business.value.official_name || "";
  }
});

const router = useRouter();
const businessName = ref("");
const streetAddress = ref("");
const city = ref("");
const state = ref("");
const zipCode = ref("");
const category = ref("");

const submitBusinessDetails = async () => {
  try {
    await $fetch("http://localhost:8000/api/business/onboard/", {
      method: "POST",
      body: {
        official_name: businessName.value,
        street_address: streetAddress.value,
        city: city.value,
        state: state.value,
        zip_code: zipCode.value,
        category: category.value,
      },
    });

    router.push("/business/dashboard");
  } catch (error) {
    console.error("Error saving business details", error);
  }
};
</script>

<template>
  <div class="h-screen flex flex-col justify-center items-center">
    <h2>Business Onboarding</h2>
    <form @submit.prevent="submitBusinessDetails" class="flex flex-col gap-4">
      <input
        v-model="businessName"
        type="text"
        placeholder="Business Name"
        required
        class="border p-2"
      />
      <input
        v-model="streetAddress"
        type="text"
        placeholder="Street Address"
        required
        class="border p-2"
      />
      <input
        v-model="city"
        type="text"
        placeholder="City"
        required
        class="border p-2"
      />
      <input
        v-model="state"
        type="text"
        placeholder="State"
        required
        class="border p-2"
      />
      <input
        v-model="zipCode"
        type="text"
        placeholder="ZIP Code"
        required
        class="border p-2"
      />
      <input
        v-model="category"
        type="text"
        placeholder="Category (e.g., Coffee Shop, Barbershop)"
        required
        class="border p-2"
      />
      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
        Complete Onboarding
      </button>
    </form>
  </div>
</template>
