#!/usr/bin/env bash
set -euo pipefail

# Partenon Installer
# Prepares the local Python environment, installs Partenon profiles into Hermes
# (when available), and verifies the Scribe demo. It does NOT install the Hermes
# Agent CLI, which is distributed separately by Nous Research.

PARTENON_VERSION="1.0.0"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Minimum required Python version
PYTHON_MIN_MAJOR=3
PYTHON_MIN_MINOR=10

echo "Partenon v${PARTENON_VERSION} installer"
echo "========================================"

# ---------------------------------------------------------------------------
# 1. Locate Python 3.10+
# ---------------------------------------------------------------------------
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

PYTHON_VERSION=$("$PYTHON_CMD" -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$("$PYTHON_CMD" -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$("$PYTHON_CMD" -c 'import sys; print(sys.version_info[1])')

if [ "$PYTHON_MAJOR" -lt "$PYTHON_MIN_MAJOR" ] || { [ "$PYTHON_MAJOR" -eq "$PYTHON_MIN_MAJOR" ] && [ "$PYTHON_MINOR" -lt "$PYTHON_MIN_MINOR" ]; }; then
  echo "ERROR: Python ${PYTHON_MIN_MAJOR}.${PYTHON_MIN_MINOR} or newer is required. Found Python ${PYTHON_VERSION} via ${PYTHON_CMD}."
  echo "Please install Python ${PYTHON_MIN_MAJOR}.${PYTHON_MIN_MINOR}+ and ensure it is in your PATH."
  exit 1
fi
echo "Python ${PYTHON_VERSION} OK (${PYTHON_CMD})"

# ---------------------------------------------------------------------------
# 2. Manage Python virtual environment
# ---------------------------------------------------------------------------
VENV_DIR="$REPO_ROOT/.venv"
VENV_NEEDS_CREATE=false

if [ ! -d "$VENV_DIR" ]; then
  VENV_NEEDS_CREATE=true
else
  # If the venv exists, check whether its Python is still usable and new enough.
  VENV_PYTHON="$VENV_DIR/bin/python"
  if [ ! -x "$VENV_PYTHON" ]; then
    VENV_NEEDS_CREATE=true
  else
    VENV_VERSION=$("$VENV_PYTHON" -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    VENV_MAJOR=$("$VENV_PYTHON" -c 'import sys; print(sys.version_info[0])')
    VENV_MINOR=$("$VENV_PYTHON" -c 'import sys; print(sys.version_info[1])')
    if [ "$VENV_MAJOR" -lt "$PYTHON_MIN_MAJOR" ] || { [ "$VENV_MAJOR" -eq "$PYTHON_MIN_MAJOR" ] && [ "$VENV_MINOR" -lt "$PYTHON_MIN_MINOR" ]; }; then
      echo "Existing .venv uses Python ${VENV_VERSION}, which is too old. Recreating..."
      rm -rf "$VENV_DIR"
      VENV_NEEDS_CREATE=true
    fi
  fi
fi

if [ "$VENV_NEEDS_CREATE" = true ]; then
  echo "Creating Python virtual environment..."
  "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -q -r "$REPO_ROOT/requirements.txt"

# ---------------------------------------------------------------------------
# 3. Check Hermes CLI (optional — not bundled)
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# 4. Install Partenon core skills
# ---------------------------------------------------------------------------
for skill in partenon-core partenon-judge partenon-workflows; do
  SKILL_SRC="$REPO_ROOT/skills/$skill/SKILL.md"
  if [ -f "$SKILL_SRC" ]; then
    echo "Installing $skill skill reference..."
    mkdir -p "$HOME/.hermes/skills/$skill"
    cp -R "$SKILL_SRC" "$HOME/.hermes/skills/$skill/"
  fi
done

# ---------------------------------------------------------------------------
# 5. Install hero profiles into Hermes (best-effort if Hermes CLI is available)
# ---------------------------------------------------------------------------
HERMES_PROFILES_DIR="$HOME/.hermes/profiles"
PROFILES=(scribe herald collector guardian strategist diplomat brain)

if command -v hermes &> /dev/null; then
  for profile in "${PROFILES[@]}"; do
    echo "Installing partenon-${profile}..."
    mkdir -p "$HERMES_PROFILES_DIR"
    cp -R "$REPO_ROOT/hermes/profiles/partenon-${profile}" "$HERMES_PROFILES_DIR/" || true
  done
  echo "Profiles copied to $HERMES_PROFILES_DIR"
else
  echo "Skipping Hermes profile install because the CLI is not available."
fi

# ---------------------------------------------------------------------------
# 6. Copy environment template and generate secure defaults
# ---------------------------------------------------------------------------
ENV_FILE="$REPO_ROOT/.env"
ENV_EXAMPLE="$REPO_ROOT/.env.example"

if [ ! -f "$ENV_FILE" ]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  echo "Created .env from template."
fi

# Ensure the dashboard has a strong secret and credentials.
# These are idempotent: only added if the placeholder or missing value is detected.
ensure_env_value() {
  local key="$1"
  local value="$2"
  local pattern="^${key}="
  if ! grep -qE "$pattern" "$ENV_FILE"; then
    echo "${key}=${value}" >> "$ENV_FILE"
  fi
}

generate_secret() {
  if command -v openssl &> /dev/null; then
    openssl rand -base64 32 | tr -d '\n'
  else
    python3 -c 'import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())'
  fi
}

if grep -qE '^DASHBOARD_AUTH_SECRET=REPLACE_WITH_A_STRONG_SECRET_AT_LEAST_32_CHARS$' "$ENV_FILE"; then
  SECRET=$(generate_secret)
  sed -i '' "s|^DASHBOARD_AUTH_SECRET=REPLACE_WITH_A_STRONG_SECRET_AT_LEAST_32_CHARS$|DASHBOARD_AUTH_SECRET=${SECRET}|" "$ENV_FILE"
  echo "Generated DASHBOARD_AUTH_SECRET in .env"
fi

if grep -qE '^# DASHBOARD_APP_USERNAME=admin$' "$ENV_FILE"; then
  DASHBOARD_USER="admin"
  DASHBOARD_PASS=$(generate_secret | cut -c1-24)
  sed -i '' "s|^# DASHBOARD_APP_USERNAME=admin$|DASHBOARD_APP_USERNAME=${DASHBOARD_USER}|" "$ENV_FILE"
  sed -i '' "s|^# DASHBOARD_APP_PASSWORD=partenon$|DASHBOARD_APP_PASSWORD=${DASHBOARD_PASS}|" "$ENV_FILE"
  echo "Generated DASHBOARD_APP_USERNAME and DASHBOARD_APP_PASSWORD in .env"
fi

# ---------------------------------------------------------------------------
# 7. Create workspace structure
# ---------------------------------------------------------------------------
mkdir -p "$REPO_ROOT/data"
mkdir -p "$REPO_ROOT/logs"

# ---------------------------------------------------------------------------
# 8. Verify demo
# ---------------------------------------------------------------------------
echo ""
echo "Running Scribe demo to verify the install..."
"$REPO_ROOT/.venv/bin/python" "$REPO_ROOT/scripts/demo_scribe.py"

echo ""
echo "Partenon local setup complete. Next steps:"
echo "1. cd $REPO_ROOT"
echo "2. Review .env and add your real credentials when ready."
echo "3. If you have Hermes CLI: hermes profile use partenon-scribe"
echo "4. Run: python3 scripts/demo_scribe.py"
echo "5. Start the dashboard: cd dashboard && npm install && npm run dev"
