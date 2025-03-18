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
          Complete your business profile to start attracting new customers.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form @submit.prevent="completeOnboarding" class="space-y-4">
          <div>
            <Label>Business Name</Label>
            <Input v-model="business.official_name" required />
          </div>

          <div>
            <Label>Street Address</Label>
            <Input v-model="business.street_address" required />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <Label>City</Label>
              <Input v-model="business.city" required />
            </div>
            <div>
              <Label>State</Label>
              <Input v-model="business.state" required />
            </div>
            <div>
              <Label>Zip Code</Label>
              <Input v-model="business.zip_code" required />
            </div>
          </div>

          <div>
            <Label>Business Category</Label>
            <Input
              v-model="business.category"
              placeholder="e.g. Cafe, Retail, Salon"
              required
            />
          </div>

          <div>
            <Label>Website URL</Label>
            <Input v-model="business.website" type="url" required />
          </div>

          <div>
            <Label>Contact Phone Number (Optional)</Label>
            <Input
              v-model="business.phone"
              type="tel"
              placeholder="123-456-7890"
            />
          </div>

          <Button type="submit" class="w-full">Save & Complete</Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

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
    };
  } catch (error) {
    console.error("Error fetching user profile:", error);
  }
});

const completeOnboarding = async () => {
  try {
    const token = useCookie("auth_token");

    await $fetch("http://localhost:8000/account/onboarding/", {
      method: "PUT",
      headers: {
        Authorization: `Token ${token.value}`,
      },
      body: business.value,
    });

    router.replace("/business");
  } catch (error) {
    console.error("Failed to complete onboarding:", error);
    alert("Failed to complete onboarding. Please try again.");
  }
};
</script>
