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
const newPasswordError = ref<string | null>(null);

const touched = ref({
  newPassword: false,
  confirmPassword: false,
});

const markTouched = (field: string) => {
  touched.value[field] = true;
};

const passwordRules = computed(() => ({
  length: newPassword.value.length >= 8,
  uppercase: /[A-Z]/.test(newPassword.value),
  digit: /\d/.test(newPassword.value),
  special: /[^a-zA-Z0-9]/.test(newPassword.value),
}));

const registrationSchema = z
  .object({
    newPassword: z
      .string()
      .min(8, "Password must be at least 8 characters")
      .regex(/[A-Z]/, "Include at least one uppercase letter")
      .regex(/\d/, "Include at least one digit")
      .regex(/[^a-zA-Z0-9]/, "Include at least one special character"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.newPassword === data.confirmPassword, {
    message: "Passwords must match",
    path: ["confirmPassword"],
  });

const registrationErrors = computed(() => {
  const result = registrationSchema.safeParse({
    newPassword: newPassword.value,
    confirmPassword: confirmPassword.value,
  });
  if (result.success) return {};
  return Object.fromEntries(
    result.error.issues.map((issue) => [issue.path[0], issue.message])
  );
});

const isRegistrationValid = computed(
  () => Object.keys(registrationErrors.value).length === 0
);

watch(newPassword, () => {
  const result = registrationSchema.safeParse({
    newPassword: newPassword.value,
    confirmPassword: confirmPassword.value || "placeholder",
  });

  const pwdIssue = result.success
    ? null
    : result.error.issues.find((i) => i.path[0] === "newPassword");

  newPasswordError.value = pwdIssue?.message ?? null;
});

type CompleteRegistrationResponse = {
  message: string;
  auth_token: string;
};

const authStore = useAuthS();

const submit = async () => {
  markTouched("newPassword");
  markTouched("confirmPassword");

  if (!isRegistrationValid.value) {
    toast({
      title: "Form Error",
      description: "Please correct errors before submitting.",
    });
    return;
  }

  try {
    const response = await $fetch<CompleteRegistrationResponse>(
      "http://localhost:8000/account/reset-password/",
      {
        method: "POST",
        body: {
          email: props.email,
          code: props.code,
          new_password: newPassword.value,
        },
      }
    );

    console.log(response.auth_token);

    authStore.setToken(response.auth_token);

    toast({
      title: "Password Reset",
      description: "Your password has been updated.",
    });

    router.push("/business/dashboard");
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
      <Label for="newPassword" class="block text-sm font-medium text-gray-700">
        New Password
      </Label>
      <Input
        id="newPassword"
        v-model="newPassword"
        type="password"
        class="w-full p-3 border rounded-lg mt-1"
        @blur="markTouched('newPassword')"
      />
      <div v-if="touched.newPassword" class="space-y-1 my-4 text-sm">
        <p
          :class="[
            'flex items-center gap-2',
            passwordRules.length ? 'text-green-600' : 'text-red-600',
          ]"
        >
          <span>{{ passwordRules.length ? "✅" : "❌" }}</span>
          At least 8 characters
        </p>
        <p
          :class="[
            'flex items-center gap-2',
            passwordRules.uppercase ? 'text-green-600' : 'text-red-600',
          ]"
        >
          <span>{{ passwordRules.uppercase ? "✅" : "❌" }}</span>
          At least one uppercase letter
        </p>
        <p
          :class="[
            'flex items-center gap-2',
            passwordRules.digit ? 'text-green-600' : 'text-red-600',
          ]"
        >
          <span>{{ passwordRules.digit ? "✅" : "❌" }}</span>
          At least one number
        </p>
        <p
          :class="[
            'flex items-center gap-2',
            passwordRules.special ? 'text-green-600' : 'text-red-600',
          ]"
        >
          <span>{{ passwordRules.special ? "✅" : "❌" }}</span>
          At least one special character
        </p>
      </div>
    </div>

    <div>
      <Label
        for="confirmPassword"
        class="block text-sm font-medium text-gray-700"
      >
        Confirm Password
      </Label>
      <Input
        id="confirmPassword"
        v-model="confirmPassword"
        type="password"
        class="w-full p-3 border rounded-lg mt-1"
      />
    </div>

    <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>

    <Button
      type="submit"
      :disabled="!isRegistrationValid || codeExpired"
      :class="[
        !isRegistrationValid || codeExpired
          ? 'bg-gray-400 cursor-not-allowed'
          : 'bg-blue-600 hover:bg-blue-500',
        'w-full py-2 text-white rounded-lg transition-all',
      ]"
    >
      Update Password
    </Button>
  </form>
</template>
