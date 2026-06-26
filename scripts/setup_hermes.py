#!/usr/bin/env python3
"""Setup helper para instalar Partenon en Hermes Agent."""

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
    """Ejecuta un comando e imprime salida."""
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=False, text=True)


def ensure_venv() -> Path:
    """Crea o reusa el virtualenv del proyecto."""
    venv = REPO_ROOT / ".venv"
    if not venv.exists():
        print("Creando virtualenv...")
        run([sys.executable, "-m", "venv", str(venv)])
    pip = venv / "bin" / "pip"
    requirements = REPO_ROOT / "requirements.txt"
    if requirements.exists():
        print("Instalando dependencias Python...")
        run([str(pip), "install", "-q", "-r", str(requirements)])
    return venv


def ensure_hermes_cli() -> None:
    """Verifica que Hermes CLI este instalado."""
    if shutil.which("hermes"):
        print("Hermes CLI encontrado.")
        run(["hermes", "--version"], check=False)
        return
    print("Hermes CLI no encontrado. Instalando...")
    subprocess.run(
        "curl -fsSL https://install.hermes-agent.nousresearch.com | bash",
        shell=True,
        check=True,
    )
    os.environ["PATH"] = f"{HERMES_DIR / 'bin'}:{os.environ.get('PATH', '')}"


def install_core_skill() -> None:
    """Instala el skill partenon-core en Hermes."""
    dest = HERMES_DIR / "skills" / "partenon-core"
    dest.mkdir(parents=True, exist_ok=True)
    src = REPO_ROOT / "partenon-core" / "SKILL.md"
    if src.exists():
        shutil.copy2(src, dest / "SKILL.md")
        print("Skill partenon-core instalado.")


def install_profiles() -> None:
    """Instala los 7 perfiles de Partenon en Hermes."""
    for profile in PROFILES:
        profile_path = PROFILES_DIR / profile
        if not profile_path.exists():
            print(f"WARNING: Perfil no encontrado: {profile_path}")
            continue
        print(f"Instalando {profile}...")
        run(
            ["hermes", "profile", "install", str(profile_path), "--alias", profile],
            check=False,
        )


def ensure_env_file() -> None:
    """Copia .env.example a .env si no existe."""
    env_file = REPO_ROOT / ".env"
    example = REPO_ROOT / ".env.example"
    if env_file.exists():
        print(".env ya existe. No se sobreescribe.")
        return
    if example.exists():
        shutil.copy2(example, env_file)
        print("Creado .env desde .env.example. Editalo con tus credenciales.")


def ensure_directories() -> None:
    """Crea directorios de trabajo."""
    (REPO_ROOT / "data").mkdir(exist_ok=True)
    (REPO_ROOT / "logs").mkdir(exist_ok=True)


def main() -> int:
    print("Partenon Setup para Hermes Agent")
    print("=" * 40)

    ensure_venv()
    ensure_hermes_cli()
    install_core_skill()
    install_profiles()
    ensure_env_file()
    ensure_directories()

    print("\nSetup completado.")
    print("Pasos siguientes:")
    print(f"1. cd {REPO_ROOT}")
    print("2. Edita .env con tus credenciales.")
    print("3. Ejecuta: hermes profile use partenon-tesorero")
    print("4. Ejecuta: python scripts/demo_tesorero.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
