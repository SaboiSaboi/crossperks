<script setup lang="ts">
import { computed, ref } from "vue";

const businessName = ref("Champion Central Spot Barbershop");
const perkMessage = ref("Thanks for shopping. Please call again!");
const headline = ref("Scan to discover a surprise perk!");
const qrData = ref("https://crossperks.com/surprise-perk");

const qrCodeUrl = computed(
  () =>
    `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(
      qrData.value
    )}`
);

const printFlyer = () => {
  window.print();
};
</script>

<template>
  <div class="container mx-auto px-4 py-8 min-h-screen bg-slate-100">
    <!-- Print Button -->
    <div class="print:hidden text-center mb-6">
      <button
        @click="printFlyer"
        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded"
      >
        Print Flyer
      </button>
      <p class="text-sm text-gray-500 mt-2">
        Click on the flyer text to edit it directly.
      </p>
    </div>

    <!-- Editable Printable Flyer -->
    <div
      class="print-area mx-auto bg-white p-8 rounded shadow-lg max-w-md text-center border-2 border-dashed border-gray-400"
    >
      <h1
        class="text-xl font-bold text-gray-900 mb-2 editable"
        contenteditable="true"
        @input="businessName = ($event.target as HTMLElement).innerText"
      >
        {{ businessName }}
      </h1>

      <p
        class="text-sm text-gray-600 mb-4 editable"
        contenteditable="true"
        @input="perkMessage = ($event.target as HTMLElement).innerText"
      >
        {{ perkMessage }}
      </p>

      <p
        class="text-lg font-semibold text-gray-800 mb-4 editable"
        contenteditable="true"
        @input="headline = ($event.target as HTMLElement).innerText"
      >
        {{ headline }}
      </p>

      <img :src="qrCodeUrl" alt="QR Code" class="w-40 h-40 mx-auto mb-4" />

      <div class="text-xs text-gray-500 mt-4">
        Powered by <strong class="text-blue-600">CrossPerks</strong><br />
        www.crossperks.com
      </div>

      <p class="text-[10px] text-gray-400 mt-6 hidden print:block">
        ✂️ Cut along the dashed border and display this flyer at your business.
      </p>
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

  .print\:hidden,
  .editable {
    outline: none !important;
    background: none !important;
  }
}
</style>
