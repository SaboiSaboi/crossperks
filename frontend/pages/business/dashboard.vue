<template>
  <div>
    <div v-if="perkStore.isLoading" class="flex justify-center py-5">
      <p class="text-gray-500">Loading campaign...</p>
    </div>

    <!-- ✅ Show Perk ONLY after it is fully loaded -->
    <ClientOnly>
      <div
        v-if="perkStore.perk"
        class="flex flex-col items-center justify-center py-20"
      >
        <h2 class="text-2xl font-bold text-gray-800">Active Campaign</h2>
        <p class="text-gray-600 mt-2 text-lg">{{ perkStore.perk.title }}</p>
      </div>

      <div v-else class="flex flex-col items-center justify-center py-20">
        <h2 class="text-2xl font-bold text-gray-800">No Active Campaign</h2>
        <p class="text-gray-600 mt-2 text-lg">
          Create a new campaign to start sending and receiving referrals.
        </p>
        <CampaignModal />
      </div>

      <pre v-if="perkStore.perk">{{
        JSON.stringify(perkStore.perk, null, 2)
      }}</pre>
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { usePerkStore } from "@/stores/perk";

const perkStore = usePerkStore();

onMounted(async () => {
  await perkStore.loadPerk(); // ✅ Ensure perks are fully loaded before rendering
});
</script>
