#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$PROJECT_ROOT/skills"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
TARGET_ROOT="$CODEX_HOME_DIR/skills"

mkdir -p "$TARGET_ROOT"

for SOURCE in "$SOURCE_ROOT"/*; do
  [ -d "$SOURCE" ] || continue
  NAME="$(basename "$SOURCE")"
  TARGET="$TARGET_ROOT/$NAME"
  rm -rf "$TARGET"
  cp -R "$SOURCE" "$TARGET"
  echo "Installed $NAME to $TARGET"
done

echo "Restart Codex or start a new session to use the skill."
