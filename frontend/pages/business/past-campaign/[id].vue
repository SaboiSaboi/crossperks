<template>
  <div class="min-h-screen bg-gray-50">
    <HeaderSignedIn />
    <div class="h-dvh flex justify-center items-center px-4">
      <div
        class="container mx-auto max-w-3xl bg-white p-6 rounded-lg shadow-md border border-gray-300"
      >
        <!-- ✅ Campaign Title & Description -->
        <h1 class="text-3xl font-bold text-gray-900">
          {{ campaign?.title || "Loading..." }}
        </h1>
        <p class="text-lg text-gray-700 mt-2">{{ campaign?.description }}</p>

        <!-- ✅ Campaign Statistics -->
        <div v-if="campaign" class="mt-6 grid grid-cols-2 gap-4">
          <div class="bg-gray-100 p-4 rounded-lg text-center">
            <p class="text-gray-600 text-sm">Total Perks</p>
            <p class="text-xl font-semibold text-gray-900">
              {{ campaign.total }}
            </p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg text-center">
            <p class="text-gray-600 text-sm">Redemptions</p>
            <p class="text-xl font-semibold text-gray-900">
              {{ campaign.redemptions }}
            </p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg text-center">
            <p class="text-gray-600 text-sm">Success Rate</p>
            <p class="text-xl font-semibold text-gray-900">
              {{ successRate }}%
            </p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg text-center">
            <p class="text-gray-600 text-sm">Campaign Duration</p>
            <p class="text-md font-semibold text-gray-900">
              {{ campaignDuration }}
            </p>
          </div>
        </div>

        <!-- ✅ Simple Engagement Chart -->
        <div class="mt-8 bg-gray-50 p-6 rounded-lg shadow-inner">
          <p class="text-gray-700 font-medium mb-4">📊 Campaign Engagement</p>
          <CampaignChart />
        </div>

        <!-- ✅ Action Buttons -->
        <div class="mt-8 flex flex-col md:flex-row gap-4 justify-center">
          <button
            @click="recreateCampaign"
            class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
          >
            Recreate Campaign
          </button>
          <button
            @click="goBack"
            class="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";
import { usePerkStore } from "@/stores/perk";

const route = useRoute();
const router = useRouter();
const perkStore = usePerkStore();
const campaign = ref<any>(null);

// ✅ Success Rate Calculation
const successRate = computed(() => {
  if (!campaign.value || campaign.value.total === 0) return "0.00";
  return ((campaign.value.redemptions / campaign.value.total) * 100).toFixed(2);
});

// ✅ Campaign Duration Calculation
const campaignDuration = computed(() => {
  if (!campaign.value?.created_at || !campaign.value?.ended_at) return "N/A";

  const start = new Date(campaign.value.created_at);
  const end = new Date(campaign.value.ended_at);
  const diffMs = end.getTime() - start.getTime();

  const hours = Math.floor(diffMs / (1000 * 60 * 60));
  const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diffMs % (1000 * 60)) / 1000);

  if (hours > 0) {
    return `${hours}h ${minutes}m ${seconds}s`;
  } else if (minutes > 0) {
    return `${minutes}m ${seconds}s`;
  } else {
    return `${seconds}s`; // If campaign lasted just a few seconds
  }
});

// ✅ Load Campaign Data
onMounted(async () => {
  if (!route.params.id) {
    console.error("Missing campaign ID in route.");
    return;
  }

  const campaignId = Number(route.params.id);
  if (isNaN(campaignId)) {
    console.error("Invalid campaign ID:", route.params.id);
    return;
  }

  await perkStore.loadPastPerksFromDB();
  campaign.value = perkStore.pastPerks?.find((p) => p.id === campaignId);

  if (!campaign.value) {
    console.warn("Campaign not found:", campaignId);
  }
});

// ✅ Recreate Campaign
const recreateCampaign = () => {
  if (!campaign.value) return;
  router.push({ path: "/business/create-campaign", query: campaign.value });
};

// ✅ Go Back
const goBack = () => {
  router.push("/business");
};
</script>
