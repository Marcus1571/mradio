# mradio — assistant behavior (permanent rules)

> This file governs HOW I work, independent of the project's current state.
> Read it together with `MEMORY.md` (project state) at the start of every
> session. These rules stand unless the user explicitly overrides them.

## 1. Commit & push is the DEFAULT

- After **every completed task**, the work is committed and pushed to GitHub
  without being asked — `c.p` is standard behavior.
- "Not pushed" only when the user explicitly says so ("don't push", "keep it
  local", …).
- When a change is version-worthy, the full release flow runs by default (see
  rule 4). Trivial/doc-only changes may go to `main` without a new release.

## 2. The four documentation duties (never skip)

Every change that fixes a bug or adds / alters / removes a feature must, **in
the same commit**, also:

1. **Project memory** — keep `MEMORY.md` (and this file) current.
2. **`CHANGELOG.md`** — always reflect the change (release history).
3. **`README.md`** — update *if* a reader of the marketing page would care.
4. **`KB.md`** — the canonical reference; update *always* when behavior
   changes (KB is the single source of truth).

## 3. UI conventions (user's taste)

- **Steady warning messages live ONLY in the right-side yellow pill**.
  No "restart to update" / "new version …" steady text on the left.
  Transient flashes (`v`, `a`, updates) may use the mid row for a few seconds.
- Favorites are **exactly 10** hot slots (`1-9` + `0`).
- The TUI is a thin remote control over mpv; steady state must stay quiet.

## 4. Release discipline (full sequence, never stop early)

1. bump `VERSION` in `./mradio`;
2. add the `## [X.Y.Z] - date` CHANGELOG section;
3. `make check` and `make test` (all tests green);
4. commit;
5. `git tag vX.Y.Z` and `git push origin vX.Y.Z`;
6. `gh release create vX.Y.Z --repo Marcus1571/mradio --title "mradio vX.Y.Z"
   --notes-file <section body> mradio install.sh`;
7. **verify** `gh release list | head` shows the new version as `Latest`;
8. push `main` so it stays in sync.

A GitHub **release** (with assets + notes) is the only thing that counts —
a bare tag is NOT a release.

## 5. Stations & data

- The user personally approves every station; the assistant NEVER adds
  stations on its own initiative (`stationsproject.md` holds the list).
- `stations.json` (favorites) is the user's file — releases never touch it.
- **Update flow (non-negotiable):** the user updates locally with the in-app
  `U` self-update. Never run `install.sh` — and never install/update the local
  binary on your own — unless the user explicitly asks. After cutting a
  release, just commit & push; leave the local install to the user's `U`.

## 6. Verification limits

- The assistant cannot view images; verify screenshots via OCR + pixel probes
  and let the user eyeball them.