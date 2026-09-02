# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.84] - 2026-09-02

### Added

- **Volume & mute work everywhere** — `+` `=` `→` (up), `-` `←` (down) and `m`
  (mute) now work inside the favorites/genre menus too, not just on the player,
  so you can adjust the sound without leaving a menu. Refactored into a single
  `vol_key()` helper shared by both loops. Tests → **104 pass**.

## [0.7.83] - 2026-09-02

### Changed

- **`Space` acts like `Enter` for selection actions** — play a picked station,
  land a move, pick a genre. The confirmation popups (delete confirm) still
  require their explicit keys (`Y`/`del`/`Enter`), not `Space`. Footer nav hints
  now read `Enter/Space:play` / `...:move` / `...:pick`. Tests → **103 pass**.

## [0.7.82] - 2026-09-02

### Changed

- **Quick-pick slots 16 → 12** (`MAX_FAV`): `1`-`9`, slot #10 stays **`0`**, and
  slots 11-12 are reached with the arrow keys. Tests → **103 pass**.

## [0.7.81] - 2026-09-02

### Added

- **Edit mode (`e`)** — replaces the old delete mode on the favorites/genre
  menus. Toggling shows an `EDIT` chip between `SELECT` and the theme name, and
  the housekeeping row drops `e:edit` in favour of `s:select` and `d:delete`.
- **Move favorites**: in edit mode, `s` marks the station under the `▶` with a
  full-width light-blue highlight, then `↑`/`↓` (or numbers) pick the landing
  slot and `Enter` moves the station there — the landing slot is reused and the
  rest are pushed down (e.g. `1.radio1 / 3.radio5` select-3-land-1 gives
  `1.radio5 2.radio1`). Deterministic via `move_favorite`.
- **16 quick-pick slots** (was 10): `1`-`9`, slot #10 stays labelled **`0`**, and
  slots 11-16 are reached with the arrow keys. `MAX_FAV = 16`.
- **Delete** now lives inside edit mode: `d` deletes the slot under the `▶`
  after the usual confirmation popup (slot stays `— empty`).

### Changed

- **`s` → `g`** everywhere for opening the **genres** chooser (`s:genres` →
  `g:genres` in the player and menu footers); `s` is now **select-to-move** in
  edit mode (favorites). The mode label reads **`EDIT`** (was `DELETE MODE`).
- **New color pair 13** for the selected-to-move highlight: black on light blue.
- The favorites count hint counts **occupied** slots, so it reads the real number
  (e.g. `3 favorite(s)`) rather than the fixed 16.

### Tests

- **103 pass** (added `slot_tag`, `move_favorite` push-down/enter-empty/16-clamp).

## [0.7.80] - 2026-09-02

### Changed

- **Favorites-menu footer lead-in shortened**: `1-9,0:pick  ↑/↓:move` now reads
  `1-9,0:pick  ↑/↓`. Tests → **99 pass**.

## [0.7.79] - 2026-09-02

### Changed

- **Favorites menu now leads with `1-9,0:pick  ↑/↓:move`** at the top of the
  footer, to the left of `pick a number — N favorite(s)`. It was dropped from
  the mid (housekeeping) row to avoid duplication. The mid row keeps the rest
  (`s:genres  v:check  d:delete  l:last played  i:input`); `q/ESC` + `Enter`
  stay on the bottom row. Tests → **99 pass**.

## [0.7.78] - 2026-09-02

### Changed

- **Footer reorganized into two distinct bands so nothing is cut off on narrow
  terminals.** The station-menu footer is now a stacked three-band layout: the
  dynamic message (slot count / delete-mode note) sits on its own row; the
  housekeeping keys (`1-9,0:pick ↑/↓:move s:genres v:check d:delete
  l:last played i:input u/U`) live on the mid row; and `q/ESC` + `Enter` live on
  the bottom row. The player already split work this way (housekeeping mid row,
  transport bottom row). Both now clip to the footer's right-hand zone (update
  pill / version) so keys never collide on the right. Primary nav (`q/ESC`,
  `Enter`) always stays visible. Tests → **99 pass** (+1).

## [0.7.77] - 2026-09-02

### Added

- **`d:delete` — maintenance for your favorites.** From a favorites or genre
  submenu, `d` toggles a `DELETE MODE` chip (black on red); pick a slot with a
  number or `↑/↓`, then a confirmation popup shows the slot + host:

  ```
   Do you want to delete:
   6. Classic FM   ice-the.musicradio.com
   press Y or del to delete / press n, q or ESC to go back
  ```

  Confirm with `Y`/`del`/`Enter`. A deleted slot **stays empty** (rendered
  `— empty`) — the 10-numbering never shifts, and a later `i` (URL add) or
  future move can reuse the hole. Press `q`/`Esc` once to leave delete mode,
  again to go back. Slot-preserving favorites are persisted as `null`
  placeholders and survive restarts. Tests → **98 pass** (+9).

## [0.7.76] - 2026-09-01

### Fixed

- **Mute badge reads `MUTED`** (not `MUTE`), centered black-on-red in the
  volume bar.

## [0.7.75] - 2026-09-01

### Changed

- **Mute indicator moved into the volume bar.** Instead of `vol MUTED` to the
  left, a **`MUTE` badge (black on red, pair 12)** now sits centered inside the
  graphical volume bar when muted; the stored level still shows as `%` on the
  right. Tests → **89 pass** (+2).

## [0.7.74] - 2026-09-01

### Added

- **`i:input` — add a stream URL on the fly.** Shown in the mid/footer line to
  the right of `l:last played`, pressing `i` opens a prompt to paste any
  http(s) stream URL: it plays immediately and is saved as a favorite
  (de-duplicated by URL, genre auto-derived from the host). Works from any
  menu and from the player. `parse_stream_url` / `upsert_favorite` helpers
  power it (tested). Tests → **87 pass** (+2).

## [0.7.73] - 2026-09-01

### Added

- **Startup timing logged.** mradio now writes a `startup: X.XXs to UI (v…,
  menu=…, last_url=yes/no, provider=…)` line to `mradio.log` right before the
  UI renders, so a slow launch is diagnosable from the logs instead of a guess.

## [0.7.72] - 2026-09-01

### Added

- **Resume the last-played station.** The app now remembers the most recent
  station you tuned (url + name, kept in `config.json` under `last_url` /
  `last_name`). At startup the shortcut row offers **`l:last played`** to the
  right of `v:check`; press `l` (in a menu or on the player) to play it
  instantly. The hint only appears once a station has actually been played.
  Tests → **85 pass** (+3).

## [0.7.71] - 2026-09-01

### Fixed

- **Update check no longer looks "stuck" on `checking for updates…".**
  While a GitHub feed fetch is in flight the transient line now stays on
  screen with a spinner (`▚/▞`) and the elapsed seconds, so a slow or hung
  check never appears frozen. On completion it always resolves to a real
  result ("up to date", "new version … press U", or "check failed (offline?)").
  Feed-fetch timeout tightened to a single 6s budget (`CHECK_TIMEOUT`); a failed
  fetch now reads "check failed (offline?)" instead of the bare "check failed".
  New `check_msg()` helper centralizes the flash logic (resolved note ~5s).
  Tests → **82 pass** (+3 for the new helper).

## [0.7.70] - 2026-09-01

### Added

- **New "Focus" (category 7) and "Chill" (category 8) genres, 10 curated each.**
  The genre picker is now 1 Classical, 2 Jazz, 3 Blues, 4 Country, 5 Rock,
  6 Pop, 7 Focus, 8 Chill, with **Other kept as the literal `0` slot** (last).
  Both aggregate curated + favorites (de-duplicated), like all other genres.
  Every station was researched and live-tested (real audio via mpv + bitrate +
  `icy-title` confirmed):
  - **Focus (10)** — the deep-concentration ambient / new-age / meditative /
    instrumental palette (the Vangelis / Enya / Vollenweider world, tuned for
    concentrating, working and producing): SomaFM Space Station Soma (320k,
    ambient synth), Ambient Sleeping Pill (256k, dreamy ambient), SomaFM Drone
    Zone (128k, the classic focus/drone channel), SomaFM Groove Salad (128k,
    the classic work-music), Cryosleep / Echoes of Blue Mars (128k, deep-space
    ambient), SomaFM Deep Space One (128k, slow ambient), Radio Caprice -
    Relaxation Music (320k AAC), Total Instrumental (laut.fm, 128k), Yoga Chill
    (128k, meditative), Radio Art - Deep Focus & Concentration (96k).
  - **Chill (10)** — the loungier / downtempo side: 1.FM Chillout Lounge
    (256k), Chilltrax (128k), Café del Mar (192k), Smooth Chill UK (128k),
    Antenne Bayern Chillout (128k), SomaFM Fluid (128k), Costa del Mar -
    Chillout (96k AAC), Jazz Lounge (320k), Hi On Line Lounge (320k),
    Costa del Mar - Zen (96k).
- **`genre_of` now recognizes focus & chill keywords** ("meditation",
  "relax", "new age", "yoga", "zen", "ambient", "drone", "instrumental",
  "focus"; "chill", "chillout", "lounge", "downtempo", "del mar") so legacy
  favorites backfill correctly.
- Favorites file still untouched. `findings.md` updated with the Focus/Chill
  research + full rosters. Tests updated → **79 pass**.

## [0.7.69] - 2026-09-01

### Added

- **New "Rock" (category 5) and "Pop" (category 6) genres, 10 curated each.**
  The genre chooser is now 1 Classical, 2 Jazz, 3 Blues, 4 Country, 5 Rock,
  6 Pop, with **Other kept as the literal `0` slot** (last). Both new genres
  aggregate curated + favorites (de-duplicated), exactly like the others. Every
  station was researched and live-tested (real audio via mpv + bitrate +
  `icy-title` confirmed):
  - **Rock (10):** Radio Caroline (offshore pirate icon, 128k, icy),
    Virgin Classic Rock (IT, 128k, icy), Rock Antenne (128k, icy),
    Arrow Classic Rock (192k), 1.FM Classic Rock Replay (256k, icy),
    SomaFM Left Coast 70s (320k, icy), Radio ROKS Hard'n'Heavy (320k, icy),
    Radio ROKS Ballads (320k, icy), 181.FM Rock 181 (128k, icy),
    Hard Rock Heaven (128k, icy).
  - **Pop (10):** Capital FM London (helper, icy), Heart 80s (128k, icy),
    Heart 70s (128k, icy), Radio 105 Italy (128k, icy), LOS 40 España
    (128k, icy), Radio 538 NL (128k, icy), Energy Zürich NRJ CH (128k, icy),
    1.FM Absolute TOP 40 (256k, icy), SWR3 DE (128k), Chocolate FM ES (192k,
    icy).
- **`genre_of` now recognizes rock & pop** ("rock", "rockabilly", "metal",
  "hard rock", "punk"; "pop", "top 40", "top40", "hits") so legacy favorites
  backfill correctly.
- Favorites file still untouched. `findings.md` updated with the Rock/Pop
  research + full rosters. Tests updated → **75 pass**.

## [0.7.68] - 2026-09-01

### Added

- **New "Country" genre (category 4) with 10 curated, live-verified stations.**
  The genre chooser is now 1 Classical, 2 Jazz, 3 Blues, 4 Country, with
  **Other pushed to the literal `0` slot** (last). The Country submenu
  aggregates curated + favorites (de-duplicated), just like Classical/Jazz/Blues.
  Every station was researched and live-tested (real audio via mpv + bitrate +
  `icy-title` confirmed):
  - **WSM 650 AM** (Nashville, home of the Grand Ole Opry) — 64k, icy
  - **.977 Country** — 128k, icy, 55k votes (most popular on radio-browser)
  - **1.FM Absolute Country Hits** — 256k, icy, 16.6k votes
  - **1.FM Classic Country** — 256k, icy, 14.3k votes
  - **181.FM Highway 181** — 128k, icy, 20.3k votes
  - **181.FM Kickin' Country** — 128k, 8.5k votes
  - **181.FM Real Country** — 128k, icy, 3.3k votes
  - **KIX Country** (Australia) — 128k
  - **Big R Radio Country** — 128k, icy
  - **Country Radio (CZ)** — 128k AAC
- **`genre_of` now recognizes country station names** ("country", "americana",
  "bluegrass", "honky-tonk", "nash") and checks them ahead of the generic
  "classic" keyword so "Classic Country" resolves to Country, not Classical.
- **Other is now the last/"0" slot** in the genre chooser; pressing `0` (or the
  arrow keys + Enter) selects it, and it renders as `0` even though the menu has
  fewer than 10 entries.
- Favorites file still untouched. `findings.md` updated with the Country
  research + full roster. Tests updated → **70 pass**.

### Changed

- `GENRES` order is now `classical, jazz, blues, country, other`.

## [0.7.67] - 2026-09-01

### Changed

- **Curated Classical now fills the Classical submenu.** The Classical genre
  submenu previously showed only your favorites; it now aggregates curated
  Classical + favorites (de-duplicated) exactly like Jazz/Blues, so the curated
  catalog can fill the submenu to 10 (0 = 10th slot) and beyond (arrow keys
  scroll). Only **Other** stays favorites-only.
- **Added 3 curated Classical stations** (all live-verified): **WCRB** (Boston,
  256k), **KUSC** (Los Angeles, 256k, icy metadata), **WFMT** (Chicago, 260k,
  icy metadata) — three premier US public classical stations.
- **Jazz filled to 10**: added **KMHD** (Portland public, 256k AAC, icy) —
  reached 9 via its direct non-HLS URL.
- **Blues filled to 10**: added **Radio Caprice - Chicago Blues** (320k AAC,
  icy, 1333 votes). Original pick **61 Blues** couldn't be live-verified
  (0 listeners / no stream URL found), so the verified Chicago-electric-blues
  station was chosen instead to match the intent.
- Favorites file still untouched. `findings.md` updated with the Classical
  research + full rosters.

## [0.7.66] - 2026-09-01

### Changed

- **Expanded Jazz & Blues genre submenus to 9 stations each, re-ranked.**
  Every station was researched, then **live-tested** (HTTP status + real
  audio decoded via mpv with bitrate + `icy-title` confirmed), preferring
  higher bitrate and stations with track (`icy-title`) metadata.
  - **Jazz (9):** Swiss Jazz (existing favorite) + WBGO, WWOZ, KCSM 91.1,
    KJAZZ 88.1, Jazz24 (256k), 1.FM Adore Jazz (256k), TSF Jazz (Paris),
    JazzRadio 106.8 Berlin (192k). Replaced **Adroit Jazz Underground** and
    **SomaFM Secret Agent** — which could not be live-verified from this
    environment and lost out to higher-bitrate, better-reviewed alternatives.
  - **Blues (9):** Jazz Radio Blues (64.5k votes — most popular blues stream
    anywhere), Blues Radio Greece (320k), Blues Music Fan (320k, "#1
    contemporary blues"), Blues Rock Cafe, 1.FM Blues (256k), 181.FM True
    Blues, Buddy Guy Radio Legends, WDCB 90.9, exclusive BB King.
- `findings.md` updated with the full final rosters, live-verification method,
  bitrate, icy-title support, and radio-browser vote counts for every station.

## [0.7.65] - 2026-08-31

### Added

- **Curated Jazz & Blues stations in the genre submenus.** The **Jazz** genre
  submenu now lists 6 curated jazz stations (WBGO, WWOZ, KCSM 91.1, KJAZZ 88.1,
  Adroit Jazz Underground, SomaFM Secret Agent) and the **Blues** submenu lists
  3 curated blues stations (1.FM Blues, 181.FM True Blues, WDCB 90.9) — shown
  **in addition to** any Jazz/Blues favorites you already have (de-duplicated).
  The favorites file (`stations.json`) is **never touched**: it was already
  full at its 10-slot cap, so the curated stations come from the built-in
  catalog instead. Classical and Other submenus stay favorites-only.
- **`findings.md`** at the repo root — a persistent log of every researched
  station URL, its verification status, and the decisions made (so research is
  never lost again).

### Changed

- `s` genre chooser counts now include the curated Jazz/Blues stations, so the
  Jazz bucket shows `Jazz (7)` and Blues `Blues (3)` once favorites exist there.

## [0.7.64] - 2026-08-31

### Fixed

- **`Esc`/`q` inside a genre submenu now goes back to the genre chooser**
  (parent menu) instead of leaving the menu or killing the app. The back
  decision is extracted into `back_target()` (unit-tested). Exit still happens
  from a menu only on a bare-launch screen (no player).

## [0.7.63] - 2026-08-31

### Added

- **Genre submenus.** `s` now opens a genre chooser (Classical / Jazz /
  Blues / Other) built from your favorites; genres with no favorites are
  hidden. Pick a number to open that genre's submenu, then pick a station.
  Each favorite is auto-classified from its name (`genre_of()`); unknown names
  fall into **Other**. `DEFAULT_STATIONS` entries carry an explicit `genre`.

### Changed

- The flat all-stations catalog (`S01…Snn`) and the `a` add-to-favorites key
  were **removed**: browsing is now your favorites grouped by genre. Numbered
  hot-picks (`1-9`, `0`) work inside the favorites list and each genre submenu.

### Fixed

- Genre menu no longer crashes on entry (undefined `heading`/`sts` in the
  `genres` render path).

## [0.7.62] - 2026-08-31

### Fixed

- **In-play spinner label for NIM.** While the AI is querying, the spinner
  (e.g. `▞ NIM 10s`) now shows the same display name as the footer (`NIM`)
  instead of the internal `openai` name.

## [0.7.61] - 2026-08-31

### Added

- **Ollama URL setup popup.** Pressing `2` when no Ollama server is configured
  opens a TUI popup asking for the server URL, with three example lines
  (`http://localhost:11434`, `http://192.168.1.12:11434`,
  `https://internet.accessible.server`). Press `c` while provider 2 is active
  to change it. Saved to `settings.json` (`ollama_url`). The generic popup now
  powers both the NIM key and Ollama URL flows.

## [0.7.60] - 2026-08-31

### Changed

- **NIM API key popup layout**: explanation hints pushed down a line for
  separation; the input field is now a full-width light-grey block that
  stands out; a rectangular terminal cursor sits at the left of the field and
  moves right as you type or jumps to the end on paste.

## [0.7.59] - 2026-08-31

### Fixed

- **NIM API key popup no longer prefills `nvapi-`.** The placeholder now shows
  as light-grey hint text below an empty input field, so pasting a full key
  from NVIDIA works without doubling the prefix. The popup is framed and
  validates the key on Enter.

## [0.7.58] - 2026-08-30

### Added

- **NIM (NVIDIA) in-app setup.** Pressing `3` when no API key is configured
  opens a TUI popup where you paste your `nvapi-…` key (from
  build.nvidia.com). The key is saved to `settings.json` immediately. Press
  `c` to change it later. While NIM is active the footer shows `c:change API
  Key` for 10 seconds after each switch.
- **Full AI installation guide in KB.md** — per-provider setup for OpenCode,
  Ollama (local / Docker / remote, model recommendation), and NIM (signup,
  phone number, API key, in-app wizard).
- Provider `openai` renamed to **NIM** in the UI (`3=NIM`, `now:NIM`). Internal
  name stays `openai` for config.json backwards compatibility.

### Changed

- Footer volume hint leads with arrows: `← -/+ →:volume` (v0.7.57).

## [0.7.57] - 2026-08-30

### Changed

- **Volume hint text** in the footer now reads `← -/+ →:volume` instead of
  `+ / -:volume` — the arrow keys are the visible affordance, so the label
  leads with them.

## [0.7.56] - 2026-08-30

### Fixed

- **`v` no longer reports a stale "up to date".** Two update-check bugs could
  make a fresh release invisible: a `304` (GitHub's CDN can answer "unchanged"
  for a feed that already changed) re-used the last-known version instead of
  re-checking, and `v` only refreshed in the background if the last check was
  over an hour old. A `304` now triggers an unconditional re-fetch, the highest
  version found wins (never the first feed entry), and every `v` press forces a
  background refresh after flashing the cached answer.

## [0.7.55] - 2026-08-30

### Fixed

- **Stream data line flags an unknown bitrate with a label.** When mpv does
  not report the stream bitrate, the line now reads `— kbps` instead of a
  bare `—`, so the format is always `bitrate · sample · codec · cache · time`.

## [0.7.54] - 2026-08-30

### Added

- **Anti-hallucination rules for Choice 3 (API key / `openai` provider).** The
  API prompt now carries extra "HARD TRUTHFULNESS RULES" aimed at the cloud
  models: never invent a fact (premiere dates, dedicatees, film/TV/commercial
  appearances, notable recordings, performers, awards); never claim a piece
  appears in a film unless certain; prefer verifiable structural facts;
  return `wiki` only if confident the article exists; and never drift onto a
  composer, performer, or work other than the one in the tag. Length is
  secondary to truth — a ~450-character trivia of verified facts beats a padded
  one. opencode and ollama keep the stock prompt unchanged.

## [0.7.53] - 2026-08-30

### Fixed

- **`v` answers instantly again.** The manual update check used to flash
  "checking…" for six seconds and, if the fetch took longer, the result landed
  after the flash already closed — so it *looked* like it never finished (and
  the silent startup check still worked). `v` now shows the last known result
  (e.g. "up to date (v0.7.53)") the moment you press it, and only quietly
  re-checks in the background when that answer is stale.

### Changed

- **Picker chip spacing.** After `U` applies an update the `q/ESC:quit` chip is
  followed by two spaces before the pick hints (previously glued on).

## [0.7.52] - 2026-08-30

### Changed

- **Dark grey subtext on the light themes.** Pair 5 — the station-picker hint
  row, the player footer's mid row (`f:favorites s:all …`), the station host
  subtitles, and the AI trivia note — was a washed-out light grey and/or
  terminal-`dim` on a white background. All three light palettes (`light`,
  `light-navy`, `light-mauve`) now use a solid dark grey, and the `A_DIM`
  attribute was dropped from those draws so the grey stays grey on white.

## [0.7.51] - 2026-08-30

### Changed

- **Cleaner picker footer.** The escape hint is now written `q/ESC:back`
  (uppercase `ESC`), is **always the leftmost** item in the bottom row — and
  that stays true on the bare-launch screen, where it reads `q/ESC:quit`
  (and turns light-green after `U` applies an update). The two-update roll +
  move hints now follow it.

## [0.7.50] - 2026-08-29

### Changed

- **`opencode` CLI is auto-detected.** On a fresh machine (e.g. a new WSL
  Debian box) the AI providers were all off until you configured
  `MRADIO_OPENCODE` — so installing the CLI did nothing. If `opencode` is on
  `PATH` the provider now enables itself automatically (port 4096, spawning
  `opencode serve` as before), so AI works with zero configuration.
  `MRADIO_OPENCODE=0` still disables it explicitly; any non-empty value still
  behaves as before.

## [0.7.49] - 2026-08-29

### Changed

- **Picker hints become the suggested action.** On the station picker the
  escape key now honestly reads `q/Esc:quit` at the bare-launch screen (no
  player to go back to; `q/Esc:back` still appears mid-session while music
  plays). After `U` applies an update, `q/Esc:quit` is drawn as a
  **light-green chip** — the same treatment as `SELECT` in the top bar —
  pointing at the one action you should take next: quit & restart onto the
  new version.

## [0.7.48] - 2026-08-29

### Fixed

- **No more random ghost digits at the shell prompt.** Keystrokes tapped while
  mradio exits (up to ~2 s of mpv cleanup) used to linger in the terminal
  buffer and get replayed by the shell after `endwin()` — you'd see a stray
  `9` (or similar) on your command line. mradio now drains pending terminal
  input just before handing the tty back.

### Housekeeping

- `.opencode/BEHAVIOR.md` added: c.p is now the **default** (commit & push
  after every task, full release when version-worthy, unless "don't push"),
  the four documentation duties (project memory / CHANGELOG / README / KB) are
  etched as permanent rules, and the "steady warnings only in the yellow pill"
  UI convention is recorded.

## [0.7.47] - 2026-08-29

### Changed

- **Steady warnings live in the right-side yellow pill only.** The redundant
  left-side steady texts are gone: the mid row keeps its normal hints
  (no `restart to update`, no `new version vX — press U` at rest) and the
  picker's bottom line stays `1-9,0:pick … v:check`. The `UPDATE` →
  `RESTART TO UPDATE` pill is the one steady indicator (the transient `v`
  flashes still give full detail).

## [0.7.46] - 2026-08-29

### Dummy

- No functional change — placeholder release for the user to verify the
  update flow end to end (silent `v` check at startup on the station picker,
  then `U` → `RESTART TO UPDATE` → restart onto the new version).

## [0.7.45] - 2026-08-29

### Changed

- **`UPDATE` pill becomes `RESTART TO UPDATE` after `U`.** Once a new file has
  been swapped in, the running copy is still the old version until you
  restart — so the pill now says `RESTART TO UPDATE` (instead of inviting yet
  another `U`), the mid row/hints read `restart to update`, and `v` echoes
  `updated to vX — restart to apply`. The pill clears once you restart onto
  the new file. Applies on the player and the station picker alike.

## [0.7.44] - 2026-08-29

### Changed

- **Update check surfaces on the station picker too.** The silent startup
  check runs while you're still choosing a station — the `UPDATE` pill,
  `u:page  U:apply` and a persistent `new version vX — press U` line now
  appear on the favorites / all-stations screens as soon as the check lands.
  You can update before ever picking a station (`update_url` is now derived
  for the menu loop, not just the player loop).

## [0.7.43] - 2026-08-29

### Fixed

- **`v` no longer lies after a `304`.** GitHub's `Not Modified` means "feed
  unchanged since your last check" — not "you're up to date". Pressing `v`
  after an unchanged feed previously flashed `up to date (vX.Y.Z)` even when a
  newer release was known (contradicting the `UPDATE` pill). The `304` path now
  re-derives its message from the last successful check, so it reports
  `new version vX.Y.Z — press U` whenever that's what's actually stored.

## [0.7.42] - 2026-08-29

### Fixed

- **Mute no longer silently disappears.** mpv resets `mute` on every new
  process, and mradio only re-applied the *volume* after a launch / reconnect
  (`r`) / station switch — so a mute was quietly dropped whenever mpv
  restarted in the background. Mute state is now persisted to `config.json`
  (like volume) and re-pushed together with the volume on every fresh mpv
  (`apply_volume`); `m` stores the new state.

## [0.7.41] - 2026-08-29

### Changed

- **Docs & memory housekeeping.** README's `all-stations` screenshot refreshed
  to the real post-fix capture (names show `VCR Auditorium | Venice Classic
  Radio Italia` … `NPO Klassiek`). Project memory (`.opencode/MEMORY.md`)
  gained a hard rule: every bug fix or feature add/altered/remove must be
  reflected in README.md and KB.md in the same change, and its current-state
  section now tracks 0.7.40.

## [0.7.40] - 2026-08-29

### Changed

- **Favorites are capped at 10** (the `1-9` + `0` hot slots), as originally
  agreed. The auto-seed now writes the first 10 curated stations (not all 12),
  legacy-config migration is trimmed to 10, and `a` no longer grows the list
  past 10 (it flashes "favorites full"). The favorites menu also renders only
  the 10 hot rows, so stray extras no longer show as fake `0` entries.

### Fixed

- Favorites menu no longer labels rows beyond #10 with `0`.

## [0.7.39] - 2026-08-29

### Fixed

- **All-stations names match favorites.** `DEFAULT_STATIONS` (the `s` menu's
  curated list, also the fresh-install seed) still carried the short names
  after the favorites were updated to their real broadcast names. Now shipped
  with the same corrected names: `VCR Auditorium | Venice Classic Radio Italia`,
  `VCR Classica+ | Venice Classic Radio Italia`, and `NPO Klassiek`.

## [0.7.38] - 2026-08-29

### Changed

- **README screenshots are now real captures** of the running app (taken on
  the user's terminal) instead of generated mockups. They show the true UI:
  hot-key columns, host column under each station, pills, vol state, and real
  AI liner notes. The mock renderer (`shot.swift`, `make screens`) is gone so
  nothing can overwrite them.

## [0.7.37] - 2026-08-29

### Fixed

- **README screenshots, finally laid out correctly.** The previous attempt
  had an AppKit coordinate bug (header/title/footer displaced, empty space).
  The CoreText renderer now uses a correct bottom-origin layout; header sits
  on top, body in the middle, footer reaches the very bottom. Verified with
  pixel probes + OCR.
- **README title is `mradio` again** — the in-app `● RADIO` is only the UI
  badge, not the project name.

## [0.7.36] - 2026-08-29

### Fixed

- **README screenshots, for real this time.** The previous QL/HTML rendering
  produced wrong glyphs for mradio's Unicode (`● ▸ █ ░` etc.). Screenshots are
  now drawn directly with **CoreText using Menlo** (a font verified to contain
  every glyph mradio uses) by a small Swift renderer (`screenshots/shot.swift`,
  `make screens`) — no WebKit font-fallback in the pipeline.

## [0.7.35] - 2026-08-29

### Added

- **README rewritten as a short marketing piece** — tagline, appetizers for
  every feature, real screenshots (`screenshots/player.png`,
  `screenshots/favorites.png`, `screenshots/all-stations.png`), and a
  KB-link after every paragraph. The full details stay in KB.md. Screenshots
  are re-renderable via `make screens`.

### Fixed

- **Screenshot rendering** — mradio's Unicode glyphs (`● ▸ █ ░` and the
  arrows/triangles) now render from a hardened font stack
  (`Menlo, Apple Symbols`) instead of SF Mono, which lacks several of those
  glyphs.

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