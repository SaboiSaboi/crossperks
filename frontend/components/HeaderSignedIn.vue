<script setup lang="ts">
const { logout } = useAuthS();
</script>

<template>
  <header class="z-30 w-full sm:px-2 py-4 bg-gray-50">
    <div class="mx-auto max-w-7xl px-4 sm:px-0">
      <div
        class="relative flex h-16 bg-slate-700 items-center justify-between gap-3 rounded-full px-8"
      >
        <div class="flex flex-1 items-center">
          <router-link
            class="flex shrink-0 text-white w-64 items-center gap-4"
            to="/"
            aria-label="CrossPerks Home"
          >
            <h1 class="md:text-3xl text-2xl font-semibold text-white">
              CrossPerks
            </h1>
          </router-link>
        </div>
        <nav class="hidden md:flex md:grow md:justify-end">
          <NavigationMenu>
            <NavigationMenuList class="flex gap-7">
              <NavigationMenuItem class="text-slate-200 hover:text-slate-50">
                <NavigationMenuLink href="/business/profile">
                  <p class="hover:underline text-xl">Profile</p>
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem class="text-slate-200 hover:text-slate-50">
                <NavigationMenuLink href="/business">
                  <p class="hover:underline text-xl">Settings</p>
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem
                class="text-slate-200 hover:text-slate-50"
                @click="logout"
              >
                <NavigationMenuLink href="/business">
                  <p class="hover:underline text-lg">
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
                  </p>
                </NavigationMenuLink>
              </NavigationMenuItem>
              <!-- <NavigationMenuItem class="text-black transition-colors">
                <NavigationMenuLink
                  href="/signin"
                  class="text-slate-200 hover:text-slate-50"
                >
                  <p class="hover:underline text-2xl">Sign in</p>
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem
                class="text-black text-2xl hover:text-[#F5F5F5] transition-colors border-10 border-black"
              >
                <NavigationMenuLink
                  href="/signup"
                  :class="navigationMenuTriggerStyle()"
                  class="bg-slate-200 hover:bg-slate-50 border-[1.5px] border-black"
                >
                  <p class="text-2xl">Join Now</p>
                </NavigationMenuLink>
              </NavigationMenuItem> -->
            </NavigationMenuList>
          </NavigationMenu>
        </nav>

        <BurgerMenu />
      </div>
    </div>
  </header>
</template>
