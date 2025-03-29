<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { z } from "zod";
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
  state: "Oregon",
  zip_code: "",
  category: "",
  website: "",
  phone: "",
  identifiers: [],
});

const allIdentifiers = ref<any>([]);
const errorMessages = ref<Record<string, string>>({});
const touched = ref<Record<string, boolean>>({});

const schema = z.object({
  official_name: z.string().min(2, "Business name required"),
  street_address: z.string().min(5, "Street address required"),
  city: z.string().min(2, "City required"),
  zip_code: z.string().regex(/^\d{5}$/, "Zip code must be exactly 5 digits"),
  category: z.string().min(2, "Category required"),
  website: z.string().url("Enter a valid URL"),
  phone: z.string().optional(),
});

const isFormValid = computed(() => {
  const result = schema.safeParse(business.value);
  errorMessages.value = result.success
    ? {}
    : Object.fromEntries(
        result.error.issues.map((e) => [e.path[0], e.message])
      );

  return result.success;
});

onMounted(async () => {
  try {
    const user: any = await handleCheckAuth();
    const profile = user.business_profile;

    business.value = {
      official_name: profile.official_name,
      street_address: profile.street_address,
      city: profile.city,
      state: "Oregon",
      zip_code: profile.zip_code,
      category: "",
      website: profile.website ?? "https://",
      phone: "",
      identifiers: profile.identifiers || [],
    };

    const response: any = await $fetch(
      "http://localhost:8000/account/identifiers/"
    );
    allIdentifiers.value = response;
  } catch (error) {
    console.error("Error fetching profile or identifiers:", error);
  }
});

const getIdentifierIds = (selectedNames) =>
  allIdentifiers.value
    .filter((id) => selectedNames.includes(id.name))
    .map((id) => id.id);

const completeOnboarding = async () => {
  if (!isFormValid.value) {
    alert("Please fix errors before continuing.");
    return;
  }

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
    console.error("Onboarding failed:", error);
    alert("Onboarding failed. Please try again.");
  }
};

const markTouched = (field: string) => {
  touched.value[field] = true;
};
</script>

<template>
  <div
    class="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4"
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
              @blur="markTouched('official_name')"
            />
            <p class="text-sm text-red-500">
              {{ touched.official_name && errorMessages.official_name }}
            </p>
          </div>

          <div>
            <Label for="streetAddress">Street Address</Label>
            <Input
              id="streetAddress"
              v-model="business.street_address"
              @blur="markTouched('street_address')"
            />
            <p class="text-sm text-red-500">
              {{ touched.street_address && errorMessages.street_address }}
            </p>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <Label for="city">City</Label>
              <Input
                id="city"
                v-model="business.city"
                @blur="markTouched('city')"
              />
              <p class="text-sm text-red-500">
                {{ touched.city && errorMessages.city }}
              </p>
            </div>
            <div>
              <Label for="state">State</Label>
              <Input
                id="state"
                v-model="business.state"
                disabled
                class="bg-gray-100 cursor-not-allowed"
              />
            </div>
          </div>

          <div>
            <Label for="zipCode">Zip Code</Label>
            <Input
              id="zipCode"
              v-model="business.zip_code"
              @blur="markTouched('zip_code')"
            />
            <p class="text-sm text-red-500">
              {{ touched.zip_code && errorMessages.zip_code }}
            </p>
          </div>

          <div>
            <Label for="category">Business Category</Label>
            <Input
              id="category"
              v-model="business.category"
              placeholder="e.g., Cafe, Retail"
              @blur="markTouched('category')"
            />
            <p class="text-sm text-red-500">
              {{ touched.category && errorMessages.category }}
            </p>
          </div>

          <div>
            <Label for="website">Website URL</Label>
            <Input
              id="website"
              v-model="business.website"
              type="url"
              @blur="markTouched('website')"
            />
            <p class="text-sm text-red-500">
              {{ touched.website && errorMessages.website }}
            </p>
          </div>

          <div>
            <Label for="phone">Contact Phone (Optional)</Label>
            <Input
              id="phone"
              v-model="business.phone"
              placeholder="123-456-7890"
            />
          </div>

          <div>
            <Label>Select Your Business Identifiers</Label>
            <div class="grid grid-cols-2 gap-2 mt-2">
              <label
                v-for="id in allIdentifiers"
                :key="id.id"
                class="flex items-center space-x-2"
              >
                <input
                  type="checkbox"
                  :value="id.name"
                  v-model="business.identifiers"
                  class="rounded border-gray-300"
                />
                <span>{{ id.name }}</span>
              </label>
            </div>
          </div>

          <Button type="submit" class="w-full" :disabled="!isFormValid">
            Save & Complete
          </Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
