# Guía de Desarrollo

## Resumen

Este proyecto está configurado con herramientas profesionales de calidad de código que se ejecutan automáticamente.

## Pipeline de Calidad

```
Tu Código
    ↓
[git commit]
    ↓
Pre-commit Hooks (au    tomático)
    ├── trailing-whitespace
    ├── end-of-file-fixer
    ├── Black (formateo)
    ├── isort (imports)
    ├── Ruff (linting)
    ├── Bandit (seguridad)
    ├── mypy (tipos)
    ├── pydocstyle (docs)
    └── notebook formatters
    ↓
✅ Commit exitoso
    ↓
[git push]
    ↓
GitHub Actions CI/CD
    ├── Tests en Python 3.10, 3.11, 3.12
    ├── Cobertura de código
    └── Validaciones completas
    ↓
✅ PR listo para revisión
```

## Herramientas Configuradas

### Formateo Automático

- **Black**: Formateo consistente
- **isort**: Imports organizados

### Análisis de Código

- **Ruff**: Linter ultrarrápido
- **Bandit**: Seguridad
- **mypy**: Type checking
- **pydocstyle**: Documentación

### Testing

- **pytest**: Framework de tests
- **pytest-cov**: Cobertura de código

### Notebooks

- **nbqa**: Formateo de notebooks
- **nbstripout**: Limpieza de outputs

## Comandos Rápidos

| Acción | Windows | Linux/Mac |
|--------|---------|-----------|
| Setup completo | `.\dev.ps1 setup` | `make setup` |
| Formatear | `.\dev.ps1 format` | `make format` |
| Analizar | `.\dev.ps1 lint` | `make lint` |
| Tests | `.\dev.ps1 test` | `make test` |
| Todo | `.\dev.ps1 check` | `make check` |

## Tips Pro

1. **Deja que pre-commit haga el trabajo**
   - No formatees manualmente
   - Commitea y deja que pre-commit arregle todo

2. **Usa los scripts**

   ```bash
   # Antes de commit grande
   .\dev.ps1 format    # Formatear todo
   .\dev.ps1 lint-fix  # Arreglar problemas
   ```

3. **Configura tu editor**
   - VS Code: Instala extensiones de Black, Ruff
   - PyCharm: Configura Black como formateador
   - El `.editorconfig` ayuda a todos

4. **Commits pequeños y frecuentes**
   - Pre-commit es rápido en cambios pequeños
   - Más fácil resolver conflictos

## Troubleshooting

### Pre-commit muy lento

```bash
# Solo la primera vez es lenta
# Siguientes ejecuciones son rápidas
```

### Conflictos entre herramientas

```bash
# Las configs en pyproject.toml están sincronizadas
# Si hay problema, ejecuta en orden:
.\dev.ps1 format
.\dev.ps1 lint-fix
```

### Quiero saltarme pre-commit UNA vez

```bash
git commit --no-verify -m "mensaje"
# ⚠️ USAR CON PRECAUCIÓN
```

## Recursos

- [Black Docs](https://black.readthedocs.io/)
- [Ruff Docs](https://docs.astral.sh/ruff/)
- [Pre-commit](https://pre-commit.com/)

---

**¿Preguntas?** Consulta [CONTRIBUTING.md](../CONTRIBUTING.md)
