<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center px-4 bg-gray-50"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6 text-blue-600"
      >CrossPerks</NuxtLink
    >

    <div class="w-full max-w-md bg-white shadow-lg rounded-2xl p-6 space-y-6">
      <h2 class="text-2xl font-semibold text-gray-800 text-center">
        Forgot Password
      </h2>

      <form
        v-if="!isEmailSent"
        @submit.prevent="sendResetEmail"
        class="space-y-4"
      >
        <div>
          <Label
            for="email"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Email Address</Label
          >
          <Input
            id="email"
            v-model="email"
            type="email"
            placeholder="you@example.com"
            required
            class="w-full p-3 border rounded-lg"
          />
        </div>
        <Button type="submit" class="w-full">Send Reset Link</Button>
      </form>

      <div v-else class="text-center text-gray-700 space-y-3">
        <p>
          If an account exists for <strong>{{ email }}</strong
          >, we’ve sent a password reset link.
        </p>
        <p class="text-sm text-gray-500">
          Please check your spam or junk folder if you don’t see it within a few
          minutes.
        </p>
        <Button @click="resetFlow" variant="ghost" class="mt-2 text-sm">
          Send to a different email
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { toast } from "@/components/ui/toast";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

const email = ref("");
const isEmailSent = ref(false);

const sendResetEmail = async () => {
  try {
    await $fetch("http://localhost:8000/account/send-reset-code/", {
      method: "POST",
      body: { email: email.value },
    });

    isEmailSent.value = true;

    toast({
      title: "Check Your Email",
      description: `If an account exists for ${email.value}, we’ve sent a password reset link.`,
    });
  } catch (err) {
    isEmailSent.value = true;

    console.error("Error sending reset email:", err);
    toast({
      title: "Something went wrong",
      description: "Please try again in a few minutes.",
    });
  }
};

const resetFlow = () => {
  email.value = "";
  isEmailSent.value = false;
};
</script>

<style scoped></style>
