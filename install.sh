#!/usr/bin/env bash
set -euo pipefail

# Partenon Installer
# Prepares the local Python environment, copies profile templates, and verifies
# the Tesorero demo. It does NOT install the Hermes Agent CLI, which is
# distributed separately by Nous Research.

PARTENON_VERSION="0.1.0"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Partenon v${PARTENON_VERSION} installer"
echo "========================================"

# 1. Check Python venv
if [ ! -d "$REPO_ROOT/.venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "$REPO_ROOT/.venv"
fi
"$REPO_ROOT/.venv/bin/pip" install -q -r "$REPO_ROOT/requirements.txt"

# 2. Check Hermes CLI (optional — not bundled)
if command -v hermes &> /dev/null; then
  echo "Hermes CLI found:"
  hermes --version || true
else
  echo ""
  echo "NOTE: Hermes CLI was not found."
  echo "Partenon profiles are designed for Hermes Agent (Nous Research),"
  echo "which is distributed separately. Install it from:"
  echo "  https://hermes-agent.nousresearch.com/"
  echo "Then add the binary to your PATH or set HERMES_CLI_PATH in .env"
  echo ""
fi

# 3. Install Partenon core skill reference
CORE_SRC="$REPO_ROOT/partenon-core/SKILL.md"
if [ -f "$CORE_SRC" ]; then
  echo "Installing partenon-core skill reference..."
  mkdir -p "$HOME/.hermes/skills/partenon-core"
  cp -R "$CORE_SRC" "$HOME/.hermes/skills/partenon-core/"
fi

# 4. Install hero profiles (best-effort if Hermes CLI is available)
if command -v hermes &> /dev/null; then
  for profile in tesorero mensajero cobrador guardian estratega diplomatico brain; do
    echo "Installing partenon-${profile}..."
    hermes profile install "$REPO_ROOT/hermes/profiles/partenon-${profile}" --alias "partenon-${profile}" || true
  done
else
  echo "Skipping Hermes profile install because the CLI is not available."
fi

# 5. Copy environment template
if [ ! -f "$REPO_ROOT/.env" ]; then
  cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
  echo "Created .env from template. Edit it with your keys."
fi

# 6. Create workspace structure
mkdir -p "$REPO_ROOT/data"
mkdir -p "$REPO_ROOT/logs"

# 7. Verify demo
echo ""
echo "Running Tesorero demo to verify the install..."
"$REPO_ROOT/.venv/bin/python" "$REPO_ROOT/scripts/demo_tesorero.py" || true

echo ""
echo "Partenon local setup complete. Next steps:"
echo "1. cd $REPO_ROOT"
echo "2. Edit .env with your credentials."
echo "3. If you have Hermes CLI: hermes profile use partenon-tesorero"
echo "4. Run: python scripts/demo_tesorero.py"
echo "5. Start the dashboard: cd dashboard && npm install && npm run dev"
