# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **README rewritten as a short marketing piece** — tagline, appetizers for
  every feature, real screenshots (`screenshots/player.png`,
  `screenshots/favorites.png`, `screenshots/all-stations.png`), and a
  KB-link after every paragraph. The full details stay in KB.md. Screenshots
  are re-renderable via `make screens`.

## [0.7.34] - 2026-08-29

### Fixed

- **Preset picks show the full `icy-name` again.** A station picked from the
  menus used the short `stations.json` label instead of the stream's
  broadcast name (e.g. `VCR Auditorium | Venice Classic Radio Italia`) because
  the pick path locked the name before `icy-name` could arrive. The JSON name
  is now only a connecting/fallback label; `icy-name` takes over when it
  broadcasts — matching hand-typed URL behavior.
- **README/install list:** the KB Arch branch now includes **Omarchy** (Arch
  family) alongside Manjaro/EndeavourOS.

## [0.7.33] - 2026-08-29

### Fixed

- **`v` flashes its result again** even without AI configured — the check
  status now shows in the always-present footer mid row, not only on the
  AI-only row.

### Added

- **`k` / `K` opens the knowledge base in your browser** (player screen; shown
  as `k:kb` in the footer mid row). Points at the repo's `KB.md`, fork-aware.
- **README install section now points to the KB**, which gained full
  step-by-step install recipes: macOS (Homebrew → mpv → mradio), Debian/
  Ubuntu/Mint (apt), Fedora (dnf), Arch/Manjaro/EndeavourOS (pacman), and
  WSL — plus `PATH` setup and verification steps.
- **Repo hygiene:** releases now push `main` too, so the repo always reflects
  the latest release (not just the tag).

## [0.7.32] - 2026-08-29

### Added

- **`KB.md` — full knowledge base** (linked from the README header): every key,
  both station menus, favorites/all-stations model, the self-update flow,
  AI enrichment providers + cache, complete `MRADIO_*` environment variable
  table, config/persistence reference, troubleshooting FAQ, development notes
  and a privacy section.

## [0.7.31] - 2026-08-29

### Changed

- **Three-row footer colors/roles:** mid row (`f:favorites  s:all  v:check`
  + `u:page`/`U:apply` on update) is now **dark grey**, `z:expand`/`z:collapse`
  moved up to the AI row, and the bottom row keeps the transport keys
  (`q`/`space`/`+`/`-`/`m`/`r`).

## [0.7.30] - 2026-08-29

### Changed

- **Player footer is now three rows** so the hints don't overflow: AI provider
  line on its own (row three from bottom), update row on row two
  (`v:check`, plus `u:page`/`U:apply` when an update exists), and the main
  key legend (`q`…`z`) on the bottom row. Applies to the detail view too.

## [0.7.29] - 2026-08-29

### Fixed

- **Favorites go to 10** — keys `1-9` then `0` for the 10th; the menu labels
  the last row `0`.
- **Numeric pad == main row.** Keypad digits (sent as `Esc`-prefixed sequences
  by macOS/Unix terminals) are resolved so `1-0` hot-picks the same favorite
  from the pad; pad Enter acts like Enter.

## [0.7.28] - 2026-08-29

### Added

- **Favorites vs. full list.** Your numbered quick-pick list now lives in its
  own file, `~/.local/share/mradio/stations.json` (key `"favorites"`), pointed
  to by **`f`** and seeded once from the curated selection on the first run —
  afterwards it is entirely yours and releases never touch it again.
  **`s`** now opens the full **all-stations** list labeled `S01…Snn`
  (arrows/Enter to choose), which we can keep growing every release. Press
  **`a`** inside it to copy the highlighted station into your favorites.
  Bare launch opens favorites. A legacy `stations` key in `config.json` is
  honored and migrated into `stations.json` on the first run. `MRADIO_STATIONS`
  overrides the file path.

## [0.7.27] - 2026-08-29

### Fixed

- **`v` (and `u`/`U`) now work inside the station picker** — they were dead
  keys until a station was selected. `v` runs a version check and flashes the
  result in the picker's message row; `u`/`U` open/apply an update when the
  `UPDATE` pill is showing — identical to the player screen.

## [0.7.26] - 2026-08-29

### Changed

- **Preset-station order matches the auditioned priority:** VCR Auditorium,
  VCR Classica+, Radio Swiss Classic, Naim Classical, WQXR, Classic FM,
  Swiss Jazz, Radio Paradise, radio klassik Stephansdom, NPO Radio 4,
  France Musique, BBC Radio 3.
- **Picker help now tells the truth about `q`/`Esc`:** inside the station
  menu `q`/`Esc` return to the player (press again to quit); at bare launch
  they quit. `Esc` is equivalent to `q` everywhere in the TUI.

## [0.7.25] - 2026-08-29

### Added

- **Preselected-stations picker.** Launching `mradio` with no stream URL now
  shows a picker first; `s` opens it anytime from the player. Choose with
  `1-9` (quick-pick) or arrows/Enter; `s`/`Esc` returns to the player. The
  preset list lives in `config.json` under `"stations"` (list of
  `{name, url}`), defaulting to the 12 stations tracked in
  `.opencode/stationsproject.md`.

## [0.7.24] - 2026-08-28

### Changed

- **AI description no longer shares the title's color.** The trivia note gets
  its own muted "subtext" slot (pair 5, a dim grey on light themes,
  lavender-grey on dark) instead of being the title color + `A_DIM`. A bold
  colorful title (e.g. navy in `light-navy`) can no longer be confused with
  the body text.

## [0.7.23] - 2026-08-28

### Changed

- **`p` now rotates through four color schemes** — `dark`, `light`,
  `light-navy`, `light-mauve` — so arrangements can be compared live on one
  key. The header shows the active scheme name.

### Added

- **Light-theme arrangements.** `light-navy` (navy-bold title `#000087`,
  cinnamon-brown performer `#AF5F00`, teal composer, amber work label) and
  `light-mauve` (royal-blue title, tan performer, mauve accents). Classic
  `light` (Latte) is kept unchanged as the starting point for comparison.

## [0.7.22] - 2026-08-28

### Added

- **Catppuccin-inspired color palettes.** When the terminal reports 256 colors,
  mradio now uses a proper chromatic palette — Mocha-inspired for the dark
  theme, Latte-inspired for the light theme — instead of bare ANSI hues:
  one accent family per theme, muted "subtext" tones for secondary lines, and
  chips (RADIO / LIVE / PAUSED / UPDATE) with high-contrast on-chip text. Old
  ANSI colors remain as a fallback on 8-color terminals.

## [0.7.21] - 2026-08-28

### Added

- **`v` key forces an update check** without quitting: runs one background
  check on demand (serialized if another check is in flight) and flashes the
  outcome in the AI row — "new version vX.Y.Z — press U", "up to date
  (vX.Y.Z)", or "check failed".

## [0.7.20] - 2026-08-28

### Changed

- **Update / self-update flow tested end-to-end on a live install.** On a
  machine running v0.7.18 the release-check lit up the `UPDATE` pill for
  v0.7.19, and pressing `U` downloaded the release's `mradio` asset, validated
  it (syntax + version), backed the running file up to `mradio.old`,
  atomically swapped it, and the update was applied on restart — confirmed
  clean (v0.7.18 → v0.7.19 → next launch on the new version). This release
  (version bump, no functional changes) re-pins the tested flow with the
  `mradio` + `install.sh` assets.

## [0.7.18] - 2026-08-28

### Added

- **Self-update on `U`:** when the `UPDATE` pill is showing, uppercase `U`
  downloads the newest release's `mradio` asset, validates it (Python syntax
  check + version parse, must be newer than the running version), backs up the
  running file to `mradio.old` and atomically swaps it in place. The
  downloaded code is never executed — the new file runs on the next restart. A
  short status message replaces the AI row for a few seconds. `u` still opens
  the release page; any failure (unwritable dir, release without the asset,
  git-checkout run, validation error) falls back to opening the release page.

## [0.7.17] - 2026-08-28

### Changed

- **Dummy placeholder release (version bump only, no functional changes).**
  Released so the in-app `UPDATE` pill can be validated end-to-end against a
  release newer than the currently installed binary.

## [0.7.16] - 2026-08-28

### Changed

- **Update check now runs hourly while mradio is open** (the app may stay up
  for days, so a release cut mid-session still lights up the `UPDATE` pill).
  Checks are conditional requests — the feed's ETag is sent back so an
  unchanged feed returns `304` and doesn't consume GitHub's rate limit
  (anonymous REST cap is 60 req/hr; we do 24/day and effectively ~0 after
  ETags). Cadence configurable via `MRADIO_UPDATE_INTERVAL` (seconds, min 60).
- **`UPDATE` pill restyled:** black text on a yellow chip (pair 10) so it
  stands out from the cyan RADIO badge.

## [0.7.15] - 2026-08-28

### Added

- **In-app update check (report-only):** on startup mradio makes one lightweight
  request to the GitHub releases feed. The current version is shown at the
  bottom-right corner, and if a newer release exists a clickable `UPDATE` pill
  (or the `u` key) opens the release page so you can upgrade. It never downloads
  or runs code automatically. Configurable via `MRADIO_REPO` /
  `MRADIO_UPDATE_URL`.

## [0.7.14] - 2026-08-28

### Fixed

- **Thread safety:** `Enricher.cache`/`started`/`last_key`/`epoch`/`provider`/
  `offline_until` were read and written from both the main thread and the
  enrichment worker with no lock (only the cache file write was guarded).
  All shared state now goes through a single `RLock`, so behavior no longer
  depends on GIL timing.
- **URL construction:** the ollama and OpenAI-compatible endpoints were built
  by string concatenation / `rstrip("/")`, which breaks `MRADIO_API_BASE`
  values carrying an existing path segment. Both now resolve through
  `urllib.parse.urljoin` (via `api_endpoint()`), and a base that already ends
  in `/chat/completions` is left untouched.
- **opencode process management:** `_oc_start` always spawned a fresh
  `opencode serve` on failure, even when a previous instance on the same port
  was alive but wedged, letting zombies pile up over long sessions. It now
  keeps a pidfile (`opencode.pid`), reaps a wedged instance it owns before
  spawning, refuses to spawn when an untracked listener holds the port
  unhealthily, kills a spawned serve that never becomes healthy, and reaps the
  process on shutdown.
- **Cleanup on every exit path:** `main()` only terminated mpv on the normal
  `q` path; an exception mid-loop (or terminal-resize edge cases) left mpv
  running with audio playing after the TUI died. mpv termination is now in
  `finally` and guarded so KeyboardInterrupt / exceptions always reap mpv,
  shut the Enricher down, and unlink the IPC socket.

### Changed

- `render()` extracts the duplicated artist/title/performer/work block and the
  wiki-link footer conditional into shared helpers (`draw_info`, `draw_help`).

### Added

- `make test` — stdlib `unittest` suite (`test_mradio.py`, 13 cases) covering
  `extract_json_item()` against malformed LLM output (missing fields, trailing
  prose, nested braces, markdown fences, escaped quotes) and `split_title()`
  against real icy-title samples with cp1252 mojibake repair.
- `make smoke` — runs `mradio --version` / `--help`.

## [0.7.11] - 2026-08-27

### Added

- Volume is remembered between sessions: `+`/`-` saves it to `config.json` and
  it is re-applied on startup, on `r` reconnect, and on automatic mpv restarts.

### Fixed

- Restoration used mpv's legacy `set` IPC command, which rejects numeric values
  (`invalid parameter`), so the volume silently reset to 100% every session —
  now applied via `set_property`.

## [0.7.12] - 2026-08-27

### Changed

- **Interactive trivia view (continued from 0.7.9/0.7.10):** mouse-click toggling
  is now **off by default** (`"mouse": 0` in `config.json`) so the terminal's
  native text selection works normally again; set it to `1` to re-enable
  click-to-expand. The `z` key is unaffected.

## [0.7.13] - 2026-08-27

### Added

- The station name in the top bar now comes from the stream's own icy-name
  metadata (e.g. `VCR Auditorium | Venice Classic Radio Italia`) instead of the
  CDN host; an optional second argument `mradio <url> "<name>"` overrides it.

[0.7.13]: https://github.com/Marcus1571/mradio/releases/tag/v0.7.13

[0.7.12]: https://github.com/Marcus1571/mradio/releases/tag/v0.7.12

[0.7.11]: https://github.com/Marcus1571/mradio/releases/tag/v0.7.11

[0.7.10]: https://github.com/Marcus1571/mradio/releases/tag/v0.7.10

### Fixed

- **Interactive trivia view (introduced in 0.7.9):** click toggling was too
  greedy — any click anywhere in the window expanded/collapsed it, which stole
  plain clicks meant to focus or select the terminal in mouse-first terminals
  (e.g. WezTerm). Clicks now expand/collapse only when they land on the trivia
  text itself; clicks on empty rows, the header, the meters or the help lines
  fall through untouched, so focusing the terminal no longer flips the view.

[0.7.10]: https://github.com/Marcus1571/mradio/releases/tag/v0.7.10

## [0.7.9] - 2026-08-27

### Added

- `z` toggles a full-screen view of the current trivia note (clicking the text
  with the mouse toggles it too), and auto-collapses when the station moves to
  a new track.
- Help lines updated (`z:expand` / `z:collapse`) and README/docs extended.

### Fixed

- Trivia in the normal view was hard-sliced at the column width, splitting words
  mid-way, and surplus lines were dropped silently. It now word-wraps, and a
  note that does not fit the window is marked with `…` instead of being cut
  without a trace.

[0.7.10]: https://github.com/Marcus1571/mradio/releases/tag/v0.7.10

[0.7.9]: https://github.com/Marcus1571/mradio/releases/tag/v0.7.9

## [0.7.8] - 2026-08-27

Initial public release. A single-file, stdlib-only terminal radio player that
drives `mpv` and adds optional AI enrichment for the now-playing track.

### Added

- Full-color `curses` TUI — one self-contained Python file, no pip dependencies.
- `mpv` as the audio engine, remote-controlled over an IPC socket: pause,
  volume, mute, reconnect, real stream metadata and elapsed time.
- Live icy-metadata parsing with mojibake repair and artist/title splitting;
  plays Venice Classic Radio by default or any stream URL.
- AI enrichment (fully opt-in, silent fallback): a trivia note about the work,
  a `Work:` line when the tag was only a movement/fragment, and a Wikipedia
  link — the article is verified to exist *and* match before it is ever shown.
- Three AI providers, switchable live with `1`/`2`/`3`:
  - **opencode** headless server (zero-auth gateway) — default in this build;
  - **ollama** — a local instance or one on your LAN (`localhost:11434` default);
  - **any OpenAI-compatible API** (Groq, OpenRouter, Gemini, NVIDIA NIM, …).
- Per-provider timing and ollama telemetry in the logs; the display shows the
  full trivia text, uncut.
- Persistence: `config.json` (provider + color theme), `cache.json`
  (enrichment cache tagged with the provider that produced it), `settings.json`
  (all AI settings self-contained; shell env vars still work as overrides).
- Instant dark/light palette toggle with `p`, remembered across sessions.
- `mradio --settings` prints the effective configuration (API keys masked).
- `install.sh` / `Makefile` installers and a `make check` syntax target.

[0.7.8]: https://github.com/Marcus1571/mradio/releases/tag/v0.7.8