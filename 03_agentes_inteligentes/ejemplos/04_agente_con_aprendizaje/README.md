# Ejemplo 4: Agente con Aprendizaje por Refuerzo (Q-Learning)

## Concepto Clave

Este ejemplo introduce **Machine Learning** en agentes inteligentes mediante **Aprendizaje por Refuerzo (Reinforcement Learning)**:

- El agente **aprende** la política óptima mediante **prueba y error**
- **No requiere reglas manuales** complejas
- Se adapta a **entornos complejos y dinámicos**
- Utiliza **Q-Learning** para aprender valores de acciones

## El Problema: Aspiradora en Entorno Complejo

Una aspiradora debe limpiar un **grid de 5x5** con:

- 🧱 **Obstáculos** aleatorios
- 💰 **Costos** por movimiento (-1 punto)
- ✨ **Recompensas** por limpiar (+10 puntos)
- 🔄 **Suciedad dinámica** (aparece aleatoriamente)
- 🚫 **Penalización** por chocar con obstáculos (-5 puntos)

### ¿Por qué ML?

| Con Reglas Manuales | Con Q-Learning |
|---------------------|----------------|
| ❌ Imposible escribir reglas para 25 estados | ✅ Aprende automáticamente |
| ❌ No se adapta a obstáculos | ✅ Aprende a evitar obstáculos |
| ❌ No optimiza costo/beneficio | ✅ Maximiza recompensa |
| ❌ Requiere re-programar si cambia entorno | ✅ Re-entrena y se adapta |

## Análisis PEAS

| Componente | Descripción |
|------------|-------------|
| **Performance** | Maximizar recompensa acumulada (limpieza - costos) |
| **Environment** | Grid 5x5 con obstáculos, suciedad dinámica |
| **Actuators** | Arriba, Abajo, Izquierda, Derecha, Aspirar |
| **Sensors** | Posición (x,y), Mapa de suciedad, Mapa de obstáculos |

### Características del Entorno

- ⚠️ **Parcialmente Observable**: Solo ve su posición y celda actual
- ⚠️ **Estocástico**: La suciedad aparece aleatoriamente
- ✅ **Secuencial**: Las decisiones afectan estados futuros
- ⚠️ **Dinámico**: La suciedad aparece mientras el agente actúa
- ✅ **Discreto**: Grid discreto de posiciones
- ✅ **Agente único**: Una sola aspiradora

## Q-Learning: ¿Cómo Funciona?

### Conceptos Fundamentales

**Q-Table**: Tabla que guarda el "valor" de cada acción en cada estado

```
         ↑      ↓      ←      →    ASPIRAR
(0,0)  [0.5]  [0.2]  [0.1]  [0.8]  [2.3]
(0,1)  [0.3]  [0.6]  [0.4]  [0.2]  [0.1]
(1,0)  [0.9]  [0.3]  [0.7]  [0.5]  [1.5]
...
```

### Fórmula de Actualización

```
Q(s, a) = Q(s, a) + α × [r + γ × max(Q(s', a')) - Q(s, a)]
```

Donde:

- **Q(s,a)**: Valor de tomar acción `a` en estado `s`
- **α**: Tasa de aprendizaje (learning rate) = 0.1
- **γ**: Factor de descuento (discount factor) = 0.9
- **r**: Recompensa inmediata
- **s'**: Nuevo estado
- **max(Q(s', a'))**: Mejor valor futuro posible

### Proceso de Aprendizaje

```
1. Observar estado actual s
2. Elegir acción a (ε-greedy: exploración vs. explotación)
3. Ejecutar acción a
4. Observar recompensa r y nuevo estado s'
5. Actualizar Q(s,a) con la fórmula
6. Repetir
```

## Arquitectura del Agente

```
┌──────────────────────────────────────────────┐
│         AGENTE CON Q-LEARNING                │
│                                              │
│  ┌──────────────┐                           │
│  │ Percepción   │                           │
│  │ (x, y, grid) │                           │
│  └──────┬───────┘                           │
│         │                                    │
│         ▼                                    │
│  ┌──────────────┐      ┌──────────────┐    │
│  │   Q-TABLE    │◀─────│ Actualización│    │
│  │              │      │   Q(s,a)     │    │
│  │ Estado-Acción│      └──────▲───────┘    │
│  │   → Valor    │             │            │
│  └──────┬───────┘             │            │
│         │              ┌──────┴───────┐    │
│         ▼              │  Recompensa  │    │
│  ┌──────────────┐     │  del Entorno │    │
│  │ ε-greedy     │     └──────────────┘    │
│  │ Explorar o   │                          │
│  │ Explotar     │                          │
│  └──────┬───────┘                          │
│         │                                   │
│         ▼                                   │
│  ┌──────────────┐                          │
│  │   ACCIÓN     │                          │
│  └──────────────┘                          │
└──────────────────────────────────────────────┘
```

## Sistema de Recompensas

```python
RECOMPENSAS = {
    'limpiar_suciedad': +10,     # Limpiar una celda sucia
    'movimiento': -1,             # Cada movimiento cuesta energía
    'chocar_obstaculo': -5,       # Penalización por chocar
    'celda_limpia': 0,            # Aspirar celda ya limpia
    'completar_todo': +50         # Bonus por limpiar todo
}
```

## Estrategia ε-greedy

Balance entre **exploración** (probar cosas nuevas) y **explotación** (usar lo aprendido):

```python
if random() < epsilon:
    # EXPLORACIÓN: Acción aleatoria
    accion = random.choice(acciones)
else:
    # EXPLOTACIÓN: Mejor acción según Q-table
    accion = argmax(Q[estado])

# Decaimiento de epsilon
epsilon = epsilon * 0.995  # Menos exploración con el tiempo
```

## Comparación: Reglas vs. Q-Learning

### Ejemplo de Complejidad

**Escenario**: Grid 5x5 con 3 obstáculos y 5 celdas sucias

#### Con Reglas Manuales (Imposible)

```python
if posicion == (0,0) and hay_suciedad:
    return "ASPIRAR"
elif posicion == (0,0) and not hay_suciedad and obstaculo_en[(0,1)]:
    return "DERECHA"
elif posicion == (0,0) and not hay_suciedad and not obstaculo_en[(0,1)] and suciedad_en[(2,3)]:
    # ... ¡IMPOSIBLE! Demasiadas combinaciones
```

**Número de reglas necesarias**: ~10,000+

#### Con Q-Learning (Automático)

```python
# El agente aprende solo en ~1000 episodios
agente = AgenteQLearning()
agente.entrenar(episodios=1000)
agente.ejecutar()  # ¡Ya sabe la política óptima!
```

## Código Explicado

### 1. Entorno Grid

```python
class EntornoGrid:
    def __init__(self, tamano=5, obstaculos=3):
        self.grid = np.zeros((tamano, tamano))
        self.obstaculos = self.generar_obstaculos(obstaculos)
        self.suciedad = self.generar_suciedad()

    def ejecutar_accion(self, accion):
        # Retorna: nuevo_estado, recompensa, terminado
        pass
```

### 2. Q-Learning Agent

```python
class AgenteQLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0):
        self.q_table = {}  # {estado: {accion: valor}}
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def elegir_accion(self, estado):
        if random() < self.epsilon:
            return random.choice(self.acciones)  # Explorar
        else:
            return argmax(self.q_table[estado])  # Explotar

    def actualizar_q(self, estado, accion, recompensa, nuevo_estado):
        q_actual = self.q_table[estado][accion]
        max_q_futuro = max(self.q_table[nuevo_estado].values())

        # Fórmula de Q-Learning
        nuevo_q = q_actual + self.alpha * (
            recompensa + self.gamma * max_q_futuro - q_actual
        )

        self.q_table[estado][accion] = nuevo_q
```

### 3. Entrenamiento

```python
def entrenar(episodios=1000):
    for episodio in range(episodios):
        estado = entorno.reset()

        while not terminado:
            # 1. Elegir acción
            accion = agente.elegir_accion(estado)

            # 2. Ejecutar
            nuevo_estado, recompensa, terminado = entorno.step(accion)

            # 3. Aprender
            agente.actualizar_q(estado, accion, recompensa, nuevo_estado)

            estado = nuevo_estado

        # Decaer epsilon
        agente.epsilon *= 0.995
```

## Ejecución

### Opción 1: Entrenar y ejecutar (automático)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Entrenar y ejecutar (todo en uno)
python agente_qlearning.py
```

### Opción 2: Usar modelo guardado (sin re-entrenar)

```bash
# Probar modelo guardado (3 episodios con visualización)
python probar_modelo.py

# Probar sin visualización (más rápido)
python probar_modelo.py --sin-render --episodios 10

# Continuar entrenamiento desde modelo guardado
python probar_modelo.py --continuar

# Comparar diferentes modelos
python probar_modelo.py --comparar
```

### Opción 3: Visualizar aprendizaje (gráficos)

```bash
# Generar gráficos del entrenamiento
python visualizar.py
```

Salida esperada durante entrenamiento:

```
Episodio 0: Recompensa total = -25 (random)
Episodio 100: Recompensa total = 15 (aprendiendo...)
Episodio 500: Recompensa total = 45 (mejorando)
Episodio 1000: Recompensa total = 80 (óptimo!)

✅ Entrenamiento completado
📊 Q-table guardada en 'modelo_qlearning.pkl'
```

## Visualización del Aprendizaje

El código genera gráficos mostrando:

1. **Recompensa por episodio**: Curva de aprendizaje
2. **Política aprendida**: Mapa de calor con mejores acciones
3. **Q-values**: Valores de cada estado-acción
4. **Trayectoria óptima**: Camino que sigue el agente

## Ventajas del Q-Learning

### 1. **Aprende Automáticamente**

- No requiere programar reglas complejas
- Descubre estrategias no obvias

### 2. **Se Adapta**

```python
# Si el entorno cambia, simplemente re-entrena
entorno.agregar_obstaculos(5)
agente.entrenar(episodios=500)  # Se adapta al nuevo entorno
```

### 3. **Optimiza Automáticamente**

- Balance óptimo entre limpieza y costo de movimiento
- Aprende rutas eficientes

### 4. **Generaliza**

- Lo aprendido en una parte del grid ayuda en otras

## Limitaciones del Q-Learning

1. **Requiere Muchos Episodios**: ~1000+ para entornos complejos
2. **No escala bien**: Grid muy grande → Q-table gigante
3. **No generaliza entre entornos**: Debe re-entrenar si cambia mucho
4. **Exploración inicial costosa**: Muchos errores al principio

### Soluciones Avanzadas

Para entornos más complejos:

- **Deep Q-Learning (DQN)**: Reemplaza Q-table por red neuronal
- **Policy Gradients**: Aprende directamente la política
- **Actor-Critic**: Combina valor y política

## Hiperparámetros Importantes

```python
HIPERPARAMETROS = {
    'alpha': 0.1,        # Learning rate (qué tan rápido aprende)
    'gamma': 0.9,        # Discount factor (importancia del futuro)
    'epsilon_inicio': 1.0,     # Exploración inicial (100%)
    'epsilon_fin': 0.01,       # Exploración final (1%)
    'epsilon_decay': 0.995,    # Tasa de decaimiento
    'episodios': 1000          # Número de episodios de entrenamiento
}
```

## Experimentos Sugeridos

1. **Variar learning rate**: ¿Cómo afecta α = 0.01 vs. α = 0.5?
2. **Cambiar discount factor**: ¿Qué pasa con γ = 0.5 vs. γ = 0.99?
3. **Más obstáculos**: ¿Cómo aprende con 50% del grid bloqueado?
4. **Suciedad muy dinámica**: ¿Puede adaptarse a cambios constantes?
5. **Grid más grande**: Probar con 10x10 o 20x20

## Preguntas para Reflexionar

1. **¿Por qué Q-Learning necesita muchos episodios?**
   - Debe explorar todas las combinaciones estado-acción

2. **¿Qué pasa si epsilon nunca decrece?**
   - El agente seguiría explorando aleatoriamente

3. **¿Por qué gamma < 1?**
   - Prioriza recompensas inmediatas sobre futuras

4. **¿Cuándo fallaría Q-Learning?**
   - Estados infinitos, entornos que cambian muy rápido

5. **¿Es esto mejor que reglas manuales?**
   - Para entornos complejos: SÍ
   - Para entornos simples: NO (overkill)

## Conceptos Aprendidos

✅ Aprendizaje por Refuerzo
✅ Q-Learning y Q-table
✅ Exploración vs. Explotación (ε-greedy)
✅ Sistema de recompensas
✅ Entrenamiento de agentes
✅ Visualización del aprendizaje
✅ Hiperparámetros de ML

## Comparación con Ejemplos Anteriores

| Ejemplo | Tipo | Complejidad | Adaptabilidad | ML |
|---------|------|-------------|---------------|-----|
| 01. Termostato | Reactivo Simple | Muy Baja | ❌ | ❌ |
| 02. Aspiradora 2 hab. | Reactivo Simple | Baja | ❌ | ❌ |
| 03. Con Modelo | Basado en Modelo | Media | ⚠️ | ❌ |
| **04. Q-Learning** | **Con Aprendizaje** | **Alta** | **✅** | **✅** |

## Siguiente Paso

Este es un ejemplo avanzado de agentes inteligentes. Para ir más allá:

- **Deep Q-Networks (DQN)**: Usa redes neuronales
- **Policy Gradients**: Aprende políticas directamente
- **Multi-Agent RL**: Múltiples agentes que cooperan/compiten

## Referencias

- Sutton & Barto: "Reinforcement Learning: An Introduction"
- Q-Learning paper original (Watkins, 1989)
- OpenAI Gym para entornos de RL
- Stable Baselines3 para algoritmos RL avanzados

## Modelo Guardado (modelo_qlearning.pkl)

### ¿Qué es?

El archivo `.pkl` contiene la **Q-table entrenada** serializada. Es todo el conocimiento que el agente aprendió durante el entrenamiento.

### ¿Para qué sirve?

1. **Evitar re-entrenar**: Cargar y usar directamente (ahorra ~5-10 minutos de entrenamiento)
2. **Compartir conocimiento**: Enviar a otros sin que tengan que entrenar
3. **Continuar mejorando**: Cargar y seguir entrenando desde ese punto
4. **Comparar versiones**: Guardar múltiples versiones y comparar rendimiento

### ¿Cómo usarlo?

```python
# En tu código
agente = AgenteQLearning(EntornoGrid.ACCIONES)
agente.cargar_modelo("modelo_qlearning.pkl")  # ¡Listo para usar!

# Ejecutar sin re-entrenar
recompensa, pasos = agente.ejecutar_episodio(entorno)
```

O usando el script dedicado:

```bash
# Forma más simple
python probar_modelo.py

# Con opciones
python probar_modelo.py --episodios 10 --sin-render
```

### Contenido del archivo

```python
# Estructura interna (simplificado)
{
    EstadoGrid(pos=(0,0), suciedad={...}): {
        ARRIBA: 2.5,      # Valor Q
        ABAJO: 1.2,
        IZQUIERDA: -0.3,
        DERECHA: 3.1,
        ASPIRAR: 5.8      # ← Mejor acción
    },
    EstadoGrid(pos=(1,1), suciedad={...}): {
        # ... más valores Q
    }
    # ... ~1000+ estados explorados
}
```

## Archivos del Ejemplo

```
04_agente_con_aprendizaje/
├── README.md                 # Este archivo
├── agente_qlearning.py      # Implementación principal
├── visualizar.py            # Herramientas de visualización
├── probar_modelo.py         # 🆕 Script para usar modelos guardados
├── requirements.txt         # Dependencias (numpy, matplotlib)
└── modelo_qlearning.pkl     # 💾 Q-table entrenada (se crea al ejecutar)
```
