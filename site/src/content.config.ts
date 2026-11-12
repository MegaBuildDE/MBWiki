import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

export const collections = {
	/** Eigene UI-Texte, z. B. die deutsche Suche (src/content/i18n/de.json). */
	i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema({
			extend: z.object({
				/** Seiten-Icon aus GitBook (Font-Awesome-Name), noch nicht angezeigt. */
				icon: z.string().optional(),
				/** Titelbild aus GitBook, als öffentliche Adresse (/assets/…). */
				cover: z.string().optional(),
				/** Quelldatei im Repo, z. B. sb/start.md. */
				source: z.string().optional(),
			}),
		}),
	}),
};
