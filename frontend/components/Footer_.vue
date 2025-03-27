<template>
  <div class="flex justify-center bg-black w-full">
    <div class="max-w-6xl mx-auto px-4">
      <div
        class="flex flex-col gap-10 items-center sm:items-start sm:flex-row sm:justify-center w-full sm:py-12 mb-4"
      >
        <div class="sm:col-span-6 md:col-span-3 lg:col-span-2">
          <h6 class="text-base text-white font-medium mb-2">Company</h6>
          <ul class="text-sm space-y-2 flex flex-col items-center">
            <li>
              <a
                class="text-slate-200 hover:text-slate-200 transition duration-150 ease-in-out"
                href="#0"
                >About</a
              >
            </li>
            <li>
              <a
                class="text-slate-200 hover:text-slate-200 transition duration-150 ease-in-out"
                href="#0"
                >Terms</a
              >
            </li>

            <li>
              <a
                class="text-slate-200 hover:text-slate-200 transition duration-150 ease-in-out"
                href="#0"
                >Privacy</a
              >
            </li>
          </ul>
        </div>
        <div
          class="sm:col-span-6 md:col-span-3 lg:col-span-2 h-full flex flex-col justify-center items-center"
        >
          <h6 class="text-base text-white font-medium mb-2">Product</h6>
          <ul class="text-sm space-y-2 flex flex-col items-center">
            <li>
              <a
                class="text-slate-200 hover:text-slate-200 transition duration-150 ease-in-out"
                href="/business"
                >Business</a
              >
            </li>
            <li>
              <a
                class="text-slate-200 hover:text-slate-200 transition duration-150 ease-in-out"
                href="/"
                >Customers</a
              >
            </li>
          </ul>
        </div>
      </div>
      <div class="sm:col-span-12 lg:col-span-4 order-1 lg:order-none mb-6">
        <div
          class="h-full flex flex-col sm:flex-row lg:flex-col justify-between"
        >
          <div class="mb-4 sm:mb-0 h-full flex items-center justify-center">
            <div class="text-sm text-white text-center w-[80%] sm:w-full">
              &copy; 2025, CrossPerks - All rights reserved.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
</script>
