<template>
  <div class="container flex flex-col items-center mt-8">
    <button
      @click="printCard"
      class="bg-blue-500 text-white px-4 py-2 text-lg font-bold rounded-md hover:bg-blue-600"
    >
      Print Card
    </button>

    <div
      ref="printSection"
      class="cut-card card-wrapper flex flex-col items-center justify-between"
    >
      <div class="banner w-full p-2 text-center">
        <h1
          class="business-name text-black font-roboto font-semibold text-sm uppercase"
        >
          {{ businessName }}
        </h1>
        <p class="text-xs text-roboto mt-2">
          {{ perkMessage }}
        </p>
      </div>

      <p
        class="text-2xl font-roboto font-bold text-gray-900 text-balance px-2 py-1"
      >
        Scan to discover a surprise perk!
      </p>

      <div class="qr-section flex flex-col items-center justify-center my-1">
        <img
          :src="qrCodeUrl"
          alt="QR Code"
          class="qr-code w-[120px] h-[120px] mb-1"
        />
      </div>

      <div class="footer text-xs text-gray-600 mb-1">
        <p>
          Powered by
          <strong class="text-blue-500 bg-lime-500">CrossPerks</strong>.
          www.crossperks.com
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const businessName = ref("Champion Central Spot Barbershop");
const perkMessage = ref("Thanks for shopping. Please call again!");
const qrData = ref("https://crossperks.com/surprise-perk");

const qrCodeUrl = computed(
  () =>
    `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(
      qrData.value
    )}`
);

const printCard = () => {
  const content = document.querySelector(".cut-card")?.innerHTML ?? "";
  const printWindow = window.open("", "", "width=600,height=400");
  if (!printWindow) return;

  printWindow.document.open();
  printWindow.document.close();

  const fullHTML = `
    <!DOCTYPE html>
    <html>
      <head>
        <title>Print Card</title>
        <meta charset="utf-8" />
        <style>
          /* 
            3" x 5" card with 0.25" margins => 2.5" x 4.5" area
            We'll add padding for comfortable spacing inside the dashed border.
          */
          @page {
            size: 3in 5in;
            margin: 0.25in;
          }

          body {
            margin: 0;
            padding: 0;
            font-family: "Arial", sans-serif;
            background-color: #fff;
            text-align: center;
          }

          .card-wrapper {
            width: 2.5in;
            height: 4.5in;
            margin: 0 auto;
            border: 2px dashed #555; /* Dashed border for cutting */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            position: relative;
            padding: 0.2in; /* Some padding inside the dashed area */
          }

          /* Minimal Tailwind-like classes used on screen */
          .bg-blue-500 {
            background-color: #007bff;
          }
          .text-white {
            color: #fff;
          }
          .text-xs {
            font-size: 0.75rem; /* 12px */
          }
          .text-sm {
            font-size: 0.875rem; /* 14px */
          }
          .uppercase {
            text-transform: uppercase;
          }
          .text-gray-900 {
            color: #1a1a1a;
          }
          .text-gray-600 {
            color: #666;
          }
          .font-roboto {
            font-family: Roboto, sans-serif;
          }
          .font-bold {
            font-weight: bold;
          }
          .leading-4 {
            line-height: 1rem;
          }
          .p-1 {
            padding: 0.25rem;
          }
          .mt-2 {
            margin-top: 0.5rem;
          }
          .my-1 {
            margin: 0.25rem 0;
          }
          .mb-1 {
            margin-bottom: 0.25rem;
          }
          .text-2xl {
            font-size: 1.5rem;
          }
          .bg-slate-500 {
            background-color: #64748b;
          }
          .px-2 {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
          }
          .py-1 {
            padding-top: 0.25rem;
            padding-bottom: 0.25rem;
          }
          .w-[120px] {
            width: 120px;
          }
          .h-[120px] {
            height: 120px;
          }
        </style>
      </head>
      <!-- 
        No <script> block here. 
        Instead, we use an onload attribute to auto-print.
      -->
      <body onload="(function(){ window.print(); window.close(); })()">
        <div class="card-wrapper flex flex-col items-center justify-between">
          ${content}
        </div>
      </body>
    </html>
  `;

  printWindow.document.documentElement.innerHTML = fullHTML;
};
</script>

<style scoped>
.cut-card {
  display: none;
}
</style>
