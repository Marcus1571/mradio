# MEMORY.md — Current State Snapshot

## Latest Version / Release
- **In-code VERSION**: 0.7.87 (from mradio script)
- **Latest git tag**: v0.7.87 (matches in-code version)
- **Latest CHANGELOG entry**: [0.7.87] - 2026-09-03
- **Platform release status**: Tag v0.7.87 exists and is the latest valid release

## Current Feature / Data Model
- **Genres**: 10 curated genres (classical, jazz, blues, country, rock, pop, focus, chill, funk, other)
- **Favorites system**: 12 quick-pick slots (1-9, 0=#10, 11-12 via arrows), persisted to stations.json
- **AI enrichment**: Three providers (opencode preferred, ollama, NIM) with background caching and truthfulness rules
- **Self-update**: GitHub release feed polling with ETag, atomic swap on apply
- **UI**: 4 color schemes (dark, light, light-navy, light-mauve) with 256-color support
- **Persistence**: Self-contained in ~/.local/share/mradio/ (settings, config, stations, cache, logs)

## Architecture Map (Key Modules/Decisions)
- **Single-file stdlib Python** (~2800 lines) + mpv IPC socket
- **Background threads**: Enricher (AI metadata), update watcher (GitHub feeds)
- **State management**: Central state dict passed to renderers
- **Configuration hierarchy**: Env vars > settings.json > defaults
- **Favorites numbering**: Never-shifting slots use None placeholders for deleted entries
- **Volume/mute**: Re-applied from config on every stream switch/reconnect
- **TUI rendering**: Curses-based with dynamic layout adaptation

## Open Questions / Pending Items
1. **Version/tag discrepancy**: CODE VERSION=0.7.87 vs LATEST TAG=v0.7.9 (semantically older). Need to verify which is correct and fix inconsistency per governance rules (single source of truth).
2. **Research log**: findings.md exists in project root but not yet checked for recent entries.
3. **Curated data compliance**: Verify that no curated stations were added by agent without user approval (per 2.5).

## Recent Meaningful Changes (from CHANGELOG)
- **v0.7.87**: Fixed volume not persisting on station change (apply_volume now reads fresh config)
- **v0.7.86**: Added Funk genre (10 stations), updated genre menu to 9 genres + Other
- **v0.7.85**: Added favorites via * key (player and genre submenu edit mode)
- **v0.7.84**: Volume & mute work everywhere (global keys in menus)