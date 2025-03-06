<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref } from "vue";

const route = useRoute();
const router = useRouter();
const claimToken = route.params.token;

const errorMessage = ref(null);
const successMessage = ref(null);

// Form Data
const officialName = ref("");
const streetAddress = ref("");
const city = ref("");
const state = ref("");
const zipCode = ref("");
const email = ref("");
const password = ref("");

const claimBusiness = async () => {
  try {
    const response = await $fetch(
      "http://localhost:8000/account/claim-business/",
      {
        method: "POST",
        body: {
          claim_token: claimToken,
          official_name: officialName.value,
          street_address: streetAddress.value,
          city: city.value,
          state: state.value,
          zip_code: zipCode.value,
          email: email.value,
          password: password.value,
        },
      }
    );

    successMessage.value = "Business successfully claimed! Redirecting...";
    setTimeout(() => {
      router.push("/business/dashboard");
    }, 2000);
  } catch (error) {
    errorMessage.value = "Failed to claim business. Try again.";
  }
};
</script>

<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>

    <h2 class="text-4xl mb-10">Claim Your Business</h2>

    <div class="w-full max-w-3xl bg-white p-8 rounded-2xl shadow-lg">
      <form @submit.prevent="claimBusiness" class="flex flex-col">
        <div class="gap-4 grid grid-cols-2">
          <input
            v-model="officialName"
            type="text"
            placeholder="Business Name"
            required
            class="w-full p-3 mb-4 border rounded-lg"
          />
          <input
            v-model="streetAddress"
            type="text"
            placeholder="Street Address"
            required
            class="w-full p-3 mb-4 border rounded-lg"
          />
          <input
            v-model="city"
            type="text"
            placeholder="City"
            required
            class="w-full p-3 mb-4 border rounded-lg"
          />
          <input
            v-model="state"
            type="text"
            placeholder="State"
            required
            class="w-full p-3 mb-4 border rounded-lg"
          />
          <input
            v-model="zipCode"
            type="text"
            placeholder="ZIP Code"
            required
            class="w-full p-3 mb-4 border rounded-lg"
          />

          <input
            v-model="email"
            type="email"
            placeholder="Your Email"
            required
            class="w-full p-3 mb-4 border rounded-lg"
          />
          <input
            v-model="password"
            type="password"
            placeholder="Create Password"
            required
            class="w-full p-3 mb-4 border rounded-lg"
          />
        </div>
        <div class="flex justify-center items-center mt-4">
          <Button
            type="submit"
            :disabled="
              !officialName ||
              !streetAddress ||
              !city ||
              !state ||
              !zipCode ||
              !email ||
              !password
            "
            :class="[
              !userName || !userEmail
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-500',
              'w-full py-2 text-white rounded-lg transition mb-4',
            ]"
          >
            Claim & Verify
          </Button>
        </div>
      </form>
    </div>

    <p v-if="successMessage" class="text-green-600">{{ successMessage }}</p>
    <p v-if="errorMessage" class="text-red-600">{{ errorMessage }}</p>
  </div>
</template>
