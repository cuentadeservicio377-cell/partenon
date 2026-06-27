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

# 1. Locate Python 3.10+
PYTHON_CMD=""
for cmd in python3.14 python3.13 python3.12 python3.11 python3.10; do
  if command -v "$cmd" &> /dev/null; then
    PYTHON_CMD="$cmd"
    break
  fi
done
if [ -z "$PYTHON_CMD" ]; then
  PYTHON_CMD="python3"
fi

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info[1])')
if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; }; then
  echo "ERROR: Python 3.10 or newer is required. Found Python ${PYTHON_VERSION} via ${PYTHON_CMD}."
  echo "Please install Python 3.10+ and ensure python3.10+ is in your PATH."
  echo "On macOS you can run: brew install python@3.11"
  exit 1
fi
echo "Python ${PYTHON_VERSION} OK (${PYTHON_CMD})"

# 2. Check Python venv
if [ ! -d "$REPO_ROOT/.venv" ]; then
  echo "Creating Python virtual environment..."
  "$PYTHON_CMD" -m venv "$REPO_ROOT/.venv"
fi
"$REPO_ROOT/.venv/bin/pip" install --upgrade pip -q
"$REPO_ROOT/.venv/bin/pip" install -q -r "$REPO_ROOT/requirements.txt"

# 3. Check Hermes CLI (optional — not bundled)
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

# 4. Install Partenon core skill reference
CORE_SRC="$REPO_ROOT/partenon-core/SKILL.md"
if [ -f "$CORE_SRC" ]; then
  echo "Installing partenon-core skill reference..."
  mkdir -p "$HOME/.hermes/skills/partenon-core"
  cp -R "$CORE_SRC" "$HOME/.hermes/skills/partenon-core/"
fi

# 5. Install hero profiles into Hermes (best-effort if Hermes CLI is available)
HERMES_PROFILES_DIR="$HOME/.hermes/profiles"
if command -v hermes &> /dev/null; then
  for profile in tesorero mensajero cobrador guardian estratega diplomatico brain; do
    echo "Installing partenon-${profile}..."
    mkdir -p "$HERMES_PROFILES_DIR"
    cp -R "$REPO_ROOT/hermes/profiles/partenon-${profile}" "$HERMES_PROFILES_DIR/" || true
  done
  echo "Profiles copied to $HERMES_PROFILES_DIR"
else
  echo "Skipping Hermes profile install because the CLI is not available."
fi

# 6. Copy environment template
if [ ! -f "$REPO_ROOT/.env" ]; then
  cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
  echo "Created .env from template. Edit it with your keys."
fi

# 7. Create workspace structure
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
echo "4. Run: python3 scripts/demo_tesorero.py"
echo "5. Start the dashboard: cd dashboard && npm install && npm run dev"
