<script setup lang="ts">
import { toast } from "@/components/ui/toast";
import { ref, computed } from "vue";
import * as z from "zod";
import Input from "./ui/input/Input.vue";

const isOpen = ref(false);

const perkTitle = ref("");
const perkDescription = ref("");
const totalPerks = ref<number | undefined>(undefined); // fixed here

const touched = ref({
  perkTitle: false,
  perkDescription: false,
  totalPerks: false,
});

// Mark field as touched
const markTouched = (field: string) => {
  touched.value[field] = true;
};

// Form validation schema
const formSchema = z.object({
  perkTitle: z
    .string()
    .min(5, "Perk title must be at least 5 characters.")
    .max(50, "Perk title must be fewer than 50 characters"),
  perkDescription: z
    .string()
    .min(5, "Perk description must be at least 5 characters.")
    .max(100, "Perk description must be fewer than 100 characters"),
  totalPerks: z
    .number({ invalid_type_error: "Total perks must be a valid number" })
    .min(1, "Total perks must be at least 1"),
});

// Compute validation errors
const formErrors = computed(() => {
  const result = formSchema.safeParse({
    perkTitle: perkTitle.value,
    perkDescription: perkDescription.value,
    totalPerks: totalPerks.value !== undefined ? totalPerks.value : NaN,
  });

  if (result.success) return {};

  return Object.fromEntries(
    result.error.issues.map((issue) => [issue.path[0], issue.message])
  );
});

const isFormValid = computed(() => Object.keys(formErrors.value).length === 0);

// Utility to get auth token from cookies
const getToken = () => {
  const match = document.cookie.match(new RegExp("(^| )auth_token=([^;]+)"));
  return match ? match[2] : null;
};

// Form submission
async function onSubmit() {
  if (!isFormValid.value) {
    toast({
      title: "Form Error",
      description: "Please correct errors before submitting.",
    });
    return;
  }

  try {
    const response: any = await $fetch(
      "http://localhost:8000/account/create-perk/",
      {
        method: "POST",
        headers: { Authorization: `Token ${getToken()}` },
        body: {
          title: perkTitle.value,
          description: perkDescription.value,
          total: totalPerks.value,
        },
      }
    );

    const store = usePerkStore();
    store.setPerk(response);

    isOpen.value = false;

    toast({
      title: "Congratulations 🎉",
      description:
        "Your perk campaign has been successfully created! Please print your QR code.",
    });
  } catch (error) {
    console.error("Failed to create campaign:", error);
    toast({
      title: "Error",
      description: "Failed to create the campaign. Please try again.",
    });
  }
}
</script>

<template>
  <div>
    <Dialog v-model:open="isOpen">
      <DialogTrigger as-child>
        <button
          class="mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
        >
          Create New Campaign
        </button>
      </DialogTrigger>

      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle class="text-2xl font-bold text-gray-800">
            Create a New Campaign
          </DialogTitle>
          <DialogDescription>
            Fill in the details below to create your perk campaign.
          </DialogDescription>
        </DialogHeader>

        <form @submit.prevent="onSubmit">
          <!-- Perk Title -->
          <Label class="block mb-1 font-medium text-gray-700" for="perkTitle"
            >Perk Title</Label
          >
          <Input
            id="perkTitle"
            v-model="perkTitle"
            placeholder="Discounted Latte"
            class="w-full p-2 border rounded-lg"
            @blur="markTouched('perkTitle')"
          />
          <p class="text-red-500 text-sm h-5">
            {{ touched.perkTitle ? formErrors.perkTitle : "" }}
          </p>

          <!-- Perk Description -->
          <Label
            class="block mt-3 mb-1 font-medium text-gray-700"
            for="perkDescription"
          >
            Perk Description
          </Label>
          <Textarea
            id="perkDescription"
            v-model="perkDescription"
            placeholder="Get $2 off a latte"
            class="w-full p-2 border rounded-lg"
            @blur="markTouched('perkDescription')"
          />
          <p class="text-red-500 text-sm h-5">
            {{ touched.perkDescription ? formErrors.perkDescription : "" }}
          </p>

          <!-- Total Perks -->
          <Label
            class="block mt-3 mb-1 font-medium text-gray-700"
            for="totalPerks"
          >
            Total Perks Available
          </Label>
          <Input
            id="totalPerks"
            v-model.number="totalPerks"
            type="number"
            placeholder="50"
            class="w-full p-2 border rounded-lg no-arrows"
            @blur="markTouched('totalPerks')"
          />
          <p class="text-red-500 text-sm h-5">
            {{ touched.totalPerks ? formErrors.totalPerks : "" }}
          </p>

          <!-- Submit Button -->
          <DialogFooter>
            <div class="mt-6 w-full">
              <button
                type="submit"
                :disabled="!isFormValid"
                :class="[
                  'w-full py-2 rounded-lg transition text-white',
                  isFormValid
                    ? 'bg-blue-600 hover:bg-blue-700'
                    : 'bg-gray-400 cursor-not-allowed',
                ]"
              >
                Confirm & Generate QR
              </button>
            </div>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  </div>
</template>
