<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>
    <h2 class="text-4xl mb-10">Create an Account</h2>

    <!-- <div class="flex gap-6 mb-8">
      <button
        :class="{
          'bg-slate-900 text-white': selected === 'customer',
          'bg-white text-slate-900': selected !== 'customer',
        }"
        class="px-6 py-3 rounded-full shadow hover:shadow-lg transition"
        @click="selected = 'customer'"
      >
        Customer
      </button>
      <button
        :class="{
          'bg-slate-900 text-white': selected === 'business',
          'bg-white text-slate-900': selected !== 'business',
        }"
        class="px-6 py-3 rounded-full shadow hover:shadow-lg transition"
        @click="selected = 'business'"
      >
        Business
      </button>
    </div> -->

    <!-- Form Section -->
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
      <form @submit.prevent="handleSubmit">
        <div v-if="selected === 'customer' || selected === 'business'">
          <Label class="block mb-2 font-medium" for="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="Your Email"
            class="w-full p-3 mb-4 border rounded-lg"
            v-model="userEmail"
            :disabled="emailSent"
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
            <Label class="block mb-2 font-medium" for="verificationCode"
              >Enter Verification Code</Label
            >
            <Input
              id="verificationCode"
              type="text"
              placeholder="Verification Code"
              class="w-full p-3 mb-4 border rounded-lg"
              v-model="verificationCode"
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
              class="w-full p-3 mb-4 border rounded-lg"
            /><Label for="userPassword" class="block mb-2 font-medium"
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
const selected = ref("customer");
const userName = ref("");
const userEmail = ref("");
const isValidEmail = computed(() => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(userEmail.value);
});
const verificationCode = ref("");
const userPassword = ref("");
const confirmPassword = ref("");
const emailSent = ref(false);
const isVerified = ref(false);

const handleSubmit = async () => {
  if (isVerified.value) {
    await completeRegistration();
  }
};

const sendVerificationCode = async () => {
  if (!isValidEmail.value) return;
  try {
    const response = await $fetch("http://localhost:8000/account/send-code/", {
      method: "POST",
      body: {
        name: userName.value,
        email: userEmail.value,
        user_type: "customer",
      },
    });
    console.log(response);
    emailSent.value = true;
    isVerified.value = false;
  } catch (error) {
    console.error("Failed to send verification code:", error);
  }
};

const verifyCode = async () => {
  if (!verificationCode.value) return;
  try {
    const response = await $fetch(
      "http://localhost:8000/account/verify-code/",
      {
        method: "POST",
        body: {
          email: userEmail.value,
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
          name: userName.value,
          email: userEmail.value,
          password: userPassword.value,
        },
      }
    );

    // navigateTo("/")
    console.log("Registration complete:", response);
  } catch (error) {
    console.error("Failed to complete registration:", error);
  }
};
</script>

<style>
html {
  scroll-behavior: smooth;
}
</style>
