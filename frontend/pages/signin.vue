<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>
    <h2 class="text-4xl mb-10">Sign Into Your Account</h2>

    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
      <form @submit.prevent="handleSignIn">
        <Label class="block mb-2 font-medium" for="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="Your Email"
          class="w-full p-3 mb-4 border rounded-lg"
          v-model="email"
        />

        <Label class="block mb-2 font-medium" for="password">Password</Label>
        <Input
          id="password"
          type="password"
          placeholder="Your Password"
          class="w-full p-3 mb-6 border rounded-lg"
          v-model="password"
        />

        <button
          :disabled="!email || !password"
          :class="[
            !email || !password
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-500',
            'w-full py-2 text-white rounded-lg transition mb-4',
          ]"
          type="submit"
        >
          Sign In
        </button>
      </form>

      <!-- Alternative Sign-In Methods -->
      <div class="text-center mt-6">
        <p class="text-slate-500">Or continue with</p>
        <div class="flex justify-center gap-4 mt-4">
          <button class="px-6 py-3 bg-slate-200 rounded-lg hover:bg-slate-300">
            Google
          </button>
          <button class="px-6 py-3 bg-slate-200 rounded-lg hover:bg-slate-300">
            Apple
          </button>
        </div>
      </div>

      <!-- Sign-Up Link -->
      <p class="text-sm text-center mt-4">
        Don't have an account?
        <NuxtLink to="/signup" class="text-slate-900 font-medium underline"
          >Create one</NuxtLink
        >
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const authStore = useAuthS();

const email = ref("");
const password = ref("");
const handleSignIn = () => {
  authStore.login({ email: email.value, password: password.value });
};
</script>

<style>
html {
  scroll-behavior: smooth;
}
</style>
