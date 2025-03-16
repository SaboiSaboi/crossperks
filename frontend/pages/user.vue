<template>
  <div class="h-dvh flex justify-center items-center">
    <input v-model="text" type="text" />
    <img :src="qrcode" alt="QR Code" />
  </div>
</template>

<script setup lang="ts">
import { useQRCode } from "@vueuse/integrations/useQRCode";
import { shallowRef } from "vue";

const text = shallowRef("text-to-encode");
const qrcode = useQRCode(text);
</script>
