import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const news = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/news' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    wpId: z.number().optional(),
    tags: z.array(z.string()).default([]),
    categories: z.array(z.string()).default([]),
    translation: z.string().optional(),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/pages' }),
  schema: z.object({
    title: z.string(),
    wpId: z.number().optional(),
    modified: z.coerce.date().optional(),
    order: z.number().default(0),
    // journal covers shown as a click-to-enlarge grid above the page body
    covers: z.array(z.object({ src: z.string(), thumb: z.string(), alt: z.string() })).default([]),
  }),
});

export const collections = { news, pages };
