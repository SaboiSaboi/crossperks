<script setup lang="ts">
import { ref, onMounted } from "vue";
import { z } from "zod";
import { toast } from "@/components/ui/toast";

const hasEdits = ref(false);

const BusinessProfileSchema = z.object({
  official_name: z.string(),
  street_address: z.string(),
  city: z.string(),
  state: z.string(),
  zip_code: z.string(),
  is_claimed: z.boolean(),
  qr_code: z.string(),
  website: z.string(),
  flyerMessage: z.string().nullable(),
  flyerHeadline: z.string().nullable(),
  created_at: z.string(),
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
  qr_code: "",
  website: "",
  flyerHeadline: "",
  flyerMessage: "",
  created_at: "",
  identifiers: [],
  phone: "",
  category: "",
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

const printFlyer = () => {
  window.print();
};

const saveEdits = async () => {
  const token = useCookie("auth_token");

  await $fetch("http://localhost:8000/account/update-flyer/", {
    method: "PUT",
    headers: {
      Authorization: `Token ${token.value}`,
    },
    body: {
      flyerHeadline: business.value.flyerHeadline,
      flyerMessage: business.value.flyerMessage,
      official_name: business.value.official_name,
    },
  });

  hasEdits.value = false;
  toast({ title: "Success", description: "Saved Flyer Details." });
};
</script>

<template>
  <div>
    <div class="no-print mb-4">
      <Label class="text-sm text-gray-500 mt-2">
        Click on the flyer text to edit it directly.
      </Label>
    </div>

    <div
      class="print-area mx-auto bg-white p-8 rounded shadow-lg max-w-md text-center border-2 border-dashed border-gray-400 mb-4"
    >
      <h1
        class="text-xl font-bold text-gray-900 mb-2 editable"
        contenteditable="true"
        @input="
          business.official_name = ($event.target as HTMLElement).innerText;
          hasEdits = true;
        "
      >
        {{ business.official_name }}
      </h1>

      <p
        class="text-sm text-gray-600 mb-4 editable"
        contenteditable="true"
        @input="
          business.flyerMessage = ($event.target as HTMLElement).innerText;
          hasEdits = true;
        "
      >
        {{ business.flyerMessage ?? "E.g Thanks for coming. Call again!" }}
      </p>

      <p
        class="text-lg font-semibold text-gray-800 mb-4 editable"
        contenteditable="true"
        @input="
          business.flyerHeadline = ($event.target as HTMLElement).innerText;
          hasEdits = true;
        "
      >
        {{ business.flyerHeadline ?? "E.g. Buy Item at 20% off discount." }}
      </p>

      <img
        :src="business.qr_code"
        alt="QR Code"
        class="w-40 h-40 mx-auto mb-4"
      />

      <div class="text-xs text-gray-500 mt-4">
        Powered by <strong class="text-blue-600">CrossPerks</strong><br />
        www.crossperks.com
      </div>
    </div>

    <p class="text-[10px] text-gray-400 mt-6 hidden print:block">
      ✂️ Cut along the dashed border and display this flyer at your business.
    </p>

    <div class="no-print flex justify-center gap-4">
      <button
        @click="printFlyer"
        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded"
      >
        Print Flyer
      </button>

      <button
        @click="saveEdits"
        :disabled="!hasEdits"
        :class="[
          'font-semibold px-6 py-2 rounded',
          hasEdits
            ? 'bg-green-600 hover:bg-green-700 text-white cursor-pointer'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed',
        ]"
      >
        Save Changes
      </button>
    </div>
  </div>
</template>

<style scoped>
.editable:focus {
  outline: 2px dashed #3b82f6;
  outline-offset: 2px;
  background-color: #eef6ff;
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
    width: 5in;
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

  .print\:hidden,
  .editable {
    outline: none !important;
    background: none !important;
  }
}
</style>
