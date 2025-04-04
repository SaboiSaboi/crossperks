<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>
    <h2 class="text-4xl mb-10">Sign Into Your Account</h2>

    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
      <form @submit.prevent="handleSignIn">
        <Label class="block mb-2 font-medium" for="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="Your Email"
          class="w-full p-3 border rounded-lg"
          v-model="email"
          @blur="markTouched('email')"
        />
        <p class="text-red-500 text-sm h-5 mb-2">
          {{ touched.email ? formErrors.email : "" }}
        </p>

        <Label class="block mb-2 font-medium" for="password">Password</Label>
        <Input
          id="password"
          type="password"
          placeholder="Your Password"
          class="w-full p-3 border rounded-lg"
          v-model="password"
          @blur="markTouched('password')"
        />
        <p class="text-red-500 text-sm h-5 mb-1">
          {{ touched.password ? formErrors.password : "" }}
        </p>
        <div class="text-black mb-4 underline w-fit text-sm">
          <NuxtLink to="/forgot-password"> Forgot Password </NuxtLink>
        </div>

        <button
          :disabled="!email || !password"
          :class="[
            !email || !password
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-500',
            'w-full py-2 text-white rounded-lg transition mb-2',
          ]"
          type="submit"
        >
          Sign In
        </button>
        <p v-if="loginErrorMessage" class="mb-2 text-sm text-red-600">
          {{ loginErrorMessage }}
        </p>
      </form>

      <!-- Alternative Sign-In Methods -->
      <div class="text-center mt-6">
        <p class="text-slate-500">Or continue with</p>
        <div class="flex justify-center gap-4 mt-4">
          <button class="px-6 py-3 bg-slate-200 rounded-lg hover:bg-slate-300">
            Google
          </button>
          <button class="px-6 py-3 bg-slate-200 rounded-lg hover:bg-slate-300">
            Apple
          </button>
        </div>
      </div>

      <!-- Sign-Up Link -->
      <p class="text-sm text-center mt-4">
        Don't have an account?
        <NuxtLink to="/signup" class="text-slate-900 font-medium underline"
          >Create one</NuxtLink
        >
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { z } from "zod";
import { toast } from "@/components/ui/toast";
import { NuxtLink } from "#components";

const authStore = useAuthS();

const email = ref("");
const loginErrorMessage = ref<string | null>(null);

const password = ref("");

const touched = ref({
  email: false,
  password: false,
});

const markTouched = (field: string) => {
  touched.value[field] = true;
};

const formSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(8, "Please enter your password"),
});

const formErrors = computed(() => {
  const result = formSchema.safeParse({
    email: email.value,
    password: password.value,
  });

  if (result.success) return {};

  return Object.fromEntries(
    result.error.issues.map((issue) => [issue.path[0], issue.message])
  );
});

const isFormValid = computed(() => Object.keys(formErrors.value).length === 0);

const handleSignIn = async () => {
  loginErrorMessage.value = null;

  if (!isFormValid.value) {
    toast({
      title: "Form Error",
      description: "Please correct errors before submitting.",
      variant: "destructive",
    });
    return;
  }

  try {
    await authStore.login({
      email: email.value,
      password: password.value,
    });
  } catch (error: unknown) {
    if (error instanceof Error) {
      loginErrorMessage.value = error.message;
      toast({
        title: "Login Failed",
        description: error.message,
        variant: "destructive",
      });
    } else {
      loginErrorMessage.value = "An unexpected error occurred.";
      toast({
        title: "Login Failed",
        description: "An unexpected error occurred.",
        variant: "destructive",
      });
    }
  }
};
</script>

<style>
html {
  scroll-behavior: smooth;
}
</style>
