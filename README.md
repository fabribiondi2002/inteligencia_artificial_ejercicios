# Inteligencia Artificial - IUA 2025

> Repositorio del curso de Inteligencia Artificial

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Descripción

Este repositorio contiene el material práctico del curso de Inteligencia Artificial 2025. Incluye ejercicios, proyectos y recursos para aprender los conceptos fundamentales de IA a través de implementaciones en Python.

## Documentación

- **[QUICK_START.md](QUICK_START.md)** - Guía rápida para desarrolladores
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía detallada de contribución

## Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/halexisgonzalez/ia-2025-iua.git
cd ia-2025-iua
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/Mac:**

```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar pre-commit (recomendado para desarrolladores)

**Opción A - Script automático:**

```bash
python setup_dev.py
```

**Opción B - Manual:**

```bash
pre-commit install
```

**Opción C - Usando comandos del proyecto (Windows):**

```powershell
.\dev.ps1 setup
```

### 6. Verificar instalación

```bash
python -c "import numpy, matplotlib; print('Se instaló correctamente')"
```

## Estructura del Proyecto

```
ia-2025-iua/
│
├── 00_introduccion/          ← Guías de configuración y ambientación
├── 03_agentes_inteligentes/  ← Ejercicios de agentes inteligentes
│
├── .gitignore                ← Archivos ignorados por Git
├── requirements.txt          ← Dependencias de Python
├── LICENSE                   ← Licencia MIT
└── README.md                 ← Este archivo
```

## Contenidos

### [00 - Introducción](00_introduccion/)

Material de bienvenida, configuración del entorno y primeros pasos.

### [03 - Agentes Inteligentes](03_agentes_inteligentes/)

Implementación de diferentes tipos de agentes inteligentes, arquitecturas y evaluación de desempeño.

## Tecnologías

- **Python 3.8+**
- **NumPy** - Computación numérica
- **Matplotlib** - Visualización de datos
- **Jupyter** - Notebooks interactivos

## Calidad de Código

Este proyecto utiliza herramientas automáticas para mantener la calidad del código:

- **Black** - Formateo automático de código
- **isort** - Organización de imports
- **Ruff** - Linter rápido y moderno
- **Bandit** - Análisis de seguridad
- **mypy** - Verificación de tipos
- **Pre-commit** - Validación automática antes de commits

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles sobre el uso de estas herramientas.

## Profesor

- **Ing. Alexis González**
- **Institución:** Centro Regional Universitario Córdoba - IUA
- **Año:** 2025

## Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Instala pre-commit: `pre-commit install`
4. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Abre un Pull Request

Para más información sobre estándares de código y herramientas, consulta [CONTRIBUTING.md](CONTRIBUTING.md).

## Contacto

Para consultas sobre el curso, usar los canales oficiales de la materia.

---

**¡Bienvenidos al curso de Inteligencia Artificial!**
