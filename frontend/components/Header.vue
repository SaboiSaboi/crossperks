<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import { navigationMenuTriggerStyle } from "@/components/ui/navigation-menu";
</script>

<template>
  <header class="z-30 mt-2 w-full md:my-5">
    <div class="mx-auto max-w-7xl px-4 sm:px-0">
      <div
        class="bg-slate-100 relative flex h-14 items-center justify-between gap-3 rounded-2xl px-8 before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:[background:linear-gradient(to_right,theme(colors.gray.800),theme(colors.gray.700), before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)] after:absolute after:inset-0 after:-z-10 after:backdrop-blur-sm"
      >
        <div class="flex flex-1 items-center">
          <router-link
            class="flex shrink-0 text-white w-64 items-center gap-4"
            to="/"
            aria-label=""
          >
            <h1 class="md:text-4xl text-2xl font-medium text-gray-700">
              CrossPerks
            </h1>
          </router-link>
        </div>
        <nav class="hidden md:flex md:grow md:justify-end">
          <NavigationMenu>
            <NavigationMenuList class="flex gap-7">
              <NavigationMenuItem class="text-gray-900">
                <NavigationMenuLink
                  href="#about"
                  :class="navigationMenuTriggerStyle()"
                >
                  About
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem class="text-gray-900">
                <NavigationMenuLink
                  href="#waitlist"
                  :class="navigationMenuTriggerStyle()"
                >
                  Join Our Waitlist
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
