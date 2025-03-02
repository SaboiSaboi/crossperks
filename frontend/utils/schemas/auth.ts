import z from "zod";

export const CustomDocumentSchema = z
  .object({
    id: z.number(),
    title: z.string(),
    description: z.string(),
    created_by: z.number(),
    company: z.number(),
    created_at: z.string(),
    updated_at: z.string(),
    // content: z.string().optional(),
    // content: z.array(
    //   z.object({
    //     order: z.number(),
    //     value: z.string(),
    //     kb: z.string(),
    //   })
    // ),
  })
  .transform((x) => ({
    ...x,
    user_id: `${x.created_by}`,
    company_id: `${x.company}`,
  }));

export const CustomDocumentSchemas = z.object({
  customDocuments: z.array(CustomDocumentSchema),
});
export type CustomDocument = z.infer<typeof CustomDocumentSchema>;

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
