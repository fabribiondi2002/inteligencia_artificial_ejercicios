#!/usr/bin/env python3
"""Script de verificación del entorno de desarrollo.

Verifica que todas las herramientas estén instaladas correctamente.
"""

import subprocess
import sys
from pathlib import Path


def check_command(command: list[str], name: str) -> bool:
    """Verifica si un comando está disponible.

    Parameters
    ----------
    command : list[str]
        Comando a verificar
    name : str
        Nombre de la herramienta

    Returns
    -------
    bool
        True si el comando está disponible

    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
        )
        print(f"✅ {name}: Instalado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print(f"❌ {name}: NO instalado")
        return False


def check_python_package(package: str) -> bool:
    """Verifica si un paquete de Python está instalado.

    Parameters
    ----------
    package : str
        Nombre del paquete

    Returns
    -------
    bool
        True si el paquete está instalado

    """
    try:
        __import__(package.replace("-", "_"))
        print(f"✅ {package}: Instalado")
        return True
    except ImportError:
        print(f"❌ {package}: NO instalado")
        return False


def check_file(file_path: Path, description: str) -> bool:
    """Verifica si un archivo existe.

    Parameters
    ----------
    file_path : Path
        Ruta del archivo
    description : str
        Descripción del archivo

    Returns
    -------
    bool
        True si el archivo existe

    """
    if file_path.exists():
        print(f"✅ {description}: Encontrado")
        return True
    else:
        print(f"❌ {description}: NO encontrado")
        return False


def main() -> None:
    """Función principal del script de verificación."""
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DEL ENTORNO DE DESARROLLO")
    print("=" * 70)

    root_dir = Path(__file__).parent
    all_ok = True

    # Verificar Python
    print("\nPython:")
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(
            f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} (se requiere 3.8+)"
        )
        all_ok = False

    # Verificar archivos de configuración
    print("\nArchivos de configuración:")
    files_to_check = [
        (root_dir / ".pre-commit-config.yaml", "Pre-commit config"),
        (root_dir / "pyproject.toml", "pyproject.toml"),
        (root_dir / ".editorconfig", ".editorconfig"),
        (root_dir / "requirements.txt", "requirements.txt"),
        (root_dir / "CONTRIBUTING.md", "CONTRIBUTING.md"),
    ]

    for file_path, description in files_to_check:
        if not check_file(file_path, description):
            all_ok = False

    # Verificar paquetes Python
    print("\nPaquetes de Python:")
    packages = [
        "numpy",
        "matplotlib",
        "pandas",
        "pytest",
        "pre_commit",
        "black",
        "isort",
        "ruff",
        "bandit",
        "mypy",
    ]

    for package in packages:
        if not check_python_package(package):
            all_ok = False

    # Verificar comandos
    print("\nHerramientas de línea de comandos:")
    commands = [
        ([sys.executable, "-m", "black", "--version"], "Black"),
        ([sys.executable, "-m", "isort", "--version"], "isort"),
        ([sys.executable, "-m", "ruff", "--version"], "Ruff"),
        ([sys.executable, "-m", "bandit", "--version"], "Bandit"),
        ([sys.executable, "-m", "mypy", "--version"], "mypy"),
        ([sys.executable, "-m", "pytest", "--version"], "pytest"),
        ([sys.executable, "-m", "pre_commit", "--version"], "pre-commit"),
    ]

    for command, name in commands:
        if not check_command(command, name):
            all_ok = False

    # Verificar pre-commit hooks
    print("\nPre-commit hooks:")
    git_dir = root_dir / ".git"
    hooks_dir = git_dir / "hooks" / "pre-commit"

    if git_dir.exists():
        if hooks_dir.exists():
            print("✅ Pre-commit hooks: Instalados")
        else:
            print("⚠️ Pre-commit hooks: NO instalados")
            print("   Ejecuta: pre-commit install")
            all_ok = False
    else:
        print("⚠️ No es un repositorio Git")

    # Resumen
    print("\n" + "=" * 70)
    if all_ok:
        print("✅ VERIFICACIÓN COMPLETADA - TODO OK")
        print("=" * 70)
        print("\nTu entorno está configurado correctamente!")
        print("\nPróximos pasos:")
        print("  1. Asegúrate de que pre-commit esté instalado: pre-commit install")
        print("  2. Consulta QUICK_START.md para comandos útiles")
        print("  3. ¡Comienza a programar!")
    else:
        print("⚠️ VERIFICACIÓN COMPLETADA - PROBLEMAS ENCONTRADOS")
        print("=" * 70)
        print("\nAcciones recomendadas:")
        print("  1. Instala las dependencias faltantes: pip install -r requirements.txt")
        print("  2. Configura pre-commit: pre-commit install")
        print("  3. Ejecuta este script nuevamente para verificar")
        print("\nO usa el script de configuración automática:")
        print("   python setup_dev.py")
        sys.exit(1)

    print("\nDocumentación disponible:")
    print("  - QUICK_START.md     - Guía rápida")
    print("  - CONTRIBUTING.md    - Guía completa de contribución")


if __name__ == "__main__":
    main()
