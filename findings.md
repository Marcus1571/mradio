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

## Jazz (10) — v0.7.66/0.7.67, inserted into the Jazz genre submenu

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
| **KMHD** (Portland public) | `https://ais-sa3.cdnstream1.com/2442_128.aac` | 256k | yes | — | verified-live |

Plus **Swiss Jazz** (user favorite, already present) gives the 10th slot.

> Note: KMHD's **direct AAC URL** (`2442_128.aac`, 256k + icy "KMHD - Jazz Radio")
> works; its HLS `playlist.m3u8` is flaky (keepalive errors) so the direct
> non-HLS URL is used instead.
>
> Dropped from the earlier 6-jazz set: **Adroit Jazz Underground** and
> **SomaFM Secret Agent** (both could not be live-verified from this
> environment and lost out to higher-bitrate, popular alternatives).

## Blues (10) — v0.7.66/0.7.67, inserted into the Blues genre submenu

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
| **Radio Caprice - Chicago Blues** | `http://79.111.14.76:8000/chicagoblues` | 320k | yes | 1333 | verified-live |

> Notes:
> - **1.FM Blues** decodes as **256k** mp3 (better than the assumed 128k);
>   the live URL is `strm112.1.fm/blues_mobile_mp3` (via radio-browser).
> - **Buddy Guy Radio Legends** is a live365 stream: `a83090` → 302 →
>   `https://das-edgeXX-live365-dalYY.cdnstream.com/a83090`, `icy-name: Buddy Guy Radio`.
> - **Blues Music Fan** bills itself "The #1 Contemporary Blues Station on the
>   internet" (4.7/5 ~205 ratings) — strong critic/public reviews, 320k.
> - **Radio Caprice - Chicago Blues** was added as the 10th slot when
>   **61 Blues** (user's original pick) proved unverifiable — its onlineradiobox
>   entry had 0 listeners and no extractable stream URL. Caprice is a verified
>   320k AAC Chicago-electric-blues stream with track metadata (fits the same
>   intent).

---

## Classical (12) — v0.7.67, now aggregated like Jazz/Blues

The Classical submenu previously showed only the user's favorites. As of
0.7.67 it **aggregates curated Classical + favorites** (de-duplicated), the
same as Jazz/Blues, so the curated classical catalog fills the submenu. Three
new public classical stations were added (all live-verified):

| Station | Stream URL | Bitrate | icy | votes | Status |
|---|---|---|---|---|---|
| **WCRB** (Boston, WGBH) | `https://wgbh-live.streamguys1.com/classical-hi` | 256k | no | 128 | verified-live |
| **KUSC** (Los Angeles) | `https://playerservices.streamtheworld.com/api/livestream-redirect/KUSCMP256.mp3` | 256k | yes | 678 | verified-live |
| **WFMT** (Chicago) | `https://wfmt.streamguys1.com/main-source` | 260k | yes | 404 | verified-live |

These join the curated classical already present (VCR Auditorium, VCR
Classica+, Radio Swiss Classic, Naim, WQXR, Classic FM, radio klassik
Stephansdom, NPO Klassiek, France Musique). With the user's 7 classical
favorites that surfaces a 12-station Classical submenu (7 favs + WQXR +
France Musique + WCRB + KUSC + WFMT).

> Runner-up classical candidates (also live-verified, available as alternates):
> **All Classical Portland** (`https://allclassical.streamguys1.com/ac96k`,
> 96k AAC, 724 votes) and **Your Classical - Relax** (MPR,
> `http://relax.stream.publicradio.org/relax.mp3`, 128k, 55k votes).

---

## Country (10) — v0.7.68, new genre (category 4), Other → "0" slot

Picked from radiostationsusa.com's "25 Best Country Radio Stations" + the
radio-browser global popularity leaderboard, then **live-verified** (mpv audio
decode + bitrate + `icy-name`/`icy-title`). Country = category **4** in the
genre picker; **Other** was pushed to the literal **`0`** (last) slot.

| Station | Stream URL | Bitrate | icy | votes | Status |
|---|---|---|---|---|---|
| **WSM 650 AM** (Nashville, Grand Ole Opry) | `http://stream01048.westreamradio.com/wsm-am-mp3` | 64k | yes | 3940 | verified-live |
| **.977 Country** | `http://26343.live.streamtheworld.com/977_COUNTRY_SC` | 128k | yes | 55119 | verified-live |
| **1.FM Absolute Country Hits** | `http://strm112.1.fm/acountry_mobile_mp3` | 256k | yes | 16624 | verified-live |
| **1.FM Classic Country** | `http://strm112.1.fm/ccountry_mobile_mp3` | 256k | yes | 14298 | verified-live |
| **181.FM Highway 181** | `http://listen.181fm.com/181-highway_128k.mp3` | 128k | yes | 20330 | verified-live |
| **181.FM Kickin' Country** | `http://listen.181fm.com/181-kickincountry_128k.mp3` | 128k | yes | 8500 | verified-live |
| **181.FM Real Country** | `http://listen.181fm.com/181-realcountry_128k.mp3` | 128k | yes | 3320 | verified-live |
| **KIX Country** (AU) | `http://playerservices.streamtheworld.com/api/livestream-redirect/KIXCOUNTRY.mp3` | 128k | yes | — | verified-live |
| **Big R Radio Country** | `http://bigrradio.cdnstream1.com/5195_128` | 128k | yes | 1444 | verified-live |
| **Country Radio (CZ)** | `http://icecast2.play.cz:8000/country128aac` | 128k AAC | yes | 14409 | verified-live |

> Notes:
> - **WSM 650 AM** is the genre's iconic institution (home of the Grand Ole
>   Opry since 1925); its only weakness is a 64k mp3 — kept despite that.
> - Streaming networks win the popularity slots: **.977** (55k votes) and
>   **1.FM** (16.6k + 14.3k) are the top two online country providers on
>   radio-browser; 181.FM contributes 3 curated feeds (Highway = roots/classic,
>   Kickin' = today's hits, Real = mainstream).
> - **Dropped as not-good-enough for "best":** Czech "Country Radio" was going
>   to be cut for non-English icy titles but its 14.4k-vote relevance won the
>   10th slot; **KORA Texas Country 98.3** (48k only) and the iHeart/Audacy US
>   terrestrial stations (KILT, WSIX, KKBQ, KYGO, KSON, WSOC, KPLX, KNIX)
>   have no reliable direct/geo-unrestricted URLs; **Boot Kickin' Country**
>   direct URL not found; **Nash Icon** streams are 48k AAC via streamtheworld.
> - `genre_of` learned country keywords ("country", "americana", "bluegrass",
>   "honky tonk", "honky-tonk", "nash") and checks them **before** the generic
>   "classic" keyword, so "Classic Country" parses as Country, not Classical.

---

## URLs researched but NOT used

- **Arrow Blues Box** (StreamTheWorld) — 302 redirect; not chosen.
- **61 Blues** — original user pick for the 10th blues slot, but could not be
  live-verified (onlineradiobox entry: 0 listeners, no extractable stream URL;
  no working direct URL found). Replaced by Radio Caprice - Chicago Blues.
  Houston Blues Radio / Blues 93.1 — highly reviewed per radiostationsusa.com
  but direct stream URLs could not be pinned here either. Left as future work.
- **KMHD HLS** `https://ais-sa3.cdnstream1.com/2442_128.aac/playlist.m3u8` —
  flaky keepalive; the direct AAC `2442_128.aac` is used instead.
- **Country rejects (0.7.68):**
  - **KORA Texas Country 98.3** — only 48k AAC (`7410_48k.aac/playlist.m3u8`,
    streamon.fm); dropped on bitrate.
  - **Nash Icon** (95.5 WWSM etc.) — 48k AAC+ via streamtheworld (some FLV);
    listed under "best country" by radiostationsusa but bitrate too low vs. the
    10 chosen.
  - **US terrestrial iHeart/Audacy** (KILT, WSIX, KKBQ, KYGO, KSON, WSOC,
    KPLX, KNIX, WIVK, KSON) — radio-browser shows them as iHeart HLS
    (`revma.ihrhls`) or geo-blocked Audacy; no reliable direct URL verifiable.
  - **Boot Kickin' Country** — only "Classic Kickin' Country" web artifact; no
    direct stream URL found.

## How these are surfaced in mradio (decision, 0.7.65, extended 0.7.67)

Per user direction: **favorites file is NOT touched.** The Classical / Jazz /
Blues / Country genre submenus aggregate the user's favorites in that genre
**plus** the curated stations for that genre (from `DEFAULT_STATIONS`,
de-duplicated). Only **Other** stays favorites-only. Since the aggregation is
uniform, each genre's curated catalog can fill its submenu to 10 (0 acts as the
10th hot-slot) or beyond (arrow keys scroll). This way Classical/Jazz/Blues/
Country show up under `s` even though the favorites list is already full at its
10-slot cap, and the curated catalog is the controllable lever (favorites are
never written to).

As of 0.7.68 the genre picker order is 1 Classical, 2 Jazz, 3 Blues,
4 Country, and **Other is rendered as the literal `0` slot** (last entry in the
list, even with fewer than 10 entries; the `0` key always selects the final
genre).

Live verification method: `curl -sS -I` for HTTP status + icy headers, then
`mpv --no-video --ao=null <url>` for a few seconds to confirm the audio codec
and samplerate actually decode, and to capture `icy-title` (track metadata).
Radio-browser `votes`/`clickcount` used as a popularity proxy.
