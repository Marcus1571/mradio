#!/usr/bin/env bash
# mradio installer — copies the script into ~/.local/bin (or $MPREFIX).
set -euo pipefail

PREFIX="${MPREFIX:-$HOME/.local/bin}"

# ---------------------------------------------------------------------------
# dependency checks
# ---------------------------------------------------------------------------
need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "mradio: MISSING DEPENDENCY: '$1' was not found on your PATH." >&2
    return 1
  fi
}

fail=0
need python3 || fail=1
need mpv || fail=1
if [ "$fail" -ne 0 ]; then
  echo >&2
  echo "Install mpv (e.g. 'brew install mpv') before running mradio." >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# install
# ---------------------------------------------------------------------------
mkdir -p "$PREFIX"
install -m 0755 "$(dirname "$0")/mradio" "$PREFIX/mradio"
echo "Installed mradio $( "$PREFIX/mradio" --version ) into $PREFIX/mradio"

if ! echo ":$PATH:" | grep -q ":$PREFIX:"; then
  echo "Note: $PREFIX is not on your PATH. Add it to your shell rc file:"
  echo "  export PATH=\"$PREFIX:\$PATH\""
fi