#!/bin/sh
# Connect the lab agent overlay at a pinned version: submodule + symlink + import line in CLAUDE.md.
# Usage: sh scripts/connect_overlay.sh v0.1.0   (or: make overlay OVERLAY_VERSION=v0.1.0)
set -eu
VERSION="${1:?usage: connect_overlay.sh <tag>}"
URL="https://github.com/Industrial-AI-Research-Lab/nir-agent-overlay.git"

if [ ! -d .agents/overlay ]; then
  git submodule add "$URL" .agents/overlay
fi
git -C .agents/overlay fetch --tags --quiet
git -C .agents/overlay checkout --quiet "$VERSION"

mkdir -p .claude/rules
if [ ! -e .claude/rules/overlay ]; then
  ln -s ../../.agents/overlay/rules .claude/rules/overlay
fi

grep -qx '@.agents/overlay/AGENTS.md' CLAUDE.md 2>/dev/null \
  || printf '\n@.agents/overlay/AGENTS.md\n' >> CLAUDE.md

git add .gitmodules .agents/overlay .claude/rules/overlay CLAUDE.md
echo "Overlay $VERSION connected. Review the staged changes and commit: chore: connect agent overlay $VERSION"
echo "Windows without symlink rights: remove .claude/rules/overlay and import the rules file by file in CLAUDE.md."
