// robots.txt mit der Sitemap der gerade gebauten Adresse (site in astro.config.mjs).
// Auf der Test-Subdomain liefert nginx stattdessen eine sperrende robots.txt aus (deploy/nginx-wiki.conf.example).
import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) =>
	new Response(`User-agent: *\nAllow: /\n\nSitemap: ${new URL('sitemap-index.xml', site).href}\n`, {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
