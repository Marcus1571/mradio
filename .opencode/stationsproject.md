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
- **candidate** — verified live (HTTP 200, correct codec), not yet auditioned.

## Stations

| Status | Station | Stream (as verified) | Origin / quality | icy | Notes |
|---|---|---|---|---|---|
| 👍 | **WQXR** | `https://stream.wqxr.org/wqxr.mp3` | US, member-supported, 128k MP3 | yes | User-tested and OK. No ad breaks, occasional underwriting. |
| candidate | **VCR Auditorium** | `https://uk2.streamingpulse.com/ssl/vcr1` | Venice Classic Radio Italia, 128k MP3 | yes | icy-name `VCR Auditorium \| Venice Classic Radio Italia`. |
| candidate | **VCR Classica+** | `https://uk2.streamingpulse.com/ssl/vcr2` | Venice Classic Radio Italia, 128k MP3 | yes | icy-name `VCR Classica+ \| Venice Classic Radio Italia`. |
| candidate | **Naim Classical** | `http://mscp3.live-streams.nl:8250/class-high.aac` | Naim Audio radio, 320k AAC | yes | icy-name `Naim Classical`; brand radio (naimaudio.com). |
| candidate | **Classic FM** | `http://ice-the.musicradio.com/ClassicFMMP3` | UK commercial (Global), 128k MP3 | yes | icy-name `Classic FM`. **Has ad breaks** — not commercial-free (user auditioning anyway). |
| candidate | **Radio Paradise** | `https://stream-uk1.radioparadise.com/mp3-128` | US listener-supported, 128k MP3 | yes | icy-name `Radio Paradise (128k mp3)`. Eclectic (not classical): rock/electronica/world. icy: "Always 100% commercial-free". |
| candidate | **VRT Klara Continuo** | `https://icecast.vrtcdn.be/klaracontinuo-high.mp3` | Belgium public, 128k MP3 | yes | 24/7 pure classical, zero talk/interruption. |
| candidate | **VRT Klara** | `https://icecast.vrtcdn.be/klara-high.mp3` | Belgium public, 128k MP3 | yes | Classical + jazz, lightly presented. |
| candidate | **Radio Swiss Classic** | `https://stream.srg-ssr.ch/srgssr/rsc_de/mp3/128` | Swiss public, 128k MP3 | yes | "Ohne Werbung" (no ads), German-language. |
| candidate | **BR-Klassik** | `https://streams.br.de/br-klassik_3.m3u` (physical: `https://dispatcher.rndfnk.com/br/brklassik/live/mp3/high`) | German public, 256k MP3 | yes | Highest fidelity of the lot; m3u is BR's stable entry point. |
| candidate | **radio klassik Stephansdom** | `http://radioklassikstephansdom.ice.infomaniak.ch/radioklassikstephansdom.mp3` | Austria, non-profit, 128k MP3 | yes | Vienna classical radio, donation-funded. http (not https). |
| candidate | **NPO Radio 4 / Klassiek** | `https://icecast.omroep.nl/radio4-bb-mp3` | Dutch public, 192k MP3 | yes | icy-name "NPO Klassiek", genre Classical. |
| candidate | **France Musique** | `https://icecast.radiofrance.fr/francemusique-midfi.mp3` (or `.aac` for 96k) | French public, 128k MP3 | yes | Classical + jazz + live concerts. |
| candidate | **BBC Radio 3** | `http://a.files.bbci.co.uk/ms6/live/3441A116-B12E-4D2F-ACA8-C1984642FA4B/audio/simulcast/hls/nonuk/audio_syndication_low_sbr_v1/ak/bbc_radio_three.m3u8` | UK public, HLS AAC+ 96k | **no** | HLS only (BBC killed MP3 in 2023); worldwide geo caveats; no artist/title metadata. |

## Research notes

- All picks are **public-service or non-profit** → no commercial ad breaks.
  WQXR is member-supported and runs occasional underwriting only.
- Verified 2026-08-29: every URL returned HTTP 200 with the expected codec
  and (except BBC) `icy-name` + `icy-metaint` for metadata parsing.
- BR's `dispatcher.rndfnk.com` URL is the physical stream; preferring
  `streams.br.de/...m3u` survives CDN address changes.
- **VCR Auditorium (vcr1)** is mradio's current default stream
  (`DEFAULT_URL` in `./mradio` is `https://uk2.streamingpulse.com/ssl/vcr1`);
  **VCR Classica+ (vcr2)** is its companion stream on the same host.
- Deferred/not workable: ORF Ö1 (mount names retired), RTBF Musiq3 (TLS 503),
  RTÉ lyric fm (404), ABC Classic & MPR/YourClassical (stream hosts moved).
- Klara Continuo is the strongest "set and forget" candidate (nothing but
  music); Radio Swiss Classic and BR-Klassik are likely the best "station"
  experience (moderated but ad-free).