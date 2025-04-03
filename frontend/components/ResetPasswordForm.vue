<script setup lang="ts">
import { ref, computed } from "vue";
import { z } from "zod";
import { useRouter } from "vue-router";
import { toast } from "@/components/ui/toast";

const props = defineProps<{
  email: string;
  code: string;
}>();

const router = useRouter();
const codeExpired = ref(false);
const newPassword = ref("");
const confirmPassword = ref("");
const error = ref("");

const passwordSchema = z
  .string()
  .min(8, "Must be at least 8 characters")
  .regex(/[A-Z]/, "One uppercase letter required")
  .regex(/\d/, "At least one number required")
  .regex(/[^a-zA-Z0-9]/, "At least one special character required");

const isFormValid = computed(() => {
  if (newPassword.value !== confirmPassword.value) {
    error.value = "Passwords do not match";
    return false;
  }
  const result = passwordSchema.safeParse(newPassword.value);
  if (!result.success) {
    error.value = result.error.issues[0].message;
    return false;
  }
  error.value = "";
  return true;
});

const submit = async () => {
  if (!isFormValid.value) return;

  try {
    await $fetch("http://localhost:8000/account/reset-password/", {
      method: "POST",
      body: {
        email: props.email,
        code: props.code,
        new_password: newPassword.value,
      },
    });

    toast({
      title: "Password Reset",
      description: "Your password has been updated. You can now sign in.",
    });

    router.push("/signin");
  } catch (err) {
    let message = "Something went wrong. Please try again.";

    if (
      typeof err === "object" &&
      err !== null &&
      "response" in err &&
      typeof err.response === "object" &&
      err.response !== null &&
      "_data" in err.response &&
      typeof err.response._data === "object" &&
      err.response._data !== null &&
      "detail" in err.response._data
    ) {
      message = (err.response as any)._data.detail;
      if (message.includes("expired")) {
        codeExpired.value = true;
      }
      toast({
        title: "Password Reset",
        description: message,
      });
      error.value = message;
    }
  }
};
</script>

<template>
  <form @submit.prevent="submit" class="space-y-4">
    <p class="text-sm text-gray-600 mb-2">Resetting password for {{ email }}</p>

    <div>
      <label for="newPassword" class="block text-sm font-medium text-gray-700">
        New Password
      </label>
      <input
        id="newPassword"
        v-model="newPassword"
        type="password"
        class="w-full p-3 border rounded-lg mt-1"
      />
    </div>

    <div>
      <label
        for="confirmPassword"
        class="block text-sm font-medium text-gray-700"
      >
        Confirm Password
      </label>
      <input
        id="confirmPassword"
        v-model="confirmPassword"
        type="password"
        class="w-full p-3 border rounded-lg mt-1"
      />
    </div>

    <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>

    <Button
      type="submit"
      :disabled="!isFormValid || codeExpired"
      :class="[
        !isFormValid || codeExpired
          ? 'bg-gray-400 cursor-not-allowed'
          : 'bg-blue-600 hover:bg-blue-500',
        'w-full py-2 text-white rounded-lg transition-all',
      ]"
    >
      Update Password
    </Button>
  </form>
</template>
