// Tabs für umgewandelte GitBook-Tab-Blöcke (<div class="mb-tabs"><div class="mb-tab" data-label="…">).
// Gleiche Tab-Namen (z. B. „Java Edition“ / „Bedrock Edition“) bleiben seitenübergreifend gewählt.
(() => {
	const STORE = 'mb-tab-choice';
	const read = () => {
		try {
			return JSON.parse(localStorage.getItem(STORE) || '{}');
		} catch {
			return {};
		}
	};
	const write = (v) => {
		try {
			localStorage.setItem(STORE, JSON.stringify(v));
		} catch {}
	};

	const groups = [];

	function select(group, label, remember) {
		group.tabs.forEach((tab, i) => {
			const on = tab.dataset.label === label;
			tab.hidden = !on;
			group.buttons[i].setAttribute('aria-selected', String(on));
			group.buttons[i].tabIndex = on ? 0 : -1;
		});
		if (remember) {
			const choice = read();
			choice[group.key] = label;
			write(choice);
			// andere Tab-Gruppen mit denselben Namen mitziehen
			for (const g of groups) if (g !== group && g.key === group.key) select(g, label, false);
		}
	}

	document.querySelectorAll('.mb-tabs').forEach((root, n) => {
		const tabs = [...root.children].filter((c) => c.classList.contains('mb-tab'));
		if (!tabs.length) return;
		const labels = tabs.map((t) => t.dataset.label || '');
		const list = document.createElement('div');
		list.className = 'mb-tabs__list';
		list.setAttribute('role', 'tablist');
		const buttons = tabs.map((tab, i) => {
			const id = `mb-tab-${n}-${i}`;
			tab.id = id;
			tab.setAttribute('role', 'tabpanel');
			const b = document.createElement('button');
			b.type = 'button';
			b.className = 'mb-tabs__button';
			b.setAttribute('role', 'tab');
			b.setAttribute('aria-controls', id);
			b.textContent = labels[i];
			list.append(b);
			return b;
		});
		root.prepend(list);
		root.classList.add('is-ready');
		const group = { root, tabs, buttons, key: [...labels].sort().join('|') };
		groups.push(group);

		buttons.forEach((b, i) => {
			b.addEventListener('click', () => select(group, labels[i], true));
			b.addEventListener('keydown', (e) => {
				const dir = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
				if (!dir) return;
				const next = (i + dir + buttons.length) % buttons.length;
				buttons[next].focus();
				select(group, labels[next], true);
			});
		});

		const saved = read()[group.key];
		select(group, labels.includes(saved) ? saved : labels[0], false);
	});
})();

// Rezepte, Item-Plätze und Mobplate-Galerie (erzeugt von scripts/convert.mjs aus data/items.json):
// Tooltip wie im Spiel, gleiche Items hervorheben, Crafting-Animation beim ersten Hinsehen,
// wechselnde Zutaten (z. B. die Mobplates im Spawner-Rezept) und Suche/Filter in der Galerie.
(() => {
	const slots = document.querySelectorAll('.mb-slot[data-item]');
	if (!slots.length) return;

	const en = document.documentElement.lang === 'en';
	const T = en ? { replay: 'Craft again' } : { replay: 'Nochmal craften' };
	const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
	const MC = { 0: '#000000', 1: '#0000aa', 2: '#00aa00', 3: '#00aaaa', 4: '#aa0000', 5: '#aa00aa', 6: '#ffaa00', 7: '#aaaaaa', 8: '#555555', 9: '#5555ff', a: '#55ff55', b: '#55ffff', c: '#ff5555', d: '#ff55ff', e: '#ffff55', f: '#ffffff' };
	const boxOf = (el) => el.closest('.mb-craft, .mb-gallery, .mb-itemrow');

	// ---- Tooltip ----
	const tip = document.createElement('div');
	tip.className = 'mb-tooltip';
	tip.setAttribute('role', 'tooltip');
	tip.setAttribute('aria-hidden', 'true');
	document.body.append(tip);
	let current = null;
	let pointer = 'mouse';

	const line = (text, cls, color) => {
		const p = document.createElement('p');
		const code = text.match(/^§([0-9a-f])/);
		if (code) text = text.slice(2);
		if (cls) p.className = cls;
		if (code || color) p.style.color = code ? MC[code[1]] : color;
		p.textContent = text;
		return p;
	};

	function fill(slot) {
		const lore = slot.dataset.lore ? JSON.parse(slot.dataset.lore) : [];
		// Ergebnis, das der wechselnden Zutat folgt (der Spawner zeigt die Plate darin)
		const source = slot.hasAttribute('data-follow') ? boxOf(slot)?.querySelector('.mb-slot[data-cycle]') : null;
		tip.replaceChildren(
			line(slot.dataset.name, 'mb-tooltip__name', slot.dataset.color),
			...(source ? [line(source.dataset.name, '', source.dataset.color)] : []),
			...lore.map((l) => line(l)),
			line(slot.hasAttribute('data-vanilla') ? 'Minecraft' : 'MegaBuild.de', 'mb-tooltip__src'),
		);
	}

	function placeAtPointer(x, y) {
		const w = tip.offsetWidth;
		const h = tip.offsetHeight;
		let left = x + 14;
		let top = y - h - 6;
		if (left + w > innerWidth - 8) left = x - w - 14;
		if (top < 8) top = y + 22;
		tip.style.transform = `translate(${Math.max(8, left)}px, ${top}px)`;
	}

	function placeAtSlot(slot) {
		const r = slot.getBoundingClientRect();
		const w = tip.offsetWidth;
		const h = tip.offsetHeight;
		const left = Math.min(Math.max(8, r.left + r.width / 2 - w / 2), innerWidth - w - 8);
		const top = r.top - h - 10 < 8 ? r.bottom + 10 : r.top - h - 10;
		tip.style.transform = `translate(${left}px, ${top}px)`;
	}

	function mark(slot, on) {
		slot.classList.toggle('is-active', on && pointer !== 'mouse');
		const box = boxOf(slot);
		if (!box || box.classList.contains('mb-gallery')) return;
		box.querySelectorAll(`.mb-slot[data-item="${CSS.escape(slot.dataset.item)}"]`).forEach((s) => {
			if (s !== slot) s.classList.toggle('is-match', on);
		});
	}

	function show(slot, event) {
		if (current && current !== slot) hide();
		current = slot;
		fill(slot);
		mark(slot, true);
		tip.classList.add('is-visible');
		if (event && pointer === 'mouse') placeAtPointer(event.clientX, event.clientY);
		else placeAtSlot(slot);
	}

	function hide() {
		if (!current) return;
		mark(current, false);
		current = null;
		tip.classList.remove('is-visible');
	}

	const slotAt = (el) => el?.closest?.('.mb-slot[data-item]');

	document.addEventListener('pointerdown', (e) => {
		pointer = e.pointerType || 'mouse';
		if (pointer !== 'mouse' && !slotAt(e.target)) hide();
	});
	document.addEventListener('pointerover', (e) => {
		if (e.pointerType !== 'mouse' && e.pointerType !== 'pen') return;
		pointer = 'mouse';
		const slot = slotAt(e.target);
		if (slot) show(slot, e);
	});
	document.addEventListener('pointermove', (e) => {
		if (current && e.pointerType === 'mouse') placeAtPointer(e.clientX, e.clientY);
	});
	document.addEventListener('pointerout', (e) => {
		if (e.pointerType !== 'mouse' || !current) return;
		if (!current.contains(e.relatedTarget)) hide();
	});
	document.addEventListener('focusin', (e) => {
		const slot = slotAt(e.target);
		if (slot && pointer !== 'touch' && pointer !== 'mouse') show(slot);
	});
	document.addEventListener('keydown', (e) => {
		if (e.key === 'Tab') pointer = 'keyboard';
		if (e.key === 'Escape') hide();
	});
	document.addEventListener('focusout', (e) => {
		if (slotAt(e.target) === current && pointer === 'keyboard') hide();
	});
	// Handy: erster Tipp zeigt den Tooltip, zweiter folgt dem Link.
	document.addEventListener('click', (e) => {
		const slot = slotAt(e.target);
		if (!slot || pointer === 'mouse' || pointer === 'keyboard') return;
		if (current !== slot) {
			e.preventDefault();
			show(slot);
		} else if (!slot.href) {
			hide();
		}
	});
	addEventListener('scroll', () => pointer !== 'mouse' && hide(), { passive: true });

	// ---- Crafting-Animation ----
	const crafts = [...document.querySelectorAll('.mb-craft')];
	// Erst abspielen, wenn alle Bilder dekodiert sind - sonst ploppen sie mitten in der Animation auf.
	const ready = (fig) => Promise.all([...fig.querySelectorAll('img')].map((img) => img.decode?.().catch(() => {})));
	function play(fig) {
		fig.classList.add('mb-craft--anim');
		fig.classList.remove('is-play');
		ready(fig).then(() => {
			void fig.offsetWidth; // Neustart der CSS-Animation erzwingen
			fig.classList.add('is-play');
		});
	}
	if (!reduce && 'IntersectionObserver' in window) {
		const io = new IntersectionObserver(
			(entries) =>
				entries.forEach((entry) => {
					if (!entry.isIntersecting) return;
					io.unobserve(entry.target);
					play(entry.target);
				}),
			{ threshold: 0.55 },
		);
		crafts.forEach((fig) => {
			fig.classList.add('mb-craft--anim');
			io.observe(fig);
			const again = document.createElement('div');
			again.className = 'mb-craft__again';
			const btn = document.createElement('button');
			btn.type = 'button';
			btn.className = 'mb-craft__replay';
			btn.innerHTML =
				'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 2.6-6.4"/><path d="M3 3.5V9h5.5"/></svg>';
			btn.append(T.replay);
			btn.addEventListener('click', () => {
				io.unobserve(fig);
				play(fig);
			});
			again.append(btn);
			fig.querySelector('.mb-craft__table')?.after(again);
		});
	}

	// ---- Wechselnde Zutaten ----
	const cycling = [...document.querySelectorAll('.mb-slot[data-cycle]')].map((slot) => ({
		slot,
		list: JSON.parse(slot.dataset.cycle),
		img: slot.querySelector('img'),
	}));
	if (cycling.length > 0) {
		let tick = 0;
		setInterval(() => {
			if (document.hidden) return;
			tick++;
			for (const { slot, list, img } of cycling) {
				if (!img || list.length < 2) continue;
				// Nicht wechseln, während jemand in diesem Rezept liest
				if (current && boxOf(current) === boxOf(slot)) continue;
				const [src, name] = list[tick % list.length];
				new Image().src = list[(tick + 1) % list.length][0];
				slot.classList.add('is-swap');
				setTimeout(() => {
					img.src = src;
					if (name) {
						slot.dataset.name = name;
						slot.setAttribute('aria-label', name);
					}
					slot.classList.remove('is-swap');
				}, 180);
			}
		}, 1700);
	}

	// ---- Galerie: Suche und Spawner-Filter ----
	const norm = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
	document.querySelectorAll('.mb-gallery').forEach((gallery) => {
		const bar = gallery.querySelector('.mb-gallery__bar');
		const input = gallery.querySelector('.mb-gallery__search');
		const chip = gallery.querySelector('.mb-gallery__chip');
		const count = gallery.querySelector('.mb-gallery__count');
		const empty = gallery.querySelector('.mb-gallery__empty');
		if (!bar || !input || !chip || !count) return;
		const items = [...gallery.querySelectorAll('.mb-slot[data-search]')].map((slot) => ({
			slot,
			text: norm(slot.dataset.search),
			spawner: slot.classList.contains('mb-slot--spawner'),
		}));
		bar.hidden = false;
		const total = Number(count.dataset.total);
		const update = () => {
			const q = norm(input.value.trim());
			const onlySpawner = chip.getAttribute('aria-pressed') === 'true';
			let n = 0;
			for (const it of items) {
				const ok = (!q || it.text.includes(q)) && (!onlySpawner || it.spawner);
				it.slot.hidden = !ok;
				if (ok) n++;
			}
			count.textContent = n === total ? `${total} ${count.dataset.unit}` : `${n} / ${total} ${count.dataset.unit}`;
			if (empty) empty.hidden = n > 0;
			hide();
		};
		input.addEventListener('input', update);
		chip.addEventListener('click', () => {
			chip.setAttribute('aria-pressed', String(chip.getAttribute('aria-pressed') !== 'true'));
			update();
		});
	});
})();

// Skilltree als Baum (erzeugt von scripts/convert.mjs aus data/skilltree.generated.json):
// Kristall oder Biom antippen zeigt Quest, Voraussetzung, Preis und Bilder; der Weg dorthin leuchtet auf.
(() => {
	const trees = document.querySelectorAll('.mb-tree[data-tree]');
	if (!trees.length) return;
	const en = document.documentElement.lang === 'en';
	const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
	const h = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
	const fill = (tpl, vars) => tpl.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? vars[k] : m));
	const bold = (s) => s.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
	const num = (n) => n.toLocaleString(en ? 'en' : 'de');

	trees.forEach((tree) => {
		const data = JSON.parse(tree.dataset.tree);
		const { ui, price } = data;
		const detail = tree.querySelector('.mb-tree__detail');
		const paths = [...tree.querySelectorAll('.mb-tree__path')];
		const nodes = [...tree.querySelectorAll('.mb-tree__node')];
		// Käufe insgesamt: alle Biome ohne das geschenkte Startbiom
		const total = data.paths.reduce((n, p) => n + p.biomes.length, 0) - 1;
		let buyNo = 1;
		let active = null;

		// wie PathRules.Prices#price im Plugin
		const cost = (bought, pos) =>
			Math.max(price.roundTo, Math.round((price.base * (1 + price.growth) ** bought * (1 + price.perStep * (pos - 1))) / price.roundTo) * price.roundTo);

		const shots = (list) =>
			list.length
				? `<div class="mb-tree__shots">${list
						.map((s) => `<figure><img src="${h(s.src)}" alt="${h(s.alt)}" loading="lazy" decoding="async">${s.cap ? `<figcaption>${h(s.cap)}</figcaption>` : ''}</figure>`)
						.join('')}</div>`
				: '';
		const head = (img, title, sub, crystal) =>
			`<div class="mb-tree__head"><span class="mb-tree__big${crystal ? ' is-crystal' : ''}"><img src="${h(img)}" alt="" width="16" height="16"></span>` +
			`<div><p class="mb-tree__title">${h(title)}</p>${sub ? `<p class="mb-tree__sub">${h(sub)}</p>` : ''}</div>` +
			`<button type="button" class="mb-tree__close" aria-label="${h(ui.close)}">×</button></div>`;
		const fact = (label, body) => `<div class="mb-tree__fact"><span class="mb-tree__label">${h(label)}</span><div>${body}</div></div>`;

		function openPath(p) {
			paths.forEach((el, i) => {
				el.classList.toggle('is-open', i === p);
				el.querySelector('.mb-tree__crystal')?.setAttribute('aria-expanded', String(i === p));
			});
		}

		function mark(p, b) {
			tree.classList.toggle('has-active', p !== null);
			nodes.forEach((n) => {
				const np = Number(n.dataset.p);
				const nb = n.dataset.b === undefined ? -1 : Number(n.dataset.b);
				const on = p !== null && np === p && nb === b;
				n.classList.toggle('is-active', on);
				n.classList.toggle('is-trail', p !== null && np === p && nb < b && !on);
				n.setAttribute('aria-pressed', String(on));
			});
			paths.forEach((el, i) => el.classList.toggle('is-focus', i === p));
		}

		function priceText(pos) {
			const min = Math.max(1, pos - 1);
			buyNo = Math.min(total, Math.max(min, buyNo));
			return { min, value: cost(buyNo - 1, pos) };
		}

		function render(p, b) {
			if (p === null) {
				detail.innerHTML = `<p class="mb-tree__pick">${h(ui.pick)}</p>`;
				return;
			}
			const path = data.paths[p];
			if (b < 0) {
				detail.innerHTML =
					head(path.crystal, path.name, path.desc, true) +
					`<div class="mb-tree__facts">${path.quest ? fact(ui.crystalQuest, `<b>${h(path.quest)}</b><small>${h(ui.crystalNote)}</small>`) : ''}</div>` +
					shots(path.shots);
				return;
			}
			const biome = path.biomes[b];
			const pos = b + 1;
			const prev = path.biomes[b - 1];
			const next = path.biomes[b + 1];
			const unlock = prev ? bold(fill(h(ui.unlockNext), { prev: h(prev.name), q: h(prev.quest) })) : bold(fill(h(ui.unlockStart), { q: h(path.quest) }));
			const quest = biome.quest
				? `<b>${h(biome.quest)}</b> <span class="mb-tree__opens">→ ${h(next ? fill(ui.opens, { next: next.name }) : ui.last)}</span>` +
					(data.reward ? `<small>${h(fill(ui.reward, { n: data.reward }))}</small>` : '')
				: '–';
			const { min, value } = priceText(pos);
			detail.innerHTML =
				head(biome.icon, biome.name, fill(ui.place, { path: path.name, n: pos })) +
				`<div class="mb-tree__facts">` +
				fact(ui.unlock, unlock) +
				fact(ui.quest, quest) +
				fact(
					ui.price,
					`<b class="mb-tree__price">${num(value)} Mana</b> <span class="mb-tree__at">${h(fill(ui.priceAt, { n: buyNo }))}</span>` +
						`<input class="mb-tree__range" type="range" min="${min}" max="${total}" value="${buyNo}" aria-label="${h(ui.priceLabel)}">`,
				) +
				`</div>` +
				shots(biome.shots);
			const range = detail.querySelector('.mb-tree__range');
			range.addEventListener('input', () => {
				buyNo = Number(range.value);
				detail.querySelector('.mb-tree__price').textContent = `${num(cost(buyNo - 1, pos))} Mana`;
				detail.querySelector('.mb-tree__at').textContent = fill(ui.priceAt, { n: buyNo });
			});
		}

		function select(p, b, user) {
			const key = p === null ? null : `${p}/${b}`;
			if (user && key !== null && key === active) return select(null, -1, true);
			active = key;
			if (p !== null) openPath(p);
			mark(p, b);
			render(p, b);
			detail.classList.remove('is-in');
			if (p !== null && !reduce) {
				void detail.offsetWidth; // Einblenden neu starten
				detail.classList.add('is-in');
			}
			if (user && p !== null) {
				const r = detail.getBoundingClientRect();
				if (r.bottom > innerHeight || r.top < 0) detail.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
			}
		}

		tree.addEventListener('click', (e) => {
			if (e.target.closest('.mb-tree__close')) {
				const last = (active ?? '').split('/');
				select(null, -1, true);
				const sel = last[1] === '-1' ? ':not([data-b])' : `[data-b="${last[1]}"]`;
				tree.querySelector(`.mb-tree__node[data-p="${last[0]}"]${sel}`)?.focus();
				return;
			}
			const node = e.target.closest('.mb-tree__node');
			if (!node) return;
			select(Number(node.dataset.p), node.dataset.b === undefined ? -1 : Number(node.dataset.b), true);
		});
		tree.addEventListener('keydown', (e) => {
			if (e.key === 'Escape' && active) select(null, -1, true);
		});

		detail.hidden = false;
		openPath(0);
		tree.classList.add('is-ready');
	});
})();
