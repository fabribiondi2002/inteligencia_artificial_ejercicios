# Script de desarrollo para Windows PowerShell
# Uso: .\dev.ps1 <comando>
# Ejemplo: .\dev.ps1 setup

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "`n=== Comandos disponibles ===" -ForegroundColor Cyan
    Write-Host "  setup          - Configuración completa del entorno" -ForegroundColor Green
    Write-Host "  install        - Instalar dependencias" -ForegroundColor Green
    Write-Host "  format         - Formatear código (Black + isort)" -ForegroundColor Green
    Write-Host "  lint           - Analizar código (Ruff)" -ForegroundColor Green
    Write-Host "  lint-fix       - Analizar y corregir automáticamente" -ForegroundColor Green
    Write-Host "  security       - Análisis de seguridad (Bandit)" -ForegroundColor Green
    Write-Host "  typecheck      - Verificar tipos (mypy)" -ForegroundColor Green
    Write-Host "  test           - Ejecutar tests" -ForegroundColor Green
    Write-Host "  test-cov       - Ejecutar tests con cobertura" -ForegroundColor Green
    Write-Host "  pre-commit     - Ejecutar pre-commit en todos los archivos" -ForegroundColor Green
    Write-Host "  notebook-clean - Limpiar outputs de notebooks" -ForegroundColor Green
    Write-Host "  clean          - Limpiar archivos temporales" -ForegroundColor Green
    Write-Host "  check          - Verificación completa" -ForegroundColor Green
    Write-Host "  help           - Mostrar esta ayuda`n" -ForegroundColor Green
}

function Install-Dependencies {
    Write-Host "`nInstalando dependencias..." -ForegroundColor Cyan
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    Write-Host "Dependencias instaladas`n" -ForegroundColor Green
}

function Setup-Environment {
    Write-Host "`nConfigurando entorno de desarrollo..." -ForegroundColor Cyan
    Install-Dependencies
    python -m pre_commit install
    Write-Host "Entorno configurado correctamente`n" -ForegroundColor Green
}

function Format-Code {
    Write-Host "`nFormateando código..." -ForegroundColor Cyan
    black .
    isort .
    Write-Host "Código formateado`n" -ForegroundColor Green
}

function Lint-Code {
    Write-Host "`nAnalizando código..." -ForegroundColor Cyan
    ruff check .
    Write-Host "Análisis completado`n" -ForegroundColor Green
}

function Lint-Fix {
    Write-Host "`nAnalizando y corrigiendo código..." -ForegroundColor Cyan
    ruff check --fix .
    Write-Host "Código corregido`n" -ForegroundColor Green
}

function Security-Check {
    Write-Host "`nAnálisis de seguridad..." -ForegroundColor Cyan
    bandit -c pyproject.toml -r .
    Write-Host "Análisis de seguridad completado`n" -ForegroundColor Green
}

function Type-Check {
    Write-Host "`nVerificando tipos..." -ForegroundColor Cyan
    mypy .
    Write-Host "Verificación de tipos completada`n" -ForegroundColor Green
}

function Run-Tests {
    Write-Host "`nEjecutando tests..." -ForegroundColor Cyan
    pytest -v
    Write-Host "Tests ejecutados`n" -ForegroundColor Green
}

function Run-Tests-Coverage {
    Write-Host "`nEjecutando tests con cobertura..." -ForegroundColor Cyan
    pytest -v --cov=. --cov-report=html --cov-report=term-missing
    Write-Host "Reporte generado en htmlcov/`n" -ForegroundColor Green
}

function Run-PreCommit {
    Write-Host "`nEjecutando pre-commit..." -ForegroundColor Cyan
    python -m pre_commit run --all-files
    Write-Host "Pre-commit ejecutado`n" -ForegroundColor Green
}

function Clean-Notebooks {
    Write-Host "`nLimpiando notebooks..." -ForegroundColor Cyan
    Get-ChildItem -Recurse -Filter "*.ipynb" | ForEach-Object {
        nbstripout $_.FullName
    }
    Write-Host "Notebooks limpiados`n" -ForegroundColor Green
}

function Clean-Files {
    Write-Host "`nLimpiando archivos temporales..." -ForegroundColor Cyan
    Get-ChildItem -Path . -Recurse -Include "__pycache__","*.pyc","*.pyo" -Force | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Recurse -Include "*.egg-info",".pytest_cache",".mypy_cache",".ruff_cache" -Force | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
    Remove-Item -Path "htmlcov" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path ".coverage" -Force -ErrorAction SilentlyContinue
    Write-Host "Archivos temporales eliminados`n" -ForegroundColor Green
}

function Full-Check {
    Write-Host "`nVerificación completa..." -ForegroundColor Cyan
    Format-Code
    Lint-Code
    Security-Check
    Type-Check
    Run-Tests
    Write-Host "Verificación completa finalizada`n" -ForegroundColor Green
}

# Ejecutar comando
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "setup" { Setup-Environment }
    "format" { Format-Code }
    "lint" { Lint-Code }
    "lint-fix" { Lint-Fix }
    "security" { Security-Check }
    "typecheck" { Type-Check }
    "test" { Run-Tests }
    "test-cov" { Run-Tests-Coverage }
    "pre-commit" { Run-PreCommit }
    "notebook-clean" { Clean-Notebooks }
    "clean" { Clean-Files }
    "check" { Full-Check }
    default {
        Write-Host "`n❌ Comando desconocido: $Command" -ForegroundColor Red
        Show-Help
    }
}
