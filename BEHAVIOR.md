# Project — Agent Self-Governance Playbook

> A single file you can drop into any project (or Notion) to initialize an
> AI coding agent with a proven set of working conventions. Feed this to the
> agent at the start of a session and it "remembers" our best practices
> without reproducing past mistakes. Replace the bracketed `<…>` placeholders
> with the specifics of the new project.

---

## 1. The core idea: one source of truth per concern

The biggest source of past mistakes was **duplicating the same fact in more
than one file** — when one copy got updated and the other didn't, the two
silently contradicted (e.g. an install/update policy that said "run the
installer" in one place and "never run the installer" in another).

So we split the governance docs so **each concern lives in exactly one
canonical file, and every other file only points to it.** A rule is never
re-stated; it is referenced.

The split (names are conventions; adjust to fit the project):

| File | Job | Changes... |
|------|-----|-----------|
| `BEHAVIOR.md` | **Permanent rules** (how to work, never changes) | rarely / never |
| `MEMORY.md` | **Current state** (where the project is right now) | every meaningful change |
| `findings.md` | **Research log** (every option researched + verdict) | as research happens |
| `KB.md` | **Canonical reference** (all features, keys, config, env vars) | when behavior changes |
| `CHANGELOG.md` | **Release history** (version-by-version changelog) | every release |

**The golden rule:** if a piece of information already lives in one of these,
do NOT copy it into another. Reference it with a pointer instead. This is what
kills contradictory/stale rules forever.

---

## 2. Permanent rules file (`BEHAVIOR.md`) — "How I work"

This file holds the non-negotiable modus operandi. It is pure rules, no
project state, no history. Contents:

### 2.1 Commit & push is the DEFAULT
- **`c.p` = standard behavior.** After every completed task, the work is
  committed AND pushed to the remote without being asked.
- Only don't push when the user explicitly says so ("don't push", "keep it
  local", …).
- Version-worthy change → run the full release flow (§2.4). Trivial/doc-only →
  plain push to the main branch, no release.

### 2.2 The four documentation duties (never skip)
Every change that fixes a bug or adds/alters/removes a feature must, **in the
same commit**, also update:
1. **Project memory** (`MEMORY.md`, the state file)
2. **`CHANGELOG.md`** (release history)
3. **`README.md`** — only if a reader of the marketing page would care
4. **`KB.md`** — the canonical reference; **always** when behavior changes

### 2.3 UI / product conventions (user's taste)
- Steady warnings live ONLY in one dedicated status area; the main view stays
  quiet.
- The product surface the user cares about is a fixed, curated set of items
  (e.g. hot keys / slots); don't spill clutter into it.
- The agent is a thin control layer over an external engine; steady state
  stays quiet.

### 2.4 Release discipline — full sequence, never stop early
A **platform Release** (tag + assets + notes) is the only thing that counts. A
bare git tag is NOT a release.

1. bump `VERSION` in the main artifact (e.g. the script)
2. add the `## [X.Y.Z] - date` CHANGELOG section
3. run checks + tests (all green)
4. commit
5. `git tag vX.Y.Z` and `git push origin vX.Y.Z`
6. publish the release with the version tag, attaching its assets + notes
7. **verify** the release list shows the new version as `Latest`
8. push the main branch so it stays in sync

> **The painful lesson:** bumping the in-source version and committing to the
> branch does NOTHING for any self-update/check that reads the **platform
> release tag**, not the source string. If you cut a release but forget the
> tag + release, the product keeps reporting "up to date (old version)" and
> the feature looks missing even though it's committed.

### 2.5 Curated data
- The user personally approves every curated item (e.g. every added entry);
  the agent NEVER adds such items on its own initiative.
- User-owned data files are never touched by releases.

### 2.6 Update flow (non-negotiable) — **user applies updates themselves**
- **The user updates the installed/running artifact themselves (e.g. via an
  in-app self-update). The agent NEVER runs the installer / never applies the
  local update on its own — only if explicitly asked.**
- After cutting a release, the agent just commits & pushes. The user applies
  it locally.
- If a feature "seems missing", the installed copy is simply stale until the
  user updates. Don't "fix" it by installing.

---

## 3. Self-update / release mechanism — understand it before releasing

Some projects ship with a built-in self-updater. Understanding the mechanism
explains *why* the release flow above is mandatory. The exact keys/URLs are
project-specific, but the shape is:

- A background thread checks the platform's **release feed** at startup and on
  an interval.
- It parses the feed for release **tags**, takes the *max* version, and
  compares to the current version.
- If newer, the apply step downloads
  `https://github.com/{OWNER}/{REPO}/releases/download/{tag}/{asset}`,
  **validates** it (compile/syntax + version parse), backs up the old one, and
  swaps it — it never executes the download directly.
- So the release must have: a **git tag** + a **platform Release** with the
  artifact + installer as **assets**. Without the release, the feed reports the
  old tag and the user sees "up to date" forever.

---

## 4. Current state file (`MEMORY.md`) — "where we are"

This is a living **state snapshot**, not a rules file. It holds:
- The **latest version / release** (in-code `VERSION` AND the platform release
  tag both current)
- The current **feature / data model** (the curated items, categories,
  classification)
- The **architecture map** of the codebase (its key modules and design
  decisions)
- Current **open questions / pending items**

Contrast with `BEHAVIOR.md`: rules NEVER change, state changes often. Keeping
them separate means you don't rewrite rules each session and you don't bury
the state under history.

> **Lesson:** `MEMORY.md` once duplicated the rules (a "COMMANDMENTS" section
> re-stating `BEHAVIOR.md`) plus a full changelog plus reference tables. That
> duplication is exactly how a policy contradiction happened. It's now pruned
> to state-only, and everything it dropped lives in its canonical home
> (rules→BEHAVIOR, changelog→CHANGELOG, references→KB).

---

## 5. Research log (`findings.md`) — "the hunts"

Because research was once done and then *forgotten* (the user was upset), we
keep a **persistent research log** at the repo root. Every "hunt" — e.g. the
searches that feed curated content — gets recorded here:

- every option / URL / candidate found,
- its verification status (reachable? live? quality? popularity?),
- and the decision that followed (picked vs dropped, and why).

This file is the durable record of research so nothing found is ever lost. It
is the **single owner of researched-option data** — other files (like a
candidate audit list) point to it rather than restating it.

---

## 6. The separation that fixed everything (the "aha")

The framework that emerged, in one line:

> **Rules in `BEHAVIOR.md`, state in `MEMORY.md`, research in `findings.md`,
> reference in `KB.md`, history in `CHANGELOG.md` — and every other file only
> points to these, never copies them.**

This is deliberately close to the emerging `AGENTS.md` industry convention
(one file for "how I work" + one for project context), but split further
because this project also wanted a durable research log and a canonical
reference. The value of the split is **contradiction elimination**: a fact has
one owner, one place to edit, so it can't diverge.

---

## 7. Quick checklist before finishing ANY task

1. **Committed AND pushed** (unless told not to push)?
2. If version-worthy: **full release sequence** (§2.4) run — VERSION bump,
   CHANGELOG, tag, platform Release with assets, verified `Latest`?
3. **All four documentation duties** (§2.2) reflected in the same commit?
4. Facts stored in their **single canonical home**, not duplicated?
5. **Did NOT run the installer / apply the local update** — left that to the
   user?
6. Tests green?