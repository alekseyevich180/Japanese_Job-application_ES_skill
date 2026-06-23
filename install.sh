#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$PROJECT_ROOT/skills/japanese-es-writing"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
TARGET_ROOT="$CODEX_HOME_DIR/skills"
TARGET="$TARGET_ROOT/japanese-es-writing"

mkdir -p "$TARGET_ROOT"
rm -rf "$TARGET"
cp -R "$SOURCE" "$TARGET"

echo "Installed japanese-es-writing to $TARGET"
echo "Restart Codex or start a new session to use the skill."
