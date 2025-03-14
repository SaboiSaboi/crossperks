<template>
  <div class="min-h-screen bg-gray-50">
    <HeaderSignedIn />

    <div class="container mx-auto py-10">
      <h1 class="text-3xl font-bold">Business Dashboard</h1>

      <!-- ✅ Show a loading indicator while perks are loading -->
      <div v-if="perkStore.isLoading" class="flex justify-center py-5">
        <p class="text-gray-500">Loading perk...</p>
      </div>

      <!-- ✅ Show the perk once it's loaded -->
      <div
        v-else-if="perkStore.perk"
        class="bg-black h-screen flex justify-center items-center"
      >
        <h2 class="text-xl font-semibold text-indigo-700">Active Perk</h2>
        <p>{{ perkStore.perk.title }}</p>
      </div>

      <!-- ✅ Show "Create a Perk" ONLY if perks are done loading and no perk exists -->
      <div v-else class="bg-green-300">
        <button class="btn-primary">Create a Perk</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { usePerkStore } from "@/stores/perk";

const perkStore = usePerkStore();

onMounted(async () => {
  await perkStore.loadPerk(); // ✅ Ensures perks load before rendering
});
</script>
