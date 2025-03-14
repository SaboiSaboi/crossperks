import { defineStore } from "pinia";

interface Perk {
  title: string;
  description: string;
  total: number;
  remaining: number;
  isActive: boolean;
  redemptions: number;
}

export const usePerkStore = defineStore("perk", {
  state: () => ({
    perk: import.meta.client
      ? JSON.parse(localStorage.getItem("perk") || "null")
      : (null as Perk | null),
    user: null as any,
    isLoading: true,
    pastPerks: null as Perk[] | null,
  }),

  getters: {
    currentPerk: (state) => state.perk,
  },

  actions: {
    async getStorageKey() {
      if (!this.user) {
        const { handleCheckAuth } = useAuthS();
        this.user = await handleCheckAuth(); // Ensure user is set
      }

      return this.user.id ? `perk_${this.user.id}` : null;
    },

    async loadPerkFromDB() {
      try {
        if (!this.user) await this.getStorageKey(); // Ensure user is fetched

        const token = useCookie("auth_token");

        const response: any = await $fetch(
          "http://localhost:8000/account/perk/",
          {
            method: "GET",
            headers: {
              Authorization: `Token ${token.value}`,
            },
          }
        );

        return response.perk || null;
      } catch (error) {
        console.error(error);
      }
    },
    async loadPastPerksFromDB() {
      const token = useCookie("auth_token");
      this.isLoading = true;

      try {
        const response: any = await $fetch(
          "http://localhost:8000/account/past-perks/",
          {
            method: "GET",
            headers: {
              Authorization: `Token ${token.value}`,
            },
          }
        );
        this.pastPerks = response.perks || [];
      } catch (error) {
        console.error("Failed to fetch past perks:", error);
      }

      this.isLoading = false;
    },

    async loadPerk() {
      if (import.meta.client) {
        this.isLoading = true;

        const key = await this.getStorageKey();

        if (!key) {
          this.isLoading = false;
          return;
        }

        const storedPerk = localStorage.getItem(key);
        if (storedPerk) {
          this.perk = JSON.parse(storedPerk);
        } else {
          const perkFromDB = await this.loadPerkFromDB();
          if (perkFromDB) {
            this.setPerk(perkFromDB);
          }
        }
        this.isLoading = false;
      }
    },

    async setPerk(data: Perk) {
      console.log("setPerk function is running with data:", data); // ✅ Check if it runs

      const key = await this.getStorageKey();
      if (!key) {
        console.log("Storage key not found, exiting setPerk."); // ✅ Check if key exists
        return;
      }

      this.$patch((state) => {
        state.perk = data;
      });

      localStorage.setItem(key, JSON.stringify(data));
      console.log("Perk has been set in store and localStorage:", this.perk); // ✅ Confirm it's set
    },

    async clearPerk() {
      const key = await this.getStorageKey();
      if (key) {
        localStorage.removeItem(key);
      }
      this.perk = null;
    },

    async deletePerk() {
      await $fetch(`/api/perks/${this.user.id}`, { method: "DELETE" });
      this.clearPerk();
    },

    async initializeStore() {
      const { handleCheckAuth } = useAuthS();
      this.user = await handleCheckAuth();
      await this.loadPerk();
    },
  },
});
