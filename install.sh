#!/usr/bin/env bash
# Install the motion-design-agent-skills plugin for Claude Code, Codex,
# Antigravity and Hermes Agent, plus its routing memory and optional dependencies.
#
#   ./install.sh                         # every agent found on this machine, user scope
#   ./install.sh --agent claude-code     # one agent: claude-code | codex | antigravity | hermes | all
#   ./install.sh --scope project         # skills into the current project instead of $HOME
#   ./install.sh --with-remotion         # also install the official Remotion skills from upstream
#   ./install.sh --check-deps            # only report Node, ffmpeg and Playwright status
#   ./install.sh --uninstall             # remove skills, plugin and memory block
#   ./install.sh --dry-run               # print what would change
#
# Run it from a clone of https://github.com/tarouco/motion-design-agent-skills.
# It copies files and calls each agent's own CLI; it never uses sudo.

set -euo pipefail

REPO_SLUG="tarouco/motion-design-agent-skills"
PLUGIN="motion-design-agent-skills"
MARKETPLACE="tarouco-motion"
HERMES_CATEGORY="motion-design"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_SNIPPET="$SRC/memory/motion-design-routing.md"
START_MARK="<!-- motion-design-agent-skills:start -->"
END_MARK="<!-- motion-design-agent-skills:end -->"

AGENT="auto"
SCOPE="user"
MEMORY=1
WITH_REMOTION=0
CHECK_ONLY=0
UNINSTALL=0
DRY=0
CLAUDE_FROM="github"

usage() { sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --agent) AGENT="${2:?--agent needs a value}"; shift 2 ;;
    --scope) SCOPE="${2:?--scope needs a value}"; shift 2 ;;
    --no-memory) MEMORY=0; shift ;;
    --with-remotion) WITH_REMOTION=1; shift ;;
    --check-deps) CHECK_ONLY=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --claude-from-local) CLAUDE_FROM="local"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

case "$SCOPE" in user|project) ;; *) echo "--scope must be user or project" >&2; exit 2 ;; esac

say() { printf '%s\n' "$*"; }
run() { if [ "$DRY" = 1 ]; then say "  [dry-run] $*"; else "$@"; fi; }
have() { command -v "$1" >/dev/null 2>&1; }

[ -f "$SRC/.claude-plugin/plugin.json" ] && [ -d "$SRC/skills" ] || { echo "Run this script from a clone of $REPO_SLUG" >&2; exit 1; }

SKILLS=()
for d in "$SRC"/skills/*/; do [ -f "$d/SKILL.md" ] && SKILLS+=("$(basename "$d")"); done

check_deps() {
  say "Dependencies (needed only by execution lanes; planning and review work without them):"
  if have node; then say "  ok   node $(node --version)"; else say "  miss node 18+          https://nodejs.org (Remotion, Playwright, npx skills)"; fi
  if have ffmpeg; then say "  ok   ffmpeg $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"; else say "  miss ffmpeg            macOS: brew install ffmpeg | Debian/Ubuntu: sudo apt-get install ffmpeg | Windows: winget install Gyan.FFmpeg"; fi
  if have npx && npx --no-install playwright --version >/dev/null 2>&1; then say "  ok   playwright (project)"; else say "  info playwright         per project: npm i -D @playwright/test && npx playwright install chromium"; fi
  if have claude; then say "  ok   claude $(claude --version 2>/dev/null | head -1)"; fi
  if have codex; then say "  ok   codex"; fi
  if have agy; then say "  ok   agy (Antigravity CLI)"; fi
  if have hermes; then say "  ok   hermes"; fi
}

# Insert or replace the marked block in a memory file; remove it on uninstall.
write_memory() {
  local file="$1"
  [ "$MEMORY" = 1 ] || return 0
  if [ "$DRY" = 1 ]; then say "  [dry-run] update memory block in $file"; return 0; fi
  mkdir -p "$(dirname "$file")"
  touch "$file"
  local tmp; tmp="$(mktemp)"
  awk -v s="$START_MARK" -v e="$END_MARK" '$0==s{skip=1;next} $0==e{skip=0;next} !skip' "$file" > "$tmp"
  if [ "$UNINSTALL" = 0 ]; then
    [ -s "$tmp" ] && printf '\n' >> "$tmp"
    cat "$MEMORY_SNIPPET" >> "$tmp"
  fi
  cat "$tmp" > "$file"; rm -f "$tmp"
  say "  memory: $file"
}

copy_skills() {
  local dest="$1"
  run mkdir -p "$dest"
  for s in "${SKILLS[@]}"; do
    run rm -rf "${dest:?}/$s"
    [ "$UNINSTALL" = 1 ] || run cp -R "$SRC/skills/$s" "$dest/$s"
  done
  say "  skills: ${#SKILLS[@]} $([ "$UNINSTALL" = 1 ] && echo removed from || echo copied to) $dest"
}

remotion_skills() {
  local target="$1"
  [ "$WITH_REMOTION" = 1 ] && [ "$UNINSTALL" = 0 ] || return 0
  if ! have npx; then say "  skip remotion skills: npx not found"; return 0; fi
  local g=(); [ "$SCOPE" = user ] && g=(-g)
  run npx --yes skills add remotion-dev/skills -a "$target" ${g[@]+"${g[@]}"} -y --copy
}

install_claude() {
  say "Claude Code"
  if have claude; then
    local source="$REPO_SLUG"; [ "$CLAUDE_FROM" = local ] && source="$SRC"
    local cscope="user"; [ "$SCOPE" = project ] && cscope="project"
    if [ "$UNINSTALL" = 1 ]; then
      run claude plugin uninstall "$PLUGIN@$MARKETPLACE" --scope "$cscope" || true
    else
      run claude plugin marketplace add "$source" || true
      if ! run claude plugin install "$PLUGIN@$MARKETPLACE" --scope "$cscope"; then
        say "  warning: plugin install failed; retry inside Claude Code with:"
        say "    /plugin marketplace add $REPO_SLUG"
        say "    /plugin install $PLUGIN@$MARKETPLACE"
      fi
    fi
  else
    say "  claude CLI not found: installing plain skills instead of the plugin"
    if [ "$SCOPE" = user ]; then copy_skills "$HOME/.claude/skills"; else copy_skills "$PWD/.claude/skills"; fi
  fi
  remotion_skills claude-code
  if [ "$SCOPE" = user ]; then
    write_memory "$HOME/.claude/CLAUDE.md"
  elif [ ! -f "$PWD/CLAUDE.md" ] && [ -f "$PWD/AGENTS.md" ]; then
    write_memory "$PWD/AGENTS.md"   # a new CLAUDE.md would stop Claude Code from reading AGENTS.md
  else
    write_memory "$PWD/CLAUDE.md"
  fi
}

install_codex() {
  say "Codex"
  if [ "$SCOPE" = user ]; then copy_skills "$HOME/.agents/skills"; else copy_skills "$PWD/.agents/skills"; fi
  remotion_skills codex
  if [ "$SCOPE" = user ]; then write_memory "${CODEX_HOME:-$HOME/.codex}/AGENTS.md"; else write_memory "$PWD/AGENTS.md"; fi
}

install_antigravity() {
  say "Antigravity"
  if [ "$SCOPE" = user ]; then copy_skills "$HOME/.gemini/config/skills"; else copy_skills "$PWD/.agents/skills"; fi
  remotion_skills antigravity
  if [ "$SCOPE" = user ]; then write_memory "$HOME/.gemini/GEMINI.md"; else write_memory "$PWD/AGENTS.md"; fi
}

install_hermes() {
  say "Hermes Agent"
  if [ "$SCOPE" = user ]; then copy_skills "$HOME/.hermes/skills/$HERMES_CATEGORY"; else copy_skills "$PWD/.hermes/skills"; fi
  remotion_skills hermes-agent
  if [ "$SCOPE" = project ]; then
    write_memory "$PWD/AGENTS.md"
  elif [ "$MEMORY" = 1 ] && [ "$UNINSTALL" = 0 ]; then
    say "  memory: Hermes manages MEMORY.md itself; send it the message in memory/hermes.md once"
  fi
  [ "$SCOPE" = project ] && say "  note: run 'hermes skills trust' so project skills load"
  return 0
}

if [ "$CHECK_ONLY" = 1 ]; then check_deps; exit 0; fi

if [ "$AGENT" = auto ]; then
  AGENTS=()
  have claude || [ -d "$HOME/.claude" ] && AGENTS+=(claude-code)
  have codex || [ -d "$HOME/.codex" ] && AGENTS+=(codex)
  have agy || have antigravity || [ -d "$HOME/.gemini" ] && AGENTS+=(antigravity)
  have hermes || [ -d "$HOME/.hermes" ] && AGENTS+=(hermes)
  [ ${#AGENTS[@]} -gt 0 ] || { echo "No supported agent found. Pass --agent claude-code|codex|antigravity|hermes|all" >&2; exit 1; }
elif [ "$AGENT" = all ]; then
  AGENTS=(claude-code codex antigravity hermes)
else
  AGENTS=("$AGENT")
fi

say "$([ "$UNINSTALL" = 1 ] && echo Uninstalling || echo Installing) $PLUGIN (${#SKILLS[@]} skills, scope: $SCOPE) for: ${AGENTS[*]}"
for a in "${AGENTS[@]}"; do
  case "$a" in
    claude-code|claude) install_claude ;;
    codex) install_codex ;;
    antigravity|gemini) install_antigravity ;;
    hermes|hermes-agent) install_hermes ;;
    *) echo "Unknown agent: $a" >&2; exit 2 ;;
  esac
done
[ "$UNINSTALL" = 1 ] || check_deps
say "Done. Restart the agent (or reload skills) so it picks up the changes."
