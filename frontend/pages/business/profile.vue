<template>
  <div>
    <HeaderSignedIn />
    <div
      class="max-w-2xl mx-auto py-10 h-screen flex flex-col gap-10 items-center"
    >
      <Card class="w-full px-32 h-[25.3rem]">
        <CardHeader class="border-b pb-4">
          <CardTitle class="text-xl font-semibold">
            {{ business.official_name }} Profile
          </CardTitle>
        </CardHeader>
        <CardContent class="mt-4">
          <div class="space-y-4">
            <div>
              <span class="text-sm text-gray-500">Business Name</span>
              <p class="text-lg">{{ business.official_name }}</p>
            </div>
            <div>
              <span class="text-sm text-gray-500">Address</span>
              <p class="text-lg">{{ business.street_address }}</p>
              <p>
                {{ business.city }}, {{ business.state }}
                {{ business.zip_code }}
              </p>
            </div>
            <div v-if="website">
              <span class="text-sm text-gray-500">Website</span>
              <p class="text-lg text-blue-600 hover:underline">
                <a :href="website" target="_blank">{{ website }}</a>
              </p>
            </div>
          </div>
        </CardContent>

        <CardFooter class="text-sm text-muted-foreground border-t pt-4">
          <div>
            <p v-if="business.is_claimed" class="text-green-500">Verified ✔️</p>
            <p v-else class="h-5 bg-slate-300"></p>
            <p>Joined on {{ formattedDate }}</p>
          </div>
        </CardFooter>
      </Card>

      <div class="flex flex-col items-center justify-center">
        <h2 class="mb-4">QR Code for your business:</h2>

        <div>
          <img
            :src="business.qr_code"
            alt="Business QR Code"
            class="w-48 h-48 border p-2"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { z } from "zod";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
const website = "https://www.honeycomb-bakery.com";
const BusinessProfileSchema = z.object({
  official_name: z.string(),
  street_address: z.string(),
  city: z.string(),
  state: z.string(),
  zip_code: z.string(),
  is_claimed: z.boolean(),
  created_at: z.string().datetime(),
  qr_code: z.string(),
});

type BusinessProfile = z.infer<typeof BusinessProfileSchema>;

const business = ref<BusinessProfile>({
  official_name: "",
  street_address: "",
  city: "",
  state: "",
  zip_code: "",
  is_claimed: false,
  created_at: new Date().toISOString(),
  qr_code: "",
});

const formattedDate = computed(() => {
  return new Date(business.value.created_at).toLocaleDateString();
});

onMounted(async () => {
  const { handleCheckAuth } = useAuthS();
  const business_user: any = await handleCheckAuth();
  const parsed = BusinessProfileSchema.safeParse(
    business_user.business_profile
  );
  if (parsed.success) {
    business.value = parsed.data;
  } else {
    console.error("Business profile data is invalid:", parsed.error);
  }
});
</script>
