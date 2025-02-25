<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-10"
  >
    <!-- Header -->
    <NuxtLink to="/" class="text-3xl font-bold mb-6">CrossPerks</NuxtLink>
    <h2 class="text-4xl mb-10">Create an Account</h2>

    <!-- Selection Toggle -->
    <div class="flex gap-6 mb-8">
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
    </div>

    <!-- Form Section -->
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
      <form @submit.prevent="handleSubmit">
        <div v-if="selected === 'customer' || selected === 'business'">
          <label class="block mb-2 font-medium">{{
            selected === "customer" ? "Name" : "Business Name"
          }}</label>
          <input
            type="text"
            :placeholder="
              selected === 'customer' ? 'Your Name' : 'Your Business Name'
            "
            class="w-full p-3 mb-4 border rounded-lg"
            v-model="userName"
            :disabled="emailSent"
          />

          <label class="block mb-2 font-medium">Email</label>
          <input
            type="email"
            placeholder="Your Email"
            class="w-full p-3 mb-4 border rounded-lg"
            v-model="userEmail"
            :disabled="emailSent"
          />

          <button
            v-if="!emailSent"
            type="button"
            :disabled="!userName || !userEmail"
            :class="[
              !userName || !userEmail
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-500',
              'w-full py-2 text-white rounded-lg transition mb-4',
            ]"
            @click="sendVerificationCode"
          >
            Send Verification Code
          </button>

          <div v-if="emailSent && !isVerified">
            <label class="block mb-2 font-medium"
              >Enter Verification Code</label
            >
            <input
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
            <label class="block mb-2 font-medium">Password</label>
            <input
              type="password"
              placeholder="Password"
              class="w-full p-3 mb-4 border rounded-lg"
              v-model="userPassword"
            />

            <label class="block mb-2 font-medium">Confirm Password</label>
            <input
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
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

const selected = ref("customer");
const userName = ref("");
const userEmail = ref("");
const verificationCode = ref("");
const userPassword = ref("");
const confirmPassword = ref("");
const emailSent = ref(false);
const isVerified = ref(false);

const canSendVerification = computed(() => userName.value && userEmail.value);

const handleSubmit = async () => {
  if (isVerified.value) {
    await completeRegistration();
  }
};

const sendVerificationCode = async () => {
  try {
    const response = await $fetch("http://localhost:8000/account/send-code/", {
      method: "POST",
      body: {
        name: userName.value,
        email: userEmail.value,
        user_type: selected.value,
      },
    });
    console.log(response);
    emailSent.value = true;
    isVerified.value = false; // Trigger showing the code input field immediately
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
          email: userEmail.value,
          password: userPassword.value,
        },
      }
    );
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
