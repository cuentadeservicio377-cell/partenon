#!/usr/bin/env python3
"""Setup helper to install Partenon locally."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HERMES_DIR = Path.home() / ".hermes"
PROFILES_DIR = REPO_ROOT / "hermes" / "profiles"
PROFILES = [
    "partenon-tesorero",
    "partenon-mensajero",
    "partenon-cobrador",
    "partenon-guardian",
    "partenon-estratega",
    "partenon-diplomatico",
    "partenon-brain",
]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and print it."""
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=False, text=True)


def ensure_venv() -> Path:
    """Create or reuse the project virtualenv."""
    venv = REPO_ROOT / ".venv"
    if not venv.exists():
        print("Creating virtualenv...")
        run([sys.executable, "-m", "venv", str(venv)])
    pip = venv / "bin" / "pip"
    requirements = REPO_ROOT / "requirements.txt"
    if requirements.exists():
        print("Installing Python dependencies...")
        run([str(pip), "install", "-q", "-r", str(requirements)])
    return venv


def check_hermes_cli() -> bool:
    """Check whether Hermes CLI is installed."""
    hermes_path = shutil.which("hermes")
    if hermes_path:
        print(f"Hermes CLI found: {hermes_path}")
        run(["hermes", "--version"], check=False)
        return True
    print("")
    print("NOTE: Hermes CLI was not found.")
    print("Partenon profiles are designed for Hermes Agent (Nous Research),")
    print("which is distributed separately. Install it from:")
    print("  https://hermes-agent.nousresearch.com/")
    print("Then add the binary to your PATH or set HERMES_CLI_PATH in .env")
    print("")
    return False


def install_core_skill() -> None:
    """Install the partenon-core skill reference in Hermes."""
    dest = HERMES_DIR / "skills" / "partenon-core"
    dest.mkdir(parents=True, exist_ok=True)
    src = REPO_ROOT / "partenon-core" / "SKILL.md"
    if src.exists():
        shutil.copy2(src, dest / "SKILL.md")
        print("partenon-core skill reference installed.")


def install_profiles() -> None:
    """Install the 7 Partenon profiles in Hermes (best-effort)."""
    for profile in PROFILES:
        profile_path = PROFILES_DIR / profile
        if not profile_path.exists():
            print(f"WARNING: Profile not found: {profile_path}")
            continue
        print(f"Installing {profile}...")
        run(
            ["hermes", "profile", "install", str(profile_path), "--alias", profile],
            check=False,
        )


def ensure_env_file() -> None:
    """Copy .env.example to .env if it does not exist."""
    env_file = REPO_ROOT / ".env"
    example = REPO_ROOT / ".env.example"
    if env_file.exists():
        print(".env already exists. Skipping.")
        return
    if example.exists():
        shutil.copy2(example, env_file)
        print("Created .env from .env.example. Edit it with your credentials.")


def ensure_directories() -> None:
    """Create working directories."""
    (REPO_ROOT / "data").mkdir(exist_ok=True)
    (REPO_ROOT / "logs").mkdir(exist_ok=True)


def verify_demo() -> None:
    """Run the Tesorero demo to verify the local setup."""
    print("")
    print("Running Tesorero demo to verify the install...")
    venv_python = REPO_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        subprocess.run([str(venv_python), "scripts/demo_tesorero.py"], cwd=REPO_ROOT)
    else:
        subprocess.run([sys.executable, "scripts/demo_tesorero.py"], cwd=REPO_ROOT)


def main() -> int:
    print("Partenon Setup for Hermes Agent")
    print("=" * 40)

    ensure_venv()
    has_hermes = check_hermes_cli()
    install_core_skill()
    if has_hermes:
        install_profiles()
    else:
        print("Skipping Hermes profile install because the CLI is not available.")
    ensure_env_file()
    ensure_directories()
    verify_demo()

    print("\nSetup complete.")
    print("Next steps:")
    print(f"1. cd {REPO_ROOT}")
    print("2. Edit .env with your credentials.")
    print("3. If you have Hermes CLI: hermes profile use partenon-tesorero")
    print("4. Run: python scripts/demo_tesorero.py")
    print("5. Start the dashboard: cd dashboard && npm install && npm run dev")
    return 0


if __name__ == "__main__":
    sys.exit(main())
