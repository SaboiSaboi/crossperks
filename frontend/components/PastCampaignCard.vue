<template>
  <div class="bg-white p-6 rounded-lg shadow-lg">
    <p class="text-lg font-bold text-gray-800">{{ campaign.name }}</p>
    <p class="text-gray-600">
      Redemptions: <span class="font-semibold">{{ campaign.redemptions }}</span>
    </p>
    <p class="text-gray-600">
      Total Scans: <span class="font-semibold">{{ campaign.scans }}</span>
    </p>
  </div>
</template>

<script setup>
defineProps({
  campaign: Object,
});
</script>
