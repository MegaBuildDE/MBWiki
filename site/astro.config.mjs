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
	// Auf der Test-Subdomain setzt der Server SITE_URL (siehe deploy/build-wiki.sh).
	site: process.env.SITE_URL || 'https://wiki.megabuild.de',
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
				// Symbol, wenn jemand das Wiki auf dem Handy zum Home-Bildschirm hinzufügt (512 px)
				{ tag: 'link', attrs: { rel: 'apple-touch-icon', href: '/favicon.png' } },
			],
			components: {
				ThemeProvider: './src/components/ThemeProvider.astro',
				ThemeSelect: './src/components/ThemeSelect.astro',
				SocialIcons: './src/components/SocialIcons.astro',
				Header: './src/components/Header.astro',
				LanguageSelect: './src/components/LanguageSelect.astro',
				Hero: './src/components/Hero.astro',
				PageTitle: './src/components/PageTitle.astro',
				MobileTableOfContents: './src/components/MobileTableOfContents.astro',
			},
			tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
			// Codeblöcke: abgerundet, dunkler Grund mit feinem Rand, passend zu Karten und Tabellen.
			expressiveCode: {
				styleOverrides: {
					borderRadius: '0.75rem',
					borderColor: 'rgba(211, 176, 255, 0.18)',
					codePaddingBlock: '0.85rem',
					codePaddingInline: '1.1rem',
				},
				customizeTheme: (theme) => {
					const bg = 'rgba(10, 5, 22, 0.55)';
					theme.styleOverrides.frames = {
						...theme.styleOverrides.frames,
						editorBackground: bg,
						terminalBackground: bg,
						editorActiveTabBackground: bg,
						tooltipSuccessBackground: '#a958ff',
						tooltipSuccessForeground: '#fff',
					};
					return theme;
				},
			},
			credits: false,
		}),
	],
});
