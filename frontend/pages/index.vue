<template>
  <div
    class="min-h-screen flex flex-col justify-center items-center bg-[#007B82] text-white font-roboto w-full"
  >
    <Header />

    <div
      class="flex flex-col items-center gap-6 p-4 sm:p-16 rounded-lg w-full lg:flex lg:flex-row lg:gap-4"
    >
      <!-- Text Section -->
      <section class="flex flex-col gap-8 w-full lg:w-1/2 lg:text-left py-4">
        <div class="">
          <!-- Tagline (visible when showTagline is true) -->
          <p
            v-if="showTagline"
            class="text-[#D1F2EB] font-normal text-4xl sm:text-5xl lg:text-5xl sm:h-[5rem] lg:h-fit"
          >
            Enjoy Surprise Perks & <br />Support Local Spots Like
          </p>
          <!-- Typing Text -->
          <p
            class="w-fit font-bold text-[#FFB347] text-3xl md:text-3xl lg:text-5xl h-[5rem] md:h-[7rem] lg:h-[7rem] pt-4"
          >
            {{ typedText }}
          </p>
        </div>

        <!-- Descriptive Text -->
        <p class="text-lg md:text-xl text-white font-normal lg:text-2xl">
          Shop as usual — Enjoy Surprise Perks along the way.
          <br class="hidden md:block" />
          <span class="text-[#D1F2EB]">
            Support businesses that match your values.
          </span>
        </p>
        <div class="flex justify-start items-center">
          <button
            class="text-2xl px-8 py-4 bg-[#FFB347] text-[#333333] font-semibold rounded-full hover:bg-[#E1A300] transition"
          >
            Join Now
          </button>
        </div>
      </section>

      <!-- Image Section -->
      <div class="h-full">
        <NuxtImg
          src="https://images.pexels.com/photos/3907306/pexels-photo-3907306.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
          alt="Perks Illustration"
          class="w-full lg:max-w-[35rem] max-w-md object-cover rounded-lg shadow-lg transition-transform hover:scale-105 duration-1000"
        />
      </div>
    </div>

    <Clients />

    <div
      class="min-h-screen bg-gradient-to-b from-[#D1F2EB] to-[#F5F5F5] text-[#2E294E] w-full"
    >
      <section class="py-24 px-6 sm:py-32 sm:px-10 flex flex-col gap-24">
        <!-- Reusable Section Template -->
        <div
          class="flex flex-col md:flex-row items-center gap-12 md:gap-16 mx-auto max-w-7xl transition-opacity duration-700 ease-in opacity-100"
        >
          <div class="md:flex-1">
            <h2
              class="flex gap-6 items-center text-3xl sm:text-4xl md:text-5xl font-bold mb-6 tracking-wide"
            >
              <div class="text-7xl">1.</div>
              <div>Shop at Local Businesses</div>
            </h2>
            <p class="text-lg text-[#4A4A4A] leading-relaxed">
              Visit your favorite CrossPerks partner businesses and discover
              special offers while enjoying your usual purchases. <br />
              <br />
              Explore new places or revisit your go-to spots for everyday
              purchases.
            </p>
          </div>
          <div class="md:flex-1 w-full">
            <div
              class="w-full aspect-video bg-cover bg-center rounded-2xl shadow-lg transition-all duration-700 hover:scale-105 hover:brightness-95"
              style="
                background-image: url('https://images.pexels.com/photos/4056722/pexels-photo-4056722.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
              "
            ></div>
          </div>
        </div>

        <div
          class="flex flex-col md:flex-row-reverse items-center gap-12 md:gap-16 mx-auto max-w-7xl transition-opacity duration-700 ease-in opacity-100"
        >
          <div class="md:flex-1 md:w-[49rem]">
            <h2
              class="flex gap-6 items-center text-3xl sm:text-4xl md:text-5xl font-bold mb-6 tracking-wide"
            >
              <div class="text-7xl">2.</div>
              <div>Scan the QR Code</div>
            </h2>
            <p class="text-lg text-[#4A4A4A] leading-relaxed">
              Quickly scan the business's CrossPerks QR code with your phone to
              unlock exclusive rewards. One quick scan connects you to surprise
              perks and exclusive deals.
            </p>
            <!-- <div
              class="w-fit mt-8 p-4 border border-[#B77B57] rounded-2xl shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-transform duration-500"
            >
              <h3 class="font-semibold">📱 Scan</h3>
            </div> -->
          </div>
          <div class="md:flex-1 w-full">
            <div class="md:flex-1 w-full">
              <div
                class="w-full aspect-video bg-cover bg-center rounded-2xl shadow-lg transition-all duration-700 hover:scale-105 hover:brightness-95"
                style="
                  background-image: url('https://images.pexels.com/photos/7289717/pexels-photo-7289717.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
                "
              ></div>
            </div>
          </div>
        </div>

        <div
          class="flex flex-col md:flex-row items-center gap-12 md:gap-16 mx-auto max-w-7xl transition-opacity duration-700 ease-in opacity-100"
        >
          <div class="md:flex-1 md:w-[49rem]">
            <h2
              class="flex gap-6 text-3xl sm:text-4xl md:text-5xl font-bold mb-6 tracking-wide"
            >
              <div class="text-7xl">3.</div>
              Get Surprise Perks
            </h2>
            <p class="text-lg text-[#4A4A4A] leading-relaxed">
              Unlock discounts, freebies, or special rewards tailored to your
              shopping experience. Your loyalty earns you unexpected rewards
              every time.
            </p>
            <!-- <div
              class="mt-8 p-4 border border-[#B77B57] rounded-2xl shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-transform duration-500 w-fit"
            >
              <h3 class="font-semibold">🎁 Get Perks</h3>
            </div> -->
          </div>
          <div class="md:flex-1 w-full">
            <div
              class="w-full aspect-video bg-cover bg-center rounded-2xl shadow-lg transition-all duration-700 hover:scale-105 hover:brightness-95"
              style="
                background-image: url('https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
              "
            ></div>
          </div>
        </div>

        <div
          class="flex flex-col md:flex-row-reverse items-center gap-12 md:gap-16 mx-auto max-w-7xl transition-opacity duration-700 ease-in opacity-100"
        >
          <div class="md:flex-1 md:w-[49rem]">
            <h2
              class="flex gap-6 text-3xl sm:text-4xl md:text-5xl font-bold mb-6 tracking-wide"
            >
              <div class="text-7xl">4.</div>
              Repeat and Keep Earning
            </h2>
            <p class="text-lg text-[#4A4A4A] leading-relaxed">
              Redeem your perks at any participating business and keep the
              rewards flowing. Continue your journey, unlocking more perks as
              you go.
            </p>
            <!-- <div
              class="w-fit mt-8 p-4 border border-[#B77B57] rounded-2xl shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-transform duration-500"
            >
              <h3 class="font-semibold">🔄 Repeat</h3>
            </div> -->
          </div>
          <div class="md:flex-1 w-full">
            <div
              class="w-full aspect-video bg-cover bg-center rounded-2xl shadow-lg transition-all duration-700 hover:scale-105 hover:brightness-95"
              style="
                background-image: url('https://images.pexels.com/photos/16838917/pexels-photo-16838917/free-photo-of-repeat-until-funny.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');
              "
            ></div>
          </div>
        </div>
      </section>
    </div>

    <!-- Call to Action Section -->
    <section
      class="py-16 bg-[#007B82] text-white text-center w-full justify-center items-center"
    >
      <h2 class="text-4xl font-bold mb-6">Ready to Unlock Your Perks?</h2>
      <button
        class="mt-4 px-10 py-4 bg-[#FFB347] text-[#333333] rounded-full hover:bg-[#E1A300] transition"
      >
        Get Started
      </button>
    </section>
    <Footer />
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
