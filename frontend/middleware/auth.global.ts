// export default defineNuxtRouteMiddleware(async (to) => {
//   const token = useCookie("auth_token");

//   const publicRoutes = [
//     "/signin",
//     "/signup",
//     "/resetpassword",
//     "/registeruser",
//     "/",
//   ];

//   const onboardingRoutes = ["/customer/onboarding", "/business/onboarding"];

//   const isPublicRoute =
//     publicRoutes.includes(to.path) ||
//     to.path.startsWith("/business/claim-business/");

//   if (!token.value) {
//     if (!isPublicRoute) return navigateTo("/signin");
//     return;
//   }

//   try {
//     const { handleCheckAuth } = useAuthS();
//     const res: any = await handleCheckAuth();

//     if (!res || !res.user) {
//       token.value = null;
//       return navigateTo("/signin");
//     }

//     console.log("the res", res);

//     const perkStore = usePerkStore();
//     // perkStore.user = res.user; // Store user in Pinia for consistency
//     await perkStore.loadPerk(); // ✅ Load perk from DB/localStorage

//     const userType = res.user.user_type;
//     const isOnboarded = res.user.is_onboarded;

//     // Redirect users who haven't onboarded, but only if they're NOT already on onboarding route
//     if (!isOnboarded && !onboardingRoutes.includes(to.path)) {
//       return navigateTo(`/${userType}/onboarding`);
//     }

//     // Redirect authenticated users away from public routes
//     if (isPublicRoute) {
//       return navigateTo(`/${userType}`);
//     }

//     // Protect role-specific routes
//     if (to.path.startsWith("/customer") && userType !== "customer") {
//       return navigateTo(`/${userType}`);
//     }
//     if (to.path.startsWith("/business") && userType !== "business") {
//       return navigateTo(`/${userType}`);
//     }

//     // User has proper role and route, allow access
//   } catch (error) {
//     console.error("Auth check failed:", error);
//     token.value = null;
//     return navigateTo("/signin");
//   }
// });

export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie("auth_token");

  const publicRoutes = [
    "/signin",
    "/signup",
    "/resetpassword",
    "/registeruser",
    "/",
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

    // console.log("the res", res);

    const perkStore = usePerkStore();
    perkStore.user = res.user; // ✅ Set user in Pinia before loading perks
    await perkStore.loadPerk(); // ✅ Load perk from DB/localStorage

    const userType = res.user.user_type;
    const isOnboarded = res.user.is_onboarded;

    // Redirect users who haven't onboarded, but only if they're NOT already on onboarding route
    if (!isOnboarded && !onboardingRoutes.includes(to.path)) {
      return navigateTo(`/${userType}/onboarding`);
    }

    // Redirect authenticated users away from public routes
    if (isPublicRoute) {
      return navigateTo(`/${userType}`);
    }

    // Protect role-specific routes
    if (to.path.startsWith("/customer") && userType !== "customer") {
      return navigateTo(`/${userType}`);
    }
    if (to.path.startsWith("/business") && userType !== "business") {
      return navigateTo(`/${userType}`);
    }

    // User has proper role and route, allow access
  } catch (error) {
    console.error("Auth check failed:", error);
    token.value = null;
    return navigateTo("/signin");
  }
});
