import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,markdown}', base: './_posts' }),
  schema: z.object({
    title: z.string().optional(),
    date: z.union([z.date(), z.string()]).optional(),
    layout: z.string().optional(),
    tags: z.union([z.array(z.string()), z.string()]).optional(),
    categories: z.union([z.array(z.string()), z.string()]).optional(),
  }),
});

export const collections = { blog };
