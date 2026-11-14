// robots.txt mit der Sitemap der gerade gebauten Adresse (site in astro.config.mjs).
// Für eine Test-Subdomain steht in deploy/nginx-wiki.conf.example, wie nginx sie stattdessen sperrt.
import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) =>
	new Response(`User-agent: *\nAllow: /\n\nSitemap: ${new URL('sitemap-index.xml', site).href}\n`, {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
