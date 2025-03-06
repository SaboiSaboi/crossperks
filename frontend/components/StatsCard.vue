<template>
  <div class="bg-white p-6 rounded-lg shadow-lg">
    <h2 class="text-xl font-semibold text-indigo-700">{{ title }}</h2>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  title: String,
});
</script>
