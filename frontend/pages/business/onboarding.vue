<script setup lang="ts">
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
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>

    <Card class="w-full max-w-lg shadow-lg overflow-y-auto h-[80dvh]">
      <CardHeader>
        <CardTitle class="text-2xl text-center"
          >Welcome to CrossPerks!</CardTitle
        >
        <CardDescription class="text-center">
          Complete your business profile to start attracting new customers.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form @submit.prevent="completeOnboarding" class="space-y-4">
          <div>
            <Label for="official_name">Business Name</Label>
            <Input
              id="official_name"
              v-model="business.official_name"
              required
            />
          </div>

          <div>
            <Label for="streetAddress">Street Address</Label>
            <Input
              id="streetAddress"
              v-model="business.street_address"
              required
            />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <Label for="city">City</Label>
              <Input id="city" v-model="business.city" required />
            </div>
            <div>
              <Label for="state">State</Label>
              <Input id="state" v-model="business.state" required />
            </div>
            <div>
              <Label for="zipCode">Zip Code</Label>
              <Input id="zipCode" v-model="business.zip_code" required />
            </div>
          </div>

          <div>
            <Label for="category">Business Category</Label>
            <Input
              id="category"
              v-model="business.category"
              placeholder="e.g. Cafe, Retail, Salon"
              required
            />
          </div>

          <div>
            <Label for="website">Website URL</Label>
            <Input
              id="website"
              v-model="business.website"
              type="url"
              required
            />
          </div>

          <div>
            <Label for="phone">Contact Phone Number (Optional)</Label>
            <Input
              id="phone"
              v-model="business.phone"
              type="tel"
              placeholder="123-456-7890"
            />
          </div>

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
</template>
