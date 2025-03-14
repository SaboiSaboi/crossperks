<script setup lang="ts">
// Define campaign types
interface Campaign {
  id: number;
  name: string;
  remaining: number;
  total: number;
  redemptions: number;
}

interface Insights {
  newCustomers: number;
  returningCustomers: number;
  scans: number;
  conversionRate: number;
}

const campaign = ref<Campaign | null>(null);

const insights = ref<Insights>({
  newCustomers: 0,
  returningCustomers: 0,
  scans: 0,
  conversionRate: 0,
});

const pastCampaigns = ref<Campaign[] | null>(null);
const perkStore = usePerkStore();

// Computed properties
const campaignProgress = computed(() => {
  if (perkStore.perk && perkStore.perk.total) {
    return (perkStore.perk.remaining / perkStore.perk.total) * 100;
  }
  return 0; // or any default value you'd prefer
});

// Event Handlers
const downloadQR = () => {
  alert("Downloading QR Code...");
};

const generateCode = () => {
  alert("Generated new one-time use code.");
};

const endCampaign = () => {
  campaign.value = null;
  // alert("Campaign ended. Create a new one when you're ready.");
};

const { handleCheckAuth } = useAuthS();

const business_user: any = await handleCheckAuth();
const business = business_user.business_profile;

onMounted(() => {
  perkStore.loadPerk();
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-900">
    <HeaderSignedIn />
    <div
      class="shadow-md p-6 md:p-10 flex flex-col md:flex-row justify-center items-center"
    >
      <div class="flex flex-col justify-center items-center">
        <h1 class="text-4xl font-extrabold text-gray-800">
          {{ business.official_name }} Dashboard
        </h1>
        <p class="text-lg text-gray-600 mt-2">
          Manage your CrossPerks campaigns and track results.
        </p>
      </div>
    </div>
    <div
      class="max-w-6xl mx-auto p-6 md:p-10 h-screen flex flex-col justify-center"
    >
      <div
        v-if="perkStore.isLoading"
        class="flex justify-center py-5 h-[20rem]"
      >
        <p class="text-gray-500">Loading</p>
      </div>
      <div
        v-else-if="perkStore.perk"
        class="grid grid-cols-1 md:grid-cols-3 gap-6 h-[19rem]"
      >
        <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
          <h2 class="text-xl font-semibold text-indigo-700">Active Campaign</h2>
          <p class="mt-2 text-lg font-bold text-gray-800">
            {{ perkStore.perk?.title }}
          </p>

          <p class="mb-2 text-base text-gray-800">
            {{ perkStore.perk?.description }}
          </p>
          <hr class="my-2" />
          <p class="text-gray-600">
            Perks Remaining:
            <span class="font-semibold"
              >{{ perkStore.perk?.remaining }} /
              {{ perkStore.perk?.total }}</span
            >
          </p>
          <p class="text-gray-600">
            Redemptions:
            <span class="font-semibold">{{ perkStore.perk?.redemptions }}</span>
          </p>

          <Progress class="mt-4" :model-value="campaignProgress" />
          <p class="mt-1 text-sm text-gray-500">
            Redemptions: {{ campaignProgress }}%
          </p>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
          <h2 class="text-xl font-semibold text-indigo-700">
            Performance Insights
          </h2>
          <p class="mt-2 text-gray-600">
            New Customers:
            <span class="font-bold text-gray-800">{{
              insights.newCustomers
            }}</span>
          </p>
          <p class="text-gray-600">
            Returning Customers:
            <span class="font-bold text-gray-800">{{
              insights.returningCustomers
            }}</span>
          </p>
          <p class="text-gray-600">
            Total Scans:
            <span class="font-bold text-gray-800">{{ insights.scans }}</span>
          </p>
          <p class="text-gray-600">
            Conversion Rate:
            <span class="font-bold text-gray-800"
              >{{ insights.conversionRate }}%</span
            >
          </p>
        </div>

        <div
          class="bg-white p-6 rounded-lg shadow-lg border border-gray-200 items-center"
        >
          <h2 class="text-xl font-semibold text-indigo-700">Manage Campaign</h2>
          <button
            @click="generateCode"
            class="mt-4 px-5 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
          >
            Generate One-Time Code
          </button>
          <!-- <div class="relative text-xs text-gray-500">
            <button @click="endCampaign">End Campaign</button>
          </div> -->
        </div>
      </div>

      <span v-else>
        <div class="flex flex-col items-center justify-center py-20">
          <h2 class="text-2xl font-bold text-gray-800">No Active Campaign</h2>
          <p class="text-gray-600 mt-2 text-lg">
            Create a new campaign to start sending and receiving referrals.
          </p>
          <CampaignModal />
        </div>
      </span>
      <div class="mt-10">
        <h2 class="text-2xl font-extrabold text-gray-800">Past Campaigns</h2>
        <div
          v-if="pastCampaigns"
          class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6"
        >
          <div
            v-for="past in pastCampaigns"
            :key="past.id"
            class="bg-white p-6 rounded-lg shadow-lg border border-gray-200"
          >
            <p class="text-lg font-bold text-gray-800">{{ past.name }}</p>
            <p class="text-gray-600">
              Redemptions:
              <span class="font-semibold">{{ past.redemptions }}</span>
            </p>
            <p class="text-gray-600">
              Total Scans: <span class="font-semibold">{{ past.total }}</span>
            </p>
          </div>
        </div>
        <div v-else class="mt-24 text-lg flex justify-center items-center">
          No past campaigns yet
        </div>
      </div>
    </div>
  </div>
</template>
