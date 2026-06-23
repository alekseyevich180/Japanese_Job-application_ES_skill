#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"
TARGET_ROOT="$CODEX_HOME_DIR/skills"
SKILL_NAMES=(
  "japanese-es-writing"
  "nature-polishing"
  "nature-writing"
)

mkdir -p "$TARGET_ROOT"

for SKILL_NAME in "${SKILL_NAMES[@]}"; do
  SOURCE="$PROJECT_ROOT/skills/$SKILL_NAME"
  TARGET="$TARGET_ROOT/$SKILL_NAME"

  if [ ! -d "$SOURCE" ]; then
    echo "Skill source not found: $SOURCE" >&2
    exit 1
  fi

  rm -rf "$TARGET"
  cp -R "$SOURCE" "$TARGET"
  echo "Installed $SKILL_NAME to $TARGET"
done

echo "Restart Codex or start a new session to use the skill."
