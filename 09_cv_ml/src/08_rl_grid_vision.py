"""
08 - Aprendizaje por Refuerzo con Visión
=========================================

APRENDIZAJE POR REFUERZO: El agente aprende a tomar decisiones basándose en recompensas.

¿Qué es Aprendizaje por Refuerzo (RL)?
- Agente interactúa con un entorno
- Recibe recompensas (positivas o negativas) por sus acciones
- Objetivo: Aprender política óptima para maximizar recompensa acumulada
- NO necesita etiquetas, aprende por ensayo y error

Componentes:
- Estado (s): Situación actual del agente
- Acción (a): Lo que puede hacer el agente
- Recompensa (r): Feedback del entorno
- Política (π): Estrategia del agente (qué acción tomar en cada estado)

Q-Learning:
- Algoritmo clásico de RL
- Aprende función Q(s, a) = recompensa esperada
- Usa tabla Q o red neuronal (Deep Q-Network)

En este ejemplo:
- Agente navega en un grid 10x10
- Entrada: IMAGEN del grid (visión)
- Objetivo: Llegar a la meta evitando obstáculos
- Conexión con CV: El agente "ve" el entorno como imagen
"""

import os
import random

import matplotlib.pyplot as plt
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tensorflow import keras
from tensorflow.keras import layers

os.makedirs("../img", exist_ok=True)
os.makedirs("../models", exist_ok=True)


# Crear entorno de grid
class GridWorld:
    """
    Entorno de grid simple para RL.

    Grid 10x10 con:
    - Agente (posición inicial)
    - Meta (posición objetivo)
    - Obstáculos (paredes)
    """

    def __init__(self, size=10):
        self.size = size
        self.reset()

    def reset(self):
        """Reinicia el entorno."""
        # Posiciones
        self.agent_pos = [0, 0]  # Esquina superior izquierda
        self.goal_pos = [self.size - 1, self.size - 1]  # Esquina inferior derecha

        # Obstáculos aleatorios
        self.obstacles = []
        for _ in range(15):
            obs = [random.randint(1, self.size - 2), random.randint(1, self.size - 2)]
            if obs != self.agent_pos and obs != self.goal_pos:
                self.obstacles.append(obs)

        return self.get_state()

    def get_state(self):
        """
        Devuelve estado como imagen 10x10x3 (RGB).

        - Fondo: Negro (0, 0, 0)
        - Agente: Azul (0, 0, 255)
        - Meta: Verde (0, 255, 0)
        - Obstáculos: Rojo (255, 0, 0)
        """
        state = np.zeros((self.size, self.size, 3), dtype=np.uint8)

        # Obstáculos en rojo
        for obs in self.obstacles:
            state[obs[0], obs[1]] = [255, 0, 0]

        # Meta en verde
        state[self.goal_pos[0], self.goal_pos[1]] = [0, 255, 0]

        # Agente en azul
        state[self.agent_pos[0], self.agent_pos[1]] = [0, 0, 255]

        return state

    def step(self, action):
        """
        Ejecuta acción y devuelve (estado, recompensa, terminado).

        Acciones:
            0: Arriba
            1: Abajo
            2: Izquierda
            3: Derecha
        """
        # Guardar posición anterior
        old_pos = self.agent_pos.copy()

        # Aplicar acción
        if action == 0:  # Arriba
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == 1:  # Abajo
            self.agent_pos[0] = min(self.size - 1, self.agent_pos[0] + 1)
        elif action == 2:  # Izquierda
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == 3:  # Derecha
            self.agent_pos[1] = min(self.size - 1, self.agent_pos[1] + 1)

        # Calcular recompensa
        reward = -0.1  # Penalización por cada paso (incentiva llegar rápido)

        # Verificar si llegó a la meta
        done = False
        if self.agent_pos == self.goal_pos:
            reward = 10.0
            done = True

        # Verificar si chocó con obstáculo
        elif self.agent_pos in self.obstacles:
            reward = -5.0
            self.agent_pos = old_pos  # Rebotar

        return self.get_state(), reward, done


# Crear red neuronal para Q-Learning (DQN)
def crear_dqn():
    """
    Crea Deep Q-Network que predice Q-values para cada acción.

    Input: Estado como imagen (10, 10, 3)
    Output: Q-values para 4 acciones
    """
    model = keras.Sequential(
        [
            layers.Input(shape=(10, 10, 3)),
            # Capas convolucionales para procesar imagen
            layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
            layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            layers.Flatten(),
            # Capas densas
            layers.Dense(128, activation="relu"),
            layers.Dense(4, activation="linear"),  # Q-value por cada acción
        ],
        name="dqn",
    )

    model.compile(optimizer="adam", loss="mse")

    return model


print("=" * 60)
print("APRENDIZAJE POR REFUERZO CON VISIÓN")
print("=" * 60)

# Crear entorno y modelo
env = GridWorld(size=10)
model = crear_dqn()

print("\n✓ Entorno y modelo creados")
print(f"  - Grid: {env.size}x{env.size}")
print(f"  - Acciones: 4 (arriba, abajo, izquierda, derecha)")
print(f"  - Estado: Imagen RGB de {env.size}x{env.size}x3")

# Visualizar entorno inicial
state = env.reset()
plt.figure(figsize=(6, 6))
plt.imshow(state)
plt.title("Entorno de Grid\nAzul=Agente, Verde=Meta, Rojo=Obstáculos")
plt.axis("off")
plt.tight_layout()
plt.savefig("../img/08_grid_inicial.png", dpi=150, bbox_inches="tight")
print("\n✓ Entorno guardado en: ../img/08_grid_inicial.png")
plt.show()


# Parámetros de entrenamiento
print("\n" + "=" * 60)
print("ENTRENAMIENTO DEL AGENTE")
print("=" * 60)

EPISODES = 200  # Número de episodios
EPSILON = 1.0  # Exploración inicial (100%)
EPSILON_DECAY = 0.995  # Decaimiento de exploración
EPSILON_MIN = 0.01  # Exploración mínima
GAMMA = 0.95  # Factor de descuento (importancia de recompensas futuras)

# Memoria de experiencias
memory = []
MEMORY_SIZE = 2000

# Estadísticas
episode_rewards = []
episode_steps = []

print(f"\nParámetros:")
print(f"  - Episodios: {EPISODES}")
print(f"  - Epsilon inicial: {EPSILON}")
print(f"  - Gamma: {GAMMA}")
print("\nEntrenando (esto puede tardar 5-10 minutos)...\n")

# Entrenar
for episode in range(EPISODES):
    state = env.reset()
    state_normalized = state.astype("float32") / 255.0
    total_reward = 0
    steps = 0

    for step in range(100):  # Máximo 100 pasos por episodio
        steps += 1

        # Epsilon-greedy: exploración vs explotación
        if random.random() < EPSILON:
            action = random.randint(0, 3)  # Acción aleatoria (exploración)
        else:
            # Predecir Q-values y elegir mejor acción (explotación)
            q_values = model.predict(
                state_normalized.reshape(1, 10, 10, 3), verbose=0
            )[0]
            action = np.argmax(q_values)

        # Ejecutar acción
        next_state, reward, done = env.step(action)
        next_state_normalized = next_state.astype("float32") / 255.0

        total_reward += reward

        # Guardar experiencia en memoria
        memory.append((state_normalized, action, reward, next_state_normalized, done))
        if len(memory) > MEMORY_SIZE:
            memory.pop(0)

        state_normalized = next_state_normalized

        # Entrenar con batch de experiencias
        if len(memory) > 32:
            # Muestrear batch
            batch = random.sample(memory, 32)

            states = np.array([exp[0] for exp in batch])
            actions = np.array([exp[1] for exp in batch])
            rewards = np.array([exp[2] for exp in batch])
            next_states = np.array([exp[3] for exp in batch])
            dones = np.array([exp[4] for exp in batch])

            # Calcular targets Q
            q_values = model.predict(states, verbose=0)
            next_q_values = model.predict(next_states, verbose=0)

            for i in range(32):
                if dones[i]:
                    q_values[i][actions[i]] = rewards[i]
                else:
                    q_values[i][actions[i]] = rewards[i] + GAMMA * np.max(
                        next_q_values[i]
                    )

            # Entrenar modelo
            model.fit(states, q_values, epochs=1, verbose=0)

        if done:
            break

    # Decaer epsilon (reducir exploración)
    EPSILON = max(EPSILON_MIN, EPSILON * EPSILON_DECAY)

    # Guardar estadísticas
    episode_rewards.append(total_reward)
    episode_steps.append(steps)

    # Imprimir progreso
    if (episode + 1) % 20 == 0:
        avg_reward = np.mean(episode_rewards[-20:])
        avg_steps = np.mean(episode_steps[-20:])
        print(
            f"Episodio {episode + 1}/{EPISODES} | "
            f"Recompensa promedio: {avg_reward:.2f} | "
            f"Pasos promedio: {avg_steps:.1f} | "
            f"Epsilon: {EPSILON:.3f}"
        )

print("\n✓ Entrenamiento completado")

# Guardar modelo
modelo_path = "../models/dqn_grid.keras"
model.save(modelo_path)
print(f"✓ Modelo guardado en: {modelo_path}")


# Visualizar aprendizaje
print("\n" + "=" * 60)
print("ANÁLISIS DEL APRENDIZAJE")
print("=" * 60)

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(episode_rewards)
plt.title("Recompensa por Episodio")
plt.xlabel("Episodio")
plt.ylabel("Recompensa Total")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(episode_steps)
plt.title("Pasos por Episodio")
plt.xlabel("Episodio")
plt.ylabel("Número de Pasos")
plt.grid(True)

plt.suptitle("Evolución del Aprendizaje", fontsize=14)
plt.tight_layout()
plt.savefig("../img/08_learning_curves.png", dpi=150, bbox_inches="tight")
print("\n✓ Curvas guardadas en: ../img/08_learning_curves.png")
plt.show()


# Probar agente entrenado
print("\n" + "=" * 60)
print("PRUEBA DEL AGENTE ENTRENADO")
print("=" * 60)

env_test = GridWorld(size=10)
state = env_test.reset()
state_normalized = state.astype("float32") / 255.0

trajectory = [state.copy()]
done = False
steps = 0

while not done and steps < 50:
    # Elegir mejor acción (sin exploración)
    q_values = model.predict(state_normalized.reshape(1, 10, 10, 3), verbose=0)[0]
    action = np.argmax(q_values)

    state, reward, done = env_test.step(action)
    state_normalized = state.astype("float32") / 255.0
    trajectory.append(state.copy())
    steps += 1

print(f"\n✓ Episodio de prueba:")
print(f"  - Pasos hasta la meta: {steps}")
print(f"  - ¿Llegó a la meta?: {'Sí' if done else 'No'}")

# Visualizar trayectoria
fig, axes = plt.subplots(2, 5, figsize=(15, 6))
axes = axes.flatten()

for i in range(min(10, len(trajectory))):
    axes[i].imshow(trajectory[i * (len(trajectory) // 10)])
    axes[i].set_title(f"Paso {i * (len(trajectory) // 10)}")
    axes[i].axis("off")

plt.suptitle("Trayectoria del Agente Entrenado", fontsize=14)
plt.tight_layout()
plt.savefig("../img/08_trajectory.png", dpi=150, bbox_inches="tight")
print("✓ Trayectoria guardada en: ../img/08_trajectory.png")
plt.show()


print("\n" + "=" * 60)
print("CONCLUSIONES:")
print("=" * 60)
print("""
1. APRENDIZAJE POR REFUERZO (RL):
   - NO supervisado: Sin etiquetas explícitas
   - Aprende por RECOMPENSAS (positivas/negativas)
   - Trial and error: Explora y aprende de errores
   - Mejora con la experiencia (como humanos/animales)

2. DIFERENCIAS CON APRENDIZAJE SUPERVISADO:
   
   SUPERVISADO (archivos 04-07):
   - Tiene etiquetas: "Esta imagen es un gato"
   - Aprende patrones: input → output
   - Requiere datos etiquetados
   
   REFUERZO (este archivo):
   - NO tiene etiquetas explícitas
   - Tiene objetivo: "Llega a la meta"
   - Aprende qué acciones maximizan recompensa
   - Explora el ambiente para descubrir qué funciona

3. VISIÓN + RL (Deep RL):
   - Estado como IMAGEN (10×10×3 píxeles)
   - NO coordenadas explícitas (x, y)
   - CNN procesa información visual
   - Agente "ve" el mundo como nosotros
   - Más realista que usar coordenadas

4. DQN (Deep Q-Network):
   - Q-Learning clásico: Tabla Q(estado, acción)
   - DQN: Red neuronal aproxima función Q
   - Q(estado, acción) = Recompensa total esperada
   - Usa CNN para procesar imágenes de estado

5. COMPONENTES CLAVE:
   
   a) EPSILON (ε-greedy):
      - Exploration vs Exploitation
      - Alta (0.9): Explora (acciones aleatorias)
      - Baja (0.1): Explota (mejor acción conocida)
      - Decay: Empieza explorando, termina explotando
   
   b) GAMMA (γ):
      - Descuento de recompensas futuras
      - γ=0.99: Valora recompensas a largo plazo
      - γ=0.0: Solo importa recompensa inmediata
   
   c) EXPERIENCE REPLAY:
      - Memoria de (estado, acción, recompensa, siguiente_estado)
      - Batch aleatorio de experiencias para entrenar
      - Rompe correlación temporal
      - Más eficiente en datos

VENTAJAS del RL con Visión:
✓ No requiere etiquetas (solo recompensas)
✓ Aprende comportamientos complejos
✓ Se adapta a cambios en el ambiente
✓ Generaliza a situaciones nuevas
✓ Similar a aprendizaje humano/animal
✓ Descubre estrategias no obvias
✓ Funciona en entornos dinámicos

DESVENTAJAS del RL con Visión:
✗ Necesita MUCHAS iteraciones (miles de episodios)
✗ Muy sensible a hiperparámetros (LR, gamma, epsilon)
✗ Entrenamiento lento (horas/días)
✗ Difícil de debuggear (¿por qué no aprende?)
✗ Puede quedar atrapado en mínimos locales
✗ Inestable (puede olvidar lo aprendido)
✗ Requiere diseñar buenas recompensas (reward shaping)
✗ Consume mucha memoria (experience replay)

6. COMPARACIÓN: RL vs SUPERVISADO

   CUÁNDO USAR RL:
   ✓ Decisiones secuenciales (juegos, robótica)
   ✓ Interacción con ambiente
   ✓ Objetivo claro pero sin ejemplos de cómo lograrlo
   ✓ Recompensas disponibles
   
   CUÁNDO USAR SUPERVISADO:
   ✓ Clasificación/detección (imágenes estáticas)
   ✓ Datos etiquetados disponibles
   ✓ Respuesta única correcta
   ✓ No hay secuencia temporal

7. APLICACIONES PRÁCTICAS:
   
   JUEGOS:
   - AlphaGo: Maestro de Go
   - DQN: Atari (Pong, Breakout)
   - OpenAI Five: Dota 2
   
   ROBÓTICA:
   - Navegación autónoma
   - Manipulación de objetos
   - Caminar (robots humanoides)
   
   SISTEMAS AUTÓNOMOS:
   - Autos autónomos
   - Drones de entrega
   - Trading algorítmico
   
   OPTIMIZACIÓN:
   - Gestión de recursos
   - Control de tráfico
   - Centros de datos (enfriamiento)

8. MEJORAS POSIBLES:
   - Arquitectura más profunda (más capas CNN)
   - Double DQN (reduce sobreestimación)
   - Dueling DQN (separa value y advantage)
   - Prioritized Experience Replay
   - A3C (asíncrono, multi-agente)

PRÓXIMO PASO: Ver detección de objetos con YOLO (archivo 09)
- Detecta MÚLTIPLES objetos simultáneamente
- Como Haar Cascade (Módulo 08) pero mucho más potente
- Tiempo real (30+ FPS)
""")
