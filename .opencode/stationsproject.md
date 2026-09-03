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

- **Wired into mradio:** the curated presets below are baked in as part of
  `DEFAULT_STATIONS` in `./mradio`. **0.7.70** adds the **Focus (category 7)**
  and **Chill (category 8)** genres — the user's "concentration music" request
  (instrumental / meditative / new-age / ambient / unplugged, the
  Vangelis/Enya/Vollenweider world), split into two — with **10 curated each**,
  all live-verified: Focus — **SomaFM Space Station Soma** (320k, 24.3k
  votes), **Ambient Sleeping Pill** (256k, 54.1k votes), **SomaFM Drone Zone**
  (128k, the classic focus/drone channel), **SomaFM Groove Salad** (128k, 47.5k
  votes), **Cryosleep / Echoes of Blue Mars** (128k, 29.3k votes), **SomaFM
  Deep Space One** (128k), **Radio Caprice - Relaxation Music** (320k AAC),
  **Total Instrumental** (laut.fm, 128k), **Yoga Chill** (128k, 7.9k votes),
  **Radio Art - Deep Focus & Concentration** (96k); Chill — **1.FM Chillout
  Lounge** (256k, 11.9k votes), **Chilltrax** (128k, 10k votes), **Café del
  Mar** (192k, 8.7k votes), **Smooth Chill** UK (128k, 13.2k votes),
  **Antenne Bayern Chillout** (128k, 15.2k votes), **SomaFM Fluid** (128k),
  **Costa del Mar - Chillout** (96k AAC, 8.6k votes), **Jazz Lounge** (320k,
  17.6k votes), **Hi On Line Lounge** (320k), **Costa del Mar - Zen** (96k).
  The genre picker order is now 1 Classical, 2 Jazz, 3 Blues, 4 Country,
  5 Rock, 6 Pop, 7 Focus, 8 Chill, and **Other is the literal `0` slot**
  (last). Focus/Chill aggregate curated + favorites like the others;
  **0.7.86** adds **Funk (category 9)** with **10 curated stations** — the
  user "as usual curate the best 10 stations worldwide" request: **Amsterdam
  Funk Channel** (NL, 80s/90s+ pure funky grooves, 256k AAC — `https://live.afc.fm`),
  **Funky Radio Classic Funk** (IT, 1963–1982 classics/vinyl rarities, 128k MP3 —
  `http://funkyradio.streamingmedia.it:8001/play.mp3`), **Radio Meuh** (FR,
  Funk/Jazz/Soul/Electro, 128k MP3 — `http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3`),
  **Capital Jazz Radio** (US, groove jazz/instrumental funk, 128k MP3 —
  `http://stream.radio.co/s7c1ea5960/listen`), **Funk the Planet** (US,
  classic funk + rare groove + jazz-funk, 128k MP3 —
  `https://streaming.live365.com/a01484`), **DanceGroove Radio** (80s
  funk/soul/boogie, 128k MP3 — `http://s13.streamingcloud.online:34128`),
  **Funk42 Radio** (NL, funk/soul/disco/house, 320k — `http://213.133.97.249:8843/stream`),
  **Funkstar Radio** (CZ, funk/soul/boogie/disco/jazz funk/R&B, 192k MP3 —
  `https://funkstar.radioca.st/stream`), **Ministry of Soul** (DE, laut.fm
  soul/funk/disco/jazz/R&B, 128k MP3 — `https://soul.stream.laut.fm/soul`),
  **Funky Radio Disco Funk** (IT, disco funk/modern soul/boogie rarities,
  128k MP3 — `https://funky.radio/discofunk_modernsoul_boogie/`). `funk`
  auto-classification keywords added (funk/funky/groove/boogie/soul/r&b/rnb/
  disco funk/jazz funk); genre picker now shows 1–9 + Other as `0`.
  **0.7.69** added **Rock (5)** & **Pop (6)** with 10 each:
  Rock — Radio Caroline, Virgin Classic Rock (IT), Rock Antenne, Arrow Classic
  Rock (NL), 1.FM Classic Rock Replay, SomaFM Left Coast 70s, Radio ROKS
  Hard'n'Heavy & Ballads, 181.FM Rock 181, Hard Rock Heaven; Pop — Capital FM
  London, Heart 80s & 70s, Radio 105 Italy, LOS 40 España, Radio 538, Energy
  Zürich NRJ, 1.FM Absolute TOP 40, SWR3, Chocolate FM. **0.7.68** added the
  **Country genre** (category 4) with 10 curated stations:
  **WSM 650 AM** (Nashville/Grand Ole Opry, 64k, icy), **.977 Country**
  (128k, 55k votes), **1.FM Absolute Country Hits** (256k, 16.6k votes),
  **1.FM Classic Country** (256k, 14.3k votes), **181.FM Highway 181**
  (128k, 20.3k votes), **181.FM Kickin' Country** (128k, 8.5k votes),
  **181.FM Real Country** (128k, 3.3k votes), **KIX Country** (AUS, 128k),
  **Big R Radio Country** (128k, 1.4k votes), **Country Radio** (CZ, 128k AAC,
  14.4k votes). **0.7.67** gives
  **10 curated Jazz** (adds KMHD, Portland public, 256k AAC), **10 curated
  Blues** (adds Radio Caprice - Chicago Blues, 320k AAC, 1333 votes —
  replacing the unverifiable 61 Blues) and the **Classical submenu also
  aggregates curated + favorites** (only Other stays favorites-only) with 3 new
  curated classical stations: **WCRB** (Boston, 256k), **KUSC** (LA, 256k,
  icy), **WFMT** (Chicago, 260k, icy). Earlier (0.7.66) the curated genres went
  to 9 each, replacing the 6 Jazz (incl. Adroit Jazz Underground & SomaFM
  Secret Agent) / 3 Blues from **0.7.65**. All new entries live-verified via
  mpv (audio, bitrate, icy-title); higher bitrate + popular/reviewed picks win.
  Surfaced in the **`s` genre submenus** for Classical/Jazz/Blues/Country/
  Rock/Pop/Focus/Chill/Funk (de-duplicated against favorites; the favorites
  file is untouched). Your favorites live in `~/.local/share/mradio/stations.json`
  (key `"favorites"`, opened by `f`), seeded once from the first 10 of
  `DEFAULT_STATIONS` on first run; afterwards the file is entirely the user's
  (releases never touch it). The old `S01…Snn` all-stations catalog and the `a`
  key were removed in **0.7.63**. Favorite hot-keys are `1-9` then **`0`** (10th);
  the numeric keypad behaves like the main number row. `MRADIO_STATIONS`
  overrides the path; a legacy
  `config.json` → `"stations"` list is migrated on first run.
  **`findings.md`** at the repo root logs every researched station URL + status.
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