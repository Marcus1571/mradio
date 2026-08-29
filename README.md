# ● RADIO

> **A tiny terminal radio with big ears.** Live classical & jazz from curated
> streams, AI liner notes on whatever is playing, and a UI that behaves — all
> in one ~1700-line Python file with **zero dependencies**.

<p align="center">
  <img src="screenshots/player.png" alt="mradio player" width="860">
</p>

> **The complete, living knowledge base — every key, every setting, every
> stream — lives in [**KB.md**](KB.md).** This page is just the appetizer.

---

## The idea

You open a terminal, press one key, and the world's great music is playing —
Brahms from the Chicago Symphony, this minute, with a scholar's paragraph
explaining what you're hearing. No accounts. No ads. No Electron.

- **Curated, not curated-to-death.** A hand-picked list, `1-9` away at all
  times. Every entry is cleaned, tagged, and meaningfully described — not a
  firehose of 40,000 streams.
- **Favorites that are yours.** `stations.json` is a plain file you own,
  edit, and back up. `a` adds the row under your cursor. Your list, your rule.
- **AI in your corner.** Press `1` — or just watch — and mradio writes an
  intelligent liner note about the playing work via opencode, ollama, or any
  OpenAI-compatible API. No API key? Nothing to install, it still works.
- **Radios that keep themselves fresh.** One file for config, cache, streams,
  and settings; a self-update that pulls the latest release in-place with `U`.

Every valve lives in the machine room: **[KB.md](KB.md) (the long read)**.

---

## In the wild

<p align="center">
  <img src="screenshots/favorites.png" alt="favorites menu" width="420">
  <img src="screenshots/all-stations.png" alt="all-stations menu" width="420">
</p>

`f` drops your favorites — one press tunes in. `s` opens the full curated
catalog. `k` leaps straight to this book.

---

## 30-second start

```sh
git clone https://github.com/Marcus1571/mradio.git
cd mradio
./install.sh        # -> ~/.local/bin, no root needed
mradio
```

That's it. **python3 (stdlib only) + mpv** is the whole machine room —
context in **[KB §2 — Requirements & install](KB.md#2-requirements--install)**.

### The keys that matter

| Key | What it does |
| --- | ------------ |
| `1`-`9`, `0` | tune a favorite, instantly |
| `v` | check for the latest release (and watch it land) |
| `k` | open the knowledge base |
| **Full keyboard & menus**: **[KB.md](KB.md)** |

---

## Why you're reading this

**This README is the appetizer.** The full guide —

installation for macOS / Debian / Ubuntu / Fedora / Arch & friends / WSL,
every menu, every theme, every `MRADIO_*` setting, the AI providers, the
self-update flow, and answers to "but why…?" — is one link away:

<p align="center">
  <a href="KB.md"><strong>→ Open the Knowledge Base ←</strong></a>
</p>

Terminal, but make it *cultural*.

---

*License: MIT. Author: [Marcus1571](https://github.com/Marcus1571).*