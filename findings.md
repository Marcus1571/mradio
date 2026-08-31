# findings.md — station research log (persistent)

Research notes for radio stations researched for mradio's genre submenus.
This file exists because the user was upset that earlier Jazz/Blues research
was done, then forgotten and never saved. It is the **persistent record** of
every URL found, its verification status, and the decisions that followed.

> Status legend:
> - **verified** — returned HTTP 200 + the expected `icy-name`/codec from here.
> - **needs-retest** — reachable identity confirmed, but no response observed
>   from this environment (may be blocked by host or firewall); retest on a
>   normal network before trusting.

---

## Jazz (6) — user-approved, inserted into the Jazz genre submenu

| Station | Stream URL | Status | Notes |
|---|---|---|---|
| **WBGO** (Newark Jazz 88.3) | `https://ais-sa8.cdnstream1.com/3629_128.mp3` | verified | Empty `icy-name`; identity confirmed by search. |
| **WWOZ** (New Orleans) | `http://wwoz-sc.streamguys.com/wwoz-hi.mp3` | verified | `icy-name` WWOZ Mp3-ORD; HTTP 200. |
| **KCSM 91.1** (Bay Area Jazz) | `http://ice7.securenetsystems.net/KCSM2` | verified | `icy-name` KCSM2; HTTP 200. |
| **KJAZZ 88.1** (Los Angeles) | `https://streaming.live365.com/a49833` | verified | 302 → `https://das-edge11-live365-dal03.cdnstream.com/a49833`. |
| **Adroit Jazz Underground** | `https://icecast.walmradio.com:8443/jazz` | needs-retest | No headers returned in this env; likely valid. |
| **SomaFM Secret Agent** | `https://ice2.somafm.com/secretagent-128-mp3` | needs-retest | No headers returned in this env; likely valid. |

## Blues (3) — user-approved ("standard blues picks"), inserted into the Blues genre submenu

| Station | Stream URL | Status | Notes |
|---|---|---|---|
| **1.FM Blues** | `http://strm112.1.fm/blues_mobile_mp3` | verified | `icy-name` 1.FM - Blues Radio; HTTP 200. HTTPS variant works too. |
| **181.FM True Blues** | `http://listen.181fm.com/181-blues_128k.mp3` | verified | `icy-name` 181.FM Blues; HTTP 200. Found in 181.fm player page source. |
| **WDCB 90.9** (Chicago public) | `https://wdcb-ice.streamguys1.com/wdcb128` | verified | `icy-name` wdcb-MP3; HTTP 200. Jazz/Blues mix — grouped under Blues here. |

---

## URLs researched but NOT used

- Blues Radio (GR) — `http://play.streams.gr:22015/stream` — verified, but not
  one of the three chosen blues picks (kept as backup).
- Arrow Blues Box (StreamTheWorld) — 302 redirect; not chosen.
- 1.FM Blues old CDN guesses (`sc*1.fm` ports, `ais-sa2.cdnstream1.com/1004_128.mp3`) —
  all dead/404/moved. The live URL is `strm112.1.fm/blues_mobile_mp3` (via
  radio-browser).

## How these are surfaced in mradio (decision, 0.7.65)

Per user direction: **favorites file is NOT touched.** Instead the Jazz and
Blues genre submenus aggregate the user's favorites in that genre **plus** the
curated Jazz/Blues stations above (from `DEFAULT_STATIONS`, de-duplicated).
Classical and Other submenus stay favorites-only. This way Jazz/Blues show up
under `s` even though the favorites list is already full at its 10-slot cap.
