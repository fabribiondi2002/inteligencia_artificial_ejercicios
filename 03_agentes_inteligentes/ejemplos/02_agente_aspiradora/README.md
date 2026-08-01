# Ejemplo 2: Agente Aspiradora - Múltiples Percepciones

## Concepto Clave

Este ejemplo extiende el agente reactivo simple para manejar:

- **Múltiples percepciones** simultáneas
- **Múltiples acciones** posibles
- **Entorno con posiciones** discretas

## El Problema: Aspiradora Robótica

Una aspiradora debe limpiar dos habitaciones (A y B).

### Análisis PEAS

| Componente | Descripción |
|------------|-------------|
| **Performance** | Maximizar limpieza, minimizar movimientos |
| **Environment** | Dos habitaciones (A, B) con suciedad |
| **Actuators** | Mover_izquierda, Mover_derecha, Aspirar, No_hacer_nada |
| **Sensors** | Posición actual, ¿Hay suciedad aquí? |

### Características del Entorno

- ✅ **Observable**: El agente ve su posición y si hay suciedad
- ✅ **Determinista**: Las acciones tienen efectos predecibles
- ⚠️ **Secuencial**: Las decisiones previas afectan el futuro
- ✅ **Estático**: Solo cambia por acciones del agente
- ✅ **Discreto**: Posiciones y estados discretos
- ✅ **Agente único**: Una sola aspiradora

## La Solución

### Reglas del Agente

```python
SI hay_suciedad_aqui ENTONCES aspirar
SI posicion == A Y habitacion_A_limpia ENTONCES mover_derecha
SI posicion == B Y habitacion_B_limpia ENTONCES mover_izquierda
SI todo_limpio ENTONCES no_hacer_nada
```

### Diagrama

```
Estado del mundo: [A:Sucio, B:Limpio, Pos:A]
                        ↓
                    [Reglas]
                        ↓
                   Acción: ASPIRAR
                        ↓
Nuevo estado:      [A:Limpio, B:Limpio, Pos:A]
```

## Código Explicado

### 1. Percepciones

```python
@dataclass
class Percepcion:
    posicion: str      # 'A' o 'B'
    hay_suciedad: bool # True/False
```

### 2. Entorno

```python
class EntornoAspirador:
    def __init__(self):
        self.habitaciones = {
            'A': True,  # True = sucio
            'B': True
        }
        self.posicion_agente = 'A'
```

### 3. Agente

```python
class AspiradoraSimple:
    def decidir_accion(self, percepcion):
        if percepcion.hay_suciedad:
            return "ASPIRAR"
        elif percepcion.posicion == 'A':
            return "DERECHA"
        elif percepcion.posicion == 'B':
            return "IZQUIERDA"
```

## Ejecución

```bash
python aspiradora.py
```

Salida esperada:

```
Paso 0: [A:Sucio, B:Sucio] Pos:A → ASPIRAR
Paso 1: [A:Limpio, B:Sucio] Pos:A → DERECHA
Paso 2: [A:Limpio, B:Sucio] Pos:B → ASPIRAR
Paso 3: [A:Limpio, B:Limpio] Pos:B → IZQUIERDA
Paso 4: [A:Limpio, B:Limpio] Pos:A → DERECHA
...
```

## Problemas del Agente Reactivo Simple

1. **Oscilación Infinita**: Una vez limpio todo, sigue moviéndose
2. **No recuerda**: No sabe que ya limpió
3. **Ineficiencia**: Movimientos innecesarios

### Mejora: Añadir regla de terminación

```python
SI todo_limpio ENTONCES NO_HACER_NADA
```

Pero esto requiere **modelo del mundo** completo, ¡que no tenemos en un agente simple!

## Variantes para Explorar

### 1. Aspiradora con Sensor Completo

```python
# Puede ver TODAS las habitaciones a la vez
class Percepcion:
    habitaciones: dict  # {'A': bool, 'B': bool}
    posicion: str
```

### 2. Aspiradora con Costo de Movimiento

```python
# Cada movimiento cuesta energía
# Cada aspirado cuesta energía
# Objetivo: minimizar costo total
```

### 3. Aspiradora con Suciedad Aleatoria

```python
# La suciedad aparece aleatoriamente
# Entorno estocástico
```

## Tabla de Comportamiento Completo

| Estado Inicial | Percepción | Acción | Nuevo Estado |
|----------------|------------|--------|--------------|
| [A:S, B:S, @A] | (A, sucio) | ASPIRAR | [A:L, B:S, @A] |
| [A:L, B:S, @A] | (A, limpio) | DERECHA | [A:L, B:S, @B] |
| [A:L, B:S, @B] | (B, sucio) | ASPIRAR | [A:L, B:L, @B] |
| [A:L, B:L, @B] | (B, limpio) | IZQUIERDA | [A:L, B:L, @A] |

## Preguntas para Reflexionar

1. **¿Cuántos estados posibles hay en este mundo?**
   - 2 habitaciones × 2 estados × 2 posiciones = 8 estados

2. **¿Es racional este agente?**
   - Parcialmente: limpia todo, pero luego oscila

3. **¿Cómo mejoraríamos el agente?**
   - Necesitamos **memoria** (estado interno)
   - Ver ejemplo 3: Agente con Modelo

4. **¿Qué pasa con 3 habitaciones?**
   - Las reglas simples se vuelven complejas
   - Necesitamos arquitecturas más sofisticadas

## Experimentos Sugeridos

1. **Agrega una tercera habitación C**
2. **Cambia el estado inicial** (todo limpio, todo sucio)
3. **Añade probabilidad** de ensuciar (entorno estocástico)
4. **Implementa contador** de acciones
5. **Compara eficiencia** entre diferentes estrategias

## Conceptos Aprendidos

✅ Percepciones compuestas (múltiples valores)
✅ Múltiples acciones posibles
✅ Entorno con posiciones
✅ Limitaciones del agente reactivo simple
✅ Necesidad de memoria/estado
✅ Análisis de racionalidad

## Siguiente Paso

Pasa a `03_agente_con_modelo` para ver cómo un agente con **estado interno** puede resolver las limitaciones del agente reactivo simple.
