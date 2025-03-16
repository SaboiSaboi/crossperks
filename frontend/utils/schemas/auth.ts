import z from "zod";

export const UserRoleSchema = z.enum(["admin", "staff"]);

export const UserSchema = z.object({
  message: z.string(),
  user: z.object({
    id: z.number(),
    email: z.string().email(),
    user_type: z.string(),
  }),
  auth_token: z.string(),
});

export const UserSchemaLogin = z.object({
  message: z.string(),
  user: z.object({
    id: z.number(),
    email: z.string().email(),
    name: z.string(),
    user_type: z.string(),
    onboarded: z.boolean(),
  }),
  auth_token: z.string(),
});

export const RegisterUserSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  password: z.string().min(8, "You need at least 8 characters."),
  user_type: z.string(),
});

export const UserLoginSchema = z.object({
  email: z.string().email(),
  password: z.string(),
});
