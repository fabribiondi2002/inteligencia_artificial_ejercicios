#!/usr/bin/env python3
"""Script de configuración del entorno de desarrollo.

Instala dependencias y configura pre-commit hooks automáticamente.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], description: str) -> bool:
    """Ejecuta un comando y muestra el resultado.

    Parameters
    ----------
    command : list[str]
        Comando a ejecutar
    description : str
        Descripción de lo que hace el comando

    Returns
    -------
    bool
        True si el comando fue exitoso, False en caso contrario

    """
    print(f"\n{'='*60}")
    print(f" - {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✅ {description} - COMPLETADO")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FALLÓ")
        print(f"Error: {e.stderr}")
        return False


def main() -> None:
    """Función principal del script de configuración."""
    print("\n" + "=" * 60)
    print("CONFIGURACIÓN DEL ENTORNO DE DESARROLLO")
    print("=" * 60)

    # Verificar Python
    python_version = sys.version_info
    print(f"\n✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")

    if python_version < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        sys.exit(1)

    # Verificar que estamos en el directorio correcto
    root_dir = Path(__file__).parent
    requirements_file = root_dir / "requirements.txt"

    if not requirements_file.exists():
        print("❌ Error: No se encontró requirements.txt")
        sys.exit(1)

    # Instalar dependencias
    success = run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Actualizar pip"
    )

    if not success:
        print("\n---- Advertencia: No se pudo actualizar pip, continuando...")

    success = run_command(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
        "Instalar dependencias de requirements.txt",
    )

    if not success:
        print("\n❌ Error crítico: No se pudieron instalar las dependencias")
        sys.exit(1)

    # Configurar pre-commit
    success = run_command(
        [sys.executable, "-m", "pre_commit", "install"], "Configurar pre-commit hooks"
    )

    if not success:
        print("\n---- Advertencia: No se pudo configurar pre-commit")
        print("Ejecuta manualmente: pre-commit install")

    # Ejecutar pre-commit en todos los archivos (opcional)
    print("\n" + "=" * 60)
    print("¿Ejecutar validación de código en todos los archivos?")
    print("=" * 60)
    response = input("Esto puede tomar varios minutos (s/N): ").strip().lower()

    if response in ["s", "si", "sí", "y", "yes"]:
        success = run_command(
            [sys.executable, "-m", "pre_commit", "run", "--all-files"],
            "Validar código con pre-commit",
        )

        if not success:
            print("\n---- Se encontraron problemas en el código")
            print("Los archivos fueron modificados automáticamente")
            print("Revisa los cambios con: git diff")

    # Resumen final
    print("\n" + "=" * 60)
    print("CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("  1. Verifica la instalación: python -c 'import numpy; print(\"OK\")'")
    print("  2. Los pre-commit hooks se ejecutarán automáticamente en cada commit")
    print("  3. Consulta CONTRIBUTING.md para más información")
    print("\n¡Listo para comenzar a programar!")


if __name__ == "__main__":
    main()
