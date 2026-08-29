# mradio — project memory

## IMPORTANT RULES BETWEEN US

- **`c.p` means: commit & push.** Whenever the user says `c.p`, do a full
  `git add` of the relevant files, commit with a clear message, and `git push`
  to origin — then confirm with the resulting commit hash. Never leave work
  uncommitted/unpushed after a task; committing AND pushing correctly is
  critical and has been the source of past mistakes.

> Read this first in every session so we can pick up where we left off.
> Update it whenever the project state changes significantly.

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

- Single self-contained file: `./mradio` (~1058 lines), Python 3.8+, **stdlib
  only, no pip dependencies**.
- Repo: `git@github.com:Marcus1571/mradio.git` (user: `Marcus1571`).
- No local demo branch conventions — trivial `main` history, semantic-version
  tags released on GitHub (`v0.7.x`).

## Current state

- **Latest version:** `0.7.24` (in-code `VERSION`; released tag + GitHub
  Release with assets, `Latest`).
- **Palettes:** `p` rotates `dark` → `light` → `light-navy` → `light-mauve`
  (256-color Catppuccin-inspired, ANSI fallback; pair 5 = muted subtext).
- **Sub-project — station presets:** see `.opencode/stationsproject.md` for
  the living candidate/approved station list. **The user personally approves
  each station; the assistant must NEVER add stations to the file on its own
  initiative.** Approved: `WQXR`, `Radio Swiss Classic` (label "Swiss Classic
  I" — Italian feed). **Implemented (unreleased, on `main`):** `mradio` now
  starts in a "Preselected stations" picker when launched without a URL, and
  `s` opens it anytime; presets in `config.json` key `stations`, defaulting
  to the 12 stations in the doc (see `DEFAULT_STATIONS` in `./mradio`).
- **Latest release:** `0.7.20` (tag + GitHub Release, assets mradio/install.sh).
  The U self-update flow was validated live earlier (v0.7.18 → v0.7.19 → apply
  on restart) and is documented as tested in the 0.7.20 changelog.
- **0.7.21 work (uncommitted until c.p'd):** `v` key forces a version check
  without quitting — `force_check(state)` serializes via `_forced_lock` /
  `_check_lock`, flashes outcome via `_latest["note"]` → `update_msg`
  ("new version vX — press U" / "up to date (vX)" / "check failed"). Hints now
  `u:page  U:apply  v:check`. 25 unit tests.
- **NOTE:** user prefers to update locally themselves via the `U` key
  (self-update) — do NOT run `install.sh` for them unless asked.

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
| `v` | force a version check now (flashes the result in the AI row) |
| `z` | expand/collapse full trivia note (full-screen) |
| `1`/`2`/`3` | pick AI provider (opencode/ollama/api) — re-fetches current track even if cached |
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
- **0.7.14** *(unreleased)* — thread-safety lock for all Enricher shared state;
  `urljoin` endpoint building; opencode pidfile + port-probe zombie prevention;
  guaranteed mpv/Enricher/socket cleanup on every exit path; render() dedup
  helpers; `make test` / `make smoke` / `test_mradio.py` (13 unit tests).

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
  `releases.atom` (a `304` is logged and skipped) → `latest_release_version()`
  parses the body → compare with `ver_key()`; sets `state["update_url"]` →
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

- 0.7.14 fixes are uncommitted; when the user wants, commit + tag `v0.7.14`
  + push (only when asked).
- `.opencode/MEMORY.md` and `.opencode/` are untracked — decide whether to
  commit them (recommended) or keep them local.