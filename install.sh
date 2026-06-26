#!/usr/bin/env bash
set -euo pipefail

# Partenon Installer
# Installs Hermes Agent CLI, Partenon core, and the 6 hero profiles.

PARTENON_VERSION="0.1.0"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Partenon v${PARTENON_VERSION} installer"
echo "========================================"

# 1. Check Hermes CLI
if ! command -v hermes &> /dev/null; then
  echo "Hermes CLI not found. Installing..."
  curl -fsSL https://install.hermes-agent.nousresearch.com | bash
  export PATH="$HOME/.hermes/bin:$PATH"
fi

hermes --version

# 2. Install Partenon core skill
echo "Installing partenon-core..."
mkdir -p "$HOME/.hermes/skills/partenon-core"
cp -R "$REPO_ROOT/partenon-core/SKILL.md" "$HOME/.hermes/skills/partenon-core/"

# 3. Install hero profiles
for profile in tesorero mensajero cobrador guardian estratega diplomatico; do
  echo "Installing partenon-${profile}..."
  hermes profile install "$REPO_ROOT/hermes/profiles/partenon-${profile}" --alias "partenon-${profile}" || true
done

# 4. Copy environment template
if [ ! -f "$REPO_ROOT/.env" ]; then
  cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
  echo "Created .env from template. Edit it with your keys."
fi

# 5. Create workspace structure
mkdir -p "$REPO_ROOT/data"
mkdir -p "$REPO_ROOT/logs"

echo ""
echo "Partenon installed. Next steps:"
echo "1. cd $REPO_ROOT"
echo "2. Edit .env with your credentials."
echo "3. Run: hermes profile use partenon-tesorero"
echo "4. Run: ./scripts/demo_tesorero.py"
