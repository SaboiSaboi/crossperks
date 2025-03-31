<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>
    <h2 class="text-4xl mb-10">Create an Account</h2>

    <!-- Form Section -->
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
      <form @submit.prevent="handleSubmit">
        <div v-if="selected === 'customer' || selected === 'business'">
          <Label class="block mb-2 font-medium" for="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="Your Email"
            class="w-full p-3 mb-1 border rounded-lg"
            v-model="email"
            :disabled="emailSent || isVerified"
            @blur="markTouched('email')"
          />
          <p
            v-if="touched.email && emailError"
            class="text-red-500 text-sm mb-2"
          >
            {{ emailError }}
          </p>
          <p v-else class="text-red-500 text-sm mb-2 h-[1.23rem]"></p>

          <button
            v-if="!emailSent"
            type="button"
            :disabled="!!emailError"
            :class="[
              !emailError ? 'bg-blue-600' : 'bg-gray-400 cursor-not-allowed',
              'w-full py-2 text-white rounded-lg transition',
            ]"
            @click="sendVerificationCode"
          >
            Send Verification Code
          </button>

          <div v-if="emailSent && !isVerified">
            <Label class="block mb-2 font-medium" for="verificationCode"
              >Enter Verification Code sent to your email</Label
            >
            <Input
              id="verificationCode"
              type="text"
              placeholder="Code from email"
              class="w-full p-3 mb-4 border rounded-lg"
              v-model="verificationCode"
              @blur="markTouched('verificationCode')"
            />
            <button
              type="button"
              :disabled="!verificationCode"
              :class="[
                !verificationCode
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-green-600 hover:bg-green-500',
                'w-full py-2 text-white rounded-lg transition mb-4',
              ]"
              @click="verifyCode"
            >
              Verify Code
            </button>
          </div>

          <div v-if="isVerified">
            <Label class="block mb-2 font-medium" for="userName">Name</Label>
            <Input
              id="userName"
              v-model="userName"
              type="text"
              placeholder="Your Name"
              required
              class="w-full p-3 mb-1 border rounded-lg"
              @blur="markTouched('userName')"
            />
            <p
              v-if="touched.userName && registrationErrors.userName"
              class="text-red-500 text-sm mb-2"
            >
              {{ registrationErrors.userName }}
            </p>
            <p v-else class="text-red-500 text-sm mb-2 h-[1.23rem]"></p>
            <!-- Password Field -->
            <Label for="userPassword" class="block mb-2 font-medium"
              >Password</Label
            >
            <Input
              id="userPassword"
              type="password"
              placeholder="Password"
              class="w-full p-3 mb-2 border rounded-lg"
              v-model="userPassword"
              @blur="markTouched('userPassword')"
            />

            <div v-if="touched.userPassword" class="space-y-1 my-4 text-sm">
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
            <p v-else class="text-red-500 text-sm mb-2 h-[1.23rem]"></p>
            <Label for="confirmPassword" class="block mb-2 font-medium"
              >Confirm Password</Label
            >
            <Input
              id="confirmPassword"
              type="password"
              placeholder="Confirm Password"
              class="w-full p-3 mb-1 border rounded-lg"
              @blur="markTouched('confirmPassword')"
              v-model="confirmPassword"
            />
            <p
              v-if="
                touched.confirmPassword && registrationErrors.confirmPassword
              "
              class="text-red-500 text-sm mb-2"
            >
              {{ registrationErrors.confirmPassword }}
            </p>
            <p v-else class="text-red-500 text-sm mb-2 h-[1.23rem]"></p>

            <button
              :disabled="!isRegistrationValid"
              :class="
                isRegistrationValid
                  ? 'bg-blue-600'
                  : 'bg-gray-400 cursor-not-allowed'
              "
              type="submit"
              class="w-full py-3 text-white rounded-lg transition"
            >
              Complete Registration
            </button>
            <p class="text-sm text-gray-500 mt-4 text-center">
              By signing up, you agree to our
              <NuxtLink
                class="text-gray-600 underline hover:text-gray-500"
                to="/terms-of-service"
              >
                Terms of Service
              </NuxtLink>
              and
              <NuxtLink
                class="text-gray-600 underline hover:text-gray-500"
                to="/privacypolicy"
              >
                Privacy Policy.
              </NuxtLink>
            </p>
          </div>
        </div>
      </form>
      <section
        class="flex flex-col justify-center items-center text-center text-gray-700 pt-5 text-sm"
      >
        <p>Are you a business? Request account creation at</p>
        <p class="font-semibold">support@crossperks.com</p>
      </section>
      <div class="text-center mt-4">
        <p class="text-sm">
          Already have an account?
          <NuxtLink class="font-medium text-slate-900 underline" to="/signin">
            Sign in
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { z } from "zod";
import { toast } from "@/components/ui/toast";

const authStore = useAuthS();
const selected = ref("customer");
const userName = ref("");
const email = ref("");
const verificationCode = ref("");
const userPassword = ref("");
const confirmPassword = ref("");
const emailSent = ref(false);
const isVerified = ref(false);
const userPasswordError = ref<string | null>(null);

const touched = ref({
  email: false,
  verificationCode: false,
  userName: false,
  userPassword: false,
  confirmPassword: false,
});

const markTouched = (field: string) => {
  touched.value[field] = true;
};

// Email validation
const emailSchema = z.string().email("Please enter a valid email address");
const emailError = computed(() => {
  const result = emailSchema.safeParse(email.value);
  return result.success ? "" : result.error.issues[0].message;
});

// Password rules (live)
const passwordRules = computed(() => ({
  length: userPassword.value.length >= 8,
  uppercase: /[A-Z]/.test(userPassword.value),
  digit: /\d/.test(userPassword.value),
  special: /[^a-zA-Z0-9]/.test(userPassword.value),
}));

// Registration schema (Zod)
const registrationSchema = z
  .object({
    userName: z
      .string()
      .min(2, "Official name must have at least 2 characters"),
    userPassword: z
      .string()
      .min(8, "Password must be at least 8 characters")
      .regex(/[A-Z]/, "Include at least one uppercase letter")
      .regex(/\d/, "Include at least one digit")
      .regex(/[^a-zA-Z0-9]/, "Include at least one special character"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.userPassword === data.confirmPassword, {
    message: "Passwords must match",
    path: ["confirmPassword"],
  });

// Computed errors for full form submission
const registrationErrors = computed(() => {
  const result = registrationSchema.safeParse({
    userName: userName.value,
    userPassword: userPassword.value,
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

// Live update password error message as user types
watch(userPassword, () => {
  const result = registrationSchema.safeParse({
    userName: userName.value || "placeholder",
    userPassword: userPassword.value,
    confirmPassword: confirmPassword.value || "placeholder",
  });

  const pwdIssue = result.success
    ? null
    : result.error.issues.find((i) => i.path[0] === "userPassword");

  userPasswordError.value = pwdIssue?.message ?? null;
});

// Send verification code
const sendVerificationCode = async () => {
  markTouched("email");
  if (emailError.value) {
    toast({ title: "Invalid Email", description: emailError.value });
    return;
  }

  try {
    await $fetch("http://localhost:8000/account/send-code/", {
      method: "POST",
      body: {
        name: userName.value,
        email: email.value,
        user_type: "customer",
      },
    });
    emailSent.value = true;
    isVerified.value = false;
    toast({ title: "Code Sent", description: "Please check your email." });
  } catch (error) {
    console.error("Failed to send verification code:", error);
    toast({ title: "Error", description: "Failed to send code." });
  }
};

// Verify code
const verifyCode = async () => {
  markTouched("verificationCode");
  if (!verificationCode.value) return;
  try {
    const response = await $fetch(
      "http://localhost:8000/account/verify-code/",
      {
        method: "POST",
        body: {
          email: email.value,
          code: verificationCode.value,
        },
      }
    );
    console.log(response);
    isVerified.value = true;
  } catch (error) {
    alert("Invalid verification code.");
  }
};

// Final registration submit
const handleSubmit = async () => {
  if (isVerified.value) {
    await completeRegistration();
  }
};

type CompleteRegistrationResponse = {
  message: string;
  user: {
    email: string;
    name: string;
    user_type: "customer" | "business";
  };
  auth_token: string;
};

const completeRegistration = async () => {
  markTouched("userName");
  markTouched("userPassword");
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
      "http://localhost:8000/account/complete-registration/",
      {
        method: "POST",
        body: {
          name: userName.value,
          email: email.value,
          password: userPassword.value,
        },
      }
    );

    authStore.setToken(response.auth_token);

    toast({ title: "Success", description: "Registration completed." });
    navigateTo("/customer/dashboard");
  } catch (error) {
    toast({ title: "Error", description: "Registration failed." });
    console.error("Failed to complete registration:", error);
  }
};
</script>

<style>
html {
  scroll-behavior: smooth;
}
</style>
