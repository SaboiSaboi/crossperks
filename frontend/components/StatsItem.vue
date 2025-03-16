<template>
  <p class="text-gray-600">
    {{ label }}: <span class="font-bold text-gray-800">{{ value }}</span>
  </p>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
});
</script>
