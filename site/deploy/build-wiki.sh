#!/usr/bin/env bash
# Baut das MegaBuild.de-Wiki (Astro Starlight, Ordner site/) aus dem öffentlichen Repo
# MegaBuildDE/MBWiki und stellt es atomar unter $WEB_ROOT/current bereit, das nginx ausliefert.
#
# Läuft über mbwiki-build.timer jede Minute. Gebaut wird nur, wenn auf $BRANCH ein neuer
# Commit liegt. Der Build läuft in Docker (Node 24), weil Astro neuer ist als das Node des
# Servers. Schlägt ein Build fehl, bleibt der alte Stand live und derselbe Commit wird nicht
# jede Minute neu versucht (erst der nächste Commit oder --force).
#
#   mbwiki-build              neuen Commit bauen, sonst nichts tun
#   mbwiki-build --force      aktuellen Stand neu bauen
#   mbwiki-build --status     zeigen, was live ist
#
# Einstellungen über Umgebungsvariablen, dauerhaft in /etc/default/mbwiki-build.

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/MegaBuildDE/MBWiki.git}"
REPO_DIR="${REPO_DIR:-/opt/mbwiki/repo}"
WEB_ROOT="${WEB_ROOT:-/var/www/wiki}"
BRANCH="${BRANCH:-main}"
NODE_IMAGE="${NODE_IMAGE:-node:24-bookworm}"
NPM_CACHE_VOLUME="${NPM_CACHE_VOLUME:-mbwiki-npm-cache}"
# Der Server teilt sich die Maschine mit dem MB-Core: Build klein halten.
DOCKER_LIMITS="${DOCKER_LIMITS:---cpus=4 --memory=2g}"
KEEP_RELEASES="${KEEP_RELEASES:-5}"
# Weniger HTML-Seiten als das gilt als kaputter Build und wird nicht veröffentlicht.
MIN_PAGES="${MIN_PAGES:-50}"
LOCK_FILE="${LOCK_FILE:-/run/lock/mbwiki-build.lock}"

log() { printf '%s %s\n' "$(date '+%F %T')" "$*"; }
die() {
	log "FEHLER: $*" >&2
	exit 1
}
# Commit als fehlgeschlagen merken (der Timer versucht ihn dann nicht jede Minute neu) und abbrechen
fail() {
	printf '%s\n' "$1" >"$WEB_ROOT/.failed-commit"
	die "$2"
}
read_file() { [[ -f "$1" ]] && cat "$1" || true; }

usage() { sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; }

status() {
	local live failed current
	live="$(read_file "$WEB_ROOT/.built-commit")"
	failed="$(read_file "$WEB_ROOT/.failed-commit")"
	current="$(readlink "$WEB_ROOT/current" 2>/dev/null || true)"
	echo "Branch:       $BRANCH"
	echo "Live-Commit:  ${live:-–}"
	echo "Live-Ordner:  ${current:-–}"
	echo "Fehlgeschlagen (wird übersprungen bis zum nächsten Commit): ${failed:-–}"
	if [[ -d "$REPO_DIR/.git" ]]; then
		echo "Repo:         $(git -C "$REPO_DIR" log -1 --format='%h %cd %s' --date=format:'%F %R' "origin/$BRANCH" 2>/dev/null || echo '–')"
	fi
}

ensure_repo() {
	if [[ ! -d "$REPO_DIR/.git" ]]; then
		log "Klone $REPO_URL nach $REPO_DIR"
		mkdir -p "$(dirname "$REPO_DIR")"
		# volle Historie: die Seiten zeigen „zuletzt geändert“ aus git log
		git clone --quiet "$REPO_URL" "$REPO_DIR"
	fi
}

build() {
	local -a limits
	read -ra limits <<<"$DOCKER_LIMITS"
	docker run --rm --pull=missing "${limits[@]}" \
		-v "$REPO_DIR":/repo \
		-v "$NPM_CACHE_VOLUME":/root/.npm \
		-w /repo/site \
		"$NODE_IMAGE" \
		sh -c 'npm ci --no-audit --no-fund --loglevel=error && npm run build'
}

publish() {
	local sha="$1" dist="$REPO_DIR/site/dist" name pages
	[[ -f "$dist/index.html" ]] || fail "$sha" "dist/index.html fehlt – veröffentliche nicht"
	pages="$(find "$dist" -name '*.html' | wc -l | tr -d ' ')"
	((pages >= MIN_PAGES)) || fail "$sha" "nur $pages HTML-Seiten gebaut (mindestens $MIN_PAGES) – veröffentliche nicht"

	name="$(date '+%Y%m%d-%H%M%S')-${sha:0:7}"
	mkdir -p "$WEB_ROOT/releases"
	cp -R "$dist" "$WEB_ROOT/releases/$name"
	chmod -R a+rX "$WEB_ROOT/releases/$name"
	# atomar umschalten: neuen Link anlegen und über den alten schieben
	ln -sfn "releases/$name" "$WEB_ROOT/current.new"
	mv -Tf "$WEB_ROOT/current.new" "$WEB_ROOT/current"
	printf '%s\n' "$sha" >"$WEB_ROOT/.built-commit"
	rm -f "$WEB_ROOT/.failed-commit"
	log "Live: ${sha:0:7} mit $pages Seiten (releases/$name)"
}

prune() {
	local current dir n=0
	current="$(readlink -f "$WEB_ROOT/current")"
	while IFS= read -r dir; do
		[[ -n "$dir" ]] || continue
		n=$((n + 1))
		((n <= KEEP_RELEASES)) && continue
		[[ "$(readlink -f "$dir")" == "$current" ]] && continue
		rm -rf -- "$dir"
	done < <(find "$WEB_ROOT/releases" -mindepth 1 -maxdepth 1 -type d | sort -r)
}

main() {
	local force=0
	case "${1:-}" in
	"") ;;
	--force) force=1 ;;
	--status)
		status
		return 0
		;;
	-h | --help)
		usage
		return 0
		;;
	*) die "unbekannte Option: $1 (siehe --help)" ;;
	esac

	mkdir -p "$WEB_ROOT" "$(dirname "$LOCK_FILE")"
	exec 9>"$LOCK_FILE"
	if ! flock -n 9; then
		log "Ein Build läuft schon – übersprungen"
		return 0
	fi

	ensure_repo
	git -C "$REPO_DIR" fetch --quiet --prune origin
	local sha live failed
	sha="$(git -C "$REPO_DIR" rev-parse --verify "origin/$BRANCH^{commit}")" || die "Branch $BRANCH gibt es auf origin nicht"
	live="$(read_file "$WEB_ROOT/.built-commit")"
	failed="$(read_file "$WEB_ROOT/.failed-commit")"

	if ((force == 0)); then
		[[ "$sha" == "$live" ]] && return 0
		[[ "$sha" == "$failed" ]] && return 0
	fi

	log "Baue ${sha:0:7} von $BRANCH (live: ${live:0:7})"
	git -C "$REPO_DIR" checkout --quiet --force --detach "$sha"
	git -C "$REPO_DIR" clean -fdq

	build || fail "$sha" "Build von ${sha:0:7} fehlgeschlagen – ${live:0:7} bleibt live"
	publish "$sha"
	prune
}

main "$@"
