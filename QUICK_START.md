# Guía Rápida de Desarrollo

## Setup Rápido

```bash
# 1. Instalar todo
python setup_dev.py

# 2. Listo para programar!
```

## Comandos Útiles (Windows)

```powershell
# Formatear código
.\dev.ps1 format

# Analizar código
.\dev.ps1 lint

# Ejecutar tests
.\dev.ps1 test

# Verificación completa
.\dev.ps1 check

# Ver todos los comandos
.\dev.ps1 help
```

## Comandos Útiles (Linux/Mac)

```bash
# Formatear código
make format

# Analizar código
make lint

# Ejecutar tests
make test

# Verificación completa
make check

# Ver todos los comandos
make help
```

## Flujo de Trabajo

1. **Hacer cambios en el código**

2. **Validar antes de commit**

   ```bash
   # Windows
   .\dev.ps1 format
   .\dev.ps1 lint-fix

   # Linux/Mac
   make format
   make lint-fix
   ```

3. **Commit** (pre-commit se ejecuta automáticamente)

   ```bash
   git add .
   git commit -m "Descripción del cambio"
   ```

## Herramientas Instaladas

| Herramienta | Propósito | Comando Manual |
|-------------|-----------|----------------|
| **Black** | Formateo de código | `black .` |
| **isort** | Ordenar imports | `isort .` |
| **Ruff** | Linter (errores + estilo) | `ruff check .` |
| **Bandit** | Seguridad | `bandit -r .` |
| **mypy** | Type checking | `mypy .` |
| **pytest** | Testing | `pytest` |

## Solución Rápida de Problemas

### Pre-commit falla

```bash
# Reinstalar
pre-commit clean
pre-commit install
```

### Conflictos de formateo

```bash
# Windows
.\dev.ps1 format

# Linux/Mac
make format
```

### Tests fallan

```bash
# Ver detalles
pytest -v

# Ver con cobertura
pytest --cov
```

## Más Información

- **Guía completa:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **README principal:** [README.md](README.md)
- **Configuración:** `pyproject.toml`

## Tips

- **Pre-commit se ejecuta automáticamente** en cada commit
- **Usa los scripts** (`dev.ps1` o `make`) en lugar de comandos manuales
- **Commitea frecuentemente** - pre-commit te ayuda a mantener calidad
- **Si algo falla**, revisa `CONTRIBUTING.md` para más detalles
