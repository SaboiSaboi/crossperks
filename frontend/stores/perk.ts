import { defineStore } from "pinia";

interface Perk {
  title: string;
  description: string;
  total: number;
  remaining: number;
  isActive: boolean;
  redemptions: number;
  created_at: string;
  id: number;
}

export const usePerkStore = defineStore("perk", {
  state: () => ({
    perk: null as Perk | null, // ✅ Prevent SSR issues
    user: null as any,
    isLoading: false,
    pastPerks: null as Perk[] | null,
  }),

  getters: {
    currentPerk: (state) => state.perk,
    hasPastPerks: (state) => state.pastPerks && state.pastPerks.length > 0, // ✅ New getter
  },

  actions: {
    async initializeStore() {
      this.isLoading = true;
      const { handleCheckAuth } = useAuthS();
      this.user = await handleCheckAuth();

      if (!this.user) {
        this.isLoading = false;
        return;
      }

      await Promise.all([this.loadPerk(), this.loadPastPerksFromDB()]);
      this.isLoading = false;
    },

    getStorageKey() {
      return this.user?.id ? `perk_${this.user.id}` : null;
    },

    getStorageKeyPastPerks() {
      return this.user?.id ? `pastPerks_${this.user.id}` : null;
    },

    async loadPerkFromDB() {
      try {
        if (!this.user) return null;
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
        console.error("Failed to load perk from DB:", error);
        return null;
      }
    },

    async loadPastPerksFromDB() {
      try {
        if (!this.user) return;
        const token = useCookie("auth_token");

        const response: any = await $fetch(
          "http://localhost:8000/account/past-perks/",
          {
            method: "GET",
            headers: {
              Authorization: `Token ${token.value}`,
            },
          }
        );

        this.pastPerks = response || [];
        this.setPastPerks(response);
      } catch (error) {
        console.error("Failed to fetch past perks:", error);
      }
    },

    async loadPerk() {
      if (import.meta.client) {
        this.isLoading = true;

        const key = this.getStorageKey();
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
      const key = this.getStorageKey();
      if (!key) {
        console.warn("Storage key not found, exiting setPerk.");
        return;
      }

      this.$patch((state) => {
        state.perk = data;
      });

      localStorage.setItem(key, JSON.stringify(data));
    },

    async setPastPerks(data: Perk[]) {
      const key = this.getStorageKeyPastPerks();
      if (!key) {
        console.warn("Storage key not found, exiting setPastPerks.");
        return;
      }

      this.$patch((state) => {
        state.pastPerks = data;
      });

      localStorage.setItem(key, JSON.stringify(data));
    },

    async clearPerk() {
      const perkKey = this.getStorageKey();
      const pastPerksKey = this.getStorageKeyPastPerks();

      if (perkKey) localStorage.removeItem(perkKey);
      if (pastPerksKey) localStorage.removeItem(pastPerksKey);

      this.perk = null;
      this.pastPerks = null;
    },

    async deletePerk() {
      if (!this.user) return;
      await $fetch(`/api/perks/${this.user.id}`, { method: "DELETE" });
      this.clearPerk();
    },
  },
});
