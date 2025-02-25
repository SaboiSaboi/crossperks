import type { z } from "zod";
import { useMutation, useQuery } from "@tanstack/vue-query";
import {
  type UserLoginSchema,
  RegisterUserSchema,
  UserSchema,
  UserSchemaLogin,
} from "~/utils/schemas/auth";

export const useAuthS = () => {
  // Step 1: Send Verification Code
  async function sendVerificationCode(
    userInfo: z.infer<typeof RegisterUserSchema>
  ) {
    const data = await $fetch(`/account/send-code/`, {
      method: "POST",
      body: userInfo,
      baseURL: "http://localhost:8000",
    });

    return data;
  }

  // Step 2: Verify the Code
  async function verifyEmailCode({
    email,
    code,
  }: {
    email: string;
    code: string;
  }) {
    const data = await $fetch(`/account/verify-code/`, {
      method: "POST",
      body: { email, code },
      baseURL: "http://localhost:8000",
    });

    return data;
  }

  // Step 3: Complete Registration (Set Password)
  async function completeUserRegistration({
    email,
    password,
  }: {
    email: string;
    password: string;
  }) {
    const data = await $fetch(`/account/complete-registration/`, {
      method: "POST",
      body: { email, password },
      baseURL: "http://localhost:8000",
    });

    return UserSchema.parse(data);
  }

  // Register User Mutation Logic
  const { mutate: sendCodeMutate } = useMutation({
    mutationFn: sendVerificationCode,
  });

  const { mutate: verifyCodeMutate } = useMutation({
    mutationFn: verifyEmailCode,
  });

  const { mutate: completeRegistrationMutate } = useMutation({
    mutationFn: completeUserRegistration,
  });

  async function registerBusiness(
    businessCreationArgs: z.infer<typeof RegisterUserSchema>
  ) {
    sendCodeMutate(businessCreationArgs, {
      onError(e) {
        console.log("Verification code sending failed:", e);
      },
      onSuccess(data) {
        console.log("Verification code sent successfully:", data);
      },
    });
  }

  async function registerCustomer(
    customerCreationArgs: z.infer<typeof RegisterUserSchema>
  ) {
    sendCodeMutate(customerCreationArgs, {
      onError(e) {
        console.log("Verification code sending failed:", e);
      },
      onSuccess(data) {
        console.log("Verification code sent successfully:", data);
      },
    });
  }

  // Handle Email Verification Code Submission
  async function verifyCode(email: string, code: string) {
    verifyCodeMutate(
      { email, code },
      {
        onError(e) {
          console.log("Code verification failed:", e);
        },
        onSuccess(data) {
          console.log("Email successfully verified:", data);
        },
      }
    );
  }

  // Handle Completing Registration by Setting Password
  async function completeRegistration(email: string, password: string) {
    completeRegistrationMutate(
      { email, password },
      {
        onError(e) {
          console.log("Registration completion failed:", e);
        },
        onSuccess(data) {
          console.log("Registration completed successfully:", data);
        },
      }
    );
  }

  async function handleLogin(loginArgs: z.infer<typeof UserLoginSchema>) {
    console.log("in the handlelogin");

    const data = await $fetch(`/account/login/`, {
      method: "POST",
      body: loginArgs,
      baseURL: "http://localhost:8000",
    });

    console.log("response", data);

    return UserSchemaLogin.parse(data);
  }

  const { mutate: loginMutate, isPending: loginLoading } = useMutation({
    mutationFn: handleLogin,
  });

  function login(loginArgs: z.infer<typeof UserLoginSchema>) {
    console.log("in the login:");
    loginMutate(loginArgs, {
      onError(e) {
        console.log("this is the error", e);
      },
      onSuccess(data) {
        setToken(data.auth_token);
        navigateTo(
          {
            path: "/customer",
          },
          {
            replace: true,
          }
        );
      },
    });
  }

  async function handleLogout() {
    await $fetch(`/account/logout/`, {
      method: "POST",
      baseURL: "http://localhost:8000",
      headers: {
        Authorization: `Token ${getToken()}`,
      },
    });

    return null;
  }

  const { mutate: logoutMutate } = useMutation({ mutationFn: handleLogout });

  function logout() {
    logoutMutate(undefined, {
      onSettled() {
        clearToken();
      },
      onSuccess() {
        navigateTo(
          {
            path: "/signin",
          },
          {
            replace: true,
          }
        );
      },
    });
  }

  function setToken(token: string) {
    document.cookie = `auth_token=${token};path=/`;
  }

  function getToken() {
    // const cookie = getCookie("cookie");
    // const cookies = useRequestHeaders(["cookie"]).cookie;
    const match = document.cookie.match(
      new RegExp("(^| )" + "auth_token" + "=([^;]+)")
    );

    // if (match) {
    //   match[2];
    // } else {
    //   console.log("No auth_token cookie found");
    //   return navigateTo("/signin");
    // }
    if (!match) {
      return navigateTo("/signin");
    }

    if (import.meta.server) {
      const cookies = useRequestHeaders(["cookie"]).cookie;
      const match = cookies?.match(/auth_token=([^;]+)/);

      if (!match) {
        return navigateTo("/signin");
      }
    }

    if (import.meta.client) {
      const token = useCookie("auth_token").value;
      if (!token) {
        return navigateTo("/signin");
      }
    }
    if (import.meta.client) {
      const match = document.cookie.match(
        new RegExp("(^| )" + "auth_token" + "=([^;]+)")
      );
      console.log("below the match");
      if (match) return match[2];
    }

    return null;
  }
  function clearToken() {
    document.cookie = "auth_token=; Max-Age=0; path=/";
  }

  async function handleCheckAuth() {
    let token = null;

    if (import.meta.server) {
      const cookies = useRequestHeaders(["cookie"]).cookie;
      const match = cookies?.match(/auth_token=([^;]+)/);
      token = match?.[1];
    }

    if (import.meta.client) {
      token = useCookie("auth_token").value;
    }

    if (token) {
      try {
        const userIs = await $fetch("http://localhost:8000/account/user", {
          headers: { Authorization: `Token ${token}` },
        });

        return UserSchema.parse(userIs);
      } catch (error) {
        console.error("Error fetching user foo:", error);
        return null;
      }
    }
    return null;
  }
  const queryResponse = useQuery({
    queryFn: handleCheckAuth,
    queryKey: ["user"],
  });

  return {
    registerBusiness,
    registerCustomer,
    verifyCode,
    completeRegistration,
    getToken,
    login,
    logout,
    handleCheckAuth,
    state: queryResponse.data,
    ...queryResponse,
  };
};
