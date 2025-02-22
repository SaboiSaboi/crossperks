<template>
  <div>
    <button
      class="p-2 text-black z-50 md:hidden"
      aria-label="Open Menu"
      @click="toggleMobileNav"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
        />
      </svg>
    </button>

    <div v-if="mobileNavOpen" class="fixed inset-0 z-50 bg-black text-white">
      <button
        class="absolute top-6 right-11"
        aria-label="Close Menu"
        @click="toggleMobileNav"
      >
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <nav class="h-full w-full pt-16 px-6 overflow-y-auto">
        <div
          v-for="(categoryObj, index) in aboutEmbassy"
          :key="index"
          class="mb-6"
        >
          <h3 class="text-gray-400 uppercase tracking-widest mb-4">
            The Embassy
          </h3>
          <ul class="space-y-3">
            <li
              v-for="(service, idx) in categoryObj.items"
              :key="idx"
              class="flex items-center gap-2"
            >
              <NuxtLink to="#" class="hover:text-indigo-400">{{
                service.title
              }}</NuxtLink>
            </li>
          </ul>
        </div>

        <div
          v-for="(categoryObj, index) in consularServices"
          :key="index"
          class="mb-6"
        >
          <h3 class="text-gray-400 uppercase tracking-widest mb-4">
            Consular & Immigration
          </h3>
          <ul class="space-y-3">
            <li
              v-for="(service, idx) in categoryObj.items"
              :key="idx"
              class="flex items-center gap-2"
            >
              <NuxtLink to="#" class="hover:text-indigo-400">{{
                service.title
              }}</NuxtLink>
            </li>
          </ul>
        </div>

        <div
          v-for="(categoryObj, index) in aboutZambia"
          :key="index"
          class="mb-6"
        >
          <h3 class="text-gray-400 uppercase tracking-widest mb-4">
            About Zambia
          </h3>
          <ul class="space-y-3">
            <li
              v-for="(service, idx) in categoryObj.items"
              :key="idx"
              class="flex items-center gap-2"
            >
              <NuxtLink to="#" class="hover:text-indigo-400">{{
                service.title
              }}</NuxtLink>
            </li>
          </ul>
        </div>
        <div class="mb-6">
          <NuxtLink to="#" class="hover:text-indigo-400">
            <h3
              class="text-gray-400 uppercase tracking-widest mb-4 hover:text-indigo-400"
            >
              Media & News
            </h3>
          </NuxtLink>
        </div>

        <div class="mb-6">
          <NuxtLink to="#" class="hover:text-indigo-400"
            ><h3
              class="text-gray-400 uppercase hover:text-indigo-400 tracking-widest mb-4"
            >
              Contact and Appointments
            </h3></NuxtLink
          >
        </div>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const mobileNavOpen = ref(false);

const toggleMobileNav = () => {
  mobileNavOpen.value = !mobileNavOpen.value;
};

interface ConsularService {
  title: string;
  href: string;
  description?: string;
}

interface ConsularServiceCategory {
  category?: string;
  items?: ConsularService[];
}
const aboutEmbassy: ConsularServiceCategory[] = [
  {
    items: [
      {
        title: "Staff",
        href: "/services/passport",
      },
      {
        title: "Embassy Holidays",
        href: "/services/dual-citizenship",
      },
      {
        title: "Honorary Consuls",
        href: "/services/nationals-registration",
      },
      {
        title: "Job Opportunities",
        href: "/services/nationals-registration",
      },
    ],
  },
];
const aboutZambia: ConsularServiceCategory[] = [
  {
    category: "Visit Zambia",
    items: [
      {
        title: "Visa Requirements",
        href: "/services/passport",
        description: "Check required documents and eligibility.",
      },
      {
        title: "Attractions",
        href: "/services/dual-citizenship",
        description: "Discover Zambia’s must-see spots.",
      },
      {
        title: "Culture & Traditions",
        href: "/services/nationals-registration",
        description: "Explore Zambia’s rich heritage.",
      },
      {
        title: "Hotels & Accommodation",
        href: "/services/nationals-registration",
        description: "Find lodging for every budget.",
      },
      {
        title: "Trade Opportunities",
        href: "/services/visa",
        description: "Explore business ventures and markets.",
      },
      {
        title: "Import/Export Guide",
        href: "/services/press-accreditation",
        description: "Regulations for trading in/out of Zambia.",
      },
      {
        title: "Investment Incentives",
        href: "/services/travel-advisories",
        description: "Learn about investor benefits.",
      },
      {
        title: "Economic Reports",
        href: "/services/travel-advisories",
        description: "Review data on economic performance.",
      },
      {
        title: "National Parks & Safaris",
        href: "/info/hours",
        description: "Experience Zambia’s wildlife.",
      },
      {
        title: "Tourism Board Info",
        href: "/services/pets",
        description: "Official resources for travelers.",
      },
      {
        title: "Victoria Falls",
        href: "/services/police-clearance",
        description: "Visit the world-famous waterfall.",
      },
      {
        title: "Festivals & Events",
        href: "/services/police-clearance",
        description: "Enjoy cultural celebrations.",
      },
      {
        title: "Government Structure",
        href: "/info/hours",
        description: "Overview of Zambia’s political system.",
      },
      {
        title: "Flag & National Anthem",
        href: "/services/pets",
        description: "Discover Zambia’s symbols.",
      },
      {
        title: "National Holidays",
        href: "/services/police-clearance",
        description: "See all public holiday dates.",
      },
    ],
  },
];
const consularServices: ConsularServiceCategory[] = [
  {
    items: [
      {
        title: "Passport Application",
        href: "/services/passport",
        description: "Learn how to apply or renew your passport.",
      },
      {
        title: "Dual Citizenship",
        href: "/services/dual-citizenship",
        description: "Guidelines on how to apply for dual citizenship.",
      },
      {
        title: "Registration of Nationals",
        href: "/services/nationals-registration",
        description: "Register yourself or your family with the embassy.",
      },
      {
        title: "Visa Application",
        href: "/services/visa",
        description: "Requirements and forms for visa applications.",
      },
      {
        title: "Press Accreditation",
        href: "/services/press-accreditation",
        description: "Accreditation process for foreign journalists.",
      },
      {
        title: "Travel Advisories",
        href: "/services/travel-advisories",
        description: "Current travel warnings and advisories.",
      },
      {
        title: "Hours of Operation",
        href: "/info/hours",
        description: "Our official operating hours and holidays.",
      },
      {
        title: "Importation of Pets",
        href: "/services/pets",
        description: "Guidelines for bringing pets or livestock.",
      },
      {
        title: "Police Clearance",
        href: "/services/police-clearance",
        description: "How to request a police clearance certificate.",
      },
    ],
  },
];
</script>
