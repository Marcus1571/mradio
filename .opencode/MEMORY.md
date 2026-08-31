# mradio — project memory

> Read this first in every session so we can pick up where we left off.
> Update it whenever the project state changes significantly.

## PERMANENT RULES — see `.opencode/BEHAVIOR.md`

That file holds the eternal modus operandi (**commit & push by default**, the
four documentation duties, UI conventions, release discipline, stations
rules). Read it together with this file every session; this file only tracks
the project's CURRENT state.

## Key rules at a glance

- **`c.p` is now the DEFAULT** — commit & push to GitHub after every
  completed task, with a **full release when version-worthy**, unless the user
  says "don't push". Never leave work uncommitted/unpushed after a task;
  committing AND pushing correctly is critical and has been the source of past
  mistakes.

## ⚠️ COMMANDMENTS (non-negotiable — read before acting)

1. **A "release" is the GitHub RELEASE, not the tag.** Pushing a git tag does
   NOT update the GitHub Releases page/sidebar. A release only exists when the
   tag has a GitHub Release attached to it (notes + assets).
2. **Full release sequence, in order — never stop early:**
   1. bump `VERSION` in `./mradio` and add the CHANGELOG section;
   2. commit the changes;
   3. `git tag vX.Y.Z` and `git push origin vX.Y.Z`;
   4. `gh release create vX.Y.Z --repo Marcus1571/mradio --title "mradio vX.Y.Z" --notes-file <notes.md> mradio install.sh`
      (assets = `mradio` + `install.sh`, notes = the CHANGELOG section body);
   5. **verify** with `gh release list | head` that the new version is marked
      `Latest` — do not report "released" until this confirms.
3. **After changing `mradio` code on this machine, also install it** so the
   running copy matches the source: `./install.sh` then confirm
   `mradio --version`. The TUI's bottom-right version reflects the INSTALLED
   binary, not the src tree — if a feature seems missing, the installed copy is
   stale. Quit + reopen mradio to pick up a reinstall (running instances keep
   their in-memory copy).
3. Every release the user asks for must be **pushed to origin, then created as
   a GitHub Release with the two assets**, and confirmed `Latest`. If only a
   tag was pushed, say so and finish the job — do not declare success.
4. Do NOT change the provider fallback order, the Wikipedia verification logic
   (`_resolve_wiki` / `_relevant`), or the atomic-write pattern for
   cache.json / config.json — accepted as correct.

## What it is

`mradio` — a colorful terminal radio player (Python `curses` TUI) that drives
**mpv** as its audio engine over an IPC socket, plus optional **AI enrichment**
(trivia note / Work line / verified Wikipedia link) for the now-playing track.

- Single self-contained file: `./mradio` (~1790 lines), Python 3.8+, **stdlib
  only, no pip dependencies**.
- Repo: `git@github.com:Marcus1571/mradio.git` (user: `Marcus1571`).
- No local demo branch conventions — trivial `main` history, semantic-version
  tags released on GitHub (`v0.7.x`).

## Current state

- **Latest version / release:** `0.7.61` (in-code `VERSION`, released tag +
  GitHub Release with assets `mradio` + `install.sh`, verified `Latest`).
  `main` is kept in sync with every release (push `main` alongside each tag).
- **Palettes:** `p` rotates `dark` → `light` → `light-navy` → `light-mauve`
  (256-color Catppuccin-inspired, ANSI fallback; pair 5 = muted subtext).
- **Station model (0.7.28+):** two deliberate lists.
  - **Favorites** (`f`): user's list in
    `~/.local/share/mradio/stations.json` (key `"favorites"`), max **10** hot
    slots (`1-9` + `0`; numpad digits resolve via `_follow_esc`). Seeded once,
    on first run, from the **first 10** of `DEFAULT_STATIONS`; legacy
    `config.json` `"stations"` migrated once (trimmed to 10). Releases never
    touch it. `a` (in the `s` menu) adds a row but refuses when full ("favorites
    full"). `MRADIO_STATIONS` overrides the path.
  - **All stations** (`s`): the curated `S01…Snn` list shipped in the code
    (`DEFAULT_STATIONS`, currently 12) — this is how the project pushes new
    stations without overriding the user's list.
  - **Names:** both lists now use the real broadcast names (icy): `VCR
    Auditorium | Venice Classic Radio Italia`, `VCR Classica+ | Venice Classic
    Radio Italia`, `NPO Klassiek`. At runtime an icy-name also overrides the
    JSON label (label is only a fallback; the v0.7.34 fix).
- **Footer (0.7.30+):** 3 rows — h-3 AI (`z:expand`, `c:change API Key` when
  NIM is active), h-2 dark-grey mid
  (`f:favorites s:all k:kb v:check`; update pill + `u:page U:apply` there; the
  `v` check result flashes here, works without AI), h-1 transport + version.
- **Docs:** `README.md` = short marketing appetite (tagline, screenshots,
  every paragraph links to the KB); **`KB.md`** = the complete reference
  (keys, menus, install recipes per distro incl. Omarchy, stations, config,
  env vars, updates, AI, FAQ) — **single source of truth; keep in sync every
  change** (see the DOCS rule above). `CHANGELOG.md` = release history.
  `screenshots/` = REAL captures of the running app (not mocks — the mock
  renderer was deleted so nothing overwrites them).
- **Update flow:** `update_watcher()` daemon thread checks at every startup
  (one immediate ETag check, then hourly). `U` self-updates in place; user
  prefers to run `U` themselves — never run `install.sh` for them unless asked.
  `v` forces a check mid-session.
- **AI enrichment:** Enricher thread, provider order opencode → ollama → API
  (`1/2/3` live-switch), cache keyed per track+provider, verified Wikipedia
  links. Defaults: model `gemma3:4b`; API base `https://api.openai.com/v1`
  (`MRADIO_API_BASE`), default `gpt-4o-mini`.

## Why mpv as the engine

Radio streams are messy (icecast metadata, HTTPS, reconnects). mpv handles all
of that battle-tested. mradio is a thin, colorful display + remote control over
mpv's IPC socket — decoding/network/metadata all belong to mpv.

## Architecture (map of `./mradio`)

- Constants: socket `/tmp/mpv-radio.sock`, default stream VCR1
  (`https://uk2.streamingpulse.com/ssl/vcr1`).
- `load_settings` / `seed_settings` — AI settings in
  `~/.local/share/mradio/settings.json` (self-contained; env vars are optional
  overrides, no shell rc needed).
- `load_cfg` / `persist_cfg` — `config.json`: provider, theme, volume, mouse.
- `Mpc` class — thin mpv IPC client (`cmd`, `get`).
- `repair_mojibake`, `split_title` — icy-metadata parsing (artist/title split).
- `Enricher` class — background-thread AI enrichment:
  - **Thread safety:** a single `self._lock` (`threading.RLock`) guards
    `cache` / `started` / `last_key` / `epoch` / `provider` / `offline_until`
    across the main thread and `_worker`; `persist_cache()` uses the same lock
    for the dict snapshot + the atomic file write.
  - Cache eviction (in `_worker`, under the lock) is FIFO:
    `pop(next(iter(cache)))` removes the OLDEST entry — never the just-written
    key; verified.
   - Provider order (live-switched with `1`/`2`/`3`): **opencode → ollama → API**.
   - `_llm_opencode` (`opencode serve`, zero-auth gateway), `_llm_ollama`,
     `_llm_openai` (any OpenAI-compatible: Groq, OpenRouter, Gemini, NIM…).
     Endpoints are built with `api_endpoint()` (`urljoin`-based), not
     concatenation.
   - **Choice 3 anti-hallucination:** `_ask` runs the prompt through
     `apply_provider_rules(prompt, provider)`; provider `openai` (choice 3)
     gets `SINCERITY_RULES` appended (never invent premiere/dedicatee/film/
     award facts, no cross-composer drift, wiki only if confident, short-but-
     true trivia). Choices 1/2 keep the stock prompt. Tests:
     `TestProviderRules`.
  - **opencode process hygiene:** `opencode.pid` pidfile stores `pid port`;
    `_oc_start` reaps a wedged instance we own before spawning, refuses to
    spawn if an untracked listener holds the port unhealthily, and kills a
    spawned serve that never becomes healthy; `shutdown()` reaps + clears it.
  - `_resolve_wiki` / `_relevant` — Wikipedia title resolution; link only shown
    if the article is verified to exist AND match (composer surname + token
    overlap).
  - Cache `~/.local/share/mradio/cache.json` keyed by track tag, **tagged with
    the provider that produced it** — a note is reused only when the same
    provider is selected.
- `render` — curses drawing; dark/light palette toggle with `p`. Artist/title/
  performer/work block and the wiki footer are shared helpers (`draw_info`,
  `draw_help`).
- **Color palettes** — `DARK_256`/`LIGHT_256`/`LIGHT_NAVY_256`/`LIGHT_MAUVE_256`
  = `{1..10: (fg, bg)}` xterm-256 indices; `DARK_PALETTE`/`LIGHT_PALETTE` are
  the ANSI fallbacks (fg only) with shared `CHIP_BG`. `SCHEMES =
  ("dark","light","light-navy","light-mauve")`; `p` calls `next_theme()` to
  rotate and `init_colors()` picks the 256 map when `curses.COLORS >= 256` else
  ANSI (new light arrangements fall back to classic light ANSI). Pair meaning:
  1 = arrows/version/theme/vol label, 2 = title (navy `18` in light-navy,
  royal `19` in mauve), 4 = composer/artist + meter, 5 = muted subtext (AI
  description/prose, drawn `+ A_DIM`), 6 = performer (cinnamon `130` / tan
  `137`), 7 = work label/spinner, chips 3/8/9/10 = RADIO, LIVE, PAUSED,
  UPDATE.
- `main()` — mpv reaping lives in `finally` (terminate → wait 2s → kill),
  guarded by `proc is not None`; all exit paths (q, Ctrl-C, exceptions, resize)
  reap mpv, run `Enricher.shutdown()`, and unlink the IPC socket.

## Key bindings

| Key | Action |
| --- | ------ |
| `q` | quit |
| `space` | pause/resume |
| `+`/`-` (or `→`/`←`) | volume up/down |
| `m` | mute |
| `r` | reconnect (revive dead stream/station) |
| `o` | open the verified Wikipedia article |
| `u` | open the release page when an update is available |
| `U` | auto-update in place (download validated release asset → restart) |
| ``v`` | force a version check now (flashes the result in the footer mid row) |
| `k`/`K` | open KB.md in the browser (player screen; `k` = cursor-up inside station menus) |
| `z` | expand/collapse full trivia note (full-screen) |
| `1`/`2`/`3` | pick AI provider (opencode/ollama/api) — re-fetches current track even if cached |
| `f` | open your favorites (`1-9`,`0` quick-pick — max **10**, pads work too; `~/.local/share/mradio/stations.json`) |
| `s` | open the all-stations list (`S01…Snn`; `a` adds the row to favorites) |
| `p` | rotate color schemes: `dark`, `light`, `light-navy`, `light-mauve` (remembered) |

## Full feature history (CHANGELOG)

- **0.7.8** — initial public release: full TUI, mpv IPC control, icy-metadata
  parsing with mojibake repair, AI enrichment with verified Wikipedia links,
  three providers, persistence, palette toggle, `--settings`, installers.
- **0.7.9** — `z` key + mouse-click expand/collapse full trivia; word-wrapping
  with `…` marker instead of silent cut.
- **0.7.10** — click-expand gated to the trivia text only (fixes greedy clicks
  stealing focus in mouse-first terminals like WezTerm).
- **0.7.11** — volume remembered between sessions (`+`/`-` saved to
  `config.json`, re-applied on startup / reconnect / mpv restart). Fixed: legacy
  `set` IPC rejected numerics (`invalid parameter`) → uses `set_property`.
- **0.7.12** — mouse-click toggling now **off by default** (`"mouse": 0`) so
  terminal text selection works; opt in with `"mouse": 1`.
- **0.7.13** — station name from stream's own icy-name metadata (instead of CDN
  host); optional second arg `<url> "<name>"` to override.
- **0.7.14** — thread-safety lock for all Enricher shared state; `urljoin`
  endpoint building; opencode pidfile + port-probe zombie prevention;
  guaranteed mpv/Enricher/socket cleanup on every exit path; render() dedup
  helpers; `make test` / `make smoke` / `test_mradio.py` (13 unit tests).
- **0.7.25** — station menu/picker (pick your stream at startup).
- **0.7.26** — reordered default stations + honest help line.
- **0.7.27** — picker keys `v`/`u`/`U`.
- **0.7.28** — **favorites vs all-stations split**: `f` = your `stations.json`
  list (seeded once, never touched again), `s` = curated `S01…Snn` (`a` adds
  a row), bare launch opens favorites, legacy `config.json` migration,
  `MRADIO_STATIONS`.
- **0.7.29** — favorites up to 10 (`1-9` then `0`); numpad digits resolve to
  the hot-picks (`_follow_esc`).
- **0.7.30** — 3-row footer (AI / mid + update pill / transport); help cleanup.
- **0.7.31** — mid row dark-grey (pair 5 + A_DIM); `z:expand` on the AI row;
  `f`/`s`/`v` on the mid row.
- **0.7.32** — **KB.md** created (full reference manual), linked from README.
- **0.7.33** — `k`/`K` opens KB in browser; `v` flash moved to the always-
  present mid row (works without AI); README install → points to rich KB
  install recipes; releases push `main` too.
- **0.7.34** — **icy-name wins again**: preset picks no longer lock the label,
  the stream's broadcast name replaces the short JSON name.
- **0.7.35/36** — README becomes a marketing piece with screenshots (initial
  mock renders, then CoreText attempts, then…).
- **0.7.38** — **real screenshots** of the running app replace the generated
  mocks (`screenshots/*.png`); mock renderer deleted.
- **0.7.39** — all-stations (`DEFAULT_STATIONS`) names updated to the real
  broadcast names (matches favorites).
- **0.7.40** — **favorites capped at 10** everywhere: seed `[:10]`, migration
  trimmed, `a` refuses when full, menu renders only the 10 hot rows.
- **0.7.54** — **choice-3 anti-hallucination prompt rules** (`SINCERITY_RULES`,
  applied only for the `openai` provider; never invent premiere/dedicatee/film/
  award facts, no cross-composer drift). Kept `_llm` methods intact.
- **0.7.55** — **stream data line**: unknown bitrate now prints `— kbps` (unit
  label always present), same as the fixed-format `cache Ns` / `stream mm:ss`
  slots.
- **0.7.56** — **update check honesty**: a `304` (GitHub CDN can answer
  "unchanged" for a changed feed) now triggers an unconditional re-fetch;
  `latest_release_version/tag` take the **max** version (not first entry);
  every `v` press force-refreshes after the instant flash. Fixes "up to date
  (v0.7.54)" persisting right after v0.7.55 shipped.
- **0.7.57** — footer volume hint now leads with the arrows:
  `← -/+ →:volume` (arrows double as volume keys).
- **0.7.58** — **NIM (NVIDIA) in-app setup**: press `3` to paste API key
  (TUI popup), `c` to change; `3=NIM` in UI; full AI installation guide in
  KB.md (OpenCode, Ollama local/Docker/remote, NIM signup+key).
- **0.7.59** — NIM API key popup fixed: placeholder is now light-grey hint
  text below an empty input (no more `nvapi-` prefix doubling on paste).
- **0.7.60** — NIM API key popup layout: hints pushed down a line; input is a
  full-width light-grey block with a rectangular terminal cursor that tracks
  typing/paste.
- **0.7.61** — **Ollama URL popup**: press `2` with no server configured (or
  `c` while provider 2 active) to set the server URL; three example hints;
  generic `prompt_text` popup drives both NIM key and Ollama URL flows.

## Env vars (optional overrides; settings.json is the source of truth)

- AI: `MRADIO_OLLAMA`, `MRADIO_OLLAMA_MODEL`, `MRADIO_OLLAMA_TIMEOUT`,
  `MRADIO_OLLAMA_NUM_GPU`, `MRADIO_API_BASE`, `MRADIO_API_KEY`, `MRADIO_MODEL`,
  `MRADIO_API_TIMEOUT`, `MRADIO_OPENCODE`, `MRADIO_OPENCODE_TIMEOUT`.
- Paths: `MRADIO_LOG`, `MRADIO_SERVE_LOG`, `MRADIO_CFG`, `MRADIO_CACHE`,
  `MRADIO_SETTINGS`.
- Updates: `MRADIO_REPO` (owner/name, default `Marcus1571/mradio`),
  `MRADIO_UPDATE_URL` (full releases URL), `MRADIO_UPDATE_INTERVAL` (seconds,
  min 60, default 3600). Update check is report-only: `update_watcher()`
  daemon thread → `check_update()` sends `If-None-Match: <etag>` to
  `releases.atom` (a `304` triggers an **unconditional re-fetch** — GitHub's
  CDN can answer "unchanged" for a feed that already changed) →
  `latest_release_version()` parses the body (the **max** version found wins,
  never the first entry) → compare with `ver_key()`; sets `state["update_url"]` →
  `draw_right` renders version (bottom-right in row h-1) + ` UPDATE ` pill
  (row h-2, pair 10 = black-on-yellow chip) → mouse zone `update_zone` and
  `u` key open it. Startup thread is `update_watcher` (loops forever), NOT
  single `check_update`. `_latest` = `{"version", "etag", "tag", "note"}`;
  `_check_lock` serializes all feed requests; `_forced_lock` guards the `v`-key
  path (`force_check(state)`), which refreshes `update_msg` with "checking…"
  then the `_latest["note"]` result. The tag feeds `apply_update()` which
  downloads
  `https://github.com/{REPO}/releases/download/{tag}/mradio`, validates with
  `compile()` + VERSION parse, backs up to `mradio.old`, `os.replace`s, and
  NEVER executes. `U` = apply (fallback browser on any failure), `u`/click =
  browser only. Hints: `u:page  U:apply  v:check`. Running from a git checkout
  refuses ("use git pull").
- Default model: `gemma3:4b`; default API base: `https://api.openai.com/v1`;
  default API model: `gpt-4o-mini`.
- Ollama telemetry reported (`eval=… rate=… tok/s`); low `rate` + idle GPU ⇒
  not GPU-offloaded → set `MRADIO_OLLAMA_NUM_GPU=999`.

## Development / verification

```sh
make check   # syntax checks (py_compile + bash -n install.sh)
make test    # unit tests (test_mradio.py — extract_json_item, split_title)
make smoke   # mradio --version / --help
```

(Lint/typecheck convention: none beyond `make check` — stdlib-only project.)

## Key terms / decisions

- Provider priority is **opencode → ollama → api**, first configured AND
  responding wins.
- OpenOCode route is slowest (20–90 s/track) but richest; spinner shows
  provider + elapsed (`▚ opencode 34s`).
- Trivia aimed at ~750–850 chars.
- Persisted files are written atomically (tmp + `os.replace`) and capped on
  load — can't corrupt or grow unbounded.
- Decide-and-keep: DO NOT change the provider fallback order, the Wikipedia
  verification logic (`_resolve_wiki` / `_relevant`), or the atomic-write
  pattern for cache.json / config.json — accepted as correct.

## Open questions / possible next steps

- Nothing outstanding. `.opencode/` (`MEMORY.md`, `BEHAVIOR.md`,
  `stationsproject.md`) is tracked in the repo. House rule: keep all of it,
  plus README and KB.md, in sync with every change.