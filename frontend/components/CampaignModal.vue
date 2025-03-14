<template>
  <div>
    <Form v-slot="{ handleSubmit }" keep-values :validation-schema="formSchema">
      <Dialog v-model:open="isOpen">
        <DialogTrigger as-child>
          <Button
            class="mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 hover:text-white transition"
          >
            Create New Campaign
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
            <FormField
              v-slot="{ componentField, errorMessage }"
              name="perkTitle"
            >
              <FormItem class="mt-4">
                <FormLabel class="block text-base font-medium text-gray-700">
                  Perk Title
                </FormLabel>
                <FormControl class="">
                  <Input
                    v-bind="componentField"
                    class="my-2 p-3 border rounded-lg w-full"
                    placeholder="e.g., Free Cookie."
                  />
                </FormControl>
                <FormMessage class="h-2" v-if="errorMessage" />
                <div v-else class="text-xs h-2"></div>
              </FormItem>
            </FormField>

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
import { Inbox } from "lucide-vue-next";
import * as z from "zod";
import Input from "./ui/input/Input.vue";

const isOpen = ref(false);

const formSchema = toTypedSchema(
  z.object({
    perkTitle: z
      .string()
      .min(5, {
        message: "Perk title need to be at least 3 characters.",
      })
      .max(100, {
        message: "Perk title needs to be fewer than 50 characters",
      }),
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

const getToken = () => {
  const match = document.cookie.match(new RegExp("(^| )auth_token=([^;]+)"));
  return match ? match[2] : null;
};

async function onSubmit(values: any) {
  try {
    const response: any = await $fetch(
      "http://localhost:8000/account/create-perk/",
      {
        method: "POST",
        headers: {
          Authorization: `Token ${getToken()}`,
        },
        body: {
          title: values.perkTitle,
          description: values.perkDescription,
          total: values.totalPerks,
        },
      }
    );

    const store = usePerkStore();

    store.setPerk({
      title: response.title,
      description: response.description,
      total: response.total,
      remaining: response.remaining,
      isActive: response.is_active,
      redemptions: response.redemptions,
    });

    isOpen.value = false;

    setTimeout(() => {
      toast({
        title: "Congratulations 🎉",
        description: `Your perk campaign has been successfully created! Please print your QR code.`,
      });
    }, 300);
  } catch (error) {
    console.error("Failed to create campaign:", error);
    toast({
      title: "Error",
      description: "Failed to create the campaign. Please try again.",
    });
  }
}
</script>
