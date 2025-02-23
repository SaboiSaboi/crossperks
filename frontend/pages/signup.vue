<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <!-- Header -->
    <h1 class="text-5xl font-bold mb-10">CrossPerks</h1>

    <!-- Selection Toggle -->
    <div class="flex gap-6 mb-8">
      <button
        :class="{
          'bg-slate-900 text-white': selected === 'customer',
          'bg-white text-slate-900': selected !== 'customer',
        }"
        class="px-6 py-3 rounded-full shadow hover:shadow-lg transition"
        @click="selected = 'customer'"
      >
        Customer
      </button>
      <button
        :class="{
          'bg-slate-900 text-white': selected === 'business',
          'bg-white text-slate-900': selected !== 'business',
        }"
        class="px-6 py-3 rounded-full shadow hover:shadow-lg transition"
        @click="selected = 'business'"
      >
        Business
      </button>
    </div>

    <!-- Form Section -->
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
      <form @submit.prevent="handleSubmit">
        <div v-if="selected === 'customer'">
          <label class="block mb-2 font-medium">Name</label>
          <input
            type="text"
            placeholder="Your Name"
            class="w-full p-3 mb-4 border rounded-lg"
          />

          <label class="block mb-2 font-medium">Email</label>
          <input
            type="email"
            placeholder="Your Email"
            class="w-full p-3 mb-4 border rounded-lg"
          />

          <label class="block mb-2 font-medium">Confirm Email</label>
          <input
            type="email"
            placeholder="Confirm Email"
            class="w-full p-3 mb-6 border rounded-lg"
          />
        </div>

        <div v-if="selected === 'business'">
          <label class="block mb-2 font-medium">Business Name</label>
          <input
            type="text"
            placeholder="Your Business Name"
            class="w-full p-3 mb-4 border rounded-lg"
          />

          <label class="block mb-2 font-medium">Business Email</label>
          <input
            type="email"
            placeholder="Business Email"
            class="w-full p-3 mb-4 border rounded-lg"
          />

          <label class="block mb-2 font-medium">Confirm Email</label>
          <input
            type="email"
            placeholder="Confirm Email"
            class="w-full p-3 mb-6 border rounded-lg"
          />
        </div>

        <button
          type="submit"
          class="w-full py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-700 transition"
        >
          Sign Up
        </button>
      </form>

      <!-- Alternative Sign Up Methods -->
      <div class="text-center mt-6">
        <p class="text-slate-500">Or Continue with</p>
        <div class="flex justify-center gap-4 mt-4">
          <button class="px-6 py-3 bg-slate-200 rounded-lg hover:bg-slate-300">
            Google
          </button>
          <button class="px-6 py-3 bg-slate-200 rounded-lg hover:bg-slate-300">
            Apple
          </button>
        </div>
      </div>

      <!-- Terms and Login -->
      <p class="text-xs text-slate-400 mt-6 text-center">
        By continuing, you acknowledge that you understand and agree to the
        <a href="#" class="underline">Terms & Conditions</a> and
        <a href="#" class="underline">Privacy Policy</a>.
      </p>

      <p class="text-sm text-center mt-4">
        Already have an account?
        <a href="#" class="text-slate-900 font-medium underline"
          >Login instead</a
        >
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const selected = ref("customer");

const handleSubmit = () => {
  alert(`Signing up as a ${selected.value}`);
};
</script>

<style>
html {
  scroll-behavior: smooth;
}
</style>
