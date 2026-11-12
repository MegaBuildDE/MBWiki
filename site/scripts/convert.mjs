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

// Adresse der fertigen Seite (wie `site` in astro.config.mjs). Auf der Test-Subdomain setzt
// der Server SITE_URL, damit Vorschaubilder dort auf die Test-Subdomain zeigen.
const SITE_URL = (process.env.SITE_URL || 'https://wiki.megabuild.de').replace(/\/+$/, '');
// Vorschaubild für Discord & Co., wenn eine Seite weder Titelbild noch eigenes Bild hat
const SHARE_DEFAULT = '/share.jpg';

// Startseite: Schaltflächen im Kopfbereich (Hero), Ziel als Quelldatei. Rest kommt aus README.md / en/welcome.md.
const HOME_ACTIONS = {
	de: [
		{ text: 'Erste Schritte', src: 'sb/start.md', icon: 'right-arrow' },
		{ text: 'Verbinden', src: 'ag/join.md', variant: 'secondary' },
	],
	en: [
		{ text: 'Getting started', src: 'en/start.md', icon: 'right-arrow' },
		{ text: 'How to join', src: 'en/join.md', variant: 'secondary' },
	],
};

// Eigene Bausteine (Rezepte, Item-Reihen, Mobplate-Galerie): Daten in data/items.json,
// Texturen und Plugin-Daten aus tools/site_items.py (data/items.generated.json).
const ITEMS = JSON.parse(fs.readFileSync(path.join(SITE, 'data/items.json'), 'utf8'));
const ITEMS_GEN = JSON.parse(fs.readFileSync(path.join(SITE, 'data/items.generated.json'), 'utf8'));
// Skilltree-Baum: data/skilltree.json von Hand, der Rest aus MBSkyManager (tools/site_skilltree.py).
const TREE = JSON.parse(fs.readFileSync(path.join(SITE, 'data/skilltree.json'), 'utf8'));
const TREE_GEN = JSON.parse(fs.readFileSync(path.join(SITE, 'data/skilltree.generated.json'), 'utf8'));

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

// Adressen sind kurz und englisch: Deutsch unter /<key>/, Englisch unter /en/<key>/.
// key = Dateiname der englischen Seite (en/island.md -> island), sonst locale-map.json → slugs.
function buildIndex(groups) {
	const pages = new Map(); // src -> page
	const all = groups.flatMap((g) => flatten(g.items)).map((it) => it.src);
	const isEn = (src) => src.startsWith('en/');
	const enToDe = { ...(localeMap.pages ?? {}) };
	for (const en of all.filter(isEn)) {
		if (enToDe[en]) continue;
		const guess = all.find((d) => !isEn(d) && path.basename(d) === path.basename(en));
		if (guess) enToDe[en] = guess;
		warn(
			guess
				? `${en}: nicht in locale-map.json, per Dateiname ${guess} zugeordnet`
				: `${en}: keine deutsche Seite zugeordnet (locale-map.json) – kein Sprachwechsel möglich`,
		);
	}
	const deToEn = Object.fromEntries(Object.entries(enToDe).map(([en, de]) => [de, en]));

	const keyOf = (deSrc) => {
		if (deSrc === 'README.md') return 'index';
		if (deToEn[deSrc]) return deSlug(path.basename(deToEn[deSrc]));
		if (localeMap.slugs?.[deSrc]) return localeMap.slugs[deSrc];
		warn(`${deSrc}: keine englische Seite und kein Eintrag unter "slugs" in locale-map.json – Adresse aus dem Dateipfad`);
		return deSlug(deSrc);
	};

	const seen = new Map(); // slug -> src
	const add = (src, locale) => {
		const file = path.join(REPO, src);
		if (!fs.existsSync(file)) {
			warn(`SUMMARY.md verweist auf fehlende Datei ${src}`);
			return;
		}
		const de = locale === 'en' ? enToDe[src] : src;
		const key = de ? keyOf(de) : deSlug(path.basename(src));
		const slug = locale === 'en' ? `en/${key}` : key;
		if (seen.has(slug)) warn(`${src} und ${seen.get(slug)} bekommen beide die Adresse ${urlOf(slug)}`);
		seen.set(slug, src);
		const { data, body } = splitFrontmatter(fs.readFileSync(file, 'utf8'));
		const { title } = extractTitle(body, path.basename(src, '.md'));
		pages.set(src, { src, slug, url: urlOf(slug), locale, title, description: data.description ?? '' });
	};

	for (const src of all) add(src, isEn(src) ? 'en' : 'de');
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

// ---------------------------------------------------------------------------
// Eigene Bausteine: Rezepte, Item-Reihen, Mobplate-Galerie
// ---------------------------------------------------------------------------

const MC_COLORS = { light_purple: '#ff55ff', aqua: '#55ffff', gray: '#aaaaaa', green: '#55ff55', gold: '#ffaa00', white: '#ffffff' };
const UI = {
	de: { anySlot: 'Platz egal', search: 'Mob suchen …', searchLabel: 'Mobplates durchsuchen', spawner: 'Ergibt Spawner', spawnerLore: '§aErgibt einen Spawner', plates: 'Plates', none: 'Keine Plate gefunden.', plate: 'Mobplate' },
	en: { anySlot: 'Any slot', search: 'Search mob …', searchLabel: 'Search Mobplates', spawner: 'Makes a spawner', spawnerLore: '§aMakes a spawner', plates: 'plates', none: 'No plate found.', plate: 'Mobplate' },
};

function itemLink(pages, spec) {
	if (!spec) return null;
	const [target, anchor = ''] = spec.split('#');
	return linkFor(pages, 'items.json', target, anchor ? `#${anchor}` : '');
}

function itemInfo(id, locale, pages) {
	const it = ITEMS.items[id];
	if (!it) {
		warn(`data/items.json: Item „${id}“ fehlt`);
		return null;
	}
	const tex = ITEMS_GEN.textures[id];
	if (!tex) warn(`data/items.generated.json: keine Textur für „${id}“ – python3 tools/site_items.py laufen lassen`);
	return {
		id,
		name: it.name[locale] ?? it.name.de,
		color: MC_COLORS[it.color] ?? MC_COLORS.white,
		lore: it.lore?.[locale] ?? [],
		vanilla: Boolean(it.vanilla),
		tex: tex ?? [],
		href: itemLink(pages, it.link?.[locale] ?? it.link?.de),
	};
}

// Gefüllte Plates, die einen Spawner ergeben (aus der Plugin-Config), die Kuh zuerst wie im alten Bild.
function spawnerPlates(locale, pages) {
	const list = Object.entries(ITEMS_GEN.mobplates)
		.filter(([, p]) => p.spawner)
		.map(([id, p]) => ({ id, name: `${UI[locale].plate}: ${p[locale]}`, tex: p.tex }));
	const cow = list.findIndex((p) => p.id === 'mobplate_cow');
	if (cow > 0) list.unshift(...list.splice(cow, 1));
	return {
		id: 'mobplate_filled',
		name: list[0]?.name ?? UI[locale].plate,
		color: MC_COLORS.light_purple,
		lore: [],
		vanilla: false,
		tex: [list[0]?.tex].filter(Boolean),
		cycle: list.map((p) => [p.tex, p.name]),
		href: itemLink(pages, locale === 'en' ? 'en/mobplates.md' : 'sb/mobplates.md'),
	};
}

// Ein Platz im Raster. Tooltip-Daten stehen in data-*, mb.js zeichnet daraus den Minecraft-Tooltip.
function slotHtml(info, { cls = '', count = 0, style = '', follow = false, extra = '', lazy = true } = {}) {
	if (!info) return `<span class="mb-slot${cls ? ' ' + cls : ''}"${style ? ` style="${style}"` : ''} aria-hidden="true"></span>`;
	const tag = info.href ? 'a' : 'span';
	const attrs = [
		`class="mb-slot${cls ? ' ' + cls : ''}"`,
		info.href ? `href="${esc(info.href)}"` : '',
		style ? `style="${style}"` : '',
		`data-item="${esc(info.id)}"`,
		`data-name="${esc(info.name)}"`,
		`data-color="${info.color}"`,
		info.lore.length ? `data-lore="${esc(JSON.stringify(info.lore))}"` : '',
		info.vanilla ? 'data-vanilla' : '',
		info.cycle ? `data-cycle="${esc(JSON.stringify(info.cycle))}"` : info.tex.length > 1 ? `data-cycle="${esc(JSON.stringify(info.tex.map((t) => [t])))}"` : '',
		follow ? 'data-follow' : '',
		extra,
		`aria-label="${esc(info.name)}"`,
	].filter(Boolean);
	const img = info.tex[0] ? `<img src="${esc(info.tex[0])}" alt="" width="16" height="16"${lazy ? ' loading="lazy"' : ''} decoding="async" draggable="false">` : '';
	return `<${tag} ${attrs.join(' ')}>${img}${count > 1 ? `<span class="mb-slot__count">${count}</span>` : ''}</${tag}>`;
}

function recipeHtml(fig, alt, caption, locale, pages) {
	const rows = fig.shape.map((r) => r.padEnd(3, ' ').slice(0, 3));
	while (rows.length < 3) rows.push('   ');
	const cells = rows.join('').split('');
	let followCycle = false;
	const slots = cells.map((ch, i) => {
		const id = ch === ' ' ? null : fig.keys[ch];
		if (ch !== ' ' && !id) warn(`data/items.json: Rezept ohne Zutat für „${ch}“`);
		const info = !id ? null : id === '@spawner-plates' ? spawnerPlates(locale, pages) : itemInfo(id, locale, pages);
		if (info?.cycle && id === '@spawner-plates') followCycle = true;
		// Rezeptbilder sofort laden (16×16, winzig), damit die Animation nicht auf sie wartet
		return slotHtml(info, { style: `--i:${i}`, lazy: false });
	});
	const result = itemInfo(fig.result, locale, pages);
	const badge = fig.shapeless ? `<span class="mb-craft__badge" title="${esc(UI[locale].anySlot)}">⇄ ${esc(UI[locale].anySlot)}</span>` : '';
	return (
		`\n<figure class="mb-craft"><div class="mb-craft__table">` +
		`<div class="mb-craft__grid">${slots.join('')}</div>` +
		`<span class="mb-craft__arrow" aria-hidden="true"></span>` +
		slotHtml(result, { cls: 'mb-slot--result', count: fig.count ?? 1, follow: followCycle, lazy: false }) +
		badge +
		`</div><span class="sr-only">${alt}</span>` +
		(caption ? `<figcaption>${caption}</figcaption>` : '') +
		`</figure>\n`
	);
}

function itemRowHtml(fig, locale, pages) {
	const cards = fig.items.map((id) => {
		const info = itemInfo(id, locale, pages);
		if (!info) return '';
		const tag = info.href ? 'a' : 'div';
		return (
			`<${tag} class="mb-itemcard"${info.href ? ` href="${esc(info.href)}"` : ''}>` +
			`<span class="mb-itemcard__icon">${info.tex[0] ? `<img src="${esc(info.tex[0])}" alt="" width="16" height="16" decoding="async" draggable="false">` : ''}</span>` +
			`<span class="mb-itemcard__name" style="--mb-mc:${info.color}">${esc(info.name)}</span>` +
			`<span class="mb-itemcard__src">${info.vanilla ? 'Minecraft' : 'MegaBuild.de'}</span>` +
			`</${tag}>`
		);
	});
	return `\n<div class="mb-itemrow">${cards.join('')}</div>\n`;
}

function galleryHtml(fig, alt, locale) {
	if (fig.gallery !== 'mobplates') {
		warn(`data/items.json: unbekannte Galerie „${fig.gallery}“`);
		return null;
	}
	const ui = UI[locale];
	const plates = Object.entries(ITEMS_GEN.mobplates)
		.map(([id, p]) => ({ id, ...p, name: p[locale] ?? p.de }))
		.sort((a, b) => a.name.localeCompare(b.name, locale));
	const nSpawner = plates.filter((p) => p.spawner).length;
	const slots = plates.map((p) =>
		slotHtml(
			{ id: p.id, name: `${ui.plate}: ${p.name}`, color: MC_COLORS.light_purple, lore: p.spawner ? [ui.spawnerLore] : [], vanilla: false, tex: [p.tex] },
			{ cls: p.spawner ? 'mb-slot--spawner' : '', extra: `data-search="${esc(`${p.de} ${p.en}`.toLowerCase())}"` },
		),
	);
	const spawnerTex = ITEMS_GEN.textures.spawner?.[0] ?? '';
	return (
		`\n<div class="mb-gallery" style="--mb-spawner-icon:url('${spawnerTex}')">` +
		`<div class="mb-gallery__bar" hidden>` +
		`<input class="mb-gallery__search" type="search" placeholder="${esc(ui.search)}" aria-label="${esc(ui.searchLabel)}" autocomplete="off">` +
		`<button class="mb-gallery__chip" type="button" aria-pressed="false"><img src="${spawnerTex}" alt="" width="16" height="16">${esc(ui.spawner)} <b>${nSpawner}</b></button>` +
		`<span class="mb-gallery__count" aria-live="polite" data-total="${plates.length}" data-unit="${esc(ui.plates)}">${plates.length} ${esc(ui.plates)}</span>` +
		`</div>` +
		`<div class="mb-gallery__grid">${slots.join('')}</div>` +
		`<p class="mb-gallery__empty" hidden>${esc(ui.none)}</p>` +
		`<span class="sr-only">${alt}</span>` +
		`</div>\n`
	);
}

// ---------------------------------------------------------------------------
// Skilltree als Baum: ersetzt auf den Skilltree-Seiten den ersten Tab-Block (ein Tab je Pfad).
// GitBook zeigt weiter die Tabs; hier stehen Kristalle und Biome als Kacheln, ein Klick zeigt
// Quest, Voraussetzung, Preis und die Bilder aus dem Tab. mb.js baut daraus die Details.
// ---------------------------------------------------------------------------

const TREE_UI = {
	de: {
		root: 'Deine Insel',
		rootNote: 'Kristall wählen, dann Biom für Biom freischalten',
		pick: 'Tippe auf einen Kristall oder ein Biom.',
		biomes: 'Biome',
		place: '{path} · {n}. Biom',
		unlock: 'Freischalten',
		unlockStart: 'Startest du mit diesem Pfad, ist es dein **Startbiom**. Sonst kaufst du es nach der Kristallquest: **{q}**.',
		unlockNext: 'Das Biom davor – **{prev}** – gehört deiner Insel, und seine Biomquest ist geschafft: **{q}**.',
		quest: 'Biomquest',
		opens: 'öffnet {next}',
		last: 'letzte Stelle – öffnet noch nichts',
		reward: '+{n} Mana für jeden, der mithilft',
		price: 'Preis',
		priceAt: 'als {n}. Kauf',
		priceLabel: 'Wievielter Kauf deiner Insel?',
		crystalQuest: 'Kristallquest',
		crystalNote: 'Zählt auf allen deinen Inseln. Dein Startpfad braucht keine.',
		close: 'Schließen',
		label: 'Skilltree als Baum',
	},
	en: {
		root: 'Your island',
		rootNote: 'Pick a crystal, then unlock biome by biome',
		pick: 'Tap a crystal or a biome.',
		biomes: 'biomes',
		place: '{path} · biome {n}',
		unlock: 'Unlock',
		unlockStart: 'If you start with this path, it’s your **starting biome**. Otherwise you buy it after the crystal quest: **{q}**.',
		unlockNext: 'The biome before – **{prev}** – belongs to your island and its biome quest is done: **{q}**.',
		quest: 'Biome quest',
		opens: 'unlocks {next}',
		last: 'last spot – doesn’t unlock anything yet',
		reward: '+{n} Mana for everyone who helps',
		price: 'Price',
		priceAt: 'as purchase no. {n}',
		priceLabel: 'Which purchase of your island?',
		crystalQuest: 'Crystal quest',
		crystalNote: 'Counts on all your islands. Your starting path doesn’t need one.',
		close: 'Close',
		label: 'Skill tree as a tree',
	},
};

const stripTags = (s) => s.replace(/<[^>]+>/g, '').trim();

function skilltreeTree(src, t) {
	if (!TREE.pages.includes(src)) return t;
	const locale = src.startsWith('en/') ? 'en' : 'de';
	const ui = TREE_UI[locale];
	const block = t.match(/\{% tabs %\}([\s\S]*?)\{% endtabs %\}/);
	if (!block) {
		warn(`${src}: kein Tab-Block für den Skilltree-Baum`);
		return t;
	}
	// Bilder je Tab einsammeln; der Tab-Titel ist der Pfadname aus der Sprachdatei.
	const byName = new Map(TREE_GEN.paths.map((p) => [p.name[locale].toLowerCase(), p]));
	const shots = new Map();
	const order = [];
	for (const [, title, body] of block[1].matchAll(/\{% tab title="([^"]*)" %\}([\s\S]*?)\{% endtab %\}/g)) {
		const p = byName.get(title.toLowerCase());
		if (!p) {
			warn(`${src}: Tab „${title}“ passt zu keinem Pfad im Skilltree (gesperrt oder umbenannt?)`);
			continue;
		}
		order.push(p);
		shots.set(
			p.id,
			[...body.matchAll(/<img src="([^"]+)"[^>]*?alt="([^"]*)"[^>]*>(?:<figcaption>([\s\S]*?)<\/figcaption>)?/g)].map(([, img, alt, cap = '']) => ({
				src: img,
				alt,
				cap: stripTags(cap),
			})),
		);
	}
	const paths = [...order, ...TREE_GEN.paths.filter((p) => !order.includes(p))];

	const data = {
		ui,
		price: TREE_GEN.price,
		reward: TREE_GEN.reward,
		paths: paths.map((p) => {
			const own = shots.get(p.id) ?? [];
			// Ein Bild gehört zu dem Biom, mit dessen Namen seine Unterschrift beginnt (längster Name zuerst).
			const named = [...p.biomes.keys()].sort((a, b) => p.biomes[b].name[locale].length - p.biomes[a].name[locale].length);
			const biomeShots = p.biomes.map(() => []);
			for (const s of own) {
				const text = (s.cap || s.alt).toLowerCase();
				const i = named.find((j) => text.startsWith(p.biomes[j].name[locale].toLowerCase()));
				if (i !== undefined) biomeShots[i].push(s);
			}
			return {
				name: p.name[locale],
				desc: p.description[locale],
				quest: p.crystalQuest?.[locale] ?? '',
				crystal: p.crystal,
				shots: own,
				biomes: p.biomes.map((b, i) => ({ name: b.name[locale], icon: b.icon, quest: b.quest?.[locale] ?? '', shots: biomeShots[i] })),
			};
		}),
	};

	const cols = paths.map((p, pi) => {
		const chain = p.biomes
			.map(
				(b, bi) =>
					`<li><button type="button" class="mb-tree__node mb-tree__biome" data-p="${pi}" data-b="${bi}" aria-pressed="false">` +
					`<span class="mb-tree__step">${bi + 1}</span>` +
					`<img src="${esc(b.icon)}" alt="" width="16" height="16" decoding="async" draggable="false">` +
					`<span class="mb-tree__name">${esc(b.name[locale])}</span></button></li>`,
			)
			.join('');
		return (
			`<div class="mb-tree__path" style="--c:${p.color ?? '#a958ff'}">` +
			`<button type="button" class="mb-tree__node mb-tree__crystal" data-p="${pi}" aria-pressed="false" aria-expanded="${pi === 0}">` +
			`<img src="${esc(p.crystal)}" alt="" width="16" height="16" decoding="async" draggable="false">` +
			`<span class="mb-tree__name">${esc(p.name[locale])}</span>` +
			`<span class="mb-tree__meta">${p.biomes.length} ${esc(ui.biomes)}</span></button>` +
			`<ol class="mb-tree__chain" aria-label="${esc(p.name[locale])}">${chain}</ol></div>`
		);
	});

	const island = TREE_GEN.paths.flatMap((p) => p.biomes).find((b) => b.icon.endsWith('/grass_block.png'))?.icon;
	const html =
		`\n<div class="mb-tree not-content" role="group" aria-label="${esc(ui.label)}" data-tree="${esc(JSON.stringify(data))}" style="--n:${paths.length}">` +
		`<div class="mb-tree__root"><span class="mb-tree__island" aria-hidden="true">${island ? `<img src="${esc(island)}" alt="" width="16" height="16">` : ''}</span><span><b>${esc(ui.root)}</b><small>${esc(ui.rootNote)}</small></span></div>` +
		`<div class="mb-tree__paths">${cols.join('')}</div>` +
		`<div class="mb-tree__detail" aria-live="polite" hidden><p class="mb-tree__pick">${esc(ui.pick)}</p></div>` +
		`</div>\n`;
	return t.replace(block[0], () => html);
}

const PIXEL_ASSET = new RegExp(`^(?:${ITEMS.pixelated.map((p) => p.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&')).join('|')})`);

function customBlocks(src, t, pages) {
	const locale = pages.get(src)?.locale ?? 'de';
	t = t.replace(
		/<figure><img src="\/assets\/([^"]+)"([^>]*)>(?:<figcaption>([\s\S]*?)<\/figcaption>)?<\/figure>/g,
		(m, asset, attrs, caption = '') => {
			const fig = ITEMS.figures[asset];
			if (!fig) return m;
			const alt = attrs.match(/alt="([^"]*)"/)?.[1] ?? '';
			const cap = caption.trim();
			if (fig.shape) return recipeHtml(fig, alt, cap, locale, pages);
			if (fig.items) return itemRowHtml(fig, locale, pages);
			if (fig.gallery) return galleryHtml(fig, alt, locale) ?? m;
			return m;
		},
	);
	// Übrige Pixelbilder (z. B. Bauplan) ohne Weichzeichnen vergrößern.
	return t.replace(/<img src="\/assets\/([^"]+)"/g, (m, asset) => (PIXEL_ASSET.test(asset) ? `<img class="mb-pixel" src="/assets/${asset}"` : m));
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

	// Skilltree-Baum statt der Pfad-Tabs, dann Rezepte, Item-Reihen und Galerie statt der Bilder
	t = skilltreeTree(src, t);
	t = customBlocks(src, t, pages);

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
	// Vorschaubild beim Teilen: Titelbild, sonst erstes Bild der Seite, sonst das allgemeine
	const firstImage = body.match(/(?:\.\.\/|\.\/)*\.gitbook\/assets\/[^\s"')>]+?\.(?:webp|png|jpe?g)(?=[\s"')>])/i)?.[0];
	const share = SITE_URL + encodeURI(decodeURI(data.cover ? assetUrl(data.cover) : firstImage ? assetUrl(firstImage) : SHARE_DEFAULT));
	fm.head = [
		{ tag: 'meta', attrs: { property: 'og:image', content: share } },
		{ tag: 'meta', attrs: { name: 'twitter:image', content: share } },
	];
	const updated = dates.get(page.src);
	if (updated) fm.lastUpdated = updated.slice(0, 10);
	fm.source = page.src;

	if (page.slug === 'index' || page.slug === 'en/index') {
		// Kein Splash-Layout: wie bei GitBook bleibt die Navigation (bzw. das Burger-Menü) auch hier.
		fm.hero = {
			title: page.title,
			tagline: fm.description,
			actions: HOME_ACTIONS[page.locale].map(({ src, ...a }) => ({ ...a, link: pages.get(src)?.url ?? '/' })),
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
	const norm = (u) => u.replace(/\/+$/, '') || '/';
	// Alte GitBook-Adressen (Dateipfade wie /sb/insel, /en/welcome) -> neue (/island/, /en/)
	for (const p of pages.values()) {
		const old = norm('/' + p.src.replace(/\.md$/, '').replace(/(^|\/)README$/, ''));
		if (old !== norm(p.url)) redirects[old] = p.url;
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
