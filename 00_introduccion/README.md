# 00 - Introducción al Curso

Bienvenido al curso de Inteligencia Artificial 2025. Esta carpeta contiene todo lo necesario para configurar tu entorno de trabajo y comenzar con el curso.

## Contenido

Esta sección incluye:

- Guía de instalación y configuración
- Verificación del entorno de desarrollo
- Recursos iniciales
- Primeros pasos con Python para IA

## Configuración del Entorno

### Paso 1: Verificar Python

Asegúrate de tener Python 3.8 o superior instalado:

```bash
python --version
```

Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/)

### Paso 2: Crear Entorno Virtual

Es **muy recomendable** trabajar con un entorno virtual para aislar las dependencias del proyecto:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias

Con el entorno virtual activado, instala las dependencias necesarias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4: Verificar Instalación

Ejecuta este comando para verificar que todo está correctamente instalado:

```bash
python -c "import numpy; import matplotlib; import pandas; print('Se instaló correctamente')"
```

## Verificación Completa

### Script de Verificación

Puedes crear un archivo `test_setup.py` con el siguiente contenido:

```python
#!/usr/bin/env python3
"""
Script de verificación del entorno
"""

def verificar_instalacion():
    print("Verificando instalación...")
    print("-" * 50)

    # Verificar Python
    import sys
    print(f"Python {sys.version.split()[0]}")

    # Verificar librerías
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except ImportError:
        print("❌ NumPy no instalado")

    try:
        import matplotlib
        print(f"✅ Matplotlib {matplotlib.__version__}")
    except ImportError:
        print("❌ Matplotlib no instalado")

    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__}")
    except ImportError:
        print("❌ Pandas no instalado")

    try:
        import jupyter
        print(f"✅ Jupyter instalado")
    except ImportError:
        print("❌ Jupyter no instalado")

    print("-" * 50)
    print("Verificación completada!")

if __name__ == "__main__":
    verificar_instalacion()
```

Y ejecutarlo con:

```bash
python test_setup.py
```

## Recursos Básicos

### Python para IA

Si necesitas repasar Python, aquí algunos recursos útiles:

- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)

### Git Básico

Comandos esenciales para trabajar con el repositorio:

```bash
# Ver estado del repositorio
git status

# Ver cambios
git diff

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción del cambio"

# Ver historial
git log --oneline
```

## Próximos Pasos

Una vez que hayas configurado tu entorno:

1. Explora la estructura del repositorio
2. Revisa el README principal
3. Dirígete a la carpeta `03_agentes_inteligentes` para comenzar con los ejercicios
4. Mantén tu entorno virtual activado mientras trabajas

## Problemas Comunes (FAQ)

### El comando `python` no funciona

- En algunos sistemas, usa `python3` en lugar de `python`
- Asegúrate de que Python esté en tu PATH

### Problemas al activar el entorno virtual en Windows

- Si obtienes error de permisos, ejecuta PowerShell como administrador y ejecuta:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Error al instalar dependencias

- Actualiza pip primero: `pip install --upgrade pip`
- Si hay errores de compilación, puede que necesites instalar herramientas de compilación para tu sistema

## Soporte

Si tienes problemas con la configuración:

1. Revisa esta documentación cuidadosamente
2. Busca el error en Google/StackOverflow/ChatGPT/etc
3. Consulta con tus compañeros
4. Contacta al profesor por los canales oficiales

---
