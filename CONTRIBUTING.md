# Guía de Contribución

Este documento describe las prácticas y herramientas para mantener la calidad del código en el repositorio.

## Configuración del Entorno de Desarrollo

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Pre-commit

El proyecto usa pre-commit hooks para validar automáticamente el código antes de cada commit.

**Instalar y activar:**

```bash
pre-commit install
```

**Ejecutar manualmente:**

```bash
# En todos los archivos
pre-commit run --all-files

# Solo en archivos modificados
pre-commit run
```

**Actualizar hooks:**

```bash
pre-commit autoupdate
```

## Herramientas de Calidad de Código

### Black - Formateo de Código

Formatea automáticamente el código Python siguiendo el estilo PEP 8.

```bash
black .
black archivo.py
```

### isort - Ordenar Imports

Ordena y organiza los imports automáticamente.

```bash
isort .
isort archivo.py
```

### Ruff - Linter Rápido

Analiza el código en busca de errores, malas prácticas y problemas de estilo.

```bash
ruff check .
ruff check --fix .  # Corrige automáticamente
```

### Bandit - Análisis de Seguridad

Detecta vulnerabilidades de seguridad comunes.

```bash
bandit -r .
bandit -c pyproject.toml -r .
```

### mypy - Verificación de Tipos

Verifica tipos estáticos para prevenir errores.

```bash
mypy .
mypy archivo.py
```

### pydocstyle - Documentación

Valida que los docstrings sigan convenciones (NumPy style).

```bash
pydocstyle .
```

## Notebooks Jupyter

### Formatear Notebooks

```bash
nbqa black notebooks/
nbqa isort notebooks/
nbqa ruff notebooks/
```

### Limpiar Outputs

```bash
nbstripout notebooks/*.ipynb
```

## Estándares de Código

### Estilo

- **Longitud de línea:** 100 caracteres
- **Formateo:** Black
- **Imports:** isort con perfil Black
- **Docstrings:** Estilo NumPy

### Type Hints

Se recomienda usar type hints en funciones públicas:

```python
def procesar_datos(datos: list[int], umbral: float = 0.5) -> dict[str, float]:
    """
    Procesa datos numéricos aplicando un umbral.

    Parameters
    ----------
    datos : list[int]
        Lista de datos a procesar
    umbral : float, optional
        Valor umbral (default: 0.5)

    Returns
    -------
    dict[str, float]
        Diccionario con resultados del procesamiento
    """
    pass
```

### Docstrings

Ejemplo de docstring estilo NumPy:

```python
def funcion_ejemplo(param1: int, param2: str) -> bool:
    """
    Descripción breve de la función.

    Descripción más detallada si es necesaria, explicando
    el comportamiento y propósito de la función.

    Parameters
    ----------
    param1 : int
        Descripción del primer parámetro
    param2 : str
        Descripción del segundo parámetro

    Returns
    -------
    bool
        Descripción del valor de retorno

    Examples
    --------
    >>> funcion_ejemplo(42, "test")
    True

    Notes
    -----
    Notas adicionales sobre el comportamiento o implementación.
    """
    pass
```

## Testing

### Ejecutar Tests

```bash
pytest
pytest tests/test_archivo.py
pytest -v  # Verbose
pytest --cov  # Con cobertura
```

### Escribir Tests

```python
import pytest

def test_funcion():
    """Test básico."""
    resultado = mi_funcion(entrada)
    assert resultado == esperado

def test_funcion_error():
    """Test de excepciones."""
    with pytest.raises(ValueError):
        mi_funcion(entrada_invalida)
```

## Flujo de Trabajo

1. **Crear rama** para tu trabajo

   ```bash
   git checkout -b feature/mi-caracteristica
   ```

2. **Hacer cambios** y verificar calidad

   ```bash
   pre-commit run --all-files
   pytest
   ```

3. **Commit** (pre-commit se ejecuta automáticamente)

   ```bash
   git add .
   git commit -m "Descripción del cambio"
   ```

4. **Push** y crear Pull Request

   ```bash
   git push origin feature/mi-caracteristica
   ```

## Configuración Personalizada

Todas las herramientas están configuradas en `pyproject.toml`. Puedes ajustar:

- Longitud de línea
- Reglas de linting
- Exclusiones
- Nivel de severidad

## Solución de Problemas

### Pre-commit falla en la instalación

```bash
pre-commit clean
pre-commit install --install-hooks
```

### Conflictos entre herramientas

Las configuraciones en `pyproject.toml` están sincronizadas. Si hay conflictos:

```bash
black .
isort .
ruff check --fix .
```

### Deshabilitar temporalmente pre-commit

```bash
git commit --no-verify -m "mensaje"
```

**⚠️ Usar con precaución - solo en casos excepcionales**

## Recursos

- [Pre-commit](https://pre-commit.com/)
- [Black](https://black.readthedocs.io/)
- [Ruff](https://docs.astral.sh/ruff/)
- [Bandit](https://bandit.readthedocs.io/)
- [mypy](https://mypy.readthedocs.io/)
- [Pytest](https://docs.pytest.org/)
