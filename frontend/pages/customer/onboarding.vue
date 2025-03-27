<!-- <script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
const allIdentifiers = ref<any>([]);
const router = useRouter();
const { handleCheckAuth } = useAuthS();

const business = ref({
  official_name: "",
  street_address: "",
  city: "",
  state: "",
  zip_code: "",
  category: "",
  website: "",
  phone: "",
  identifiers: [],
});

onMounted(async () => {
  try {
    const user: any = await handleCheckAuth();
    const businessProfile = user.business_profile;

    business.value = {
      official_name: businessProfile.official_name,
      street_address: businessProfile.street_address,
      city: businessProfile.city,
      state: businessProfile.state,
      zip_code: businessProfile.zip_code,
      category: "",
      website: "https://www.somewebsite.com",
      phone: "",
      identifiers: businessProfile.identifiers,
    };
    const response: any = await $fetch(
      "http://localhost:8000/account/identifiers/"
    );
    allIdentifiers.value = response;
  } catch (error) {
    console.error("Error fetching user profile:", error);
  }
});

const getIdentifierIds = (selectedNames) => {
  return allIdentifiers.value
    .filter((identifier) => selectedNames.includes(identifier.name))
    .map((identifier) => identifier.id);
};

const completeOnboarding = async () => {
  try {
    const token = useCookie("auth_token");

    await $fetch("http://localhost:8000/account/onboarding/", {
      method: "PUT",
      headers: {
        Authorization: `Token ${token.value}`,
      },
      body: {
        ...business.value,
        identifiers: getIdentifierIds(business.value.identifiers),
      },
    });

    router.replace("/business");
  } catch (error) {
    console.error("Failed to complete onboarding:", error);
    alert("Failed to complete onboarding. Please try again.");
  }
};
</script>
<template>
  <div
    class="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8"
  >
    <Card class="w-full max-w-lg shadow-lg">
      <CardHeader>
        <CardTitle class="text-2xl text-center"
          >Welcome to CrossPerks!</CardTitle
        >
        <CardDescription class="text-center">
          Complete your profile to start earning perks.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form @submit.prevent="completeOnboarding" class="space-y-4">
          <div>
            <Label>What is your name?</Label>
            <Input v-model="business.official_name" required />
          </div>
          {{ allIdentifiers }}
          <div>
            <Label>Select Your Business Identifiers</Label>
            <div class="grid grid-cols-2 gap-2 mt-2">
              <label
                v-for="identifier in allIdentifiers"
                :key="identifier.id"
                class="flex items-center space-x-2"
              >
                <input
                  type="checkbox"
                  :value="identifier.name"
                  v-model="business.identifiers"
                  class="rounded border-gray-300"
                />
                <span>{{ identifier.name }}</span>
              </label>
            </div>
          </div>

          <Button type="submit" class="w-full">Save & Complete</Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template> -->
<template>
  <div
    class="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8"
  >
    <Card class="w-full max-w-lg shadow-lg">
      <CardHeader>
        <CardTitle class="text-2xl text-center"
          >Tell Us What Businesses You Support</CardTitle
        >
        <CardDescription class="text-center">
          Select business categories you’d like to support.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form @submit.prevent="completeCustomerOnboarding" class="space-y-4">
          <div>
            <Label>Select Business Identifiers</Label>
            <div class="grid grid-cols-2 gap-2 mt-2">
              <label
                v-for="identifier in allIdentifiers"
                :key="identifier.id"
                class="flex items-center space-x-2"
              >
                <input
                  type="checkbox"
                  :value="identifier.id"
                  v-model="selectedIdentifiers"
                  class="rounded border-gray-300"
                />
                <span>{{ identifier.name }}</span>
              </label>
            </div>
          </div>

          <Button type="submit" class="w-full">Save Preferences</Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

const router = useRouter();
const { handleCheckAuth } = useAuthS();
const allIdentifiers = ref([]);
const selectedIdentifiers = ref([]);

onMounted(async () => {
  try {
    const user = await handleCheckAuth();

    // Fetch all available business identifiers
    const response = await $fetch("http://localhost:8000/account/identifiers/");
    allIdentifiers.value = response;

    // Fetch the customer's selected preferences
    if (user.customer_profile?.preferred_identifiers) {
      selectedIdentifiers.value =
        user.customer_profile.preferred_identifiers.map(
          (identifier) => identifier.id
        );
    }
  } catch (error) {
    console.error("Error fetching identifiers:", error);
  }
});

const completeCustomerOnboarding = async () => {
  try {
    const token = useCookie("auth_token");

    await $fetch("http://localhost:8000/account/customer-onboarding/", {
      method: "PUT",
      headers: {
        Authorization: `Token ${token.value}`,
      },
      body: {
        preferred_identifiers: selectedIdentifiers.value, // ✅ Send IDs instead of names
      },
    });

    router.replace("/customer/dashboard");
  } catch (error) {
    console.error("Failed to complete onboarding:", error);
    alert("Failed to complete onboarding. Please try again.");
  }
};
</script>
