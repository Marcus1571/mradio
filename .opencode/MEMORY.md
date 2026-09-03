# mradio — project memory

> Read this first in every session so we can pick up where we left off.
> Update it whenever the project state changes significantly.

## How to govern (rules live in BEHAVIOR.md)

All **permanent rules** — commit & push by default, the four documentation
duties, release discipline, the update flow ("user runs `U`, never
`install.sh` unless asked"), verification limits — live in
**`.opencode/BEHAVIOR.md`**. Do **not** copy rules into this file; reference
`BEHAVIOR.md` instead so a rule lives in exactly one place (duplicating rules
here is how stale/contradictory rules slipped in before).

Reference docs live in their canonical homes and are **not** duplicated here:
`KB.md` = features/keys/config/env-vars (single source of truth), `CHANGELOG.md`
= release history, `findings.md` = station research log (repo root).

## What it is

`mradio` — a colorful terminal radio player (Python `curses` TUI) that drives
**mpv** as its audio engine over an IPC socket, plus optional **AI enrichment**
(trivia note / Work line / verified Wikipedia link) for the now-playing track.

- Single self-contained file: `./mradio` (~2500 lines), Python 3.8+, **stdlib
  only, no pip dependencies**.
- Repo: `git@github.com:Marcus1571/mradio.git` (user: `Marcus1571`).
- Semantic-version tags released on GitHub (`v0.7.x`) — a release is the
  GitHub **Release** (tag + assets), not just a tag.

## Current state

- **Latest version / release:** `0.7.87` (in-code `VERSION`, GitHub Release
  `v0.7.87` marked `Latest`, assets `mradio` + `install.sh`). `main` kept in
  sync with every release.
- **Palettes:** `p` rotates `dark` → `light` → `light-navy` → `light-mauve`
  (256-color Catppuccin-inspired, ANSI fallback; pair 5 = muted subtext).
- **Station model:** you own ONE list — your **favorites** — browsed two ways.
  - **Favorites** (`f`): `~/.local/share/mradio/stations.json` (key
    `"favorites"`), **12 slots** (`1-9`, #10 = `0`, 11-12 via arrows). Seeded
    once on first run from the first 12 of `DEFAULT_STATIONS`; legacy
    `config.json` `"stations"` migrated once. Releases never touch it.
    `MRADIO_STATIONS` overrides the path.
  - **Genres** (`g`): a chooser grouping favorites by genre — Classical(1) /
    Jazz(2) / Blues(3) / Country(4) / Rock(5) / Pop(6) / Focus(7) / Chill(8) /
    Funk(9), with **Other last, rendered as the literal `0` slot**. Pick a
    number to open that genre's submenu. Every curated genre aggregates the
    curated `DEFAULT_STATIONS` for that genre + favorites (de-duplicated); only
    **Other** stays favorites-only. `genre_stations_for()` = per-genre list;
    `genre_station_counts()` backs the chooser counts.
  - **Genre classification:** every favorite gets a `genre` field; auto-tagged
    on load by name via `genre_of()` (`_GENRE_KEYWORDS`); unknown names fall
    into **Other**. `DEFAULT_STATIONS` entries carry explicit `genre`.
  - **Names:** both lists use real broadcast (icy) names. At runtime an
    icy-name overrides the JSON label (label is only a fallback).
  - **Edit mode** (`e`): `s` = select-to-move, `d` = delete slot under `▶`,
    `Enter` = move landing slot pushing others down; `*` adds a station to
    favorites (fills next free slot). Deleted slots stay `— empty` and are
    persisted as `null` (numbering never shifts).
- **Update flow:** `update_watcher()` daemon checks at startup (immediate ETag
  check, then hourly). `U` self-updates in place (validates + backs up, never
  executes). **The user runs `U` themselves — never `install.sh` unless asked.**
  `v` forces a check mid-session.
- **AI enrichment:** Enricher thread, provider order opencode → ollama → API
  (`1/2/3` live-switch), cache keyed per track+provider, verified Wikipedia
  links. Defaults: model `gemma3:4b`; API base `https://api.openai.com/v1`
  (`MRADIO_API_BASE`), default `gpt-4o-mini`.
- **Footer:** 3 bands — AI row (`z:expand`, `c:change API Key`), dark-grey mid
  (`f g k v` + update pill `u`/`U`), transport (`+/-/→/←` volume, `m` mute, `q`,
  version bottom-right).

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
- `load_cfg` / `persist_cfg` — `config.json`: provider, theme, volume, mouse,
  `last_url`/`last_name`.
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
  ANSI (new light arrangements fall back to classic light ANSI).
- `main()` — mpv reaping lives in `finally` (terminate → wait 2s → kill),
  guarded by `proc is not None`; all exit paths (q, Ctrl-C, exceptions, resize)
  reap mpv, run `Enricher.shutdown()`, and unlink the IPC socket.

## Development / verification

```sh
make check   # syntax checks (py_compile + bash -n install.sh)
make test    # unit tests (test_mradio.py)
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
- **Update flow:** the user runs `U` to self-update — never `install.sh`
  unless asked (see BEHAVIOR.md rule 5).

## Open questions / possible next steps

- ⏳ **PENDING (remind each work batch until it arrives):** user will supply
  NEW screenshots to replace the current ones in `screenshots/`.
- Project docs tracked in-repo: `.opencode/` (`MEMORY.md`, `BEHAVIOR.md`,
  `stationsproject.md`) + `findings.md` + README + KB.md. Keep in sync with
  every change — but hold each piece of content in its one canonical home (no
  duplication across these files).
