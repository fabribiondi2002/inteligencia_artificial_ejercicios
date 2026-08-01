import gymnasium as gym
import numpy as np

# Crear entorno
env = gym.make("MountainCar-v0")

# Discretización del espacio de estados
bins = [20, 20]
q_table = np.zeros(bins + [env.action_space.n])

# Hiperparámetros optimizados
alpha, gamma, epsilon = 0.1, 0.99, 1.0
epsilon_decay, epsilon_min = 0.995, 0.01


def discretizar(obs):
    """Convierte estado continuo a discreto."""
    limites = [env.observation_space.low, env.observation_space.high]
    return tuple(
        np.clip(
            ((obs - limites[0]) / (limites[1] - limites[0]) * np.array(bins)).astype(int),
            0,
            np.array(bins) - 1,
        )
    )


# Entrenamiento
print("Entrenando agente Q-Learning...")
for ep in range(500):
    obs, _ = env.reset()
    estado = discretizar(obs)
    pasos, total = 0, 0

    for _ in range(200):
        # Política epsilon-greedy
        accion = (
            env.action_space.sample()
            if np.random.random() < epsilon
            else np.argmax(q_table[estado])
        )

        # Ejecutar acción
        obs, reward, done, truncated, _ = env.step(accion)
        nuevo_estado = discretizar(obs)

        # Actualizar Q-Table
        q_table[estado][accion] += alpha * (
            reward + gamma * np.max(q_table[nuevo_estado]) - q_table[estado][accion]
        )

        estado = nuevo_estado
        pasos += 1
        total += reward

        if done or truncated:
            break

    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    if (ep + 1) % 50 == 0:
        print(f"Episodio {ep+1}: Pasos={pasos}, Recompensa={total:.2f}, ε={epsilon:.3f}")

print("\n✓ Entrenamiento completo!")

# Probar agente entrenado
print("\nProbando agente entrenado...")
env = gym.make("MountainCar-v0", render_mode="human")
for prueba in range(3):
    obs, _ = env.reset()
    pasos = 0
    for _ in range(200):
        estado = discretizar(obs)
        accion = np.argmax(q_table[estado])
        obs, _, done, truncated, _ = env.step(accion)
        pasos += 1
        if done or truncated:
            break
    print(f"Prueba {prueba+1}: {pasos} pasos")

env.close()
