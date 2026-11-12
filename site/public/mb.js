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
