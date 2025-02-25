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

  return {
    registerBusiness,
    registerCustomer,
    verifyCode,
    completeRegistration,
  };
};
