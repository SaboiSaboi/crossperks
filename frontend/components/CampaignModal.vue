<template>
  <div>
    <Form v-slot="{ handleSubmit }" keep-values :validation-schema="formSchema">
      <Dialog v-model:open="isOpen">
        <DialogTrigger as-child>
          <Button
            class="mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 hover:text-white transition"
          >
            Create New Campaign here
          </Button>
        </DialogTrigger>
        <DialogContent class="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle class="text-2xl font-bold text-gray-800">
              Create a New Campaign
            </DialogTitle>
            <DialogDescription>
              Create a new campaign by filling in the following fields.
            </DialogDescription>
          </DialogHeader>

          <form id="dialogForm" @submit.prevent="handleSubmit(onSubmit)">
            <!-- Perk Description Field -->
            <FormField
              v-slot="{ componentField, errorMessage }"
              name="perkDescription"
            >
              <FormItem class="mt-4">
                <FormLabel class="block text-base font-medium text-gray-700">
                  Perk Description
                </FormLabel>
                <FormControl class="">
                  <Textarea
                    v-bind="componentField"
                    class="my-2 p-3 border rounded-lg w-full"
                    placeholder="e.g., Get a free cookie with any coffee purchase!"
                  />
                </FormControl>
                <FormMessage class="h-2" v-if="errorMessage" />
                <div v-else class="text-xs h-2"></div>
              </FormItem>
            </FormField>

            <!-- Total Perks Available Field -->
            <FormField
              v-slot="{ componentField, errorMessage }"
              name="totalPerks"
            >
              <FormItem class="mt-4">
                <FormLabel class="block text-base font-medium text-gray-700">
                  Total Perks Available
                </FormLabel>
                <FormControl>
                  <Input
                    v-bind="componentField"
                    type="number"
                    min="1"
                    class="mt-2 p-3 border rounded-lg w-full [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    placeholder="e.g., 50"
                  />
                </FormControl>
                <FormMessage class="h-2" v-if="errorMessage" />
                <div v-else class="text-xs h-2"></div>
              </FormItem>
            </FormField>

            <DialogFooter>
              <div class="mt-6 flex justify-end w-full">
                <Button
                  type="submit"
                  class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                >
                  Confirm & Generate QR
                </Button>
              </div>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </Form>
  </div>
</template>

<script setup lang="ts">
import { toast } from "@/components/ui/toast";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";

const isOpen = ref(false);

const formSchema = toTypedSchema(
  z.object({
    perkDescription: z
      .string()
      .min(5, {
        message: "Perk description need to be at least 5 characters.",
      })
      .max(100, {
        message: "Perk description needs to be fewer than 100 characters",
      }),
    totalPerks: z
      .number({ message: "Total perks must be a valid number" })
      .min(1, { message: "Total perks must be at least 1" }),
  })
);

interface Campaign {
  id: number;
  name: string;
  remaining: number;
  total: number;
  redemptions: number;
  qrCode: string;
}

interface NewCampaignInterface {
  businessName: string;
  perkDescription: string;
  totalPerks: number;
}

const newCampaignData = ref<NewCampaignInterface | null>(null);

const businessName = "Some Business Name";
const businessCampaign = `https://www.crossperks.com/${businessName}?address:"123-main-st-portland-or, "`;

function onSubmit(values: any) {
  console.log(typeof values);

  newCampaignData.value = {
    businessName: businessName,
    perkDescription: values.perkDescription,
    totalPerks: values.totalPerks,
  };

  // send data to backend, save it in table, return data describing the current perk

  isOpen.value = false;
  setTimeout(() => {
    toast({
      title: "Congratulations 🎉",
      description:
        "Your perk campaign has been successfully create! Please print your campaign's QR code provided and place it visibly near your point of sales counter.",
    });
  }, 300);
}
</script>
