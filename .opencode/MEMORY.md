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

- **Latest version / release:** `0.7.67` (in-code `VERSION`, released tag +
  GitHub Release with assets `mradio` + `install.sh`, verified `Latest`).
  `main` is kept in sync with every release (push `main` alongside each tag).
- **Palettes:** `p` rotates `dark` → `light` → `light-navy` → `light-mauve`
  (256-color Catppuccin-inspired, ANSI fallback; pair 5 = muted subtext).
- **Station model (0.7.63+):** you own ONE list — your **favorites** — browsed
  two ways.
  - **Favorites** (`f`): user's list in
    `~/.local/share/mradio/stations.json` (key `"favorites"`), max **10** hot
    slots (`1-9` + `0`; numpad digits resolve via `_follow_esc`). Seeded once,
    on first run, from the **first 10** of `DEFAULT_STATIONS`; legacy
    `config.json` `"stations"` migrated once (trimmed to 10). Releases never
    touch it. `MRADIO_STATIONS` overrides the path.
  - **Genres** (`s`, 0.7.63+): a chooser grouping your favorites by genre —
    Classical / Jazz / Blues / Other. Genres with no favorites are hidden.
    Pick a number to open that genre's submenu, then pick a station. The flat
    all-stations catalog (`S01…Snn`) and the `a` add-to-favorites key were
    **removed** (0.7.63).
  - **Curated stations in genre submenus (0.7.65+):** the **Classical**,
    **Jazz** and **Blues** genre submenus pull in the curated stations for that
    genre from `DEFAULT_STATIONS` (de-duplicated against favorites), so those
    genres have content even when the 10-slot favorites list is full. As of
    0.7.67 Classical aggregates too (only **Other** stays favorites-only). The
    favorites file is never touched. `genre_stations_for()`
    = the per-genre list; `genre_station_counts()` backs the chooser counts.
  - **Curated rosters (0.7.67):** Jazz **10** (Swiss Jazz fav + WBGO, WWOZ,
    KCSM 91.1, KJAZZ 88.1, Jazz24, 1.FM Adore Jazz, TSF Jazz, JazzRadio 106.8
    Berlin, KMHD), Blues **10** (Jazz Radio Blues, Blues Radio Greece, Blues
    Music Fan, Blues Rock Cafe, 1.FM Blues, 181.FM True Blues, Buddy Guy Radio
    Legends, WDCB 90.9, exclusive BB King, Radio Caprice Chicago Blues),
    Classical **12 curated** (adds WCRB, KUSC, WFMT to the existing curated
    classical; displays 12 = 7 favs + 5 curated-not-favorite). Every new one
    was **live-verified** (mpv-decoded audio, bitrate + icy-title confirmed).
    KMHD added for Jazz (direct AAC URL), Radio Caprice Chicago Blues for the
    blues 10th slot (user's 61 Blues pick wasn't verifiable). Full URL/bitrate/
    votes log in `findings.md`.
  - **Genre classification:** every favorite gets a `genre` field; auto-tagged
    on load by name via `genre_of()` (`_GENRE_KEYWORDS`); unknown names fall
    into **Other**. `DEFAULT_STATIONS` entries carry explicit `genre`.
  - **Names:** both lists now use the real broadcast names (icy): `VCR
    Auditorium | Venice Classic Radio Italia`, `VCR Classica+ | Venice Classic
    Radio Italia`, `NPO Klassiek`. At runtime an icy-name also overrides the
    JSON label (label is only a fallback; the v0.7.34 fix).
- **Footer (0.7.30+):** 3 rows — h-3 AI (`z:expand`, `c:change API Key` when
  NIM is active), h-2 dark-grey mid
  (`f:favorites g:genres k:kb v:check`; update pill + `u:page U:apply` there;
  the `v` check result flashes here, works without AI), h-1 transport + version.
- **Docs:** `README.md` = short marketing appetite (tagline, screenshots,
  every paragraph links to the KB); **`KB.md`** = the complete reference
  (keys, menus, install recipes per distro incl. Omarchy, stations, config,
  env vars, updates, AI, FAQ) — **single source of truth; keep in sync every
  change** (see the DOCS rule above). `CHANGELOG.md` = release history.
  `screenshots/` = REAL captures of the running app (not mocks — the mock
  renderer was deleted so nothing overwrites them).
  ⏳ **PENDING (remind weekly/at each work batch):** user will supply NEW
  screenshots to replace the current ones — keep nagging until they arrive.
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
| `f` | open your favorites (`1-9`,`0` quick-pick for slots 1-10 — `0` = #10; slots **11-12** via arrows; `~/.local/share/mradio/stations.json`, **12 slots**) |
| `g` | open the genre chooser (your favorites grouped: Classical / Jazz / Blues / Country / Rock / Pop / Focus / Chill / Other); number = open that genre's submenu, `0` = last (Other) |
| `e` | **edit mode** (favorites/genre): `s` = select-to-move (light-blue), `d` = delete slot under `▶`; `Enter` = move to landing slot, pushing others down |
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
- **0.7.62** — **Spinner label fix**: in-play AI spinner now shows the
  display name (`NIM`) instead of internal `openai`.
- **0.7.66** — **curated Jazz & Blues expanded to 9 each, re-ranked**: added
  Jazz24, 1.FM Adore Jazz, TSF Jazz, JazzRadio 106.8 Berlin to Jazz and Jazz
  Radio Blues, Blues Radio Greece, Blues Music Fan, Blues Rock Cafe, Buddy Guy
  Radio Legends, exclusive BB King to Blues; dropped Adroit Jazz Underground
  & SomaFM Secret Agent (not live-verifiable). Every station live-verified via
  mpv; higher bitrate + icy-title preferred; `findings.md` updated.
- **0.7.84** — **Volume & mute global**: `+`/`=`/`→` up, `-`/`←` down, `m`
  mute — work inside the favorites/genre menus too (shared `vol_key()` helper
  used by both the player and menu loops). Tests → 104 pass.
- **0.7.83** — **`Space` = `Enter` for selections**: play/move/pick genre accept
  `Space`; confirmation popups (delete confirm) still need `Y`/`del`/`Enter` not
  `Space`. Nav hints read `Enter/Space:play|:move|:pick`. Tests → 103 pass.
- **0.7.82** — **Slots 16 → 12**: `MAX_FAV = 12` (`1`-`9`, #10 = `0`, 11-12 via
  arrows). Tests → 103 pass.
- **0.7.81** — **Edit mode + move + 16 slots**: `e` toggles edit mode (`EDIT`
  chip between `SELECT` and theme), replacing delete mode; `s` = select-to-move
  (full-width light-blue, pair 13), `d` = delete slot under `▶`, `Enter` =
  move to landing slot pushing the rest down. Favorites now have **16** slots
  (#10 = `0`; 11-16 via arrows; `MAX_FAV`, `slot_tag`, `move_favorite`). `s`
  now selects in edit mode, so **`g`** opens genres everywhere (`s:genres` → `g:genres`).
  Count hint = occupied slots. Tests → **103 pass**.
- **0.7.80** — **fav menu footer**: lead-in reads `1-9,0:pick  ↑/↓` (dropped
  the `:move` label).
- **0.7.79** — **Favorites menu footer lead-in**: `1-9,0:pick  ↑/↓:move` moved
  to the top footer band, left of `pick a number — N favorite(s)`; dropped from
  the mid housekeeping row. Tests → 99 pass.
- **0.7.78** — **Two-band footer** (narrow-terminal fix): menus use a stacked
  three-band footer — dynamic message (slot count / delete-mode note) on its own
  row, housekeeping (`pick move s v d:delete l last i u/U`) on the mid row,
  `q/ESC`+`Enter` on the bottom row; player already split. Footer text clips to
  the pill/version right-hand zone so keys never collide. Primary nav never
  clipped. Tests → 99 pass.
- **0.7.77** — **`d:delete` maintenance**: from a favorites/genre submenu, `d`
  toggles a black-on-red `DELETE MODE` chip; pick a slot (number or `↑/↓`),
  confirm via popup (`Y`/`del`/`Enter`). Deleted slots **stay empty** — menu
  renders `— empty`, numbering never shifts, persisted as `null` and survives
  restarts; `i` (URL add) fills the first empty slot. Favorites become
  slot-preserving (`None` placeholders through load/norm, genre functions,
  render, play). Tests → 98 pass.
- **0.7.76** — **`MUTED` badge (spelling)**: the centered mute indicator reads
  `MUTED` (not `MUTE`).
- **0.7.75** — **Mute badge centered in the volume bar**: instead of `vol
  MUTED` to the left, a black-on-red **`MUTE`** chip (color pair 12) sits
  centered inside the graphical meter while muted; stored level still shows as
  `%` on the right. Tests → 89 pass.
- **0.7.74** — **`i:input` — add a stream URL on the fly**: shown in the
  mid/footer line to the right of `l:last played`; `i` prompts for any http(s)
  URL, plays it immediately, and saves it as a favorite (dedup by URL, genre
  derived from host name via `parse_stream_url`/`upsert_favorite` helpers).
  Works from menus and the player. Tests → 87 pass.
- **0.7.73** — **startup timing logged**: `startup: X.XXs to UI (v…, menu=…,
  last_url=yes/no, provider=…)` written to `mradio.log` before the UI renders,
  making a slow launch diagnosable from logs.
- **0.7.72** — **resume the last-played station** via `l`: the app remembers
  the most recent station (url+name in `config.json` `last_url`/`last_name`)
  and offers **`l:last played`** to the right of `v:check`; `l` tunes it from
  any menu or the player. `persist_cfg` gained `last_url`/`last_name`;
  `save_last_station()` persists on every switch/start. Tests → 85 pass.
- **0.7.71** — **update check no longer looks "stuck":** while a GitHub feed
  fetch is in flight, `checking for updates…` shows a `▚/▞` spinner + elapsed
  seconds so a slow check never appears frozen, and always resolves to a real
  result (`up to date` / `new version vX.Y.Z — press U` / `check failed
  (offline?)`). Single 6s fetch budget (`CHECK_TIMEOUT`). New `check_msg()`
  helper centralizes the ~5s flash. Tests → 82 pass.
- **0.7.70** — **new Focus (7) & Chill (8) genres, 10 curated each** (the user's
  "concentration" request, split into two): Focus = Space Station Soma (320k),
  Ambient Sleeping Pill, Drone Zone, Groove Salad, Cryosleep, Deep Space One,
  Radio Caprice Relaxation, Total Instrumental, Yoga Chill, Radio Art Deep
  Focus; Chill = 1.FM Chillout Lounge, Chilltrax, Café del Mar, Smooth Chill,
  Antenne Bayern Chillout, SomaFM Fluid, Costa del Mar Chillout & Zen, Jazz
  Lounge, Hi On Line Lounge. All live-verified via mpv. `genre_of` learned
  focus/chill keywords. Picker order now 1-8 = Classical/Jazz/Blues/Country/
  Rock/Pop/Focus/Chill, **Other = literal "0"** slot. Both aggregate curated +
  favorites. Favorites untouched.
- **0.7.69** — **new Rock (5) & Pop (6) genres, 10 curated each**: Rock =
  Radio Caroline, Virgin Classic Rock, Rock Antenne, Arrow Classic Rock,
  1.FM Classic Rock Replay, SomaFM Left Coast 70s, Radio ROKS Hard'n'Heavy &
  Ballads, 181.FM Rock 181, Hard Rock Heaven; Pop = Capital FM London,
  Heart 80s & 70s, Radio 105 Italy, LOS 40 España, Radio 538, Energy Zürich
  NRJ, 1.FM Absolute TOP 40, SWR3, Chocolate FM. All live-verified via mpv
  (audio + bitrate + icy-title). `genre_of` learned rock/pop keywords. Picker
  order now 1-6 = Classical/Jazz/Blues/Country/Rock/Pop, **Other = literal "0"**
  slot. Rock/Pop aggregate curated + favorites. Favorites untouched.
- **0.7.68** — **new Country genre (category 4) + Other → "0" slot**: 10 curated
  Country stations live-verified (WSM 650 AM, .977 Country, 1.FM Absolute &
  Classic Country, 181.FM Highway/Kickin'/Real Country, KIX Country, Big R
  Radio Country, Country Radio). Picker order is now 1 Classical, 2 Jazz,
  3 Blues, 4 Country, **Other last rendered as literal "0"** (`0` key selects
  the final genre even with <10 entries). `genre_of` learned country keywords
  and checks them before "classic" so "Classic Country" → Country not
  Classical. Country aggregates curated + favorites like Jazz/Blues; Other
  stays favorites-only. Favorites untouched; `findings.md` updated.
- **0.7.67** — **fill the 10th slots + Classical now fills too**: Jazz +**KMHD**
  (Portland public, 256k AAC) → 10; Blues +**Radio Caprice - Chicago Blues**
  (320k AAC, 1333 votes) → 10 (user's 61 Blues pick wasn't verifiable);
  Classical now **aggregates curated + favorites** like Jazz/Blues and gained
  **WCRB** / **KUSC** / **WFMT** (all live-verified, 256k-260k). Only Other is
  still favorites-only. Favorites untouched; `findings.md` updated.
- **0.7.65** — **curated Jazz & Blues in the genre submenus**: Jazz lists 6
  curated stations + your jazz favorites; Blues lists 3 curated + your blues
  favorites (de-duplicated). Favorites file untouched (it was already full at
  its 10-slot cap). Classical/Other stay favorites-only. New helper
  `genre_stations_for()` / `genre_station_counts()`; **`findings.md`** at repo
  root now persists all researched station URLs + status so they're never lost.
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