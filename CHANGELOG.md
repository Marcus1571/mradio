# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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