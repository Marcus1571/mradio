# mradio

A colorful terminal radio player that uses **mpv** as the audio engine and a
Python `curses` frontend to show what's playing — plus AI enrichment for the
now-playing track.

Version history: [CHANGELOG.md](CHANGELOG.md)

<p align="center">
  <img src="https://raw.githubusercontent.com/Marcus1571/mradio/main/docs/mradio-preview.png"
       alt="mradio — dark terminal (left) and light terminal (right): live-station header, AI-enriched track info and trivia, audio meters and key help">
</p>

The screenshot shows both color palettes side by side (below is the same screen
in plain text):

```
 ● RADIO  ▸  VCR Auditorium | Venice Classic Radio Italia  ▸  LIVE

 Luigi Boccherini (1743-1805)
 Quartetto per archi in Sol minore n.6 op.24
 (Europa Galante - Fabio Biondi, violino e direzione)
 work: ...
 This quartet is part of a series of works that showcases Boccherini's      <- AI trivia
 mastery of the string quartet form, often featuring virtuosic passages
 typical of the late Classical period.

  — · 44.1 kHz · mp3 · cache — · stream 00:45
  vol
  ████████████████████████████████████████████████████████████████████  100%

  q:quit   space:pause   + / -:volume   m:mute   r:reconnect   o:open article
```

## Why mpv as the engine?

Radio streams are messy: icecast metadata, HTTPS, reconnects. mpv already
handles all of that battle-tested — mradio just drives it over mpv's IPC
socket, so *you* never see a raw media player. Decoding, networking, and
stream metadata all belong to mpv; mradio is a thin, colorful display + remote
control on top.

## Requirements & platform support

mradio is a single, stdlib-only Python script that drives `mpv`, so it runs on
any modern Unix-like system with Python and mpv installed:

- **python3** (3.8+; stdlib only, no pip dependencies)
- **mpv** — the audio engine: `brew install mpv` (macOS), `apt install mpv`
  (Debian/Ubuntu), `dnf install mpv` (Fedora), `pacman -S mpv` (Arch), …

| OS | Status | Notes |
| --- | ------ | ----- |
| 🍎 macOS | ✅ works | fully tested; install mpv via Homebrew |
| 🐧 Linux | ✅ works | any distro with `python3` + `mpv` |
| 🪟 Windows | ❌ not supported | Python's official Windows build lacks `curses` — use [WSL](https://learn.microsoft.com/windows/wsl/) and follow the Linux steps |

> The UI is built with `curses`, Python's terminal-UI module. The official
> Windows build of Python does not ship `curses`, so mradio can't run natively
> on Windows — but it runs fine inside WSL (e.g. Ubuntu), where `apt install
> mpv` + `chmod +x install.sh && ./install.sh` is all it takes.

## Install

```sh
git clone https://github.com/<you>/mradio.git
cd mradio
./install.sh        # copies mradio to ~/.local/bin
```

or `make install` / `sudo install -m755 mradio /usr/local/bin/mradio`.

## Keys

| Key        | Action                                   |
| ---------- | ---------------------------------------- |
| `q`        | quit                                     |
| `space`    | pause / resume                           |
| `+` / `→`  | volume up                                |
| `-` / `←`  | volume down                              |
| `m`        | mute                                     |
| `r`        | reconnect (revive a dead stream/station) |
| `o`        | open the verified Wikipedia article      |
| `u`        | open the release page when an update is available |
| `U`        | auto-update: download & apply the newest release (restart to finish) |
| `z`        | expand/collapse the full trivia note: fills the screen with the complete text. Long notes that don't fit the window show a `…` marker instead of being silently cut. Click-to-toggle is **off by default** to keep the terminal text selectable — opt in with `mouse = 1` in `config.json` |
| `1` `2` `3`| select AI provider: 1=opencode, 2=ollama, 3=api key. Saves the choice and re-requests the current track's trivia immediately — **even if a cached note exists** |
| `p`        | swap color scheme: dark-terminal vs light-terminal palette. Instant, no reload, and remembered for next sessions (your current theme + key appear right after the LIVE pill up top) |

A second help line near the bottom shows the current AI provider whenever AI is
configured; the enrichment spinner also shows which provider is working
(`▚ opencode 34s`).

## Updates

The cornerstone of the right edge of the screen:

- the **current version** is always shown at the bottom-right (e.g. `v0.7.18`);
- if a newer release exists, a black-on-yellow **`UPDATE`** pill appears right
  above it. Click it (opt in with `"mouse": 1` in `config.json`), press **`u`**
  for the release page, or press **`U`** to **auto-update in place**:
  mradio downloads the newest release's `mradio` asset, validates it (Python
  syntax + version, requires newer-than-current), backs up the running file to
  `mradio.old` and swaps it in atomically. The downloaded code is never
  executed — the update applies on your next restart.
  Upgrade manually with the usual `git pull && ./install.sh`.

mradio checks the GitHub releases feed hourly (24 requests/day — far under
GitHub's 60 req/hr anonymous REST limit) in a background daemon thread, and
it **never downloads or executes code automatically** — it only reports. Since
0.7.16 each check is a conditional request: the feed's ETag is sent back, so an
unchanged feed returns a `304` that doesn't count against the limit at all.
Tune the cadence with `MRADIO_UPDATE_INTERVAL` (seconds, minimum 60), point at
a different repo with `MRADIO_REPO` (owner/name) or set `MRADIO_UPDATE_URL`
(full releases URL) if you fork.

Because the app can stay open for days, the check runs once at startup and
then repeats every hour so a release cut mid-session still lights up the
pill.

If `U` can't apply an update (not writable, release lacks the `mradio` asset,
validation fails, or you're running from a git checkout), mradio shows a short
status message and opens the release page instead — it never breaks the
running install.

## Usage

```sh
mradio                                # plays Venice Classic Radio (VCR1)
mradio https://some-radio-url/stream.mp3
mradio https://some-radio-url/stream.mp3 "My Station"   # force the display name
mradio --version | --help
```

The station name shown in the top bar is normally read automatically from the
stream's own icy-name metadata, e.g. `VCR Auditorium | Venice Classic Radio
Italia`. If a stream reports no name — or one you'd rather not show — force it
with an optional second argument:

```sh
mradio https://uk2.streamingpulse.com/ssl/vcr1 "Venice Classic Radio Auditorium"
```

### Handy aliases

Save your favorite stations as aliases so you don't type URLs (and so you can
force the display name once, in the alias). First find which shell you use:

```sh
echo $0                # prints something containing "zsh" or "bash"
basename "$SHELL"      # prints just "zsh" or "bash" (reliable everywhere)
```

Then append aliases to the matching startup file:

| Shell  | File to edit                                              |
| ------ | --------------------------------------------------------- |
| zsh    | `~/.zshrc`, or `~/.zsh_aliases` if you keep one           |
| bash   | `~/.bashrc`, or `~/.bash_aliases` (sourced if it exists)  |

```sh
# e.g. add these to the file for your shell
alias vcra='mradio https://uk2.streamingpulse.com/ssl/vcr1 "Venice Classic Radio Auditorium"'
alias vcrl='mradio https://uk2.streamingpulse.com/ssl/vcr2 "Venice Classic Radio Live"'
alias naim='mradio http://mscp3.live-streams.nl:8250/class-high.aac'
alias swissjazz='mradio http://stream.srg-ssr.ch/m/rsj/mp3_128'
```

Reload with `source ~/.zshrc` (or `source ~/.bashrc` / `~/.bash_aliases`) or
just open a new terminal window, then run `vcra`. Streams without a forced name
still display their icy-name automatically.

## AI enrichment (optional, opt-in)

**Zero shell-config:** mradio is fully self-contained in its own directory.
All AI settings live in `~/.local/share/mradio/settings.json`, which is
auto-created on first run with your current choices — no `.zshrc`/`.bashrc`
exports required. Shell environment variables (`MRADIO_OLLAMA`, `MRADIO_API_KEY`,
`MRADIO_OPENCODE`, …) still work as *optional* one-shot overrides for advanced
use, but nothing needs them. `mradio --settings` prints the effective settings.

By default mradio is AI-free and works anywhere mpv runs. When a track is
playing it can additionally enrich the display with:

- a dim **trivia note** about the work (era, form, premieres, film usage, …),
- a `Work:` line when the station tag was only a movement/fragment,
- an `o:` link — but only to a **Wikipedia article that has been verified to
  exist *and* match** (composer surname + token overlap), so you never get a
  random-but-existing page.

It does this by asking an LLM and then resolving the proposed work title
through Wikipedia's API. Two provider modes, both opt-in:

**1. Ollama** (your own server/box — most private):
| Variable                 | Default                | Meaning                     |
| ------------------------ | ---------------------- | --------------------------- |
| `MRADIO_OLLAMA`          | *(unset → off)*        | Ollama API base URL         |
| `MRADIO_OLLAMA_MODEL`    | `gemma3:4b`           | model to use (`gemma3:12b`, `llama3.2`, …) |
| `MRADIO_OLLAMA_TIMEOUT`  | `75`                   | seconds before giving up    |
| `MRADIO_OLLAMA_NUM_GPU`  | `-1`                   | ollama `num_gpu` (-1=auto; force e.g. `999` if the GPU idles and it's running on CPU) |

**2. OpenAI-compatible API** (any free-tier provider — Groq, OpenRouter,
Google Gemini, NVIDIA NIM, together.ai, …). This is what you hand to friends
who just want a free key:
| Variable                 | Default                  | Meaning                     |
| ------------------------ | ------------------------ | --------------------------- |
| `MRADIO_API_BASE`        | `https://api.openai.com/v1` | OpenAI-compatible endpoint |
| `MRADIO_API_KEY`         | *(unset → off)*          | API key                    |
| `MRADIO_MODEL`           | `gpt-4o-mini`            | model to use                |
| `MRADIO_API_TIMEOUT`     | `30`                     | seconds before giving up    |

Examples:

```sh
export MRADIO_API_KEY=your_free_groq_key
export MRADIO_API_BASE=https://api.groq.com/openai/v1
export MRADIO_MODEL=llama-3.3-70b-versatile
mradio
```

```sh
# or with Ollama running on this machine (the default install)
export MRADIO_OLLAMA=http://localhost:11434
export MRADIO_OLLAMA_MODEL=gemma3:4b
mradio
```

`localhost:11434` is Ollama's default address on the same machine mradio runs
on. If Ollama lives on a *different* computer (a desktop with a beefier GPU, a
NAS, a home server) just point `MRADIO_OLLAMA` at that host instead — any
`http://host:11434` works, including over your LAN. The **gemma3** family is a
great free place to start (`gemma3:4b` fits ~8 GB of VRAM; `gemma3:12b` for the
roomier ones), with `llama3.2` and `mistral` as equally solid lightweight
alternatives; any model you got via `ollama pull` is fair game.

Enrichment is fully optional and fails silently: if no provider is configured
or reachable, playback and the plain metadata display still work perfectly.
Audio playback never blocks on the AI — enrichment runs in a background thread
and is cached per track. Providers are tried in order: **opencode → ollama →
API key**, using the first that is configured and responds.

The `MRADIO_*` variables named below are mirrored as keys in `settings.json`
(`ollama_url`, `api_key`, `opencode`, …); edit the file directly or use the env
override — whichever you prefer.

**3. opencode (bonus — zero-auth when it works)**: if you have
[opencode](https://opencode.ai) installed, mradio can drive it headlessly
(`opencode serve`) and get free enrichment from whatever model opencode is
connected to — no API key needed:
| Variable                 | Default    | Meaning                            |
| ------------------------ | ---------- | ---------------------------------- |
| `MRADIO_OPENCODE`        | *(unset → off)* | `1` (use port 4096) or a port number |
| `MRADIO_OPENCODE_TIMEOUT`| `180`               | seconds to wait for a reply       |

> Note: the opencode route is the slowest of the three (free gateway often
> takes 20–90 s per track) but gives the richest trivia. Ollama is fastest,
> APIs are in between. While it works you'll see `▚ opencode 34s` in the display.
> Trivia is aimed at ~750–850 characters. In the normal view a note that does
> not fit the window is word-wrapped and marked with `…`; press `z` (or click the
> text) to read the full note full-screen, expanding again to collapse.

## Persistence & caching

Two small files under `~/.local/share/mradio/`:

- **`config.json`** — your AI provider choice, color theme, last volume, and the
  mouse mode (e.g. `{"provider": "opencode", "theme": "dark", "volume": 73,
  "mouse": 0}`); press `1/2/3` to change the provider, `p` to flip the palette,
  or `+`/`-` to set the volume — future sessions start exactly the way you left
  them. `mouse` is `0` by default (click events are not captured, so terminal
  text selection works normally); set it to `1` to let clicks on the trivia text
  expand/collapse it.
- **`cache.json`** — every enrichment ever computed, keyed by track tag, and
  **labeled with the AI provider that produced it**. A cached note is only
  reused when the same provider is selected, so switching AIs always re-fetches
  fresh info — but repeats of a track enriched by the current provider come
  back *instantly* (no LLM call), even across restarts. Both files are written
  atomically and capped on load, so they can't corrupt or grow without bound.

To diagnose a slow/unusual round-trip, the log shows exactly where time went.
The ollama path additionally reports its own telemetry, e.g.:

```
INFO llm[ollama] elapse=18.2s len=602 ok=True
INFO ollama: eval=392tok rate=21.4 tok/s total=18.3s load=2.1s
```

A low `rate` with an idle GPU usually means the model isn't GPU-offloaded —
set `MRADIO_OLLAMA_NUM_GPU=999` (or fix the ollama server config) and re-test.

## Logging & troubleshooting

mradio writes a timestamped diagnostic log where every enrichment round-trip
is broken into phases (spawn/health, session, LLM call, wiki resolve), with a
per-provider elapsed breakdown and a clean summary per track:

```sh
cat ~/.local/share/mradio/mradio.log   # main diagnostics (default)
cat ~/.local/share/mradio/serve.log    # opencode serve internals (if used)
```

| Variable                 | Default                               | Meaning                       |
| ------------------------ | ------------------------------------- | ------------------------------ |
| `MRADIO_LOG`             | `~/.local/share/mradio/mradio.log`    | diagnostic log path           |
| `MRADIO_SERVE_LOG`       | `~/.local/share/mradio/serve.log`     | `opencode serve` output log   |
| `MRADIO_CFG`             | `~/.local/share/mradio/config.json`   | remembered provider choice    |
| `MRADIO_CACHE`           | `~/.local/share/mradio/cache.json`    | past-enrichment cache         |

## Development

```sh
make check   # syntax checks
```

## License

MIT