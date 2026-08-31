# mradio — Knowledge Base

Everything about mradio, in one place: how it works, every key, every menu,
every config option, how self-updates and AI enrichment behave, and how to fix
it when something's off.

The [README](README.md) is the quick-start card; this file is the reference
manual. Version history lives in [CHANGELOG.md](CHANGELOG.md).

---

## Table of contents

1. [What mradio is](#1-what-mradio-is)
2. [Requirements & install](#2-requirements--install)
   - [2.1 Requirements](#21-requirements)
   - [2.2 macOS (Homebrew)](#22-macos-homebrew)
   - [2.3 Linux](#23-linux)
   - [2.4 Windows → WSL](#24-windows-wsl)
   - [2.5 Alternative installs](#25-alternative-installs-any-os)
3. [Running it](#3-running-it)
4. [Screen anatomy](#4-screen-anatomy)
5. [Controls](#5-controls)
   - [5.1 Player screen](#51-player-screen)
   - [5.2 Station menus](#52-station-menus-f-favorites--s-all-stations)
   - [5.3 Mouse](#53-mouse)
6. [Stations & favorites](#6-stations--favorites)
7. [Updates & self-update](#7-updates--self-update)
8. [AI enrichment](#8-ai-enrichment)
   - [8.1 What it adds](#81-what-it-adds-when-a-provider-is-enabled)
   - [8.2 Provider 1: OpenCode](#82-provider-1-opencode-recommended)
   - [8.3 Provider 2: Ollama](#83-provider-2-ollama)
   - [8.4 Provider 3: NIM](#84-provider-3-nim-nvidia)
   - [8.5 Prompt rules](#85-prompt-rules-nim--choice-3)
   - [8.6 In-session control](#86-in-session-control)
   - [8.7 How it works](#87-how-it-works)
   - [8.8 Diagnostics](#88-diagnostics)
   - [8.9 Settings & env](#89-settings-env)
9. [Configuration & persistence](#9-configuration--persistence)
   - [9.1 config.json](#91-configjson)
   - [9.2 settings.json](#92-settingsjson)
   - [9.3 stations.json](#93-stationsjson)
   - [9.4 cache.json](#94-cachejson)
10. [Environment variables](#10-environment-variables)
11. [Themes](#11-themes)
12. [Advanced use](#12-advanced-use)
13. [Troubleshooting / FAQ](#13-troubleshooting--faq)
14. [Development](#14-development)
15. [Design notes & limitations](#15-design-notes--limitations)
16. [Privacy](#16-privacy)

---

## 1. What mradio is

`mradio` is a colorful **terminal radio player** built on two pieces:

- **mpv** — the audio engine. It does the networking, demuxing, decoding and
  reconnect handling for messy internet-radio streams (icecast metadata, HTTPS,
  dead mounts). Decoding is its job, not mradio's.
- a **Python `curses` frontend** (single stdlib-only script) that drives mpv
  over its IPC socket and draws the display: live now-playing metadata,
  audio/format meters, and — when you opt in — AI enrichment for the track
  (trivia note, `Work:` line, and a *verified* Wikipedia link).

Everything is a thin, colorful display + remote control on top of mpv. There
are no pip dependencies: `python3` + `mpv` are all it needs.

## 2. Requirements & install

### 2.1 Requirements

| Requirement | Notes |
| ----------- | ----- |
| **python3** | 3.8+; stdlib only, no pip packages |
| **mpv**     | the audio engine — the only real dependency |
| **git**     | needed for the clone-and-install path (the prebuilt `install.sh`) |
| **opencode CLI** *(optional, recommended)* | zero-config AI liner notes — mradio auto-detects it on `PATH` (0.7.50+). Grab the official installer for your OS at **https://opencode.ai/download** (covers Homebrew, npm, curl installer, and the manual binary). Skip it for now — see [§8 AI enrichment](#8-ai-enrichment) for all three providers and their install steps |

| OS     | Status |
| ------ | ------ |
| macOS  | ✅ fully tested |
| Linux  | ✅ any distro with `python3` + `mpv` |
| Windows | ❌ no native support (official Python lacks `curses`) — use **WSL** |

mradio installs to **`~/.local/bin`** with **no root** needed (via `install.sh`),
or to a system prefix with `make install` / `sudo install`. Every step below
ends with the same three verification commands:

```sh
mradio --version            # prints mradio <version>
mradio --help               # prints the key map
mradio                      # opens your favorites menu
```

You need `~/.local/bin` on your `PATH`. If `mradio` isn't found after install,
add this to `~/.zshrc` (zsh) or `~/.bashrc` (bash):

```sh
export PATH="$HOME/.local/bin:$PATH"
```

**Want AI liner notes?** That's the *optional* opencode CLI row above: install it
from **https://opencode.ai/download**, and mradio's AI row lights up on its own
— no API key, no config. (Or skip it entirely: the radio plays perfectly
without it.) For the full picture — including **Ollama** (local/Docker/remote)
and **NIM** (free hosted NVIDIA inference) — jump to
**[§8 AI enrichment](#8-ai-enrichment)** for the complete setup guide for all
three providers.

### 2.2 macOS (Homebrew)

1. **Install Homebrew** (if you don't have it — check with `brew --version`):

   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   After installation, make sure `brew` is on your `PATH` — Apple Silicon:
   `eval "$(/opt/homebrew/bin/brew shellenv)"` (Intel: `/usr/local/bin/brew`).
   The installer's own output tells you the exact command to paste.

2. **Install mpv**:

   ```sh
   brew install mpv
   ```

3. **Install the opencode CLI** *(recommended — it powers the AI liner notes
   and mradio auto-detects it, so no further AI setup is needed)*:

   ```sh
   brew install anomalyco/tap/opencode
   ```

   (Any method from the official page **https://opencode.ai/download** works —
   like `curl -fsSL https://opencode.ai/install | bash` or `npm i -g opencode-ai`.)
   Prefer a different engine? See [§8 AI enrichment](#8-ai-enrichment) for the
   Ollama and NIM paths.

4. **Install mradio**:

   ```sh
   git clone https://github.com/Marcus1571/mradio.git
   cd mradio
   ./install.sh
   ```

5. **Verify** with the three commands above, then `mradio` to browse stations.

> Upgrading later: press **`U`** inside mradio to self-update, or
> `git pull && ./install.sh`.

### 2.3 Linux

Python 3 ships with essentially every distro; you only need to install **mpv**
and then mradio. Pick your branch:

#### 2.3.1 Debian / Ubuntu / Linux Mint (apt line)

1. **Install mpv** (and python3, if somehow missing):

   ```sh
   sudo apt update
   sudo apt install -y mpv python3
   ```

2. **Install the opencode CLI** *(recommended — the AI liner-notes provider;
   mradio auto-detects it)*:

   ```sh
   curl -fsSL https://opencode.ai/install | bash
   ```

   (Any method from the official page **https://opencode.ai/download** works.)
   The curl installer lands in `~/.local/bin`, which the `PATH` export above
   already covers. Not using opencode? The Ollama / NIM paths are in
   **[§8 AI enrichment](#8-ai-enrichment)**.

3. **Install mradio**:

   ```sh
   git clone https://github.com/Marcus1571/mradio.git
   cd mradio
   ./install.sh
   ```

#### 2.3.2 Fedora (dnf line)

1. **Install mpv**:

   ```sh
   sudo dnf install -y mpv python3
   ```

2. **Install the opencode CLI** *(recommended — the AI liner-notes provider;
   mradio auto-detects it)*:

   ```sh
   curl -fsSL https://opencode.ai/install | bash
   ```

3. **Install mradio** (clone, then `./install.sh`, as above).

#### 2.3.3 Arch / Manjaro / EndeavourOS / Omarchy (pacman line)

1. **Install mpv**:

   ```sh
   sudo pacman -S --noconfirm mpv python
   ```

2. **Install the opencode CLI** *(recommended — the AI liner-notes provider;
   mradio auto-detects it)*:

   ```sh
   curl -fsSL https://opencode.ai/install | bash
   ```

   …or via an AUR helper (`paru -S opencode`); any method from
   **https://opencode.ai/download** works.

3. **Install mradio** (clone, then `./install.sh`, as above).

### 2.4 Windows → WSL

The official Windows Python build has no `curses`, so mradio runs under
**WSL** instead. `wsl --install` (or your distro of choice), then follow the
**Debian/Ubuntu** branch above inside the WSL terminal — including the
`curl -fsSL https://opencode.ai/install | bash` opencode CLI step, which works
fine under WSL.

### 2.5 Alternative installs (any OS)

```sh
make install                                   # copies to ~/.local/bin
sudo make install                              # system-wide
sudo install -m755 mradio /usr/local/bin/mradio
# or run it straight from the checkout:
./mradio
```

Install:

```sh
git clone https://github.com/Marcus1571/mradio.git
cd mradio
./install.sh        # copies `mradio` to ~/.local/bin
```

Alternatives: `make install`, or `sudo install -m755 mradio /usr/local/bin/mradio`.

**Optional:** to also get the AI liner notes, install the opencode CLI per your
OS branch above (or any method from **https://opencode.ai/download**).

## 3. Running it

```sh
mradio                                # opens your favorites menu first
mradio https://some-radio-url/stream.mp3
mradio https://some-radio-url/stream.mp3 "Forced Station Name"
mradio --version | --help | --settings
```

- **Bare launch** (no URL) opens the **favorites menu** — nothing plays until
  you choose a station with `1-0`/Enter. This is the intended phone-it-in mode.
- With a **URL**, mradio tunes in immediately and the station name is read from
  the stream's own `icy-name` metadata when the stream provides it.
- The optional **second argument forces the display name** (for streams that
  report no name, or a name you'd rather not show).

## 4. Screen anatomy

Top to bottom, on the player screen:

```
 ● RADIO  ▸  VCR Auditorium | Venice Classic Radio Italia  ▸  LIVE  light-navy (p)
└ header: station name (right of ● RADIO), LIVE/PAUSED pill, active theme

 Luigi Boccherini (1743-1805)
 Quartetto per archi in Sol minore n.6 op.24   ← now-playing block (artist,
 (Europa Galante - Fabio Biondi, ...)            work, performers, Work: line)
 work: [...]
 This quartet is part of a series ...            ← grey AI trivia note

  — kbps · 44.1 kHz · mp3 · cache 0.8s · stream 00:45  ← format/stream line
  vol ████████████...  100%                       ← volume meter + value

  AI: 1=opencode  2=ollama  3=NIM  now:opencode  press to re-request  z:expand
  f:favorites   s:all   v:check                                     UPDATE
  q:quit  space:pause  ← -/+ →:volume  m:mute  r:reconnect         v0.7.51
└ three-row footer: AI line / stations+update row / transport keys;
  right edge holds the UPDATE pill and the running version
```

- **Header** — station badge, `LIVE`/`PAUSED`, and the active theme.
- **Now-playing block** — composer/performer/work lines; a `Work:` line appears
  when the station tag was only a movement/fragment.
- **Trivia note** (AI, when enabled) — dark grey, word-wrapped to the window; if it
  doesn't fit it shows `…` and you can expand it full-screen with `z`.
- **Format line** — kbps / kHz / codec / cache depth / elapsed stream time.
  The bitrate and kHz slots keep their unit labels even when mpv doesn't
  report a value (they show `— kbps · — kHz`).
- **Volume meter** — bar + percentage; `MUTED` when muted.
- **Footer (three rows)**:
  - **row 1 (top)** — AI provider hotkeys, current provider (`now:`), the
    re-request hint, and `z:expand`/`z:collapse` (z toggles the trivia note —
    it belongs to the AI row because it expands AI output).
  - **row 2 (mid, dark grey)** — `f:favorites`, `s:all` (open the two station
    menus), `k:kb` (open this knowledge base in your browser), `v:check`
    (instant answer from the last check; quiet background refresh only when
    stale); when an update exists this row
    also gains `u:page` and `U:apply`. The black-on-yellow **`UPDATE`** pill
    sits at its right edge.
  - **row 3 (bottom)** — transport keys `q`, `space`, `+/−`, `m`, `r`; the
    running version sits at the right edge.

## 5. Controls

### 5.1 Player screen

| Key | Action |
| --- | ------ |
| `q` / `Esc` | quit |
| `space`     | pause / resume |
| `+` `=` `→` | volume up (+5, remembered) |
| `-` `←`     | volume down (−5, remembered) |
| `m`         | mute toggle (**remembered**, re-applied on reconnect) |
| `r` / `R`   | reconnect the stream (revive a dead station/mount) |
| `o` / `O`   | open the **verified** Wikipedia article in your browser (only when one exists) |
| `z` / `Z`   | expand/collapse the full trivia note (fills the screen); no note = toggles detail view |
| `p` / `P`   | rotate color theme (`p`); choice is remembered in `config.json` |
| `1` `2` `3` | pick AI provider: 1=opencode, 2=ollama, 3=NIM. Saves the choice **and** re-requests the current track immediately — even if a cached note exists |
| `v`         | force a version check now; result flashes in the footer's mid row (works with or without AI configured) |
| `k` / `K`   | open the project knowledge base (KB.md) in your browser — this is the manual you're reading |
| `u`         | when an update is available: open the release page |
| `U`         | when an update is available: auto-update in place, then **restart to apply** (pill flips to `RESTART TO UPDATE`) |
| `f`         | open the **favorites** menu |
| `s`         | open the **all-stations** menu |
| mouse click | only with `"mouse": 1` in `config.json`: click the trivia text to expand/collapse it; click the `UPDATE` pill to open the release page |

Arrow keys `→`/`←` double as volume hotkeys.

### 5.2 Station menus (`f` favorites / `s` all-stations)

Both menus share their housekeeping keys; only picking differs.

| Key | Favorites (`f`) | All stations (`s`) |
| --- | --------------- | ------------------ |
| `1`…`9` `0` | **instant pick** (`0` = 10th favorite) | — |
| `↑`/`↓` or `j`/`k` | move selection | move selection |
| `Enter` | play selected | play selected |
| `a` | — | **add** the highlighted station to your favorites (flash confirms; ignored once your 10 slots are full) |
| `f` | switch to favorites | switch to favorites |
| `s` | switch to all stations | stay on all stations |
| `q` / `Esc` | back to player while something is playing; **quit** in the bare-launch screen. In the menu footer the hint is **always the leftmost item**, reading `q/ESC:back` — or `q/ESC:quit` on the startup screen, where once `U` has applied an update mradio renders it as a **light-green chip**, the suggested action (quit & restart onto the new version) | same |
| `v`, `u`, `U`, `p` | same as the player (update check / release page / auto-update / theme) | same |

- **Numeric pad** behaves exactly like the main number row: `1-0` hot-pick
  works from the pad, and pad `Enter` acts like `Enter`. (Terminals send
  keypad digits as `Esc`-prefixed sequences; mradio resolves them so a stray
  `Esc` never quits.)
- Bare-launch quit is deliberate: on the initial menu there is no player to go
  back to, so `q`/`Esc` exits the app.

### 5.3 Mouse

Clicks are **off by default** (`"mouse": 0`) so terminal text stays selectable.
Enable them with `"mouse": 1` in `config.json`; then a click on the trivia text
toggles the full-screen note, and a click on the `UPDATE` pill opens the release
page.

## 6. Stations & favorites

Two distinct lists — this split is deliberate:

- **Favorites** (`f`) — *your* list. Lives in `~/.local/share/mradio/stations.json`
  under the key `"favorites"`:
  ```json
  { "favorites": [
      { "name": "WQXR", "url": "https://stream.wqxr.org/wqxr.mp3" },
      { "name": "Radio Swiss Classic",
        "url": "https://stream.srg-ssr.ch/srgssr/rsc_it/mp3/128" }
  ] }
  ```
  Numbered `1-0` for instant hot-picks (a maximum of **10** slots), in display
  order. **Releases never touch this file** once it exists — you own it. An
  empty `"favorites": []` is valid (start with no quick-picks). On the first
  run of a fresh machine the file is **auto-seeded once** with the first 10 of
  the current curated selection so the menu is useful immediately; after that
  it's yours to edit.
- **All stations** (`s`) — *our* curated list, shipped in the program (labels
  `S01`, `S02`, …). It can grow with every release; use `a` to copy any row
  into your favorites. This is how the project can keep "pushing" new stations
  without ever overriding your personal list.

Related behaviors:

- A legacy `stations` key in `~/.local/share/mradio/config.json` (pre-0.7.28
  config files) is honored **and migrated** into `stations.json` on the first
  run after upgrading.
- `MRADIO_STATIONS` overrides the favorites file path.
- **The JSON `name` is only a fallback label.** When the stream broadcasts a
  richer `icy-name` (e.g. `VCR Auditorium | Venice Classic Radio Italia`), it
  replaces the short label, exactly as a hand-typed URL would behave. Streams
  with **no icy-name** (some HLS feeds) keep the label; force your own label
  with the second CLI argument or an alias.

The current curated list (the `S01…Snn` seed) is tracked in
`.opencode/stationsproject.md`. Favorites presets can also be extra *aliases*:

```sh
alias vcra='mradio https://uk2.streamingpulse.com/ssl/vcr1 "Venice Classic Radio Auditorium"'
alias naim='mradio http://mscp3.live-streams.nl:8250/class-high.aac'
```

## 7. Updates & self-update

mradio checks GitHub's releases **atom feed** in a background thread: once at
startup, then every `MRADIO_UPDATE_INTERVAL` (default **1 hour**, minimum 60 s
→ max 24 checks/day vs GitHub's 60 req/hr anonymous limit). After the first
check it sends the feed's **ETag** back (`If-None-Match`), so an unchanged feed
returns a cheap `304` at no cost. GitHub's CDN can answer `304` for a feed that
already changed, so mradio treats a `304` as "trust nothing" and **re-fetches
the feed unconditionally** — the result can never be a stale last-known
version. The highest version found wins (not the first feed entry), so shuffled
feed order can't report an older release. Pressing `v` always refreshes in the
background after flashing the last known answer, so a newer release is picked
up the moment it exists.

When a newer release exists:

- a black-on-yellow **`UPDATE`** pill appears at the footer's right edge;
- the mid row adds `u:page` (open the release page) and `U:apply`;
- the running version is always shown at the bottom-right.

The startup check runs in the background, so this also applies **while you are
still on the station picker** (favorites or all stations): the pill and the
`u:page  U:apply` hint appear as soon as the check lands — you can update
before ever picking a station. Steady warnings always live in the yellow pill
on the right; the rest of the screen keeps its normal, quiet text.

After `U` has swapped the new file in, the running copy is still the *old*
version until you restart — the pill stays on the right and flips to
**`RESTART TO UPDATE`** (that steady warning lives exclusively in the yellow
pill; the hints just clear `u:page  U:apply`). Pressing `v` echoes
`updated to vX — restart to apply`. The pill clears once you restart onto
the new file.

| Key | What it does |
| --- | ------------ |
| `v` | force a check *now*; flashes `checking for updates…`, then `new version vX.Y.Z — press U`, `up to date (vX.Y.Z)`, or `check failed` in the AI row |
| `u` | open the release page (falls back appropriately) |
| `U` | **auto-update in place** (then `RESTART TO UPDATE` until you restart) |

`U` downloads the newest release's `mradio` asset, then:

1. **validates** it: requires a `VERSION = "…"` line matching the release tag,
   and compiles the downloaded Python before anything is touched;
2. **backs up** the running script to `mradio.old`;
3. **atomically swaps** the new file in.

The downloaded code is **never executed** — it only replaces the file on disk,
so the update takes effect on your next restart. Any failure (unwritable
directory, running from a git checkout, release without a `mradio` asset,
validation error, download failure) returns `False` with a one-line reason and
opens the release page in your browser instead — it never breaks the running
install.

> If you use `git` for installs: run in a checkout, `U` will correctly tell you
> to `git pull` — self-update only works on plain `install.sh`/`make install`
> layouts.

Tunables: `MRADIO_REPO` (owner/name, if you fork), `MRADIO_UPDATE_URL` (full
release-page URL), `MRADIO_UPDATE_INTERVAL` (seconds, min 60).

## 8. AI enrichment

Opt-in and **fully optional**. With no provider configured, playback and the
plain metadata display work perfectly and mradio makes no network calls for AI.

### 8.1 What it adds (when a provider is enabled)

- a dark-grey **trivia note** about the work (era, form, premieres, film usage, …);
- a **`Work:`** line when the station tag was only a movement/fragment;
- an **`o:`** link — but *only* to a Wikipedia article **verified to exist and
  match** (composer-surname + token overlap), so you never get a
  random-but-existing page.

### 8.2 Provider 1: OpenCode (recommended)

Three providers, in priority order. Only one needs to be configured — the
first that is both enabled *and* responding wins.

| # | Provider | How to enable | Notes |
| - | -------- | ------------- | ----- |
| 1 | **opencode** | **auto-detected** if the `opencode` CLI is on `PATH` | richest trivia, zero-auth, slowest (20–90 s) |
| 2 | **ollama** | `MRADIO_OLLAMA=http://host:11434` | fastest, most private, requires local resources |
| 3 | **NIM** | `3` in the UI → paste your NVIDIA API key | free hosted inference, no local resources |

OpenCode is the zero-config option — no API key, no account, just install and
go. mradio auto-detects it on `PATH` and drives it headlessly.

#### Install (macOS):

```sh
brew install anomalyco/tap/opencode
```

#### Install (Linux):

```sh
curl -fsSL https://opencode.ai/install | bash
```

#### Authenticate (first time only):

```sh
opencode auth
```

**Pros:** richest trivia, zero cost, no API key
**Cons:** slowest (20–90 s per track), requires the CLI installed

### 8.3 Provider 2: Ollama

Ollama runs a local LLM server. It's the fastest and most private option —
everything stays on your machine. You can run it locally or on a remote machine
(including Docker).

#### Install (macOS):

```sh
brew install ollama
```

#### Install (Linux):

```sh
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Docker (local or remote):

```sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

#### Pull the recommended model:

```sh
ollama pull gemma3:4b
```

This is the default model mradio uses. It's small, fast, and produces good
trivia. Other models work too — `llama3`, `phi3`, `mistral` — but `gemma3:4b`
is the sweet spot for quality vs speed.

#### Remote Ollama:

If Ollama runs on another machine (or inside Docker), point mradio to it by
pressing **`2`** when no server is configured (or **`c`** while provider 2 is
active) and typing the URL in the popup. The popup shows three example lines:

```sh
http://localhost:11434
http://192.168.1.12:11434
https://internet.accessible.server
```

The URL is saved to `settings.json` (`ollama_url`). You can also set it via
env var:

```sh
MRADIO_OLLAMA=http://192.168.1.100:11434 mradio
```

Or in `~/.local/share/mradio/settings.json`:

```json
{ "ollama_url": "http://192.168.1.100:11434" }
```

#### GPU offload:

If Ollama uses CPU instead of GPU, set
`MRADIO_OLLAMA_NUM_GPU=999` (or `"ollama_gpu": 999` in settings.json).

**Pros:** fastest, most private, no API key, runs offline
**Cons:** requires local resources (RAM/GPU), quality depends on model size

### 8.4 Provider 3: NIM (NVIDIA)

NIM is NVIDIA's hosted inference service. It's free for the `minimaxai/minimax-m3`
model and requires no local resources — just an NVIDIA account and API key.

#### Sign up:

1. Go to **https://build.nvidia.com**
2. Create an NVIDIA account (email + password)
3. **Add a phone number** when prompted (required for API key access)
4. Verify your phone number

#### Get your API key:

1. Go to **https://build.nvidia.com/settings/api-keys**
2. Click **"Generate Key"**
3. Copy the `nvapi-...` key

#### Set up in mradio:

Press **`3`** in the player to select NIM. If no API key is configured, a
TUI popup will appear asking you to paste your key. Paste it and press Enter.

To change your API key later, press **`c`**.

The key is saved to `~/.local/share/mradio/settings.json`. You can also
set it via environment variable:

```sh
MRADIO_API_KEY=nvapi-... mradio
```

**Model:** mradio uses `minimaxai/minimax-m3` by default — it's the only NIM
model that produces clean, strict JSON for mradio's schema every time. The
NIM catalogue changes often; other free models may appear or disappear.

**Pros:** free, no local resources, no install required
**Cons:** requires internet, requires NVIDIA account, slower than local

### 8.5 Prompt rules (NIM / choice 3)
Choice 3 ships with **extra "HARD TRUTHFULNESS RULES"** appended to its prompt
(choices 1/2 keep the stock prompt): never invent premiere dates, dedicatees,
film/TV/commercial appearances or awards; never claim a film appearance unless
certain; prefer verifiable structural facts; return `wiki` only if confident the
article exists; and never drift onto a different composer, performer or work.
It also relaxes the trivia length target — short-but-true beats padded.

### 8.6 In-session control

- **`1` / `2` / `3`** — switch provider live. The choice is saved to
  `config.json` and the current track is **re-requested immediately, even if
  cached** (so switching AIs always shows fresh info).
  - When **`3`** is selected with no API key, a TUI popup pastes your NVIDIA
    key; when the key is set the footer shows **`c:change API Key`** for 10s.
  - When **`2`** is selected with no Ollama server, a TUI popup asks for the
    server URL; when set the footer shows **`c:change Ollama URL`** for 10s.
- **`c`** — change the current provider's credential: the NIM API key, or the
  Ollama server URL (whichever is active).
- **`z` / `Z`** — expand the trivia note to full-screen (`z:collapse`), or click
  the text with mouse enabled.

While a provider is working you'll see a spinner with time, e.g. `▚ opencode 34s`.

### 8.7 How it works

1. mradio reads the `icy-title` (and artist/station context) for the current track.
2. A background thread asks the selected LLM for a structured enrichment
   (work title, work label, trivia, suggested article).
3. The proposed Wikipedia title is **resolved through the Wikipedia API** and
   only accepted if it exists *and* matches context tokens.
4. The result is cached in `cache.json`, keyed by track tag **and** labeled
   with the producing provider.

Repeating a track enriched by the current provider comes back **instantly**
(with no LLM call), even across restarts. A cached note is only reused when the
*same* provider is selected.

### 8.8 Diagnostics

Phased per-track timing goes to the log (`~/.local/share/mradio/mradio.log`):
spawn/health, session, LLM call, wiki resolve, plus a per-provider elapsed
breakdown, e.g.:

```
INFO llm[ollama] elapse=18.2s len=602 ok=True
INFO ollama: eval=392tok rate=21.4 tok/s total=18.3s load=2.1s
```

A low `rate` with an idle GPU usually means the model isn't GPU-offloaded —
set `MRADIO_OLLAMA_NUM_GPU=999` (or fix the ollama server config) and re-test.

### 8.9 Settings & env

Zero shell-config is possible: mradio self-writes `settings.json` on first run
with your current choices, so you can just edit that file. Environment
variables (`MRADIO_OLLAMA`, `MRADIO_API_KEY`, …) act as **optional one-shot
overrides** (env wins). `mradio --settings` prints the effective values.

## 9. Configuration & persistence

Everything lives self-contained in `~/.local/share/mradio/`:

| File | Purpose | Written by | You may edit |
| ---- | ------- | ---------- | ------------ |
| `config.json` | remembered provider, theme, volume, mute, mouse mode | `1/2/3`, `p`, `+/−`, `m`, manual | ✅ |
| `stations.json` | **your** favorites list | first-run seed, `a` key | ✅ freely |
| `settings.json` | AI settings (ollama/api/opencode) | first-run seed | ✅ freely |
| `cache.json` | past enrichment notes, tagged by provider | mradio | rarely |
| `mradio.log` | main diagnostics | mradio | no |
| `serve.log` | `opencode serve` internals (if used) | mradio | no |

### 9.1 `config.json`

```json
{ "provider": "opencode", "theme": "dark", "volume": 73, "mouse": 0 }
```

- `provider` — last AI provider picked with `1/2/3`.
- `theme` — last palette (`p`).
- `volume` — last volume (`+/−`, remembered so restart matches your ear).
- `mute` — last muted state (`m`, remembered **and re-applied**: mpv resets
  mute each time it restarts, so mradio re-pushes it on every launch,
  reconnect and station switch — a mute can no longer silently disappear).
- `mouse` — `0` (default) `=` clicks off (text selectable normal); `1` enables
  click zones (trivia text, `UPDATE` pill).

### 9.2 `settings.json`

Mirrors the AI env vars (`ollama_url`, `ollama_model`, `ollama_timeout`,
`ollama_gpu`, `api_base`, `api_key`, `api_model`, `api_timeout`, `opencode`,
`opencode_timeout`). Kept in sync with env at first run; env overrides win.

### 9.3 `stations.json`

```json
{ "favorites": [ { "name": "…", "url": "…" }, … ] }
```

See [Stations & favorites](#6-stations--favorites).

### 9.4 `cache.json`

Every enrichment ever computed, keyed by track tag and labeled with the
provider that produced it. Both `config.json` and `cache.json` are written
**atomically** and capped on load — they can't corrupt or grow without bound.

## 10. Environment variables

| Variable | Default | Meaning |
| -------- | ------- | ------- |
| `MRADIO_OLLAMA` | *(unset → off)* | Ollama API base URL |
| `MRADIO_OLLAMA_MODEL` | `gemma3:4b` | model (`gemma3:12b`, `llama3.2`, `mistral`, …) |
| `MRADIO_OLLAMA_TIMEOUT` | `75` | seconds before giving up on ollama |
| `MRADIO_OLLAMA_NUM_GPU` | `-1` | ollama `num_gpu` (−1=auto; force `999` if GPU idles on CPU) |
| `MRADIO_API_BASE` | `https://api.openai.com/v1` | OpenAI-compatible endpoint |
| `MRADIO_API_KEY` | *(unset → off)* | API key |
| `MRADIO_MODEL` | `gpt-4o-mini` | model to use |
| `MRADIO_API_TIMEOUT` | `30` | seconds before giving up on the API |
| `MRADIO_OPENCODE` | *(unset → off)* | `1` (port 4096) or a port number |
| `MRADIO_OPENCODE_TIMEOUT` | `180` | seconds to wait for opencode |
| `MRADIO_REPO` | `Marcus1571/mradio` | feed/release repo for the update check (fork) |
| `MRADIO_UPDATE_URL` | *(derived)* | override the full update-check/release URL |
| `MRADIO_UPDATE_INTERVAL` | `3600` | seconds between checks (minimum `60`) |
| `MRADIO_CFG` | `~/.local/share/mradio/config.json` | remembered provider/theme/volume/mute |
| `MRADIO_CACHE` | `~/.local/share/mradio/cache.json` | enrichment cache |
| `MRADIO_STATIONS` | `~/.local/share/mradio/stations.json` | your favorites list |
| `MRADIO_SETTINGS` | `~/.local/share/mradio/settings.json` | AI settings store |
| `MRADIO_LOG` | `~/.local/share/mradio/mradio.log` | main diagnostics |
| `MRADIO_SERVE_LOG` | `~/.local/share/mradio/serve.log` | `opencode serve` internals |
| `MRADIO_OC_PID` | `~/.local/share/mradio/opencode.pid` | opencode pidfile |

## 11. Themes

`p` rotates live (no reload) and the choice is remembered:

`dark → light → light-navy → light-mauve`

- Catppuccin-inspired palettes on 256-color terminals, classic ANSI otherwise.
- The active scheme shows right after the `LIVE`/`PAUSED` pill in the header,
  e.g. `light-navy (p)`.

## 12. Advanced use

- **Force a display name**: `mradio URL "Name"`.
- **Shell aliases** for favorites that force names once (see §6).
- **Fork the update channel**: set `MRADIO_REPO` (or `MRADIO_UPDATE_URL`) and
  `MRADIO_STATIONS` to your own, and ship your own curated list — the code stays
  upstream-clean.
- **Mouse zones**: `"mouse": 1` to make trivia text and the `UPDATE` pill
  clickable (§5.3).
- **Tune private AI**: `MRADIO_OLLAMA_NUM_GPU=999` to force GPU offload.
- **Diagnose**: `cat ~/.local/share/mradio/mradio.log` has per-phase timing;
  `--settings` shows effective config.

## 13. Troubleshooting / FAQ

**No sound / dead stream.**
Press `r` (reconnect). If that fails, the stream itself is down — check the
mount with a browser, or pick another preset (`f`/`s`). mpv is the engine, so
any stream mpv can't demux won't play; mradio just relays.

**Station shows no name.**
The stream sends no `icy-name` (common with HLS/adaptive feeds, e.g. BBC).
Force one: `mradio URL "My Station"`, or use an alias / the favorites file.

**The numeric keypad seems to do nothing (or quits!).**
Terminals send pad digits as `Esc`-prefixed sequences. mradio resolves `Esc O
1…0` (and pad `Enter`) so pad hot-picks work; if a terminal sends something
exotic, treat it as *not a digit* rather than a quit. A bare `Esc` is handled as
back/quit — that's by design.

**Random digit/characters on the shell prompt after quitting.**
Keypresses typed while mradio was shutting down (mpv cleanup takes ~2 s) used
to sit in the terminal buffer and get replayed after exit. mradio drains
pending input before handing the tty back (0.7.48+) — if you still see a
stray char it was typed *after* the prompt returned.

**`U` won't apply an update.**
Likely one of: running from a git checkout (`git pull` instead), the directory
isn't writable, the release lacks the `mradio` asset, or validation failed
(version mismatch / syntax). mradio flashes the reason and opens the release
page — it never half-applies.

**AI features never show up (no AI row, no trivia).**
mradio needs *at least one* provider. Easiest: just install the **opencode
CLI** — mradio 0.7.50+ auto-detects it on `PATH` (no config needed; sign in
with `opencode auth` first). Alternatives: `MRADIO_API_KEY=…` for any
OpenAI-compatible API, or `MRADIO_OLLAMA=http://host:11434` with ollama.

**`v` says "check failed".**
Network/GitHub hiccup — hourly watcher will retry. Very small repro rate is
fine; genuinely offline machines just get `check failed`.

**AI enrichment never fires.**
No provider configured (see §8), or the current provider was unreachable and
the next-in-order also failed. Enrichment is silent by design — check
`mradio.log` for the per-phase breakdown.

**Enrichment is slow.**
opencode via the free gateway is 20–90 s by nature. Ollama is fast but check
`rate` in the log; GPU offload matters (§8.4). The cache makes repeats instant.

**Switched provider but the trivia looks stale.**
Cache is tagged by provider — a cache entry is only reused for the provider
that produced it. Pressing `1/2/3` deliberately invalidates & re-requests the
current track.

**Everyday logs grow.**
With default settings a week of normal use is tiny; `mradio.log` is a simple
append you can truncate anytime (`: > ~/.local/share/mradio/mradio.log`).

## 14. Development

```sh
make check    # py_compile mradio + bash -n install.sh
make test     # python test_mradio.py (36 tests)
make smoke    # sanity: --version/--help round-trip
```

- The whole app is **one self-contained file** (`mradio`, stdlib only) plus
  `install.sh`; `test_mradio.py` holds the test suite; `stations_mockup.py` is a
  standalone visual mock used during UI design (not shipped).
- Key areas in `mradio`: `DEFAULT_STATIONS` (curated list), `load_favorites` /
  `save_favorites` (favorites file), `render` / `render_menu` (TUI),
  `update_watcher` / `check_update` / `apply_update` (self-update),
  the `Enricher` class + cache (AI), `Mpc` (mpv IPC wrapper).

## 15. Design notes & limitations

- **Why mpv?** Live radio streams are messy: icecast metadata, HTTPS,
  reconnects. Handing the media handling to a battle-tested player (and talking
  to it over a Unix socket) means mradio never has to reimplement demuxing or
  reconnect logic.
- **Windows** is unsupported because Python's official Windows build lacks
  `curses`; WSL is the official path.
- **Playlists/HLS**: mpv handles them, but `icy-name`/`icy-title` metadata isn't
  available on HLS-style feeds, so such stations (e.g. BBC R3) show a forced or
  host-based name and no now-playing tags.
- **Geo/mount caveats** apply exactly as with any public broadcaster: some
  feeds (e.g. BBC non-UK HLS variants) can be retracted or geo-limited.
- **Updates are poll-based, never auto-executed.** The app downloads nothing
  without `U`, executes nothing from the network, and only ever replaces its own
  script file (atomically, next restart).
- **Single process, three background threads**: update watcher, enrichment/
  LLM worker(s), and the main UI loop — playback never blocks on the AI.

## 16. Privacy

- **AI is opt-in by default.** With no provider configured, mradio makes no AI
  network calls; it only touches the stream and (for updates) GitHub's feeds.
- Enrichment means sending the **current track tag** to your chosen provider.
  Ollama keeps that on your own network; opencode routes through its gateway;
  APIs send the tag to the provider (Groq, OpenRouter, …).
- Every enrichment is cached **locally** in `cache.json`; nothing leaves your
  machine for a repeat of a cached track.
- Self-update downloads are validated (version match + compile) and **never
  executed** — the running copy is untouched until your next manual restart.
- Logs are local plain text you can read and truncate freely.