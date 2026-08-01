# Ejemplo 1: Agente Reactivo Simple - Termostato

## Concepto Clave

Un **agente reactivo simple** responde directamente a las percepciones sin mantener estado interno. Usa reglas del tipo:

```
SI [condición] ENTONCES [acción]
```

## El Problema: Termostato Inteligente

Diseñaremos un termostato que mantiene una habitación a temperatura confortable.

### Análisis PEAS

| Componente | Descripción |
|------------|-------------|
| **Performance** | Mantener temperatura entre 20-22°C, minimizar cambios |
| **Environment** | Habitación con temperatura variable |
| **Actuators** | Calefacción (ON/OFF), Aire acondicionado (ON/OFF) |
| **Sensors** | Sensor de temperatura |

### Características del Entorno

- ✅ **Observable**: El agente puede ver la temperatura actual
- ✅ **Determinista**: Las acciones tienen efectos predecibles
- ✅ **Episódico**: Cada decisión es independiente
- ✅ **Estático**: El entorno solo cambia por las acciones del agente
- ✅ **Discreto**: Temperatura se lee en valores discretos
- ✅ **Agente único**: Solo un termostato

## La Solución

### Reglas del Agente

```python
SI temperatura < 20°C ENTONCES encender_calefaccion()
SI temperatura > 22°C ENTONCES encender_aire_acondicionado()
SI 20°C <= temperatura <= 22°C ENTONCES apagar_todo()
```

### Diagrama

```
Sensor → [Reglas] → Actuador
  ↓                     ↓
Temp    Si T<20: Heat
        Si T>22: Cool
        Si OK:   Off
```

## Código Explicado

### 1. Clase del Entorno

```python
class Habitacion:
    """Simula una habitación con temperatura variable"""
    def __init__(self, temperatura_inicial=15.0):
        self.temperatura = temperatura_inicial

    def actualizar(self, accion):
        # Calefacción sube 1°C
        # Aire baja 1°C
        # Sin acción: temperatura tiende a 18°C (ambiente)
```

### 2. Clase del Agente

```python
class TermostatoSimple:
    """Agente reactivo simple"""
    def __init__(self, temp_min=20, temp_max=22):
        self.temp_min = temp_min
        self.temp_max = temp_max

    def percibir(self, entorno):
        return entorno.temperatura

    def decidir_accion(self, percepcion):
        # Reglas simples basadas en percepción actual
        if percepcion < self.temp_min:
            return "HEAT"
        elif percepcion > self.temp_max:
            return "COOL"
        else:
            return "OFF"
```

### 3. Simulación

```python
habitacion = Habitacion(15.0)
termostato = TermostatoSimple()

for paso in range(100):
    temp_actual = termostato.percibir(habitacion)
    accion = termostato.decidir_accion(temp_actual)
    habitacion.actualizar(accion)
```

## Ejecución

```bash
python termostato.py
```

Salida esperada:

```
Paso 0: T=15.0°C → HEAT
Paso 1: T=16.0°C → HEAT
Paso 2: T=17.0°C → HEAT
...
Paso 5: T=20.0°C → OFF
Paso 6: T=19.5°C → HEAT
...
```

## Preguntas para Reflexionar

1. **¿Qué pasa si la temperatura ambiente es muy baja?**
   - El agente trabajará constantemente

2. **¿Es este agente racional?**
   - Sí, maximiza el desempeño dado su conocimiento

3. **¿Qué limitaciones tiene?**
   - No puede anticipar
   - No recuerda el pasado
   - Puede oscilar en el límite

4. **¿Cómo mejoraría su eficiencia?**
   - Agregar histéresis (zona muerta)
   - Predecir tendencias
   - Aprendizaje de patrones

## Experimentos Sugeridos

1. **Cambia los límites** de temperatura (15-25°C)
2. **Modifica la temperatura ambiente**
3. **Añade ruido** al sensor
4. **Agrega costo** a cada acción (energía)
5. **Implementa histéresis** para evitar oscilaciones

## Conceptos Aprendidos

✅ Estructura básica de un agente
✅ Percepciones y acciones
✅ Reglas condición-acción
✅ Ciclo percibir-decidir-actuar
✅ Análisis PEAS
✅ Evaluación de racionalidad

## Siguiente Paso

Pasa a `02_agente_aspiradora` para ver un agente con múltiples percepciones y acciones más complejas.
