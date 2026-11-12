// @ts-check
import fs from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// Beide Dateien schreibt scripts/convert.mjs aus SUMMARY.md und .gitbook.yaml.
const readGenerated = (name, fallback) => {
	try {
		return JSON.parse(fs.readFileSync(new URL(`./src/generated/${name}`, import.meta.url), 'utf8'));
	} catch {
		return fallback;
	}
};

export default defineConfig({
	site: 'https://wiki.megabuild.de',
	redirects: readGenerated('redirects.json', {}),
	integrations: [
		starlight({
			title: 'MegaBuild.de Wiki',
			description: 'Das offizielle Wiki zu MegaBuild.de – Custom Skyblock.',
			logo: { src: './src/assets/mb-logo.png', alt: 'MegaBuild.de' },
			favicon: '/favicon.png',
			defaultLocale: 'root',
			locales: {
				root: { label: 'Deutsch', lang: 'de' },
				en: { label: 'English', lang: 'en' },
			},
			social: [{ icon: 'discord', label: 'Discord', href: 'https://megabuild.de/dc/' }],
			sidebar: readGenerated('sidebar.json', []),
			customCss: ['./src/styles/mb.css'],
			head: [
				{ tag: 'script', attrs: { src: '/mb.js', defer: true } },
				{ tag: 'meta', attrs: { name: 'theme-color', content: '#170d29' } },
			],
			components: {
				ThemeProvider: './src/components/ThemeProvider.astro',
				ThemeSelect: './src/components/ThemeSelect.astro',
				SocialIcons: './src/components/SocialIcons.astro',
				Hero: './src/components/Hero.astro',
				PageTitle: './src/components/PageTitle.astro',
			},
			tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
			credits: false,
		}),
	],
});
