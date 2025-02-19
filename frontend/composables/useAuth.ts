import type { z } from "zod";

import { useMutation, useQuery } from "@tanstack/vue-query";
import {
  type UserLoginSchema,
  RegisterCompanySchema,
  type UserRoleSchema,
  UserSchema,
  UserSchemaLogin,
  type RegisterInvitedUserSchema,
} from "~/utils/schemas/auth";

type UserRole = z.infer<typeof UserRoleSchema>;
export type InvitationOptions = {
  email: string;
  role: UserRole;
};

export const useAuthS = () => {
  async function handleCompanyCreation(
    companyCreationArgs: z.infer<typeof RegisterCompanySchema>
  ) {
    const data = await $fetch(`/account/register/`, {
      method: "POST",
      body: companyCreationArgs,
      baseURL: "http://localhost:8000",
    });

    return UserSchema.parse(data);
  }

  const { mutate, isPending: registerLoading } = useMutation({
    mutationFn: handleCompanyCreation,
  });

  async function registerCompany(
    companyCreationArgs: z.infer<typeof RegisterCompanySchema>
  ) {
    const { success, data: _companyCreationArgs } =
      RegisterCompanySchema.safeParse(companyCreationArgs);
    if (!success) {
      return;
    }
    mutate(_companyCreationArgs, {
      onError(e) {
        console.log("this is the error", e);
      },
      onSuccess(data) {
        setToken(data.auth_token);
      },
    });
  }

  async function handleLogin(loginArgs: z.infer<typeof UserLoginSchema>) {
    console.log("in the handlelogin");

    const data = await $fetch(`/account/login/`, {
      method: "POST",
      body: loginArgs,
      baseURL: "http://localhost:8000",
    });

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
            path: "/workspace/all-documents",
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

  async function handleUserInvite(invitationArgs: InvitationOptions) {
    let token = null;

    if (import.meta.server) {
      const cookies = useRequestHeaders(["cookie"]).cookie;
      const match = cookies?.match(/auth_token=([^;]+)/);
      token = match?.[1];
    }

    if (import.meta.client) {
      token = useCookie("auth_token").value;
    }

    const data = await $fetch(`/account/invite/`, {
      method: "POST",
      body: invitationArgs,
      baseURL: "http://localhost:8000",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });

    console.error(
      "data we got. We know this is incorrect because we should have the userInvitationSchema ",
      data
    );

    return UserSchema.parse(data);
  }

  const { mutate: userInviteMutate } = useMutation({
    mutationFn: handleUserInvite,
  });

  async function handleAcceptInvite(
    acceptInviteArgs: z.infer<typeof RegisterInvitedUserSchema>
  ) {
    await $fetch(`/account/accept-invite/`, {
      method: "POST",
      body: acceptInviteArgs,
      baseURL: "http://localhost:8000",
    });
  }

  const { mutate: acceptInviteMutate } = useMutation({
    mutationFn: handleAcceptInvite,
  });

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

  const loading = computed(() => loginLoading.value ?? registerLoading.value);
  // const error = computed(() => loginError.value ?? registerError.value);

  return {
    handleCheckAuth,
    getToken,
    registerCompany,
    login,
    invite: userInviteMutate,
    logout,
    acceptInvite: acceptInviteMutate,
    state: queryResponse.data,
    loading,
    ...queryResponse,
  };
};
