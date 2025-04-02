<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>
    <h2 class="text-4xl mb-10">Create an Account</h2>

    <!-- Form Section -->
    <div class="w-full max-w-md bg-white p-4 rounded-2xl shadow-lg">
      <section
        class="flex flex-col justify-center items-center text-center text-gray-700 pt-5 text-base"
      >
        <p class="text-balance">
          Are you a business? Request account creation at
        </p>
        <p class="font-semibold">support@crossperks.com</p>
      </section>
      <div class="text-center mt-4">
        <p class="text-sm">
          Already have an account?
          <NuxtLink class="font-medium text-slate-900 underline" to="/signin">
            Sign in
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style>
html {
  scroll-behavior: smooth;
}
</style>
