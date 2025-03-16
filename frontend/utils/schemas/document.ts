import { z } from "zod";

export const CachedDocumentSectionSchema = z.object({
  title: z.string(),
  content: z.string(),
  kb_entry_references: z.array(z.number()),
});

export const CachedDocumentSchema = z.object({
  user_role: z.string(),
  content: z.array(CachedDocumentSectionSchema),
  version: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const CachedDocumentResponseSchema = z.object({
  data: z.array(CachedDocumentSchema),
});

export const DocumentDataSections = z.object({
  title: z.string(),
  content: z.string(),
  source: z.string(),
});

export const DocumentDataCompanyPositions = z.object({
  id: z.number(),
  name: z.string(),
  company: z.number(),
  created_at: z.string(),
});

export const DocumentDataSchema = z.object({
  title: z.string(),
  description: z.string(),
  sections: z.array(DocumentDataSections),
  company_positions: z.array(DocumentDataCompanyPositions),
});

export const DocumentNewlyCreatedSchema = z.array(
  z.object({
    id: z.number(),
    title: z.string(),
    description: z.string(),
    created_by: z.number(),
    company: z.number(),
    created_at: z.string().date(),
    updated_at: z.string().date(),
  })
);

export const KbEntryResSchema = z.object({
  id: z.number(),
  title: z.string(),
  content: z.string(),
  authorName: z.string(),
  authorEmail: z.string(),
});
