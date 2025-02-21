<template>
  <div
    class="min-h-screen flex flex-col justify-center items-center bg-[#00C4CC] text-white font-roboto w-full"
  >
    <Header />

    <div
      class="flex flex-col md:flex-row items-center gap-6 md:gap-8 lg:max-w-[87rem] mx-auto mb-24 p-16 bg-slate-500 sm:bg-lime-400 md:bg-blue-800 lg:bg-gray-900 rounded-lg"
    >
      <!-- Text Section -->
      <section class="flex flex-col gap-8 w-full md:w-1/2 md:text-left py-4">
        <div class="">
          <!-- Tagline (visible when showTagline is true) -->
          <p
            v-if="showTagline"
            class="text-cyan-200 font-normal leading-relaxed text-4xl md:text-5xl lg:text-5xl h-[5rem] md:h-[7.8rem] lg:h-fit"
          >
            Enjoy Surprise Perks & <br />Support Local Businesses Like
          </p>
          <!-- Typing Text -->
          <p
            class="w-[29rem] typing font-bold text-yellow-300 text-4xl md:text-3xl lg:text-5xl h-[5rem] md:h-[7rem] lg:h-[7rem] pt-4"
          >
            {{ typedText }}
          </p>
        </div>

        <!-- Descriptive Text -->
        <p class="text-lg md:text-xl text-cyan-200 font-normal lg:text-2xl">
          Shop as usual — Enjoy Surprise Perks along the way.
          <br class="hidden md:block" />
          <span class="text-cyan-200">
            Support businesses that match your values.
          </span>
        </p>
        <div>
          <button
            class="mt-6 px-8 py-4 bg-green-900 text-white rounded-full hover:bg-green-700 transition"
          >
            Join Now
          </button>
        </div>
      </section>

      <!-- Image Section -->
      <!-- <section class="bg-slate-300 flex justify-center h-96"> -->
      <NuxtImg
        src="https://images.pexels.com/photos/3907306/pexels-photo-3907306.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        alt="Perks Illustration"
        class="w-full md:w-[35rem] max-w-md md:max-w-none object-cover sm:rounded-lg shadow-lg transition-transform hover:scale-105 duration-1000"
      />
      <!-- </section> -->
    </div>

    <!-- <div
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
    </div> -->
    <!-- <div class="p-16 bg-slate-700 w-full h-[25rem]">
      <div class="flex justify-center gap-4">
        <Button class="text-3xl rounded-[2rem] p-6">Shop</Button>
        <Button class="text-3xl rounded-[2rem] p-6">Scan</Button>
        <Button class="text-3xl rounded-[2rem] p-6">Get Perks</Button>
        <Button class="text-3xl rounded-[2rem] p-6">Repeat</Button>
      </div>
    </div> -->

    <!-- Visual Storytelling Section -->
    <div class="min-h-screen bg-slate-50 text-slate-900 w-full">
      <section class="py-24 px-10 flex flex-col gap-20">
        <!-- Step 1: Shop -->
        <div class="flex items-center gap-20 mx-auto">
          <div class="flex-1">
            <h2 class="text-4xl font-bold mb-4">Shop at Local Businesses</h2>
            <p class="text-lg text-slate-600">
              Visit your favorite CrossPerks partner businesses and discover
              special offers while enjoying your usual purchases.
            </p>
            <div
              class="mt-6 p-6 border border-slate-300 rounded-xl shadow-sm hover:shadow-md transition"
            >
              <h3 class="font-semibold">🛍️ Shop</h3>
              <p class="text-slate-500 mt-2">
                Explore new places or revisit your go-to spots for everyday
                purchases.
              </p>
            </div>
          </div>
          <div class="flex-1">
            <div
              class="w-full h-96 bg-cover bg-center rounded-2xl shadow-lg"
              style="
                background-image: url('https://images.pexels.com/photos/4056722/pexels-photo-4056722.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
              "
            ></div>
          </div>
        </div>

        <!-- Step 2: Scan -->
        <div class="flex items-center gap-20 mx-auto flex-row-reverse">
          <div class="flex-1">
            <h2 class="text-4xl font-bold mb-4">Scan the QR Code</h2>
            <p class="text-lg text-slate-600">
              Quickly scan the business's CrossPerks QR code with your phone to
              unlock exclusive rewards.
            </p>
            <div
              class="mt-6 p-6 border border-slate-300 rounded-xl shadow-sm hover:shadow-md transition"
            >
              <h3 class="font-semibold">📱 Scan</h3>
              <p class="text-slate-500 mt-2">
                One quick scan connects you to surprise perks and exclusive
                deals.
              </p>
            </div>
          </div>
          <div class="flex-1">
            <div
              class="w-full h-96 bg-cover bg-center rounded-2xl shadow-lg"
              style="
                background-image: url('https://images.pexels.com/photos/7289717/pexels-photo-7289717.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
              "
            ></div>
          </div>
        </div>

        <!-- Step 3: Get Perks -->
        <div class="flex items-center gap-12 max-w-6xl mx-auto">
          <div class="flex-1">
            <h2 class="text-4xl font-bold mb-4">Get Surprise Perks</h2>
            <p class="text-lg text-slate-600">
              Unlock discounts, freebies, or special rewards tailored to your
              shopping experience.
            </p>
            <div
              class="mt-6 p-6 border border-slate-300 rounded-xl shadow-sm hover:shadow-md transition"
            >
              <h3 class="font-semibold">🎁 Get Perks</h3>
              <p class="text-slate-500 mt-2">
                Your loyalty earns you unexpected rewards every time.
              </p>
            </div>
          </div>
          <div class="flex-1">
            <div
              class="w-full h-80 bg-cover bg-center rounded-2xl shadow-lg"
              style="
                background-image: url('https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
              "
            ></div>
          </div>
        </div>

        <!-- Step 4: Repeat -->
        <div
          class="flex items-center gap-12 max-w-6xl mx-auto flex-row-reverse"
        >
          <div class="flex-1">
            <h2 class="text-4xl font-bold mb-4">Repeat and Keep Earning</h2>
            <p class="text-lg text-slate-600">
              Redeem your perks at any participating business and keep the
              rewards flowing.
            </p>
            <div
              class="mt-6 p-6 border border-slate-300 rounded-xl shadow-sm hover:shadow-md transition"
            >
              <h3 class="font-semibold">🔄 Repeat</h3>
              <p class="text-slate-500 mt-2">
                Continue your journey, unlocking more perks as you go.
              </p>
            </div>
          </div>
          <div class="flex-1">
            <div
              class="w-full h-80 bg-cover bg-center rounded-2xl shadow-lg"
              style="
                background-image: url('https://images.pexels.com/photos/16838917/pexels-photo-16838917/free-photo-of-repeat-until-funny.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
              "
            ></div>
          </div>
        </div>
      </section>
    </div>

    <!-- Call to Action Section -->
    <section class="py-24 bg-slate-900 text-white text-center w-full">
      <h2 class="text-4xl font-bold mb-6">Ready to Unlock Your Perks?</h2>
      <button
        class="mt-4 px-10 py-4 bg-white text-slate-900 rounded-full hover:bg-slate-200 transition mb-24"
      >
        Get Started
      </button>
      <div class="text-sm text-white text-center w-[80%] md:w-full">
        &copy; 2025, CrossPerks - All rights reserved.
      </div>
    </section>
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
  "Above ground Coffee House in Portland City",
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
