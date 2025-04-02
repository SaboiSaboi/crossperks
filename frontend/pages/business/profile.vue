<template>
  <div>
    <div class="bg-gray-950 no-print">
      <Header />
    </div>
    <div
      class="max-w-4xl mx-auto py-10 h-screen flex flex-col gap-10 items-center justify-center"
    >
      <Card class="w-full px-0 h-fit no-print">
        <CardHeader class="border-b pb-4">
          <CardTitle class="text-xl font-semibold">
            {{ business.official_name }} Profile
          </CardTitle>
        </CardHeader>
        <CardContent class="mt-4 flex flex-col sm:flex-row gap-6">
          <div class="sm:w-1/2 flex flex-col relative">
            <div class="flex gap-2">
              <div>Basic Information</div>
              <div>
                <Dialog v-model:open="isOpen">
                  <DialogTrigger as-child>
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
                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                      />
                    </svg>
                  </DialogTrigger>

                  <DialogContent class="sm:max-w-[625px]">
                    <form
                      @submit.prevent="completeOnboarding"
                      class="space-y-4"
                    >
                      <div>
                        <Label for="official_name">Business Name</Label>
                        <Input
                          id="official_name"
                          v-model="business.official_name"
                          @blur="markTouched('official_name')"
                        />
                        <p class="text-sm text-red-500">
                          {{
                            touched.official_name && errorMessages.official_name
                          }}
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
                          {{
                            touched.street_address &&
                            errorMessages.street_address
                          }}
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

                      <Button
                        type="submit"
                        class="w-full"
                        :disabled="!isFormValid"
                      >
                        Save
                      </Button>
                    </form>
                  </DialogContent>
                </Dialog>
              </div>
            </div>
            <hr class="my-2" />
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
            <div>
              <span class="text-sm text-gray-500">Website</span>
              <p class="text-lg text-blue-600 hover:underline">
                <a :href="business.website" target="_blank">
                  {{ business.website }}
                </a>
              </p>
            </div>
            <div>
              <span class="text-sm text-gray-500">Phone</span>
              <p class="text-lg">
                {{ business.phone.length > 1 ? business.phone : "Nil" }}
              </p>
            </div>
            <div>
              <span class="text-sm text-gray-500">Category</span>
              <p class="text-lg">
                {{ business.category }}
              </p>
            </div>
            <div>
              <span class="text-sm text-gray-500">Identifiers</span>
              <p class="text-lg mt-1">
                <span v-if="business.identifiers.length">
                  {{ business.identifiers.join(", ") }}
                </span>
                <span v-else class="italic text-gray-400">None selected</span>
              </p>
            </div>
            <hr class="my-2" />

            <div>
              <p v-if="business.is_claimed" class="text-green-500">
                Verified ✔️
              </p>
              <p v-else class="h-5 bg-slate-300"></p>
              <p>Joined on {{ formattedDate }}</p>
            </div>
          </div>

          <div class="sm:w-1/2">
            <div>Flyer</div>
            <hr class="my-2" />
            <Flyer_ />
          </div>
        </CardContent>
      </Card>
      <div class="only-print"><Flyer /></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { z } from "zod";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
const allIdentifiers = ref<any>([]);
const isOpen = ref(false);
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
const markTouched = (field: string) => {
  touched.value[field] = true;
};
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

    navigateTo("/business/dashboard");
  } catch (error) {
    console.error("Onboarding failed:", error);
    alert("Onboarding failed. Please try again.");
  }
};

const BusinessProfileSchema = z.object({
  official_name: z.string(),
  street_address: z.string(),
  city: z.string(),
  state: z.string(),
  zip_code: z.string(),
  is_claimed: z.boolean(),
  created_at: z.string().datetime(),
  qr_code: z.string(),
  website: z.string(),
  identifiers: z.array(z.string()),
  phone: z.string(),
  category: z.string(),
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
  website: "",
  identifiers: [],
  phone: "",
  category: "",
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

  console.log("res data", business_user);
  if (parsed.success) {
    business.value = parsed.data;
    const response: any = await $fetch(
      "http://localhost:8000/account/identifiers/"
    );
    allIdentifiers.value = response;
  } else {
    console.error("Business profile data is invalid:", parsed.error);
  }
});
</script>

<style scoped>
.no-print {
  display: block;
}

.only-print {
  display: none;
}

@media print {
  @page {
    size: auto;
    margin: 0;
  }

  html,
  body {
    background: white;
    margin: 0;
    padding: 0;
  }

  .print-area {
    width: 6.5in;
    margin: 1in auto;
    border: 2px dashed #9ca3af;
    padding: 1in;
    background-color: white !important;
    box-shadow: none;
    page-break-inside: avoid;
  }

  .no-print {
    display: none !important;
  }

  .only-print {
    display: block;
  }

  .print\:hidden,
  .editable {
    outline: none !important;
    background: none !important;
  }
}
</style>
