<template>
  <main class="grow">
    <Header />
    <section class="relative">
      <div class="relative max-w-6xl mx-auto px-4 sm:px-6">
        <div class="pt-32 pb-12 md:pt-40 md:pb-20">
          <div class="max-w-3xl mx-auto text-center pb-12">
            <h1
              class="bg-clip-text text-4xl text-gray-600 font-semibold bg-gray-600"
            >
              Sign into CrossPerks
            </h1>
          </div>
          <div class="max-w-sm mx-auto bg-white p-8 rounded-lg shadow-lg">
            <form @submit.prevent="signin">
              <div class="space-y-4">
                <div>
                  <Label
                    class="block text-sm text-slate-500 font-medium mb-1"
                    for="email"
                    >Email</Label
                  >
                  <Input
                    id="email"
                    v-model="email"
                    class="w-full px-4 py-2 mt-2 border border-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="Enter your email"
                    type="email"
                    required
                    aria-label="Email address"
                    autocomplete="email"
                  />
                </div>
                <div>
                  <div class="flex justify-between">
                    <Label
                      class="block text-sm text-slate-500 font-medium mb-1"
                      for="password"
                      >Password</Label
                    >
                  </div>
                  <Input
                    id="password"
                    v-model="password"
                    placeholder="Enter your password"
                    class="w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                    type="password"
                    required
                  />
                </div>
              </div>
              <div class="mt-6">
                <Button
                  type="submit"
                  class="w-full py-2 mt-4 font-semibold text-white bg-gray-500 rounded-lg hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                  Sign In
                </Button>
              </div>
            </form>

            <div class="text-center mt-4">
              <div class="text-sm text-slate-400">
                Don't have an account?
                <NuxtLink
                  class="font-medium text-gray-600 hover:text-gray-500 transition duration-150 ease-in-out underline"
                  to="/signup"
                  >Sign up</NuxtLink
                >
              </div>
              <p class="mt-2 text-center text-xs">
                Forgot your password?
                <NuxtLink to="/resetpassword" class="text-gray-600 underline"
                  >Reset Password</NuxtLink
                >
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useAuthS } from "~/composables/useAuth";
const authStore = useAuthS();
const email = ref("");
const password = ref("");

const signin = () => {
  authStore.login({ email: email.value, password: password.value });
};
</script>
