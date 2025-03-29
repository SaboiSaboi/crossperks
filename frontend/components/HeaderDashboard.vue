<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const { handleCheckAuth, logout } = useAuthS();

const user = ref<any>(null);
const userType = ref<string>("");

user.value = await handleCheckAuth();
userType.value = user.value?.user?.user_type || "";

const navLinks = computed(() => [
  {
    name: "Dashboard",
    path: user.value ? `/${userType.value}/dashboard` : "#",
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
    name: user.value ? "Logout" : "Sign In",
    path: user.value ? "#" : "/signin",
    show: true,
  },
  {
    name: "Join Now",
    path: "/signup",
    show: !user.value,
  },
]);

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
                  class="text-xl transition-colors flex items-center gap-2"
                  :class="
                    isActive(link.path)
                      ? 'text-slate-50 underline font-semibold'
                      : 'text-slate-200 hover:text-slate-50 hover:underline'
                  "
                >
                  <NavigationMenuLink
                    href="/signin"
                    @click="logout"
                    class="hover:underline text-xl"
                    v-if="link.name === 'Logout'"
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
                        d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9"
                      />
                    </svg>
                  </NavigationMenuLink>
                  <span v-if="link.name === 'Logout'"></span>

                  <span
                    v-else-if="link.name === 'Join Now'"
                    class="text-black text-xl bg-slate-200 hover:bg-slate-50 border-[1.5px] border-black px-4 py-2 rounded-full transition-all"
                  >
                    {{ link.name }}
                  </span>

                  <span v-else>{{ link.name }}</span>
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

.svg-text:hover,
.svg-text-small:hover {
  stroke-width: 4.1;
  filter: drop-shadow(0px 0px 8px rgba(255, 180, 50, 0.4))
    drop-shadow(0px 0px 14px rgba(255, 180, 50, 0.2));
}

@keyframes drawText {
  0% {
    stroke-dashoffset: 2200;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes drawTextSmall {
  0% {
    stroke-dashoffset: 1800;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
