<script setup lang="ts">
import { useRoute } from "vue-router";
import ResetPasswordForm from "@/components/ResetPasswordForm.vue";

const route = useRoute();
const email = (route.query.email as string) || "";
const code = (route.query.code as string) || "";
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 p-4">
    <div class="max-w-md w-full bg-white shadow-md rounded-xl p-6">
      <h2 class="text-2xl font-bold mb-4 text-center">Reset Password</h2>
      <ResetPasswordForm :email="email" :code="code" />
    </div>
  </div>
</template>
