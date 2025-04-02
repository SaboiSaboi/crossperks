export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie("auth_token");

  const authRoutes = ["/signin", "/signup", "/signupbusiness"];
  const publicRoutes = [
    "/resetpassword",
    "/registeruser",
    "/businesses",
    "/business",
    "/",
  ];

  const isAuthRoute = authRoutes.includes(to.path);
  const isPublicRoute =
    publicRoutes.includes(to.path) ||
    to.path.startsWith("/business/claim-business/");

  if (!token.value) {
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

    if (to.path === "/customer" || to.path === "/customer/") {
      return navigateTo("/customer/dashboard");
    }

    if (isAuthRoute) {
      return navigateTo(`/${userType}`);
    }

    if (isPublicRoute) {
      return;
    }

    if (!isOnboarded && to.path !== `/${userType}/onboarding`) {
      return navigateTo(`/${userType}/onboarding`);
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
    if (to.path !== "/signin") {
      return navigateTo("/signin");
    }
  }
});
