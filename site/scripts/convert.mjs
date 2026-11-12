#!/usr/bin/env node
// Baut aus den GitBook-Markdown-Dateien des Repos die Inhalte für die Starlight-Seite.
//
// Quelle bleibt das GitBook-Format im Repo-Root (SUMMARY.md, README.md, ag/, sb/, en/ …),
// damit GitBook und die neue Seite während der Umstellung parallel laufen können.
// Erzeugt (alles gitignored):
//   src/content/docs/**.md     Seiten mit Starlight-Frontmatter
//   src/generated/sidebar.json Navigation aus SUMMARY.md
//   src/generated/redirects.json alte Adressen -> neue Adressen
//   public/assets/             Kopie von .gitbook/assets
//
// Aufruf: node scripts/convert.mjs   (läuft automatisch vor `npm run dev` / `npm run build`)

import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import YAML from 'yaml';

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REPO = path.resolve(SITE, '..');
const OUT_DOCS = path.join(SITE, 'src/content/docs');
const OUT_GEN = path.join(SITE, 'src/generated');
const OUT_ASSETS = path.join(SITE, 'public/assets');

const localeMap = JSON.parse(fs.readFileSync(path.join(SITE, 'locale-map.json'), 'utf8'));

// Startseite: Schaltflächen im Kopfbereich (Hero). Rest kommt aus README.md / en/welcome.md.
const HOME_ACTIONS = {
	de: [
		{ text: 'Erste Schritte', link: '/sb/start/', icon: 'right-arrow' },
		{ text: 'Verbinden', link: '/ag/join/', variant: 'secondary' },
	],
	en: [
		{ text: 'Getting started', link: '/en/sb/start/', icon: 'right-arrow' },
		{ text: 'How to join', link: '/en/ag/join/', variant: 'secondary' },
	],
};

const HINT_TYPES = { info: 'note', success: 'tip', warning: 'caution', danger: 'danger' };
const VIDEO_EXT = /\.(mp4|webm|mov)$/i;

const warnings = [];
const warn = (msg) => warnings.push(msg);

// ---------------------------------------------------------------------------
// 1. SUMMARY.md lesen
// ---------------------------------------------------------------------------

function parseSummary() {
	const text = fs.readFileSync(path.join(REPO, 'SUMMARY.md'), 'utf8');
	const groups = [];
	let group = null;
	for (const line of text.split('\n')) {
		const h = line.match(/^##\s+(.+?)\s*(<a\b.*)?$/);
		if (h) {
			group = { label: h[1].trim(), items: [] };
			groups.push(group);
			continue;
		}
		const item = line.match(/^(\s*)[*-]\s+\[([^\]]*)\]\(([^)]+)\)/);
		if (item && group) {
			const depth = Math.floor(item[1].replace(/\t/g, '  ').length / 2);
			const entry = { label: item[2], src: decodeURI(item[3]), children: [] };
			if (depth > 0 && group.items.length) group.items.at(-1).children.push(entry);
			else group.items.push(entry);
		}
	}
	return groups;
}

// ---------------------------------------------------------------------------
// 2. Seiten-Index: Quelle -> Ziel-Slug, Titel, Beschreibung
// ---------------------------------------------------------------------------

const deSlug = (src) => (src === 'README.md' ? 'index' : src.replace(/\.md$/, ''));
const urlOf = (slug) => (slug === 'index' ? '/' : slug.endsWith('/index') ? `/${slug.slice(0, -6)}/` : `/${slug}/`);

function splitFrontmatter(raw) {
	const m = raw.match(/^---\n([\s\S]*?)\n---\n?/);
	if (!m) return { data: {}, body: raw };
	return { data: YAML.parse(m[1]) ?? {}, body: raw.slice(m[0].length) };
}

function extractTitle(body, fallback) {
	const m = body.match(/^#\s+(.+?)\s*#*\s*$/m);
	if (!m) return { title: fallback, body };
	const before = body.slice(0, m.index);
	// Nur die erste H1 am Seitenanfang wird zum Titel (wie bei GitBook).
	if (before.trim() !== '') return { title: fallback, body };
	return { title: m[1].replace(/\\([*_`])/g, '$1'), body: body.slice(m.index + m[0].length) };
}

function gitDates() {
	// Letzte Änderung je Datei aus einem einzigen git-Aufruf.
	const dates = new Map();
	try {
		const log = execFileSync(
			'git',
			['-c', 'safe.directory=*', 'log', '--format=@%cI', '--name-only', '--', '*.md'],
			{ cwd: REPO, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'ignore'] },
		);
		let current = null;
		for (const line of log.split('\n')) {
			if (line.startsWith('@')) current = line.slice(1);
			else if (line && current && !dates.has(line)) dates.set(line, current);
		}
	} catch {
		warn('git nicht verfügbar – Seiten ohne "Zuletzt aktualisiert"');
	}
	return dates;
}

function buildIndex(groups) {
	const pages = new Map(); // src -> page
	const enToDe = localeMap.pages ?? {};
	const deSources = new Set();
	for (const g of groups) for (const it of flatten(g.items)) if (!it.src.startsWith('en/')) deSources.add(it.src);

	const add = (src, locale) => {
		const file = path.join(REPO, src);
		if (!fs.existsSync(file)) {
			warn(`SUMMARY.md verweist auf fehlende Datei ${src}`);
			return;
		}
		let slug;
		if (locale === 'en') {
			let de = enToDe[src];
			if (!de) {
				const guess = [...deSources].find((d) => path.basename(d) === path.basename(src));
				if (guess) de = guess;
				warn(
					de
						? `${src}: nicht in locale-map.json, per Dateiname ${de} zugeordnet`
						: `${src}: keine deutsche Seite zugeordnet (locale-map.json) – kein Sprachwechsel möglich`,
				);
			}
			slug = de ? `en/${deSlug(de)}` : src.replace(/\.md$/, '');
		} else {
			slug = deSlug(src);
		}
		const { data, body } = splitFrontmatter(fs.readFileSync(file, 'utf8'));
		const { title } = extractTitle(body, path.basename(src, '.md'));
		pages.set(src, { src, slug, url: urlOf(slug), locale, title, description: data.description ?? '' });
	};

	for (const g of groups) {
		for (const it of flatten(g.items)) add(it.src, it.src.startsWith('en/') ? 'en' : 'de');
	}
	return pages;
}

function flatten(items) {
	return items.flatMap((it) => [it, ...flatten(it.children)]);
}

// ---------------------------------------------------------------------------
// 3. Inhalt umwandeln
// ---------------------------------------------------------------------------

const esc = (s) =>
	String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function resolveTarget(fromSrc, target) {
	// Relativer Pfad -> Repo-Pfad (ohne führendes ./)
	const clean = decodeURI(target.replace(/^<|>$/g, ''));
	return path.posix.normalize(path.posix.join(path.posix.dirname(fromSrc), clean));
}

function linkFor(pages, fromSrc, target, anchor = '') {
	const repoPath = resolveTarget(fromSrc, target);
	const page = pages.get(repoPath);
	if (!page) {
		warn(`${fromSrc}: Link auf ${repoPath} – Seite ist nicht in SUMMARY.md`);
		return `/${repoPath.replace(/\.md$/, '').replace(/(^|\/)README$/, '')}/${anchor}`.replace(/\/+/g, '/');
	}
	return page.url + anchor;
}

const assetUrl = (p) => '/assets/' + p.replace(/^(?:\.\.\/|\.\/)*\.gitbook\/assets\//, '');

function card({ href, title, desc = '', kind = 'page', attrs = '' }) {
	return (
		`<div class="mb-cards"><a class="mb-card mb-card--${kind}" href="${esc(href)}"${attrs}>` +
		`<span class="mb-card__title">${esc(title)}</span>` +
		(desc ? `<span class="mb-card__desc">${esc(desc)}</span>` : '') +
		`</a></div>`
	);
}

function videoBlock(src, caption, poster) {
	return [
		'',
		`<figure class="mb-video">`,
		`<video controls preload="metadata" playsinline${poster ? ` poster="${esc(poster)}"` : ''} src="${esc(src)}"></video>`,
		caption ? `<figcaption>\n\n${caption.trim()}\n\n</figcaption>` : '',
		`</figure>`,
		'',
	]
		.filter((l) => l !== null)
		.join('\n');
}

function convertBody(src, body, pages) {
	// Code-Blöcke und Inline-Code schützen, damit dort nichts umgeschrieben wird.
	const stash = [];
	const keep = (s) => `\u0000${stash.push(s) - 1}\u0000`;
	let t = body.replace(/^(```|~~~)[^\n]*\n[\s\S]*?^\1\s*$/gm, keep).replace(/`[^`\n]+`/g, keep);

	// Asset-Pfade (.gitbook/assets) -> /assets
	t = t.replace(/(?:\.\.\/|\.\/)*\.gitbook\/assets\/[^\s"')>]+/g, (m) => assetUrl(m));

	// Video-Standbild + Datei-Block -> ein Video-Player mit Standbild
	t = t.replace(
		/<figure><img src="([^"]+\.(?:jpe?g|png|webp))"[^>]*>(?:<figcaption>[\s\S]*?<\/figcaption>)?<\/figure>\s*\{% file src="([^"]+)" %\}([\s\S]*?)\{% endfile %\}/g,
		(m, poster, file, caption) => (VIDEO_EXT.test(file) ? videoBlock(file, caption, poster) : m),
	);

	// Datei-Blöcke
	t = t.replace(/\{% file src="([^"]+)"[^%]*%\}([\s\S]*?)\{% endfile %\}/g, (m, file, caption) => {
		if (VIDEO_EXT.test(file)) return videoBlock(file, caption);
		const name = decodeURI(file.split('/').pop());
		return '\n' + card({ href: file, title: name, desc: caption.trim().replace(/\*\*/g, ''), kind: 'file', attrs: ' download' }) + '\n';
	});
	t = t.replace(/\{% file src="([^"]+)"[^%]*%\}/g, (m, file) =>
		VIDEO_EXT.test(file) ? videoBlock(file) : '\n' + card({ href: file, title: decodeURI(file.split('/').pop()), kind: 'file', attrs: ' download' }) + '\n',
	);

	// Einbettungen (mit oder ohne Abschluss)
	t = t.replace(
		/\{% embed url="([^"]+)"[^%]*%\}(?:\n((?:(?!\{%)[\s\S])*?)\n?\{% endembed %\})?/g,
		(m, url, caption = '') => {
			if (VIDEO_EXT.test(url)) return videoBlock(url, caption);
			const yt = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})/);
			if (yt) {
				return `\n<div class="mb-embed"><iframe src="https://www.youtube-nocookie.com/embed/${yt[1]}" title="YouTube" loading="lazy" allowfullscreen></iframe></div>\n`;
			}
			const u = new URL(url);
			const title = (u.host + u.pathname).replace(/\/$/, '');
			return '\n' + card({ href: url, title, desc: caption.trim(), kind: 'external', attrs: ' rel="noopener"' }) + '\n';
		},
	);

	// Seitenkarten (content-ref)
	t = t.replace(/\{% content-ref url="([^"]+)" %\}[\s\S]*?\{% endcontent-ref %\}/g, (m, url) => {
		const [target, anchor = ''] = url.split('#');
		const page = pages.get(resolveTarget(src, target));
		const href = linkFor(pages, src, target, anchor ? `#${anchor}` : '');
		return '\n' + card({ href, title: page?.title ?? target, desc: page?.description ?? '' }) + '\n';
	});

	// Hinweise -> Starlight-Asides
	t = t.replace(/\{% hint style="(\w+)" %\}/g, (m, style) => `\n:::${HINT_TYPES[style] ?? 'note'}\n`);
	t = t.replace(/\{% endhint %\}/g, '\n:::\n');

	// Schritte
	t = t.replace(/\{% stepper %\}/g, '\n<ol class="mb-steps">\n');
	t = t.replace(/\{% step %\}/g, '\n<li>\n\n');
	t = t.replace(/\{% endstep %\}/g, '\n\n</li>\n');
	t = t.replace(/\{% endstepper %\}/g, '\n</ol>\n');

	// Tabs
	t = t.replace(/\{% tabs %\}/g, '\n<div class="mb-tabs">\n');
	t = t.replace(/\{% tab title="([^"]*)" %\}/g, (m, title) => `\n<div class="mb-tab" data-label="${esc(title)}">\n\n`);
	t = t.replace(/\{% endtab %\}/g, '\n\n</div>\n');
	t = t.replace(/\{% endtabs %\}/g, '\n</div>\n');

	// Spalten
	t = t.replace(/\{% columns[^%]*%\}/g, '\n<div class="mb-columns">\n');
	t = t.replace(/\{% column[^%]*%\}/g, '\n<div class="mb-column">\n\n');
	t = t.replace(/\{% endcolumn %\}/g, '\n\n</div>\n');
	t = t.replace(/\{% endcolumns %\}/g, '\n</div>\n');

	const leftover = t.match(/\{%\s*[a-z-]+/g);
	if (leftover) warn(`${src}: unbekannte GitBook-Blöcke: ${[...new Set(leftover)].join(', ')}`);

	// Links auf .md-Dateien -> Seitenadressen
	t = t.replace(/\]\((?!https?:|mailto:|#)(<[^>]+>|[^)\s]+?\.md)(#[^)\s]*)?\)/g, (m, target, anchor = '') =>
		`](${linkFor(pages, src, target, anchor)})`,
	);
	t = t.replace(/href="(?!https?:|mailto:|#)([^"]+?\.md)(#[^"]*)?"/g, (m, target, anchor = '') =>
		`href="${linkFor(pages, src, target, anchor)}"`,
	);

	// Aufeinanderfolgende Karten zu einem Raster zusammenfassen
	t = t.replace(/<\/a><\/div>\s*\n\s*<div class="mb-cards">/g, '</a>');

	// Mehr als zwei Leerzeilen zusammenziehen
	t = t.replace(/\n{3,}/g, '\n\n');

	return t.replace(/\u0000(\d+)\u0000/g, (m, i) => stash[Number(i)]);
}

// ---------------------------------------------------------------------------
// 4. Schreiben
// ---------------------------------------------------------------------------

function writePage(page, pages, dates) {
	const raw = fs.readFileSync(path.join(REPO, page.src), 'utf8');
	const { data, body: withTitle } = splitFrontmatter(raw);
	const { body } = extractTitle(withTitle, page.title);

	const fm = { title: page.title };
	if (data.description) fm.description = String(data.description).trim();
	if (data.icon) fm.icon = data.icon;
	if (data.cover) fm.cover = assetUrl(data.cover);
	if (data.hidden) fm.pagefind = false;
	const updated = dates.get(page.src);
	if (updated) fm.lastUpdated = updated.slice(0, 10);
	fm.source = page.src;

	if (page.slug === 'index' || page.slug === 'en/index') {
		fm.template = 'splash';
		fm.hero = {
			title: page.title,
			tagline: fm.description,
			actions: HOME_ACTIONS[page.locale],
		};
		fm.tableOfContents = false;
	}

	const out = path.join(OUT_DOCS, `${page.slug}.md`);
	fs.mkdirSync(path.dirname(out), { recursive: true });
	fs.writeFileSync(out, `---\n${YAML.stringify(fm, { lineWidth: 0 })}---\n\n${convertBody(page.src, body, pages).trim()}\n`);
}

function buildSidebar(groups, pages) {
	const enLabelForDe = new Map();
	for (const [en, de] of Object.entries(localeMap.pages ?? {})) {
		const enEntry = groups.flatMap((g) => flatten(g.items)).find((i) => i.src === en);
		if (enEntry) enLabelForDe.set(de, enEntry.label);
	}
	const toItem = (it) => {
		const page = pages.get(it.src);
		if (!page) return null;
		const hidden = isHidden(it.src);
		const en = enLabelForDe.get(it.src);
		const link = { slug: page.slug, label: it.label, ...(en ? { translations: { en } } : {}) };
		const children = it.children.map(toItem).filter(Boolean);
		if (hidden && !children.length) return null;
		if (!children.length) return link;
		return { label: it.label, collapsed: true, items: hidden ? children : [link, ...children] };
	};
	return groups
		.filter((g) => !g.items.every((i) => i.src.startsWith('en/'))) // englische Gruppe -> über Sprachwahl
		.map((g) => ({
			label: g.label,
			...(localeMap.groups?.[g.label] ? { translations: { en: localeMap.groups[g.label] } } : {}),
			items: g.items.map(toItem).filter(Boolean),
		}))
		.filter((g) => g.items.length);
}

const hiddenCache = new Map();
function isHidden(src) {
	if (!hiddenCache.has(src)) {
		const { data } = splitFrontmatter(fs.readFileSync(path.join(REPO, src), 'utf8'));
		hiddenCache.set(src, Boolean(data.hidden));
	}
	return hiddenCache.get(src);
}

function buildRedirects(pages) {
	const redirects = {};
	// Alte englische Adressen (GitBook: /en/island) -> neue (/en/sb/insel/)
	for (const p of pages.values()) {
		const old = '/' + p.src.replace(/\.md$/, '');
		if (p.locale === 'en' && old !== p.url.replace(/\/$/, '')) redirects[old] = p.url;
	}
	// Weiterleitungen aus .gitbook.yaml
	const gb = fs.existsSync(path.join(REPO, '.gitbook.yaml'))
		? YAML.parse(fs.readFileSync(path.join(REPO, '.gitbook.yaml'), 'utf8'))
		: {};
	for (const [from, to] of Object.entries(gb?.redirects ?? {})) {
		const target = pages.get(to);
		if (target) redirects['/' + from.replace(/^\/|\/$/g, '')] = target.url;
		else warn(`.gitbook.yaml: Weiterleitung ${from} -> ${to}, Ziel nicht gefunden`);
	}
	return redirects;
}

function copyAssets() {
	fs.rmSync(OUT_ASSETS, { recursive: true, force: true });
	fs.cpSync(path.join(REPO, '.gitbook/assets'), OUT_ASSETS, {
		recursive: true,
		filter: (s) => !path.basename(s).startsWith('.DS_Store'),
	});
}

// ---------------------------------------------------------------------------

const groups = parseSummary();
const pages = buildIndex(groups);
const dates = gitDates();

fs.rmSync(OUT_DOCS, { recursive: true, force: true });
for (const page of pages.values()) writePage(page, pages, dates);

// Eine 404-Seite für die ganze Seite (Starlight sucht den Eintrag „404“), zweisprachig.
fs.writeFileSync(
	path.join(OUT_DOCS, '404.md'),
	`---\n${YAML.stringify(
		{
			title: 'Seite nicht gefunden',
			template: 'splash',
			editUrl: false,
			pagefind: false,
			tableOfContents: false,
			hero: {
				title: 'Seite nicht gefunden',
				tagline: 'Diese Seite gibt es nicht (mehr). Über die Suche oben oder die Startseite findest du weiter.<br />This page does not exist (anymore).',
				actions: [
					{ text: 'Zur Startseite', link: '/', icon: 'right-arrow' },
					{ text: 'English', link: '/en/', variant: 'secondary' },
				],
			},
		},
		{ lineWidth: 0 },
	)}---\n`,
);

fs.mkdirSync(OUT_GEN, { recursive: true });
fs.writeFileSync(path.join(OUT_GEN, 'sidebar.json'), JSON.stringify(buildSidebar(groups, pages), null, 2));
fs.writeFileSync(path.join(OUT_GEN, 'redirects.json'), JSON.stringify(buildRedirects(pages), null, 2));
copyAssets();

const de = [...pages.values()].filter((p) => p.locale === 'de').length;
console.log(`convert: ${pages.size} Seiten (${de} deutsch, ${pages.size - de} englisch) nach src/content/docs`);
if (warnings.length) {
	console.log(`convert: ${warnings.length} Hinweis(e):`);
	for (const w of [...new Set(warnings)]) console.log('  - ' + w);
}
