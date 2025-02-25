<template>
  <main class="grow">
    Customer home
    <Button @click="logout">Log out</Button>
  </main>
</template>

<script setup lang="ts">
const { logout } = useAuthS();
</script>
