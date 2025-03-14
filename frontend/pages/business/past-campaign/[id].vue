<template>
  <div class="min-h-screen bg-gray-50 py-0">
    <HeaderSignedIn />
    <div class="h-dvh flex items-center">
      <div
        class="container mx-auto max-w-4xl bg-white p-6 rounded-lg shadow-md border border-gray-300"
      >
        <!-- ✅ Campaign Title -->
        <h1 class="text-3xl font-bold text-gray-900">
          {{ campaign?.title || "Loading..." }}
        </h1>
        <p class="text-lg text-gray-700 mt-2">{{ campaign?.description }}</p>

        <!-- ✅ Campaign Details -->
        <div v-if="campaign" class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-gray-600">Total Perks Offered:</p>
            <p class="text-xl font-semibold text-gray-900">
              {{ campaign.total }}
            </p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-gray-600">Redemptions:</p>
            <p class="text-xl font-semibold text-gray-900">
              {{ campaign.redemptions }}
            </p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-gray-600">Success Rate:</p>
            <p class="text-xl font-semibold text-gray-900">
              {{ successRate }}%
            </p>
          </div>
          <div class="bg-gray-100 p-4 rounded-lg">
            <p class="text-gray-600">Created At:</p>
            <p class="text-md font-semibold text-gray-900">
              {{ formattedDate }}
            </p>
          </div>
        </div>

        <!-- ✅ Action Buttons -->
        <div class="mt-8 flex flex-col md:flex-row gap-4">
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
            Back to Past Campaigns
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

// ✅ Success rate calculation
const successRate = computed(() => {
  if (!campaign.value) return 0;
  return ((campaign.value.redemptions / campaign.value.total) * 100).toFixed(2);
});

// ✅ Format Date
const formattedDate = computed(() => {
  if (!campaign.value?.created_at) return "Unknown";
  return new Date(campaign.value.created_at).toLocaleDateString();
});

// ✅ Load Campaign
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

// ✅ Recreate Campaign Function
const recreateCampaign = () => {
  if (!campaign.value) return;
  console.log("Recreating campaign:", campaign.value);

  router.push({
    path: "/business/create-campaign",
    query: {
      title: campaign.value.title,
      description: campaign.value.description,
      total: campaign.value.total,
    },
  });
};

// ✅ Go Back Function
const goBack = () => {
  router.push("/business");
};
</script>
