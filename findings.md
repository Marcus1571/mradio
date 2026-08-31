# findings.md — station research log (persistent)

Research notes for radio stations researched for mradio's genre submenus.
This file exists because the user was upset that earlier Jazz/Blues research
was done, then forgotten and never saved. It is the **persistent record** of
every URL found, its verification status, and the decisions that followed.

> Status legend:
> - **verified-live** — HTTP 200 + MP3/AAC audio actually decoded by mpv, with
>   bitrate, `icy-name`/`icy-title`, and (where known) radio-browser vote count.
> - **needs-retest** — reachable identity confirmed, but no response observed
>   from this environment (may be blocked by host or firewall); retest on a
>   normal network before trusting.

---

## Jazz (9) — v0.7.66, inserted into the Jazz genre submenu

Ranked by reputation/brand + popularity (radio-browser votes) + bitrate.

| Station | Stream URL | Bitrate | icy | votes | Status |
|---|---|---|---|---|---|
| **WBGO** (Newark Jazz 88.3) | `https://ais-sa8.cdnstream1.com/3629_128.mp3` | 128k | yes | 791 | verified-live |
| **WWOZ** (New Orleans) | `http://wwoz-sc.streamguys.com/wwoz-hi.mp3` | 128k | yes | — | verified-live |
| **KCSM 91.1** (Bay Area) | `http://ice7.securenetsystems.net/KCSM2` | 96k | yes | 2829 | verified-live |
| **KJAZZ 88.1** (Los Angeles) | `https://streaming.live365.com/a49833` | 128k | yes | — | verified-live |
| **Jazz24** (Seattle, commercial-free) | `https://knkx-live-a.edge.audiocdn.com/6285_256k` | 256k | no(broadcast) | 265 | verified-live |
| **1.FM Adore Jazz** | `http://strm112.1.fm/ajazz_mobile_mp3` | 256k | yes | 2097 | verified-live |
| **TSF Jazz** (Paris) | `http://tsfjazz.ice.infomaniak.ch/tsfjazz-high.mp3` | 128k | yes | 1488 | verified-live |
| **JazzRadio 106.8 Berlin** | `https://streaming.radio.co/s774887f7b/listen` | 192k | yes | 2029 | verified-live |

Plus **Swiss Jazz** (user favorite, already present) gives the 9th slot.

> Dropped from the earlier 6-jazz set: **Adroit Jazz Underground** and
> **SomaFM Secret Agent** (both could not be live-verified from this
> environment and lost out to higher-bitrate, popular alternatives).
>
> **KMHD** (Portland, 256k AAC) was a strong candidate but showed
> `[ffmpeg] tls: Unknown error` flakiness during live tests, so it was
> dropped in favor of reliability; its direct non-HLS URL
> `https://ais-sa3.cdnstream1.com/2442_128.aac` is kept here as a backup.

## Blues (9) — v0.7.66, inserted into the Blues genre submenu

Ranked by popularity + bitrate + reputation. All verified-live decoding mp3.

| Station | Stream URL | Bitrate | icy | votes | Status |
|---|---|---|---|---|---|
| **Jazz Radio Blues** (FR, jazzradio.fr) | `http://jazzblues.ice.infomaniak.ch/jazzblues-high.mp3` | 128k | yes | 64551 | verified-live |
| **Blues Radio Greece** | `http://cast3.radiohost.ovh:8352/` | 320k | yes | 1401 | verified-live |
| **Blues Music Fan** | `https://orbit.citrus3.com:8052/stream` | 320k | yes | 38 | verified-live |
| **Blues Rock Cafe** (laut.fm) | `https://bluesrockcafe.stream.laut.fm/bluesrockcafe` | 128k | yes | 2034 | verified-live |
| **1.FM Blues** | `http://strm112.1.fm/blues_mobile_mp3` | 256k | yes | — | verified-live |
| **181.FM True Blues** | `http://listen.181fm.com/181-blues_128k.mp3` | 128k | yes | — | verified-live |
| **Buddy Guy Radio Legends** (Chicago) | `https://streaming.live365.com/a83090` | 128k | yes | 0 | verified-live |
| **WDCB 90.9** (Chicago public) | `https://wdcb-ice.streamguys1.com/wdcb128` | 128k | yes | — | verified-live |
| **exclusive BB King** | `https://streaming.exclusive.radio/er/bbking/icecast.audio` | 128k | yes | 163 | verified-live |

> Notes:
> - **1.FM Blues** decodes as **256k** mp3 (better than the assumed 128k);
>   the live URL is `strm112.1.fm/blues_mobile_mp3` (via radio-browser).
> - **Buddy Guy Radio Legends** is a live365 stream: `a83090` → 302 →
>   `https://das-edgeXX-live365-dalYY.cdnstream.com/a83090`, `icy-name: Buddy Guy Radio`.
> - **Blues Music Fan** bills itself "The #1 Contemporary Blues Station on the
>   internet" (4.7/5 ~205 ratings) — strong critic/public reviews, 320k.

---

## URLs researched but NOT used

- **Arrow Blues Box** (StreamTheWorld) — 302 redirect; not chosen.
- **61 Blues / Houston Blues Radio / Blues 93.1** — highly reviewed per
  radiostationsusa.com but direct stream URLs could not be pinned from this
  environment (no reliable radio-browser/directory hit). Left as future work.
- **KMHD HLS** `https://ais-sa3.cdnstream1.com/2442_128.aac/playlist.m3u8` —
  flaky keepalive; direct AAC `2442_128.aac` works but showed TLS errors.

## How these are surfaced in mradio (decision, 0.7.65, extended 0.7.66)

Per user direction: **favorites file is NOT touched.** Instead the Jazz and
Blues genre submenus aggregate the user's favorites in that genre **plus** the
curated Jazz/Blues stations above (from `DEFAULT_STATIONS`, de-duplicated).
Classical and Other submenus stay favorites-only. This way Jazz/Blues show up
under `s` even though the favorites list is already full at its 10-slot cap.

Live verification method: `curl -sS -I` for HTTP status + icy headers, then
`mpv --no-video --ao=null <url>` for a few seconds to confirm the audio codec
and samplerate actually decode, and to capture `icy-title` (track metadata).
Radio-browser `votes`/`clickcount` used as a popularity proxy.
