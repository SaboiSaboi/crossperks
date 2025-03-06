export default defineNuxtRouteMiddleware(async (to) => {
  const token = useCookie("auth_token");
  const publicRoutes = [
    "/signin",
    "/signup",
    "/resetpassword",
    "/registeruser",
    "/",
  ];
  const isPublicRoute = publicRoutes.includes(to.path);

  if (!token.value && !isPublicRoute) {
    return navigateTo("/signin");
  }
  if (token.value) {
    try {
      const isValid = () => {};
      if (!isValid) {
        token.value = null;
        return navigateTo("/signin");
      }
    } catch (error) {
      console.error("Token validation failed:", error);
      token.value = null;
      return navigateTo("/signin");
    }

    if (isPublicRoute) {
      const { handleCheckAuth } = useAuthS();

      const res = await handleCheckAuth();

      const user_type = res?.user.user_type;

      return navigateTo(`/${user_type}`);
    }
  }
});
