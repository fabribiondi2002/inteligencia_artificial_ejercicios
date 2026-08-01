# 💾 Cómo Usar el Modelo Guardado (modelo_qlearning.pkl)

## Guía Rápida

### ¿Ya entrenaste y quieres probar el modelo?

```bash
python probar_modelo.py
```

Esto cargará `modelo_qlearning.pkl` y ejecutará 3 episodios con visualización.

## Opciones Disponibles

### 1. Probar con visualización (por defecto)

```bash
python probar_modelo.py --episodios 5
```

Muestra el grid con emojis en cada paso.

### 2. Probar sin visualización (más rápido)

```bash
python probar_modelo.py --sin-render --episodios 20
```

Solo muestra estadísticas finales.

### 3. Continuar entrenamiento

```bash
python probar_modelo.py --continuar
```

Carga el modelo existente y entrena 500 episodios más. Guarda el resultado como `modelo_qlearning_mejorado.pkl`.

### 4. Comparar diferentes versiones

```bash
python probar_modelo.py --comparar
```

Compara `modelo_qlearning.pkl` vs `modelo_qlearning_mejorado.pkl` (si existe).

### 5. Usar otro archivo

```bash
python probar_modelo.py --archivo mi_modelo.pkl --episodios 10
```

## Uso Programático

Si quieres usar el modelo en tu propio código:

```python
from agente_qlearning import AgenteQLearning, EntornoGrid

# Crear agente
agente = AgenteQLearning(EntornoGrid.ACCIONES)

# Cargar modelo guardado
agente.cargar_modelo("modelo_qlearning.pkl")

# Crear entorno
entorno = EntornoGrid(tamano=5, num_obstaculos=3)

# Ejecutar
recompensa, pasos = agente.ejecutar_episodio(entorno, render=True)

print(f"Recompensa: {recompensa}, Pasos: {pasos}")
```

## ¿Qué contiene el archivo?

El archivo `.pkl` es un diccionario Python serializado con la Q-table:

```python
{
    # Estado → {Acción → Valor Q}
    EstadoGrid(...): {
        0: 2.5,   # ARRIBA
        1: 1.2,   # ABAJO
        2: -0.3,  # IZQUIERDA
        3: 3.1,   # DERECHA
        4: 5.8    # ASPIRAR (mejor!)
    },
    # ... miles de estados más
}
```

## Ventajas

✅ **No necesitas re-entrenar** (ahorra ~5-10 minutos)
✅ **Puedes compartirlo** con compañeros
✅ **Puedes mejorarlo** con más entrenamiento
✅ **Reproducible**: Siempre da los mismos resultados

## Comandos Completos

```bash
# Ver ayuda
python probar_modelo.py --help

# Ejemplo completo: probar 10 episodios sin visualización
python probar_modelo.py --episodios 10 --sin-render

# Continuar entrenamiento y luego probar
python probar_modelo.py --continuar
python probar_modelo.py --archivo modelo_qlearning_mejorado.pkl

# Comparar versiones
python probar_modelo.py --comparar
```

## Troubleshooting

### Error: "No se encontró el archivo"

```
❌ Error: No se encontró el archivo 'modelo_qlearning.pkl'
```

**Solución**: Primero entrena un modelo:

```bash
python agente_qlearning.py
```

Esto creará automáticamente `modelo_qlearning.pkl` al terminar.

### El agente no aprende bien

Si la recompensa es muy baja, intenta:

1. **Entrenar más episodios**:

   ```bash
   python probar_modelo.py --continuar
   ```

2. **Ajustar hiperparámetros** en `agente_qlearning.py`:
   - Aumenta `alpha` (aprende más rápido)
   - Aumenta `gamma` (valora más el futuro)
   - Entrena más episodios

## Experimentos Sugeridos

1. **Entrenar múltiples versiones** con diferentes hiperparámetros
2. **Comparar rendimiento** entre versiones
3. **Entrenar en entornos diferentes** (más obstáculos, grids más grandes)
4. **Visualizar la política aprendida** con `visualizar.py`
