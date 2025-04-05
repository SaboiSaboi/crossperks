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
import { Button } from "@/components/ui/button";

const router = useRouter();
const { handleCheckAuth } = useAuthS();

const selectedIdentifiers = ref<string[]>([]);
const allIdentifiers = ref<any[]>([]);

onMounted(async () => {
  try {
    await handleCheckAuth();
    const response: any = await $fetch(
      "http://localhost:8000/account/identifiers/"
    );
    allIdentifiers.value = response;
  } catch (error) {
    console.error("Error loading identifiers:", error);
  }
});

// Use slug instead of ID, since server expects slugs
const getIdentifierIds = (selectedNames: string[]) =>
  allIdentifiers.value
    .filter((id) => selectedNames.includes(id.name))
    .map((id) => id.id);

const completeOnboarding = async () => {
  try {
    const token = useCookie("auth_token");

    await $fetch("http://localhost:8000/account/customer-onboarding/", {
      method: "PUT", // must match Django view
      headers: {
        Authorization: `Token ${token.value}`,
      },
      body: {
        preferred_identifiers: getIdentifierIds(selectedIdentifiers.value),
      },
    });

    router.replace("/customer/dashboard");
  } catch (error) {
    console.error("Onboarding failed:", error);
    alert("Something went wrong. Please try again.");
  }
};
</script>

<template>
  <div
    class="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>

    <Card class="w-full max-w-lg shadow-lg overflow-y-auto h-[75dvh]">
      <CardHeader>
        <CardTitle class="text-2xl text-center">Almost there!</CardTitle>
        <CardDescription class="text-center">
          Select types of businesses you’d love to support (optional).
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form @submit.prevent="completeOnboarding" class="space-y-6">
          <div>
            <div class="grid grid-cols-2 gap-2">
              <label
                v-for="id in allIdentifiers"
                :key="id.id"
                class="flex items-center space-x-2"
              >
                <input
                  type="checkbox"
                  :value="id.name"
                  v-model="selectedIdentifiers"
                  class="rounded border-gray-300"
                />
                <span>{{ id.name }}</span>
              </label>
            </div>
          </div>

          <Button type="submit" class="w-full">Continue</Button>
          <Button
            type="button"
            variant="ghost"
            class="w-full text-gray-500"
            @click="router.replace('/customer/dashboard')"
          >
            Skip for Now
          </Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
