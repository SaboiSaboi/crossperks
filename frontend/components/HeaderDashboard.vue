<script setup lang="ts">
import { computed, ref } from "vue";
import { navigationMenuTriggerStyle } from "@/components/ui/navigation-menu";
import { useRoute } from "vue-router";

// Initialize router and auth state
const route = useRoute();
const { handleCheckAuth, logout } = useAuthS();

// Properly declare reactive refs
const user = ref<any>(null);
const userType = ref<string>("");

// Ensure async data fetching on component mount
user.value = await handleCheckAuth();
userType.value = user.value?.user?.user_type || "";

// Navigation Links
const navLinks = computed(() => [
  {
    name: "Dashboard",
    path: `/${userType.value}/dashboard`,
    show: !!user.value,
  },
  {
    name: "Businesses",
    path: "/businesses",
    show: true,
  },
  {
    name: "Business",
    path: "/business",
    show: true,
  },
  {
    name: "Profile",
    path:
      userType.value === "customer"
        ? "/customer/profile"
        : userType.value === "business"
        ? "/business/profile"
        : "#",
    show: !!user.value,
  },
  {
    name: "Sign In",
    path: "/signin",
    show: !user.value,
  },
  {
    name: "Join Now",
    path: "/signup",
    show: !user.value,
  },
]);

// Highlight active link based on current route
const isActive = (path: string) => route.path === path;
</script>

<template>
  <header class="z-30 w-full sm:px-2 sm:py-10">
    <div class="mx-auto px-4">
      <div
        class="relative flex sm:h-32 items-center justify-between gap-24 rounded-full sm:p-8"
      >
        <div class="flex flex-1 items-center">
          <router-link
            class="flex shrink-0 text-white items-center gap-4"
            to="/"
            aria-label="CrossPerks Home"
          >
            <svg
              class="hidden sm:block w-auto h-[180px]"
              viewBox="0 0 1000 350"
              xmlns="http://www.w3.org/2000/svg"
              preserveAspectRatio="xMidYMid meet"
            >
              <defs>
                <linearGradient
                  id="crossperksGradient"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="0%"
                >
                  <stop offset="0%" stop-color="#FFD700" />
                  <stop offset="50%" stop-color="#FAD961" />
                  <stop offset="100%" stop-color="#F76B1C" />
                </linearGradient>
              </defs>
              <text
                x="50%"
                y="50%"
                dy="0.35em"
                text-anchor="middle"
                class="svg-text"
              >
                CrossPerks
              </text>
            </svg>

            <svg
              class="block sm:hidden w-auto h-[120px]"
              viewBox="0 0 1000 650"
              xmlns="http://www.w3.org/2000/svg"
              preserveAspectRatio="xMidYMid meet"
            >
              <defs>
                <linearGradient
                  id="crossperksGradientSmall"
                  x1="0%"
                  y1="0%"
                  x2="100%"
                  y2="0%"
                >
                  <stop offset="0%" stop-color="#FFD700" />
                  <stop offset="50%" stop-color="#FAD961" />
                  <stop offset="100%" stop-color="#F76B1C" />
                </linearGradient>
              </defs>
              <text
                x="50%"
                y="50%"
                dy="0.35em"
                text-anchor="middle"
                class="svg-text-small"
              >
                CrossPerks
              </text>
            </svg>
          </router-link>
        </div>

        <nav class="hidden sm:flex sm:grow sm:justify-end">
          <NavigationMenu>
            <NavigationMenuList class="flex gap-7">
              <NavigationMenuItem
                v-for="link in navLinks"
                :key="link.path"
                v-show="link.show"
              >
                <NavigationMenuLink
                  :href="link.path"
                  @click="link.name === 'Sign In' ? logout : null"
                  class="text-xl transition-colors"
                  :class="
                    isActive(link.path)
                      ? 'text-slate-50 underline font-semibold'
                      : 'text-slate-200 hover:text-slate-50 hover:underline'
                  "
                >
                  <span
                    v-if="link.name !== 'Sign In' && link.name !== 'Join Now'"
                  >
                    {{ link.name }}
                  </span>

                  <!-- Icon specifically for Sign In / Logout -->
                  <svg
                    v-if="link.name === 'Sign In' && user"
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
                      d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9"
                    />
                  </svg>

                  <span
                    v-if="link.name === 'Join Now'"
                    class="text-black text-xl bg-slate-200 hover:bg-slate-50 border-[1.5px] border-black px-4 py-2 rounded-full transition-all"
                  >
                    {{ link.name }}
                  </span>
                </NavigationMenuLink>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
        </nav>
        <BurgerMenu />
        <div class="block sm:hidden">a menu</div>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* Large Screen SVG Animation */
.svg-text {
  font-size: 180px;
  font-weight: 800;
  font-family: "Inter", sans-serif;
  fill: transparent;
  stroke: url(#crossperksGradient);
  stroke-width: 4;
  stroke-linecap: round;
  stroke-dasharray: 2200;
  stroke-dashoffset: 2200;
  animation: drawText 3s ease-out forwards, fadeIn 3s ease-out forwards;
  shape-rendering: crispEdges;
}

/* Small Screen SVG Animation */
.svg-text-small {
  font-size: 140px;
  font-weight: 700;
  font-family: "Inter", sans-serif;
  fill: transparent;
  stroke: url(#crossperksGradientSmall);
  stroke-width: 3;
  stroke-linecap: round;
  stroke-dasharray: 1800;
  stroke-dashoffset: 1800;
  animation: drawTextSmall 3s ease-out forwards, fadeIn 3s ease-out forwards;
  shape-rendering: crispEdges;
}

/* Hover Effect: Glow and Subtle Color Shift */
.svg-text:hover,
.svg-text-small:hover {
  stroke-width: 4.1;
  filter: drop-shadow(0px 0px 8px rgba(255, 180, 50, 0.4))
    drop-shadow(0px 0px 14px rgba(255, 180, 50, 0.2));
}

/* Large SVG Stroke Animation */
@keyframes drawText {
  0% {
    stroke-dashoffset: 2200;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

/* Small SVG Stroke Animation */
@keyframes drawTextSmall {
  0% {
    stroke-dashoffset: 1800;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

/* Smooth Fade-in Effect */
@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
