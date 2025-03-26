export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie("auth_token");

  const authRoutes = ["/signin", "/signup"];
  const publicRoutes = [
    "/resetpassword",
    "/registeruser",
    "/businesses",
    "/business",
    "/",
  ];

  const onboardingRoutes = ["/customer/onboarding", "/business/onboarding"];

  const isAuthRoute = authRoutes.includes(to.path);
  const isPublicRoute =
    publicRoutes.includes(to.path) ||
    to.path.startsWith("/business/claim-business/");

  if (!token.value) {
    // ✅ Allow access to public routes when not signed in
    if (isPublicRoute || isAuthRoute) {
      return;
    }
    return navigateTo("/signin");
  }

  try {
    const { handleCheckAuth } = useAuthS();
    const res: any = await handleCheckAuth();

    if (!res || !res.user) {
      token.value = null;
      if (to.path !== "/signin") {
        return navigateTo("/signin");
      }
      return;
    }

    const perkStore = usePerkStore();
    perkStore.user = res.user;
    await perkStore.loadPerk();

    const userType = res.user.user_type;
    const isOnboarded = res.user.is_onboarded;

    // ❌ Block signed-in users from accessing auth pages (redirect them to their dashboard)
    if (isAuthRoute) {
      return navigateTo(`/${userType}`);
    }

    // ✅ Allow access to public pages for signed-in users
    if (isPublicRoute) {
      return;
    }

    // Redirect non-onboarded users to onboarding
    if (!isOnboarded && to.path !== `/${userType}/onboarding`) {
      return navigateTo(`/${userType}/onboarding`);
    }

    // Prevent customers from accessing business routes and vice versa
    if (to.path.startsWith("/customer") && userType !== "customer") {
      return navigateTo(`/${userType}`);
    }
    if (to.path.startsWith("/business") && userType !== "business") {
      return navigateTo(`/${userType}`);
    }
  } catch (error) {
    console.error("Auth check failed:", error);
    token.value = null;
    if (to.path !== "/signin") {
      return navigateTo("/signin");
    }
  }
});
