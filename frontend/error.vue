<template>
  <div class="error-page h-screen flex justify-center items-center">
    <section>
      <h1 class="text-3xl font-bold">Oops! Page Not Found</h1>
      <p class="mb-3">The page you're looking for does not exist.</p>
      <NuxtLink to="/" class="text-blue-500"
        >Go to the CrossPerks homepage</NuxtLink
      >
    </section>
  </div>
</template>

<script setup lang="ts">
import type { NuxtError } from "#app";

const props = defineProps({
  error: Object as () => NuxtError,
});
</script>

<style scoped>
.error-page {
  text-align: center;
  padding: 20px;
}
</style>
