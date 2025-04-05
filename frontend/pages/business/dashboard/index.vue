<script setup lang="ts">
import { useRouter } from "vue-router";
const router = useRouter();

interface Insights {
  newCustomers: number;
  returningCustomers: number;
  scans: number;
  conversionRate: number;
}

const insights = ref<Insights>({
  newCustomers: 0,
  returningCustomers: 0,
  scans: 0,
  conversionRate: 0,
});

const perkStore = usePerkStore();

const campaignProgress = computed(() => {
  if (perkStore.perk && perkStore.perk.total) {
    return (perkStore.perk.remaining / perkStore.perk.total) * 100;
  }
  return 0;
});

const generateCode = () => {
  alert("Generated new one-time use code.");
};

const endCampaign = async () => {
  try {
    if (!perkStore.perk) {
      console.warn("No active campaign found.");
      return;
    }

    const campaignId = perkStore.perk.id;

    await $fetch(`http://localhost:8000/account/perks/${campaignId}/end/`, {
      method: "POST",
      headers: {
        Authorization: `Token ${useCookie("auth_token").value}`,
      },
    });

    perkStore.clearPerk();
    await perkStore.loadPastPerksFromDB();

    router.push("/business/dashboard");
  } catch (error) {
    console.error("Failed to end campaign:", error);
  }
};

const { handleCheckAuth } = useAuthS();

const business_user: any = await handleCheckAuth();
const business = business_user.business_profile;

const navigateToCampaign = (pastCampaign: any) => {
  if (!pastCampaign.id) {
    console.error("Attempted to navigate with an undefined campaign ID");
    return;
  }
  router.push(`/business/past-campaign/${pastCampaign.id}`);
};
onMounted(async () => {
  await perkStore.loadPerk();
  await perkStore.loadPastPerksFromDB();
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-900">
    <section class="bg-gray-950"><Header /></section>
    <ClientOnly>
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
        class="max-w-6xl mx-auto p-6 md:p-10 h-screen justify-center grid grid-col-2"
      >
        <!-- <div
          v-show="perkStore.isLoading"
          class="flex justify-center py-5 h-[20rem]"
        >
          <p class="text-gray-500 bg-yellow-200 w-full">Loading....</p>
        </div> -->
        <div
          class="grid grid-cols-1 md:grid-cols-3 gap-6 h-[19rem]"
          v-show="!perkStore.isLoading && perkStore.perk"
        >
          <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
            <h2 class="text-xl font-semibold text-indigo-700">
              Active Campaign
            </h2>
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
              <span class="font-semibold">{{
                perkStore.perk?.redemptions
              }}</span>
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
            class="bg-white p-6 rounded-lg shadow-lg border border-gray-200 items-center relative"
          >
            <h2 class="text-xl font-semibold text-indigo-700">
              Manage Campaign
            </h2>
            <div class="">
              <button
                @click="generateCode"
                class="mt-4 px-5 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
              >
                Generate One-Time Code
              </button>
            </div>
            <div
              class="absolute bottom-0 left-0 mb-4 ml-3 text-lg flex justify-center items-center hover:bg-none"
            >
              <DropdownMenu>
                <DropdownMenuTrigger as-child>
                  <Button variant="ghost">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke-width="1.5"
                      stroke="currentColor"
                      class="size-6"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M6.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM18.75 12a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
                      />
                    </svg>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent class="w-56">
                  <DropdownMenuLabel class="flex justify-center"
                    >Edit Campaign?</DropdownMenuLabel
                  >
                  <DropdownMenuSeparator />
                  <Button variant="ghost" class="flex justify-center w-full">
                    <AlertDialog>
                      <AlertDialogTrigger as-child>
                        <span> Continue </span>
                      </AlertDialogTrigger>
                      <AlertDialogContent>
                        <AlertDialogHeader>
                          <AlertDialogTitle
                            >Are you sure you want to end this
                            campaign?</AlertDialogTitle
                          >
                          <AlertDialogDescription>
                            Ending this campaign will archive it permanently.
                            This action cannot be undone.
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel>Cancel</AlertDialogCancel>
                          <AlertDialogAction @click="endCampaign"
                            >Continue</AlertDialogAction
                          >
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  </Button>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>

        <span v-if="!perkStore.isLoading && !perkStore.perk">
          <div class="flex flex-col items-center justify-center py-20">
            <h2 class="text-2xl font-bold text-gray-800">No Active Campaign</h2>
            <p
              class="text-gray-600 mt-6 text-lg text-center text-balance max-w-2xl flex flex-col justify-center items-center"
            >
              A campaign is a promotion that rewards customers and drives
              engagement. Create one to start receiving customers!
            </p>
            <CampaignModal />
          </div>
        </span>
        <hr />
        <div class="mt-10">
          <div
            v-if="perkStore.pastPerks && perkStore.pastPerks.length > 0"
            class=""
          >
            <h2
              class="text-2xl font-extrabold text-gray-800 flex justify-center"
            >
              Past Campaigns
            </h2>
            <div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div
                v-for="past in perkStore.pastPerks"
                :key="past.id"
                @click="navigateToCampaign(past)"
                class="bg-white p-6 rounded-lg shadow-lg border border-gray-200"
              >
                <p class="text-lg font-bold text-gray-800">{{ past.title }}</p>
                <p class="text-lg text-gray-800">{{ past.description }}</p>
                <p class="text-lg text-gray-800">Total: {{ past.total }}</p>
                <p class="text-gray-600">
                  Redemptions:
                  <span class="font-semibold">{{ past.redemptions }}</span>
                </p>
                <p class="text-gray-600">
                  Total Scans:
                  <span class="font-semibold">{{ past.total }}</span>
                </p>
              </div>
            </div>
          </div>

          <div v-else class="mt-24 text-lg flex justify-center items-center">
            No past campaigns yet
          </div>
        </div>
      </div>
    </ClientOnly>
  </div>
</template>
