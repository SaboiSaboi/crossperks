<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const { handleCheckAuth } = useAuthS();

const userName = ref("User");
const userEmail = ref("");
const preferredIdentifiers = ref<string[]>([]);
const selectedIdentifiers = ref<number[]>([]);
const allIdentifiers = ref<{ id: number; name: string }[]>([]);
const joinedDate = ref("");
const editing = ref(false);
const editingName = ref(false);
const newName = ref("");

const token = useCookie("auth_token");

const fetchIdentifiers = async () => {
  try {
    const response: any = await $fetch(
      "http://localhost:8000/account/identifiers/"
    );
    allIdentifiers.value = response;
  } catch (err) {
    console.error("Failed to fetch identifiers", err);
  }
};

const updateName = async () => {
  try {
    await $fetch("http://localhost:8000/account/update-name/", {
      method: "PUT",
      headers: {
        Authorization: `Token ${token.value}`,
      },
      body: {
        name: newName.value,
      },
    });
    userName.value = newName.value;
    editingName.value = false;
  } catch (err) {
    console.error("Failed to update name", err);
  }
};

const updatePreferences = async () => {
  try {
    await $fetch("http://localhost:8000/account/customer-onboarding/", {
      method: "PUT",
      headers: {
        Authorization: `Token ${token.value}`,
      },
      body: {
        preferred_identifiers: selectedIdentifiers.value,
      },
    });

    preferredIdentifiers.value = allIdentifiers.value
      .filter((id) => selectedIdentifiers.value.includes(id.id))
      .map((id) => id.name);

    editing.value = false;
  } catch (err) {
    console.error("Failed to update preferences", err);
  }
};

onMounted(async () => {
  try {
    const userData: any = await handleCheckAuth();

    userName.value = userData.user?.name || "User";
    newName.value = userName.value;
    userEmail.value = userData.user?.email || "";
    preferredIdentifiers.value =
      userData.customer_profile?.preferred_identifiers || [];

    joinedDate.value = new Date(
      userData.user?.created_at || Date.now()
    ).toISOString();

    await fetchIdentifiers();

    // Pre-fill selected identifiers (if any)
    selectedIdentifiers.value = allIdentifiers.value
      .filter((id) => preferredIdentifiers.value.includes(id.name))
      .map((id) => id.id);
  } catch (error) {
    console.error("Failed to fetch user data:", error);
  }
});

const formattedDate = computed(() => {
  return new Date(joinedDate.value).toLocaleDateString();
});
</script>

<template>
  <div>
    <div class="bg-gray-950"><HeaderProfilePage /></div>

    <div
      class="max-w-2xl mx-auto py-4 h-dvh flex flex-col items-center justify-center"
    >
      <Card class="w-full px-8 md:px-32 flex flex-col justify-center py-8">
        <CardHeader class="border-b pb-4">
          <CardTitle class="text-xl font-semibold">Profile</CardTitle>
        </CardHeader>

        <CardContent class="mt-4">
          <div class="space-y-4">
            <div>
              <span
                class="text-sm text-gray-500 flex justify-between items-center"
              >
                Name
                <button
                  class="text-xs underline text-blue-600"
                  @click="editingName = !editingName"
                >
                  {{ editingName ? "Cancel" : "Edit" }}
                </button>
              </span>

              <div v-if="editingName" class="mt-2 flex items-center gap-2">
                <input
                  v-model="newName"
                  type="text"
                  class="border border-gray-300 px-2 py-1 rounded text-sm w-full"
                />
                <Button class="text-sm" @click="updateName">Save</Button>
              </div>

              <p v-else class="text-lg mt-1">{{ userName }}</p>
            </div>

            <div>
              <span class="text-sm text-gray-500">Email</span>
              <p class="text-lg">{{ userEmail }}</p>
            </div>

            <div>
              <span
                class="text-sm text-gray-500 flex justify-between items-center"
              >
                Favorite business types
                <button
                  class="text-xs underline text-blue-600"
                  @click="editing = !editing"
                >
                  {{ editing ? "Cancel" : "Edit" }}
                </button>
              </span>

              <div v-if="editing" class="mt-2 space-y-2">
                <div class="grid grid-cols-2 gap-2">
                  <label
                    v-for="identifier in allIdentifiers"
                    :key="identifier.id"
                    class="flex items-center gap-2"
                  >
                    <input
                      type="checkbox"
                      :value="identifier.id"
                      v-model="selectedIdentifiers"
                      class="rounded border-gray-300"
                    />
                    <span>{{ identifier.name }}</span>
                  </label>
                </div>

                <Button
                  class="mt-4"
                  :disabled="!selectedIdentifiers.length"
                  @click="updatePreferences"
                >
                  Save Preferences
                </Button>
              </div>

              <div v-else>
                <p class="text-lg mt-1">
                  <span v-if="preferredIdentifiers.length">
                    {{ preferredIdentifiers.join(", ") }}
                  </span>
                  <span v-else class="italic text-gray-400">None selected</span>
                </p>
              </div>
            </div>
          </div>
        </CardContent>

        <CardFooter class="text-sm text-muted-foreground border-t pt-4">
          <p>Joined on {{ formattedDate }}</p>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>
