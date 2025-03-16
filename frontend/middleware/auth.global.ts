export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie("auth_token");

  const publicRoutes = [
    "/signin",
    "/signup",
    "/resetpassword",
    "/registeruser",
    "/",
    "/businesses",
  ];

  const onboardingRoutes = ["/customer/onboarding", "/business/onboarding"];

  const isPublicRoute =
    publicRoutes.includes(to.path) ||
    to.path.startsWith("/business/claim-business/");

  if (!token.value) {
    if (!isPublicRoute) return navigateTo("/signin");
    return;
  }

  try {
    const { handleCheckAuth } = useAuthS();
    const res: any = await handleCheckAuth();

    if (!res || !res.user) {
      token.value = null;
      return navigateTo("/signin");
    }

    const perkStore = usePerkStore();
    perkStore.user = res.user;
    await perkStore.loadPerk();

    const userType = res.user.user_type;
    const isOnboarded = res.user.is_onboarded;

    if (!isOnboarded && !onboardingRoutes.includes(to.path)) {
      return navigateTo(`/${userType}/onboarding`);
    }

    if (isPublicRoute) {
      return navigateTo(`/${userType}`);
    }

    if (to.path.startsWith("/customer") && userType !== "customer") {
      return navigateTo(`/${userType}`);
    }
    if (to.path.startsWith("/business") && userType !== "business") {
      return navigateTo(`/${userType}`);
    }
  } catch (error) {
    console.error("Auth check failed:", error);
    token.value = null;
    return navigateTo("/signin");
  }
});
