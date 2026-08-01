#!/usr/bin/env python3
"""Script de verificación del entorno de desarrollo
Curso: Inteligencia Artificial 2025 - IUA
"""


def verificar_instalacion():
    """Verifica que todas las dependencias estén correctamente instaladas"""
    print("Verificando instalación del entorno...")
    print("=" * 60)

    errores = []

    # Verificar Python
    import sys

    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        errores.append("Python 3.8+ es requerido")

    # Verificar librerías principales
    librerias = [
        ("numpy", "NumPy"),
        ("matplotlib", "Matplotlib"),
        ("pandas", "Pandas"),
        ("jupyter", "Jupyter"),
        ("pytest", "Pytest"),
    ]

    for modulo, nombre in librerias:
        try:
            lib = __import__(modulo)
            version = getattr(lib, "__version__", "versión desconocida")
            print(f"✅ {nombre} {version}")
        except ImportError:
            print(f"❌ {nombre} NO instalado")
            errores.append(f"{nombre} no está instalado")

    print("=" * 60)

    # Resultado final
    if errores:
        print("\nProblemas encontrados:")
        for error in errores:
            print(f"   • {error}")
        print("\nSolución: pip install -r requirements.txt")
        return False
    else:
        print("\n¡Todo está correctamente instalado!")
        print("Estás listo para comenzar con el curso")
        return True


if __name__ == "__main__":
    import sys

    exito = verificar_instalacion()
    sys.exit(0 if exito else 1)
