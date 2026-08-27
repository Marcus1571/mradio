# mradio

A colorful terminal radio player that uses **mpv** as the audio engine and a
Python `curses` frontend to show what's playing — plus AI enrichment for the
now-playing track.

```
 ● RADIO  ▸  uk2.streamingpulse.com  ▸  LIVE

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

## Requirements

- **python3** (3.8+; stdlib only, no pip dependencies)
- **mpv** — `brew install mpv` (macOS), `apt install mpv`, etc.

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
| `1` `2` `3`| select AI provider: 1=opencode, 2=ollama, 3=api key. Saves the choice and re-requests the current track's trivia immediately — **even if a cached note exists** |
| `p`        | swap color scheme: dark-terminal vs light-terminal palette. Instant, no reload, and remembered for next sessions (your current theme + key appear right after the LIVE pill up top) |

A second help line near the bottom shows the current AI provider whenever AI is
configured; the enrichment spinner also shows which provider is working
(`▚ opencode 34s`).

## Usage

```sh
mradio                              # plays Venice Classic Radio (VCR1)
mradio https://some-radio-url/stream.mp3
mradio --version / --help
```

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
| `MRADIO_OLLAMA_MODEL`    | `gemma4:e4b-it-qat`    | model to use                |
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
# or with your own ollama
export MRADIO_OLLAMA=http://192.168.88.8:11434
export MRADIO_OLLAMA_MODEL=gemma4:e4b-it-qat
mradio
```

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
> Trivia is aimed at ~750–850 characters; the display shows the full text the
> model wrote, uncut — there is no visible `…` truncation.

## Persistence & caching

Two small files under `~/.local/share/mradio/`:

- **`config.json`** — your AI provider choice and color theme
  (`{"provider": "opencode", "theme": "dark"}`); press `1/2/3` to change the
  provider or `p` to flip the terminal palette, and future sessions start the
  same way.
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