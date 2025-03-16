<template>
  <div class="flex justify-center">
    <div class="max-w-6xl mx-auto px-4">
      <div
        class="flex flex-col gap-10 items-center sm:items-start sm:flex-row sm:justify-center w-full sm:py-12 mb-4"
      >
        <div
          class="sm:col-span-6 md:col-span-3 lg:col-span-2 flex flex-col items-center justify-center"
        >
          <NuxtImg src="Coat_of_arms_of_Zambia.png" class="h-20 w-20" />
          <h6 class="text-sm text-slate-500 font-medium mb-2">
            Zambian Embassy
          </h6>
        </div>

        <div class="sm:col-span-6 md:col-span-3 lg:col-span-2">
          <h6 class="text-sm text-slate-500 font-medium mb-2">Embassy</h6>
          <ul class="text-sm space-y-2 flex flex-col items-center">
            <li>
              <a
                class="text-slate-400 hover:text-slate-200 transition duration-150 ease-in-out"
                href="#0"
                >About us</a
              >
            </li>
            <li>
              <a
                class="text-slate-400 hover:text-slate-200 transition duration-150 ease-in-out"
                href="#0"
                >Location</a
              >
            </li>

            <li>
              <a
                class="text-slate-400 hover:text-slate-200 transition duration-150 ease-in-out"
                href="#0"
                >Careers</a
              >
            </li>
          </ul>
        </div>
        <div
          class="sm:col-span-6 md:col-span-3 lg:col-span-2 h-full flex flex-col justify-center items-center"
        >
          <h6 class="text-sm text-slate-500 font-medium mb-2">Legal</h6>
          <ul class="text-sm space-y-2 flex flex-col items-center">
            <li>
              <a
                class="text-slate-400 hover:text-slate-200 transition duration-150 ease-in-out"
                href="#0"
                >Terms & Conditions</a
              >
            </li>
            <li>
              <a
                class="text-slate-400 hover:text-slate-200 transition duration-150 ease-in-out"
                href="#0"
                >Privacy policy</a
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
            <div class="text-sm text-gray-500 text-center w-[80%] sm:w-full">
              &copy; {{ platformName }}
              <span class="text-slate-500">-</span> All rights reserved.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();
const platformName = config.public.platformName;
</script>
