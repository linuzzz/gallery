import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const photos = defineCollection({
	loader: glob({ base: './src/content/photos', pattern: '**/*.md' }),
	schema: z.object({
		title: z.string(),
		location: z.string().nullable().optional(),
		tags: z.array(z.string()).min(1),
		image: z.string().url(),
		description: z.string().nullable().optional(),
		datetime: z.coerce.date(),
	}),
});

export const collections = { photos };
