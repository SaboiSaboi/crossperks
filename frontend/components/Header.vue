<script setup lang="ts">
import { navigationMenuTriggerStyle } from "@/components/ui/navigation-menu";
</script>

<template>
  <header class="z-30 w-full sm:px-2 py-4">
    <div class="mx-auto max-w-7xl px-4 sm:px-0">
      <div
        class="relative flex h-16 items-center justify-between gap-3 rounded-2xl px-8 bg-[#EFBF04]"
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
              <NavigationMenuItem
                class="text-black hover:text-[#F5F5F5] transition-colors"
              >
                <NavigationMenuLink
                  href="#waitlist"
                  :class="navigationMenuTriggerStyle()"
                >
                  Business
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem
                class="text-black hover:text-[#F5F5F5] transition-colors"
              >
                <NavigationMenuLink
                  href="#waitlist"
                  :class="navigationMenuTriggerStyle()"
                >
                  Sign In
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem
                class="text-black hover:text-[#F5F5F5] transition-colors"
              >
                <NavigationMenuLink
                  href="#about"
                  :class="navigationMenuTriggerStyle()"
                >
                  Join Now
                </NavigationMenuLink>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
        </nav>

        <BurgerMenu />
      </div>
    </div>
  </header>
</template>
