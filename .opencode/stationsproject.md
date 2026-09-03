# stationsproject.md — station audit / approval work list

## What this is

A sub-project for **auditioning and approving stations** before they are wired
into mradio. The user wants to **personally listen and approve each station**.
This file is the shared working list of stations and their approval state.

- A station only becomes part of mradio when the user marks it **👍 approved**
  (and it is then curated in `DEFAULT_STATIONS` in `./mradio`).
- **Research lives elsewhere:** the durable record of every stream URL found,
  its verification status (HTTP 200, codec, bitrate, icy-metadata, votes) and
  the how/what got shipped is **`findings.md`** at the repo root. This file
  holds only the audit/approval toggles — do **not** duplicate research notes
  or release history here (that belongs in `findings.md` / `CHANGELOG.md`).
- Rule: entries are only added when the **user explicitly asks**. The
  assistant never adds stations on its own initiative.

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

## Approval list

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

> Curated genre rosters (Classical/Jazz/Blues/Country/Rock/Pop/Focus/Chill
> and the 0.7.86 **Funk (9)** genre) that are already baked into
> `DEFAULT_STATIONS` and shipped are fully documented in **`findings.md`** —
> keep that file, not this one, current as genres evolve.
>
> Notes on picks & deferred URLs (public-service vs commercial, SRG SSR
> language feeds, the VCR default stream, deferred/unworkable stations such as
> ORF Ö1 / RTBF Musiq3 / RTÉ lyric fm / ABC Classic / MPR) are also recorded in
> `findings.md`.
