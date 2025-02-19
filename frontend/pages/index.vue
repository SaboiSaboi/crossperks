<template>
  <div
    class="min-h-screen flex flex-col justify-center items-center bg-cyan-900 text-white font-roboto w-full"
  >
    <Header />

    <div
      class="flex flex-col md:flex-row items-center gap-6 md:gap-8 lg:max-w-[87rem] mx-auto mb-24"
    >
      <!-- Text Section -->
      <section class="flex flex-col gap-4 w-full md:w-1/2 md:text-left py-4">
        <div class="px-6">
          <!-- Tagline (visible when showTagline is true) -->
          <p
            v-if="showTagline"
            class="text-cyan-200 font-normal leading-relaxed text-4xl md:text-5xl lg:text-7xl h-[5rem] md:h-[7.8rem] lg:h-[12.8rem]"
          >
            Earn Perks & Support Local Spots Like
          </p>
          <!-- Typing Text -->
          <p
            class="typing font-bold text-yellow-300 text-4xl md:text-3xl lg:text-5xl h-[5rem] md:h-[7rem] lg:h-[7rem] pt-4"
          >
            {{ typedText }}
          </p>
        </div>

        <!-- Descriptive Text -->
        <p
          class="text-lg md:text-xl text-cyan-200 font-normal px-6 lg:px-3 lg:text-3xl"
        >
          Shop as usual—get rewarded when you check out.
          <br class="hidden md:block" />
          <span class="text-cyan-200">
            Support businesses that match your values.
          </span>
        </p>
      </section>

      <!-- Image Section -->
      <NuxtImg
        src="https://images.pexels.com/photos/3907306/pexels-photo-3907306.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        alt="Perks Illustration"
        class="w-full md:w-1/2 max-w-md md:max-w-none object-cover sm:rounded-lg shadow-lg transition-transform hover:scale-105 duration-500"
      />
    </div>

    <div
      class="bg-white p-8 rounded-lg shadow-xl w-[90%] sm:w-[34rem] text-gray-800 mb-24"
    >
      <h2
        class="text-3xl font-extrabold text-center mb-4 text-indigo-700 text-balance"
      >
        Unlock Exclusive Local Perks
      </h2>
      <p class="text-center text-gray-600 mb-6 text-lg text-balance">
        Join our waitlist and be the first to enjoy special offers at your
        favorite local businesses.
      </p>

      <form
        @submit.prevent="submitForm"
        class="space-y-4 flex flex-col items-center w-full"
      >
        <div class="flex flex-col">
          <div class="mb-4">
            <Label class="block text-gray-700 font-semibold mb-2">Name</Label>
            <Input
              v-model="name"
              type="text"
              placeholder="Enter your name"
              class="w-80"
              required
            />
          </div>
          <div class="mb-4">
            <Label class="block text-gray-700 font-semibold mb-2">Email</Label>
            <Input
              v-model="email"
              type="email"
              placeholder="Enter your email"
              class="w-80"
              required
            />
          </div>
          <Label class="block text-gray-700 font-semibold mb-2"
            >Favorite Businesses</Label
          >
          <TagsInput v-model="modelValue" class="w-80">
            <TagsInputItem v-for="item in modelValue" :key="item" :value="item">
              <TagsInputItemText />
              <TagsInputItemDelete />
            </TagsInputItem>
            <TagsInputInput
              placeholder="Enter up to 5 businesses you love..."
            />
          </TagsInput>
        </div>
        <Button type="submit" class="p-6 rounded-[0.75rem] hover:bg-opacity-80"
          >Join the Waitlist</Button
        >
      </form>
      <p
        v-if="successMessage"
        class="text-green-600 text-center mt-4 font-semibold"
      >
        {{ successMessage }}
      </p>
    </div>
    <div class="py-16 bg-gray-100 text-gray-900 w-full">
      <div class="max-w-5xl mx-auto text-center">
        <h2 class="text-4xl font-extrabold text-gray-800">
          How CrossPerks Works
        </h2>
        <p class="text-lg text-gray-600 mt-4 text-balance">
          Earn rewards effortlessly while supporting your favorite local
          businesses.
        </p>
      </div>

      <div
        class="mt-12 flex flex-col lg:flex-row items-center justify-center space-y-12 lg:space-y-0 lg:space-x-16 max-w-6xl mx-auto"
      >
        <div class="flex flex-col items-center text-center">
          <NuxtImg
            src="https://images.pexels.com/photos/3184183/pexels-photo-3184183.jpeg"
            alt="Visit Local Business"
            class="w-72 h-72 rounded-lg shadow-lg object-cover transition-transform hover:scale-105 duration-1000"
          />
          <p class="mt-4 text-xl font-semibold">Visit Local Businesses</p>
          <p class="w-[90%] md:w-full text-balance text-gray-600">
            Grab a coffee, hit the gym, or book a spa treatment—just like
            normal.
          </p>
        </div>

        <div class="flex flex-col items-center text-center">
          <NuxtImg
            src="https://images.pexels.com/photos/3183171/pexels-photo-3183171.jpeg"
            alt="Check Out & Unlock Perks"
            class="w-72 h-72 rounded-lg shadow-lg object-cover transition-transform hover:scale-105 duration-1000"
          />
          <p class="mt-4 text-xl font-semibold">Check Out & Unlock Perks</p>
          <p class="text-balance text-gray-600 w-[90%] md:w-full">
            Scan your CrossPerks QR code at checkout & unlock a surprise perk!
          </p>
        </div>

        <div class="flex flex-col items-center text-center">
          <NuxtImg
            src="https://images.pexels.com/photos/3997997/pexels-photo-3997997.jpeg"
            alt="Redeem Perks"
            class="w-72 h-72 rounded-lg shadow-lg object-cover transition-transform hover:scale-105 duration-1000"
          />
          <p class="mt-4 text-xl font-semibold">
            Redeem Perks at Partner Businesses
          </p>
          <p class="text-balance text-gray-600">
            Use your perk at another awesome local business—keep the cycle
            going!
          </p>
        </div>
      </div>
    </div>

    <div class="h-52 w-full bg-gray-950 text-white">
      <div class="h-full flex flex-col md:flex-row lg:flex-col justify-between">
        <div class="mb-4 md:mb-0 h-full flex items-center justify-center">
          <div class="text-sm text-white text-center w-[80%] md:w-full">
            &copy; 2025, CrossPerks - All rights reserved.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Button } from "@/components/ui/button";
import {
  TagsInput,
  TagsInputInput,
  TagsInputItem,
  TagsInputItemDelete,
  TagsInputItemText,
} from "@/components/ui/tags-input";

const modelValue = ref(["Champions Barbershop", "Upper Left Coffeeshop"]);
const name = ref("");
const email = ref("");
const successMessage = ref("");
const showTagline = ref(false);
const businesses = [
  "Nossa Familia Coffee-Portland",
  "Zen Gym",
  "Green Spa",
  "Honey Latte Cafe",
  "Book Haven",
  "Above ground Coffee House",
];
const typedText = ref("");
let isTyping = false;

const typeText = async (text) => {
  if (isTyping) return;
  isTyping = true;
  typedText.value = "";
  for (let i = 0; i < text.length; i++) {
    await new Promise((resolve) => setTimeout(resolve, 20));
    typedText.value += text[i];
  }
  isTyping = false;
};

onMounted(() => {
  showTagline.value = true;
  let i = 0;
  const switchText = () => {
    typeText(businesses[i % businesses.length]);
    i++;
  };
  switchText();
  setInterval(switchText, 4000);
});
</script>
