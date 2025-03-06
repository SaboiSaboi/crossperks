<script setup lang="ts">
// Define campaign types
interface Campaign {
  id: number;
  name: string;
  remaining: number;
  total: number;
  redemptions: number;
  qrCode: string;
}

interface Insights {
  newCustomers: number;
  returningCustomers: number;
  scans: number;
  conversionRate: number;
}

// Reactive state
const campaign = ref<Campaign | null>({
  id: 1,
  name: "$1 Off Any Coffee Drink",
  remaining: 12,
  total: 30,
  redemptions: 18,
  qrCode: "https://your-qr-code-link.com",
});

const insights = ref<Insights>({
  newCustomers: 24,
  returningCustomers: 8,
  scans: 52,
  conversionRate: 35,
});

const pastCampaigns = ref<Campaign[]>([
  {
    id: 2,
    name: "$5 Off Haircuts",
    remaining: 0,
    total: 40,
    redemptions: 30,
    qrCode: "",
  },
  {
    id: 3,
    name: "Free Dessert with Meal",
    remaining: 0,
    total: 25,
    redemptions: 15,
    qrCode: "",
  },
]);

// Computed properties
const campaignProgress = computed(() => {
  if (!campaign.value) return 0;
  return ((campaign.value.redemptions / campaign.value.total) * 100).toFixed(0);
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

const createCampaign = () => {
  campaign.value = {
    id: 4,
    name: "10% Off Your Next Meal",
    remaining: 20,
    total: 50,
    redemptions: 0,
    qrCode: "https://your-new-qr-code.com",
  };
  alert("New campaign created!");
};

onMounted(() => {
  console.log("Business dashboard loaded.");
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-900">
    <!-- Header -->

    <div
      class="bg-white shadow-md p-6 md:p-10 flex flex-col md:flex-row justify-between items-center"
    >
      <div>
        <h1 class="text-4xl font-extrabold text-gray-800">
          Business Dashboard
        </h1>
        <p class="text-lg text-gray-600 mt-2">
          Manage your CrossPerks campaigns and track results.
        </p>
      </div>
      <button
        v-if="campaign"
        @click="endCampaign"
        class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition"
      >
        End Current Campaign
      </button>
    </div>

    <!-- Main Content -->
    <div class="max-w-6xl mx-auto p-6 md:p-10">
      <div v-if="campaign" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Active Campaign Card -->
        <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
          <h2 class="text-xl font-semibold text-indigo-700">Active Campaign</h2>
          <p class="mt-2 text-lg font-bold text-gray-800">
            {{ campaign.name }}
          </p>
          <p class="text-gray-600">
            Perks Remaining:
            <span class="font-semibold"
              >{{ campaign.remaining }} / {{ campaign.total }}</span
            >
          </p>
          <p class="text-gray-600">
            Redemptions:
            <span class="font-semibold">{{ campaign.redemptions }}</span>
          </p>

          <!-- Progress Bar -->
          <div class="mt-4 w-full bg-gray-200 rounded-full h-3">
            <div
              class="bg-indigo-600 h-3 rounded-full transition-all duration-500"
              :style="{ width: campaignProgress + '%' }"
            ></div>
          </div>
          <p class="mt-1 text-sm text-gray-500">
            Redemptions: {{ campaignProgress }}%
          </p>

          <!-- QR Code Section -->
          <div class="mt-4 flex flex-col items-center">
            <NuxtImg :src="campaign.qrCode" alt="QR Code" class="w-40 h-40" />
            <button
              @click="downloadQR"
              class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            >
              Download QR Code
            </button>
          </div>
        </div>

        <!-- Performance Insights -->
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

        <!-- Actions -->
        <div
          class="bg-white p-6 rounded-lg shadow-lg border border-gray-200 flex flex-col items-center"
        >
          <h2 class="text-xl font-semibold text-indigo-700">Manage Campaign</h2>
          <button
            @click="generateCode"
            class="mt-4 px-5 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
          >
            Generate One-Time Code
          </button>
          <button
            @click="endCampaign"
            class="mt-2 px-5 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
          >
            End Campaign
          </button>
        </div>
      </div>

      <!-- No Active Campaign -->
      <div v-else class="flex flex-col items-center justify-center py-20">
        <h2 class="text-2xl font-bold text-gray-800">No Active Campaign</h2>
        <p class="text-gray-600 mt-2 text-lg">
          Create a new campaign to start sending and receiving referrals.
        </p>
        <CampaignModal />
      </div>

      <div class="mt-10">
        <h2 class="text-2xl font-extrabold text-gray-800">Past Campaigns</h2>
        <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
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
      </div>
    </div>
  </div>
</template>
