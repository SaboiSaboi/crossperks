<template>
  <main class="flex-grow">
    <Header />
    <section class="relative text-black min-h-screen py-16">
      <div class="relative max-w-6xl mx-auto px-4 sm:px-6">
        <div class="text-center mb-12 pt-8">
          <h1 class="text-4xl font-semibold text-gray-800 mb-4 text-balance">
            Create Your Company and Admin Account
          </h1>
          <p class="text-lg text-gray-600 text-balance">
            Register your company and set up your admin account in just a few
            steps.
          </p>
        </div>

        <div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
          <form @submit.prevent="signup">
            <h2 class="text-2xl font-semibold text-gray-600 mb-6">
              Company Information
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <Label for="companyName" class="block text-sm font-medium mb-2"
                  >Company Name</Label
                >
                <Input
                  id="companyName"
                  v-model="companyName"
                  disabled
                  type="text"
                  placeholder="Enter your company name"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            <!-- About Admin Section -->
            <h2 class="text-2xl font-semibold text-gray-600 mb-6 mt-8">
              Admin Information
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <Label for="firstName" class="block text-sm font-medium mb-2"
                  >First Name</Label
                >
                <Input
                  id="firstName"
                  v-model="firstName"
                  disabled
                  type="text"
                  placeholder="Enter your first name"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <Label for="lastName" class="block text-sm font-medium mb-2"
                  >Last Name</Label
                >
                <Input
                  id="lastName"
                  v-model="lastName"
                  disabled
                  type="text"
                  placeholder="Enter your last name"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <Label for="position" class="block text-sm font-medium mb-2"
                  >Position</Label
                >
                <Input
                  id="position"
                  v-model="position"
                  disabled
                  type="text"
                  placeholder="Enter your position"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <Label for="email" class="block text-sm font-medium mb-2"
                  >Email Address</Label
                >
                <Input
                  id="email"
                  v-model="email"
                  disabled
                  type="email"
                  placeholder="Enter your email"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <Label for="password" class="block text-sm font-medium mb-2"
                  >Password</Label
                >
                <Input
                  id="password"
                  v-model="password"
                  disabled
                  type="password"
                  placeholder="Create a password"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            <!-- Terms and Conditions -->
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
                Privacy Policy
              </NuxtLink>
              .
            </p>

            <!-- Submit Button -->
            <div class="mt-6 flex justify-center">
              <Button
                type="submit"
                class="py-2 mt-4 font-semibold text-white bg-gray-500 rounded-lg hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                disabled
              >
                Sign Up
              </Button>
            </div>
          </form>

          <!-- Sign In Link -->
          <div class="text-center mt-4">
            <p class="text-sm text-gray-500">
              Already have an account?
              <NuxtLink
                class="font-medium text-purple-500 hover:text-purple-400 transition duration-150"
                to="/signin"
              >
                Sign in
              </NuxtLink>
            </p>
          </div>
        </div>
      </div>
    </section>
    <Footer />
  </main>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthS } from "~/composables/useAuth";

const authStore = useAuthS();
const companyName = ref("");
const firstName = ref("");
const lastName = ref("");
const position = ref("");
const email = ref("");
const password = ref("");
const router = useRouter();

const signup = async () => {
  const usersData = {
    company_name: companyName.value,
    first_name: firstName.value,
    last_name: lastName.value,
    position: position.value,
    email: email.value,
    password: password.value,
  };
  await authStore.registerCompany(usersData);
  if (authStore.state.value?.user) {
    router.push("/dashboard");
  }
};
</script>
