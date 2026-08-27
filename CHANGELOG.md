# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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