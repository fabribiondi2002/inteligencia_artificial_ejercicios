# Ejemplo 3: Agente con Modelo del Mundo - Estado Interno

## Concepto Clave

Este ejemplo introduce **agentes basados en modelos** que pueden:

- **Mantener estado interno** (memoria)
- **Construir un modelo** del mundo
- **Planificar** acciones futuras basándose en el modelo
- **Evitar oscilaciones** y comportamientos redundantes

## El Problema: Aspiradora Inteligente

La misma aspiradora del Ejemplo 2, pero ahora con **memoria** para recordar qué habitaciones ya limpió.

### Análisis PEAS

| Componente | Descripción |
|------------|-------------|
| **Performance** | Maximizar limpieza, minimizar movimientos innecesarios |
| **Environment** | Dos habitaciones (A, B) con suciedad |
| **Actuators** | Mover_izquierda, Mover_derecha, Aspirar, No_hacer_nada |
| **Sensors** | Posición actual, ¿Hay suciedad aquí? |

### Diferencia Clave

🔄 **Agente Reactivo Simple** (Ej. 2): Solo usa percepción actual
🧠 **Agente con Modelo** (Ej. 3): Usa percepción + estado interno + modelo del mundo

## Arquitectura del Agente

```
┌──────────────────────────────────────────────────┐
│              AGENTE CON MODELO                   │
│                                                  │
│  ┌────────────┐      ┌──────────────┐          │
│  │ Percepciones│─────▶│ Actualizar   │          │
│  │            │      │   Modelo     │          │
│  └────────────┘      └──────┬───────┘          │
│                             │                   │
│  ┌──────────────┐           ▼                   │
│  │   MODELO     │◀──────────┘                   │
│  │  DEL MUNDO   │                               │
│  │              │                               │
│  │ • Mapa de    │                               │
│  │   habitaciones│                              │
│  │ • Habitaciones│                              │
│  │   visitadas  │                               │
│  │ • Estado de  │                               │
│  │   limpieza   │                               │
│  └──────┬───────┘                               │
│         │                                        │
│         ▼                                        │
│  ┌──────────────┐                               │
│  │   REGLAS     │                               │
│  │   + MODELO   │                               │
│  └──────┬───────┘                               │
│         │                                        │
│         ▼                                        │
│  ┌──────────────┐                               │
│  │   ACCIÓN     │                               │
│  └──────────────┘                               │
└──────────────────────────────────────────────────┘
```

## La Solución

### Estado Interno del Agente

```python
class EstadoInterno:
    habitaciones_visitadas: set       # {'A', 'B'}
    habitaciones_limpias: set         # {'A'}
    posicion_creida: str              # 'A'
    acciones_realizadas: list         # ['ASPIRAR', 'DERECHA']
```

### Reglas Mejoradas

```python
SI hay_suciedad_aqui ENTONCES aspirar Y marcar_limpia(posicion)
SI todas_habitaciones_limpias ENTONCES no_hacer_nada
SI habitacion_no_visitada ENTONCES ir_a(habitacion_no_visitada)
SI posicion == A Y habitacion_B_sucia ENTONCES mover_derecha
SI posicion == B Y habitacion_A_sucia ENTONCES mover_izquierda
```

### Flujo de Decisión con Modelo

```
Estado del Mundo:    [A:Sucio, B:Sucio, Pos:A]
                              ↓
Percepción:          (Pos:A, Suciedad:True)
                              ↓
Actualizar Modelo:   Visitadas:{A}, Limpias:{}
                              ↓
Consultar Reglas     ¿Hay suciedad? → SÍ
  + Modelo:                   ↓
                         Acción: ASPIRAR
                              ↓
Actualizar Modelo:   Visitadas:{A}, Limpias:{A}
                              ↓
Nuevo Estado:        [A:Limpio, B:Sucio, Pos:A]
```

## Código Explicado

### 1. Estado Interno

```python
@dataclass
class EstadoInterno:
    """Modelo del mundo que mantiene el agente."""
    habitaciones_visitadas: set
    habitaciones_limpias: set
    posicion_actual: str
    acciones_realizadas: list
```

### 2. Agente con Modelo

```python
class AspiradoraConModelo:
    def __init__(self):
        self.estado = EstadoInterno(
            habitaciones_visitadas=set(),
            habitaciones_limpias=set(),
            posicion_actual='A',
            acciones_realizadas=[]
        )

    def actualizar_modelo(self, percepcion):
        """Actualiza el modelo interno basándose en la percepción."""
        self.estado.posicion_actual = percepcion.posicion
        self.estado.habitaciones_visitadas.add(percepcion.posicion)

        if not percepcion.hay_suciedad:
            self.estado.habitaciones_limpias.add(percepcion.posicion)

    def decidir_accion(self, percepcion):
        """Decide basándose en el modelo interno."""
        # Primero actualizar modelo
        self.actualizar_modelo(percepcion)

        # Si hay suciedad, limpiar
        if percepcion.hay_suciedad:
            return "ASPIRAR"

        # Si todo está limpio, detenerse
        if self.todo_limpio():
            return "NADA"

        # Explorar habitaciones no visitadas o sucias
        return self.planificar_movimiento()
```

## Comparación: Agente Simple vs. Con Modelo

| Aspecto | Agente Simple | Agente con Modelo |
|---------|---------------|-------------------|
| **Memoria** | ❌ No | ✅ Sí |
| **Modelo del mundo** | ❌ No | ✅ Sí |
| **Oscilación** | ❌ Infinita | ✅ Se detiene |
| **Eficiencia** | ⚠️ Baja | ✅ Alta |
| **Acciones** | ~10+ | ~4 |
| **Complejidad** | Simple | Moderada |

## Ejecución

```bash
python agente_con_modelo.py
```

Salida esperada:

```
Estado inicial: [A:Sucio, B:Sucio, @A]

Paso 0: Pos:A, Sucio → ASPIRAR    → [A:Limpio, B:Sucio, @A]
  Modelo: Visitadas={'A'}, Limpias={'A'}

Paso 1: Pos:A, Limpio → DERECHA   → [A:Limpio, B:Sucio, @B]
  Modelo: Visitadas={'A'}, Limpias={'A'}

Paso 2: Pos:B, Sucio → ASPIRAR    → [A:Limpio, B:Limpio, @B]
  Modelo: Visitadas={'A','B'}, Limpias={'A','B'}

Paso 3: Pos:B, Limpio → NADA      → [A:Limpio, B:Limpio, @B]
  Modelo: Visitadas={'A','B'}, Limpias={'A','B'}

¡Completado en 4 pasos! ✅
```

## Ventajas del Modelo

### 1. **Termina Correctamente**

- No oscila infinitamente
- Sabe cuándo ha terminado

### 2. **Más Eficiente**

- 4 acciones vs. 10+ del agente simple
- No repite acciones innecesarias

### 3. **Puede Razonar**

```python
# El agente puede planificar:
"He limpiado A, ahora debo ir a B"
"Ya visité todas las habitaciones limpias → TERMINAR"
```

### 4. **Robusto a Cambios**

```python
# Si el entorno cambia (se ensucia B):
# El agente detecta que B ya no está limpio
# y vuelve a limpiarlo
```

## Limitaciones

A pesar de las mejoras, este agente tiene limitaciones:

1. **Modelo puede desactualizarse**: Si el entorno cambia dinámicamente
2. **Memoria limitada**: Solo recuerda lo que ha visto
3. **No predice cambios**: No anticipa que una habitación podría ensuciarse
4. **Sin optimización**: No busca la ruta más eficiente

## Variantes Avanzadas

### 1. Modelo con Creencias Probabilísticas

```python
class ModeloProbabilistico:
    habitaciones = {
        'A': {'limpia': 0.9, 'sucia': 0.1},
        'B': {'limpia': 0.1, 'sucia': 0.9}
    }

    def actualizar(self, percepcion):
        # Bayesian update
        pass
```

### 2. Agente con Predicción

```python
def predecir_cambios(self):
    """Predice si una habitación podría ensuciarse."""
    if tiempo_desde_limpieza('A') > 5:
        probabilidad_sucia = 0.8
```

### 3. Agente con Planificación

```python
def planificar_ruta_optima(self):
    """Planifica la secuencia óptima de acciones."""
    # Algoritmo de búsqueda (A*, BFS, etc.)
    return ['ASPIRAR', 'DERECHA', 'ASPIRAR']
```

## Experimentos Sugeridos

1. **Agrega 3 habitaciones**: ¿Cómo escala el modelo?
2. **Entorno dinámico**: Las habitaciones se ensucian aleatoriamente
3. **Costo de movimiento**: Penaliza movimientos innecesarios
4. **Memoria limitada**: Solo recuerda últimas N observaciones
5. **Comparar rendimiento**: Simple vs. Con Modelo

## Preguntas para Reflexionar

1. **¿Por qué el modelo es importante?**
   - Permite razonar sobre el mundo sin percibirlo directamente

2. **¿Qué pasa si el modelo es incorrecto?**
   - El agente toma decisiones subóptimas o incorrectas

3. **¿Cómo actualizar el modelo si el entorno cambia?**
   - Necesitamos **actualización continua** del modelo

4. **¿Este agente es racional?**
   - Más racional que el simple, pero aún subóptimo

5. **¿Cuándo falla este agente?**
   - Entornos muy dinámicos o estocásticos

## Conceptos Aprendidos

✅ Estado interno y memoria
✅ Modelo del mundo
✅ Actualización de creencias
✅ Planificación básica
✅ Detección de terminación
✅ Comparación de arquitecturas

## Tipos de Agentes Basados en Modelos

### 1. Modelo Simple (Este ejemplo)

- Estado determinista
- Modelo completo
- Actualización directa

### 2. Modelo con Creencias

- Estados parcialmente observables
- Distribuciones de probabilidad
- Actualización bayesiana

### 3. Modelo con Metas

- Añade objetivos explícitos
- Planificación hacia metas
- Ver Ejemplo 4

### 4. Modelo con Utilidad

- Función de utilidad
- Optimización de recompensas
- Ver Ejemplo 5

## Siguiente Paso

Pasa a `04_agente_con_aprendizaje` para ver cómo un agente puede **aprender automáticamente** mediante **Machine Learning (Q-Learning)** en entornos complejos donde escribir reglas manualmente es imposible.

## Referencias

- Russell & Norvig, Cap. 2: "Model-based reflex agents"
- Concepto de "estado del mundo"
- Filtro de estados (state estimation)
