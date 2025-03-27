<script setup>
import { useRoute } from "vue-router";
import { ref, computed, watchEffect } from "vue";

const route = useRoute();
const claimToken = route.params.token;

const errorMessage = ref(null);
const claimed = ref(false);

const email = ref("");
const isValidEmail = computed(() => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value);
});
const officialName = ref("");
const verificationCode = ref("");
const userPassword = ref("");
const confirmPassword = ref("");
const emailSent = ref(false);
const isVerified = ref(false);

const verifyCode = async () => {
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
const sendVerificationCode = async () => {
  if (!isValidEmail.value) return;

  try {
    const response = await $fetch("http://localhost:8000/account/send-code/", {
      method: "POST",
      body: {
        email: email.value,
        user_type: "business",
      },
    });
    console.log(response);
    emailSent.value = true;
    isVerified.value = false;
  } catch (error) {
    console.error("Failed to send verification code:", error);
  }
};

const { data: business, error } = await useAsyncData("business", async () => {
  try {
    const businessData = await $fetch(
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

const completeRegistration = async () => {
  if (userPassword.value !== confirmPassword.value) {
    alert("Passwords do not match.");
    return;
  }

  try {
    const response = await $fetch(
      "http://localhost:8000/account/complete-registration/",
      {
        method: "POST",
        body: {
          claim_token: claimToken,
          officialName: officialName.value,
          email: email.value,
          password: userPassword.value,
        },
      }
    );

    console.log("Registration complete:", response);

    const userType = response.user.user_type;

    const token = useCookie("auth_token");
    token.value = response.auth_token;

    navigateTo(`/${userType}`, { replace: true });
  } catch (error) {
    console.error("Failed to complete registration:", error);
  }
};

const handleSubmit = async () => {
  console.log("user verfified ", isVerified.value);
  if (isVerified.value) {
    await completeRegistration();
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
      <form @submit.prevent="handleSubmit" class="flex flex-col">
        <Label class="block mb-2 font-medium" for="email">Business Email</Label>
        <Input
          id="email"
          v-model="email"
          type="text"
          placeholder="Business Email"
          required
          class="w-full p-3 mb-4 border rounded-lg"
          :disabled="emailSent || isVerified"
        />

        <button
          v-if="!emailSent"
          type="button"
          :disabled="!isValidEmail"
          :class="[
            !isValidEmail
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-500',
            'w-full py-2 text-white rounded-lg transition mb-4',
          ]"
          @click="sendVerificationCode"
        >
          Send Verification Code
        </button>
        <div v-if="emailSent && !isVerified">
          <Label for="verificationCode" class="block mb-2 font-medium"
            >Enter Verification Code</Label
          >
          <Input
            type="text"
            placeholder="Verification Code"
            class="w-full p-3 mb-4 border rounded-lg"
            v-model="verificationCode"
            id="verificationCode"
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
          <Label for="officialName" class="block mb-2 font-medium"
            >Business Name</Label
          >
          <Input
            id="officialName"
            v-model="officialName"
            type="text"
            placeholder="Business Name"
            required
            class="w-full p-3 mb-4 border rounded-lg"
          />
          <Label for="userPassword" class="block mb-2 font-medium"
            >Password</Label
          >
          <Input
            id="userPassword"
            type="password"
            placeholder="Password"
            class="w-full p-3 mb-4 border rounded-lg"
            v-model="userPassword"
          />

          <Label for="confirmPassword" class="block mb-2 font-medium"
            >Confirm Password</Label
          >
          <Input
            id="confirmPassword"
            type="password"
            placeholder="Confirm Password"
            class="w-full p-3 mb-4 border rounded-lg"
            v-model="confirmPassword"
          />
          <button
            type="submit"
            class="w-full py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-700 transition"
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
