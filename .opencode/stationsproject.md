# stationsproject.md — station presets sub-project

## What this is

A sub-project exploring the idea of adding **station toggles / a switcher** to
the mradio TUI (preset list, cycle keys, remember the last choice). The user
wants to **personally audition and approve each station** before it is wired
into the UI — so this file is the shared working list: every candidate found
during research, with its verified stream URL, status, and notes.

Nothing here is a commit to ship: a station only becomes a preset when the
user marks it **👍 approved**.

## How to audition a station today

mradio takes the stream as the first argument and an optional display name as
the second:

```sh
mradio "<stream-url>" "<Station Name>"
```

All MP3/icy streams below feed artist/title + station name into the TUI
automatically. Only BBC (HLS) has no icy metadata — pass the name as arg 2.

## Status legend

- **👍 approved** — user listened and is OK with it.
- **candidate** — user asked it be added for auditioning (verified live, HTTP 200).

Rule: entries are only added when the **user explicitly asks**. The assistant
does not add stations on its own initiative.

## Stations

| Status | Station | Stream (as verified) | Origin / quality | icy | Notes |
|---|---|---|---|---|---|
| candidate | **VCR Auditorium \| Venice Classic Radio Italia** | `https://uk2.streamingpulse.com/ssl/vcr1` | Venice Classic Radio Italia, 128k MP3 | yes | icy-name `VCR Auditorium \| Venice Classic Radio Italia`. |
| candidate | **VCR Classica+ \| Venice Classic Radio Italia** | `https://uk2.streamingpulse.com/ssl/vcr2` | Venice Classic Radio Italia, 128k MP3 | yes | icy-name `VCR Classica+ \| Venice Classic Radio Italia`. |
| 👍 | **Radio Swiss Classic** | `https://stream.srg-ssr.ch/srgssr/rsc_it/mp3/128` | Swiss public, 128k MP3 | yes | icy-name `Swiss Classic I` — the **Italian-language** feed (D = German, F = French variants exist). "Ohne Werbung" (no ads). |
| candidate | **Naim Classical** | `http://mscp3.live-streams.nl:8250/class-high.aac` | Naim Audio radio, 320k AAC | yes | icy-name `Naim Classical`; brand radio (naimaudio.com). |
| 👍 | **WQXR** | `https://stream.wqxr.org/wqxr.mp3` | US, member-supported, 128k MP3 | yes | User-tested and OK. No ad breaks, occasional underwriting. |
| candidate | **Classic FM** | `http://ice-the.musicradio.com/ClassicFMMP3` | UK commercial (Global), 128k MP3 | yes | icy-name `Classic FM`. **Has ad breaks** — not commercial-free (user auditioning anyway). |
| candidate | **Swiss Jazz** | `http://stream.srg-ssr.ch/m/rsj/mp3_128` | Swiss public, 128k MP3 | yes | icy-name `Swiss Jazz`; jazz (sibling of Radio Swiss Classic). |
| candidate | **Radio Paradise** | `https://stream-uk1.radioparadise.com/mp3-128` | US listener-supported, 128k MP3 | yes | icy-name `Radio Paradise (128k mp3)`. Eclectic (not classical): rock/electronica/world. icy: "Always 100% commercial-free". |
| candidate | **radio klassik Stephansdom** | `http://radioklassikstephansdom.ice.infomaniak.ch/radioklassikstephansdom.mp3` | Austria, non-profit, 128k MP3 | yes | Vienna classical radio, donation-funded. http (not https). |
| candidate | **NPO Klassiek** | `https://icecast.omroep.nl/radio4-bb-mp3` | Dutch public, 192k MP3 | yes | icy-name "NPO Klassiek", genre Classical. |
| candidate | **France Musique** | `https://icecast.radiofrance.fr/francemusique-midfi.mp3` (or `.aac` for 96k) | French public, 128k MP3 | yes | Classical + jazz + live concerts. |
| candidate | **BBC Radio 3** | `http://a.files.bbci.co.uk/ms6/live/3441A116-B12E-4D2F-ACA8-C1984642FA4B/audio/simulcast/hls/nonuk/audio_syndication_low_sbr_v1/ak/bbc_radio_three.m3u8` | UK public, HLS AAC+ 96k | **no** | HLS only (BBC killed MP3 in 2023); worldwide geo caveats; no artist/title metadata. |

## Research notes

- **Wired into mradio:** these 12 presets are baked in as `DEFAULT_STATIONS`
  in `./mradio` and shown by the **`s` all-stations menu** (labels `S01…Snn`,
  arrows/Enter to pick). Your **number-`1-9` favorites** live in
  `~/.local/share/mradio/stations.json` (key `"favorites"`, opened by `f`),
  seeded once from `DEFAULT_STATIONS` on first run; afterwards the file is
  entirely the user's (releases never touch it). `a` inside the `s` menu
  copies a row into favorites. Favorite hot-keys are `1-9` then **`0`** (10th);
  the numeric keypad behaves like the main number row. `MRADIO_STATIONS`
  overrides the path; a legacy
  `config.json` → `"stations"` list is migrated on first run.
- Most picks are **public-service or non-profit** → no commercial ad breaks
  (Classic FM is the exception: commercial, with ad breaks; Naim is a brand
  radio). WQXR is member-supported with occasional underwriting.
- Verified 2026-08-29: every URL returned HTTP 200 with the expected codec
  and (except BBC) `icy-name` + `icy-metaint` for metadata parsing.
- Radio Swiss Classic comes in three SRG SSR language feeds — **D** (German),
  **F** (French), **I** (Italian) — plus sibling stations Swiss Jazz (`rsj`)
  and Swiss Pop (`rsp`).
- **VCR Auditorium (vcr1)** is mradio's current default stream
  (`DEFAULT_URL` in `./mradio` is `https://uk2.streamingpulse.com/ssl/vcr1`);
  **VCR Classica+ (vcr2)** is its companion stream on the same host.
- Deferred/not workable: ORF Ö1 (mount names retired), RTBF Musiq3 (TLS 503),
  RTÉ lyric fm (404), ABC Classic & MPR/YourClassical (stream hosts moved).