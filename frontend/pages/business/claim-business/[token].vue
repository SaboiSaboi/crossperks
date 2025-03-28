<script setup lang="ts">
import { ref, computed } from "vue";
import { z } from "zod";
import { toast } from "@/components/ui/toast";
import { useRoute } from "vue-router";

// Fields
const email = ref("");
const verificationCode = ref("");
const officialName = ref("");
const userPassword = ref("");
const confirmPassword = ref("");
const errorMessage = ref<string | null>(null);
const claimed = ref(false);

const route = useRoute();
const claimToken = route.params.token as string;

// States
const emailSent = ref(false);
const isVerified = ref(false);
const touched = ref({
  email: false,
  verificationCode: false,
  officialName: false,
  userPassword: false,
  confirmPassword: false,
});

// Mark field as touched
const markTouched = (field: string) => {
  touched.value[field] = true;
};

const { data: business, error } = await useAsyncData("business", async () => {
  try {
    const businessData: any = await $fetch(
      `http://localhost:8000/account/business/${claimToken}/`
    );
    if (businessData.is_claimed) {
      claimed.value = true;
      return null;
    }
    return businessData;
  } catch (err) {
    console.error("Error fetching business data:", err);
    errorMessage.value = "Failed to load business details.";
    return null;
  }
});
watchEffect(() => {
  if (business.value && !claimed.value) {
    officialName.value = business.value.official_name || "";
  }
});

// Email Validation schema
const emailSchema = z.string().email("Please enter a valid email address");

// Registration schema (after verification)
const registrationSchema = z
  .object({
    officialName: z
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

// Computed Validations
const emailError = computed(() => {
  const result = emailSchema.safeParse(email.value);
  return result.success ? "" : result.error.issues[0].message;
});

const registrationErrors = computed(() => {
  const result = registrationSchema.safeParse({
    officialName: officialName.value,
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

// API Calls
const sendVerificationCode = async () => {
  markTouched("email");
  if (emailError.value) {
    toast({ title: "Invalid Email", description: emailError.value });
    return;
  }
  try {
    await $fetch("http://localhost:8000/account/send-code/", {
      method: "POST",
      body: { email: email.value, user_type: "business" },
    });
    emailSent.value = true;
    toast({ title: "Code Sent", description: "Please check your email." });
  } catch {
    toast({ title: "Error", description: "Failed to send code." });
  }
};

const verifyCode = async () => {
  markTouched("verificationCode");
  if (!verificationCode.value) return;
  try {
    await $fetch("http://localhost:8000/account/verify-code/", {
      method: "POST",
      body: { email: email.value, code: verificationCode.value },
    });
    isVerified.value = true;
    toast({ title: "Verified", description: "Email verified successfully." });
  } catch {
    toast({ title: "Error", description: "Invalid verification code." });
  }
};

const completeRegistration = async () => {
  markTouched("officialName");
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
    await $fetch("http://localhost:8000/account/complete-registration/", {
      method: "POST",
      body: {
        claim_token: claimToken,
        officialName: officialName.value,
        email: email.value,
        password: userPassword.value,
      },
    });
    toast({ title: "Success", description: "Registration completed." });
    navigateTo("/business");
  } catch {
    toast({ title: "Error", description: "Registration failed." });
  }
};
</script>

<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>

    <h2 class="text-4xl mb-10" v-if="business">Hello {{ officialName }} 🎉</h2>
    <h4 class="text-3xl mb-10" v-if="business">Create Your Business Account</h4>
    <div
      v-if="business"
      class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg"
    >
      <form @submit.prevent="completeRegistration" class="flex flex-col">
        <!-- Email -->
        <div>
          <Label class="block mb-2 font-medium" for="email"
            >Business Email</Label
          >

          <Input
            id="email"
            v-model="email"
            type="email"
            placeholder="name@business.com"
            class="w-full p-3 mb-1 border rounded-lg"
            @blur="markTouched('email')"
            :disabled="emailSent || isVerified"
          />
          <p
            v-if="touched.email && emailError"
            class="text-red-500 text-sm mb-2"
          >
            {{ emailError }}
          </p>
          <p v-else class="text-red-500 text-sm mb-2 h-[1.23rem]"></p>
        </div>

        <!-- Send Code Button -->
        <button
          v-if="!emailSent"
          type="button"
          @click="sendVerificationCode"
          :disabled="!!emailError"
          :class="
            !emailError ? 'bg-blue-600' : 'bg-gray-400 cursor-not-allowed'
          "
          class="w-full text-white py-2 rounded-lg"
        >
          Send Verification Code
        </button>

        <!-- Verification Code -->
        <div v-if="emailSent && !isVerified">
          <Label for="verificationCode" class="block mb-2 font-medium">
            Enter Verification Code
          </Label>
          <Input
            v-model="verificationCode"
            type="text"
            placeholder="Code from email"
            class="w-full p-3 mb-1 border rounded-lg"
            @blur="markTouched('verificationCode')"
          />
          <button
            type="button"
            @click="verifyCode"
            :disabled="!verificationCode"
            :class="
              verificationCode
                ? 'bg-green-600'
                : 'bg-gray-400 cursor-not-allowed'
            "
            class="w-full text-white py-2 rounded-lg mt-2"
          >
            Verify Code
          </button>
        </div>

        <!-- Final Registration -->
        <div v-if="isVerified">
          <div>
            <Label for="officialName" class="block mb-2 font-medium">
              Official Name
            </Label>
            <Input
              class="w-full p-3 mb-1 border rounded-lg"
              id="officialName"
              v-model="officialName"
              type="text"
              placeholder="Business name"
              @blur="markTouched('officialName')"
            />
            <p
              v-if="touched.officialName && registrationErrors.officialName"
              class="text-red-500 text-sm mb-2"
            >
              {{ registrationErrors.officialName }}
            </p>
            <p v-else class="text-red-500 text-sm mb-2 h-[1.23rem]"></p>
          </div>

          <div class="mb-3">
            <Label for="userPassword" class="block mb-2 font-medium">
              Password
            </Label>
            <Input
              class="w-full p-3 mb-1 border rounded-lg"
              id="userPassword"
              v-model="userPassword"
              type="password"
              placeholder="Password"
              @blur="markTouched('userPassword')"
            />
            <p
              v-if="touched.userPassword && registrationErrors.userPassword"
              class="text-red-500 text-sm mb-2"
            >
              {{ registrationErrors.userPassword }}
            </p>
            <p v-else class="text-red-500 text-sm mb-2 h-[1.23rem]"></p>
          </div>

          <div>
            <Label for="confirmPassword" class="block mb-2 font-medium"
              >Confirm Password</Label
            >
            <Input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              placeholder="Confirm Password"
              @blur="markTouched('confirmPassword')"
              class="w-full p-3 mb-1 border rounded-lg"
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
          </div>

          <!-- Complete Registration Button -->
          <button
            type="submit"
            :disabled="!isRegistrationValid"
            :class="
              isRegistrationValid
                ? 'bg-blue-600'
                : 'bg-gray-400 cursor-not-allowed'
            "
            class="w-full text-white py-2 rounded-lg mt-4"
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
      </form>
      <div class="text-center mt-4">
        <p class="text-sm">
          Already have an account?
          <NuxtLink class="font-medium text-slate-900 underline" to="/signin">
            Sign in
          </NuxtLink>
        </p>
      </div>
    </div>
    <div
      v-if="claimed || errorMessage"
      class="flex justify-center items-center max-w-md w-full h-[19.8rem] text-xl text-center"
    >
      No businesses found. Need help? Contact us at support@crossperks.com.
    </div>

    <div
      v-else-if="!business"
      class="flex justify-center items-center max-w-md w-full h-[19.8rem]"
    ></div>
  </div>
</template>
