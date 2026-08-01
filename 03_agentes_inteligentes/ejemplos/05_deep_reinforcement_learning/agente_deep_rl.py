"""Agente con Deep Reinforcement Learning usando Stable-Baselines3.

Este script demuestra cómo entrenar un agente con SOLO 20-30 LÍNEAS
usando una librería profesional, en lugar de 500+ líneas manual.
"""

import argparse
import os

from entorno_gym import AspiradoraEnv
from stable_baselines3 import A2C, DQN, PPO
from stable_baselines3.common.monitor import Monitor


def entrenar_agente(
    algoritmo: str = "ppo",
    timesteps: int = 50_000,
    tamano_grid: int = 5,
    obstaculos: int = 3,
    save_path: str = "modelos",
    log_path: str = "logs",
):
    """Entrena un agente usando Stable-Baselines3.

    ¡Solo ~20 líneas vs. 500+ del ejemplo manual!

    Parameters
    ----------
    algoritmo : str
        'dqn', 'ppo', o 'a2c'
    timesteps : int
        Número de pasos de entrenamiento
    tamano_grid : int
        Tamaño del grid
    obstaculos : int
        Número de obstáculos
    save_path : str
        Carpeta para guardar modelos
    log_path : str
        Carpeta para logs de TensorBoard

    """
    print("=" * 70)
    print(f"🚀 ENTRENAMIENTO CON {algoritmo.upper()} (Stable-Baselines3)")
    print("=" * 70)

    # Crear directorios
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(log_path, exist_ok=True)

    # 1. Crear entorno
    print("\n1️⃣ Creando entorno...")
    env = AspiradoraEnv(tamano=tamano_grid, num_obstaculos=obstaculos)
    env = Monitor(env)  # Para logging automático

    # 2. Crear modelo (¡con red neuronal automática!)
    print(f"2️⃣ Creando modelo {algoritmo.upper()}...")

    if algoritmo.lower() == "dqn":
        model = DQN(
            "MlpPolicy",  # Red neuronal automática
            env,
            learning_rate=1e-3,
            buffer_size=10000,
            learning_starts=100,
            batch_size=32,
            gamma=0.99,
            exploration_fraction=0.1,
            exploration_final_eps=0.02,
            target_update_interval=100,
            verbose=1,
            tensorboard_log=f"{log_path}/{algoritmo}",
        )
    elif algoritmo.lower() == "ppo":
        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=3e-4,
            n_steps=2048,
            batch_size=64,
            n_epochs=10,
            gamma=0.99,
            gae_lambda=0.95,
            clip_range=0.2,
            verbose=1,
            tensorboard_log=f"{log_path}/{algoritmo}",
        )
    elif algoritmo.lower() == "a2c":
        model = A2C(
            "MlpPolicy",
            env,
            learning_rate=7e-4,
            n_steps=5,
            gamma=0.99,
            gae_lambda=1.0,
            verbose=1,
            tensorboard_log=f"{log_path}/{algoritmo}",
        )
    else:
        raise ValueError(f"Algoritmo '{algoritmo}' no soportado. Usa: dqn, ppo, a2c")

    print("\n📊 Arquitectura del modelo:")
    print(f"   - Algoritmo: {algoritmo.upper()}")
    print("   - Policy: MlpPolicy (Red neuronal multi-capa)")
    print(f"   - Observation space: {env.observation_space.shape}")
    print(f"   - Action space: {env.action_space.n} acciones")

    # 3. Entrenar (¡TODO AUTOMÁTICO!)
    print(f"\n3️⃣ Entrenando durante {timesteps:,} timesteps...")
    print("   💡 Abre TensorBoard: tensorboard --logdir logs/")

    model.learn(total_timesteps=timesteps, progress_bar=True)

    # 4. Guardar modelo
    model_path = f"{save_path}/{algoritmo}_aspiradora"
    model.save(model_path)
    print(f"\n4️⃣ Modelo guardado en: {model_path}.zip")

    # 5. Evaluar
    print("\n5️⃣ Evaluando modelo...")
    obs, info = env.reset()
    total_reward = 0
    done = False
    steps = 0

    while not done and steps < 100:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        steps += 1
        done = terminated or truncated

    print("\n📊 Resultado evaluación:")
    print(f"   - Recompensa total: {total_reward:.1f}")
    print(f"   - Pasos: {steps}")
    print(f"   - Suciedad restante: {info['suciedad_restante']}")
    print(f"   - {'✅ Completó!' if info['suciedad_restante'] == 0 else '⏱️ Timeout'}")

    print("\n" + "=" * 70)
    print("✅ ENTRENAMIENTO COMPLETADO")
    print("=" * 70)
    print("\n💡 Comandos útiles:")
    print(f"   - Ver logs: tensorboard --logdir {log_path}")
    print(f"   - Probar modelo: python probar_modelo_deep.py --modelo {model_path}")

    return model


def probar_modelo_guardado(model_path: str, episodios: int = 5, render: bool = True):
    """Prueba un modelo guardado.

    Parameters
    ----------
    model_path : str
        Ruta al modelo (.zip)
    episodios : int
        Número de episodios a ejecutar
    render : bool
        Mostrar visualización

    """
    print("=" * 70)
    print(f"🔄 PROBANDO MODELO: {model_path}")
    print("=" * 70)

    # Detectar algoritmo del nombre del archivo
    if "dqn" in model_path.lower():
        model = DQN.load(model_path)
    elif "ppo" in model_path.lower():
        model = PPO.load(model_path)
    elif "a2c" in model_path.lower():
        model = A2C.load(model_path)
    else:
        raise ValueError("No se pudo detectar el algoritmo del nombre del archivo")

    print("✅ Modelo cargado exitosamente")

    # Crear entorno
    env = AspiradoraEnv(render_mode="human" if render else None)

    recompensas = []
    pasos_lista = []

    for ep in range(episodios):
        print(f"\n{'='*70}")
        print(f"🎮 EPISODIO {ep + 1}/{episodios}")
        print("=" * 70)

        obs, info = env.reset()
        total_reward = 0
        done = False
        steps = 0

        while not done and steps < 100:
            # Predecir acción (SIN exploración, determinístico)
            action, _states = model.predict(obs, deterministic=True)

            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated

            if render:
                env.render()
                import time

                time.sleep(0.2)

        recompensas.append(total_reward)
        pasos_lista.append(steps)

        print(f"\n📊 Resultado: Recompensa={total_reward:.1f}, Pasos={steps}")
        print(f"   {'✅ Completó!' if info['suciedad_restante'] == 0 else '⏱️ Timeout'}")

    # Estadísticas finales
    print("\n" + "=" * 70)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 70)

    import numpy as np

    print(f"Episodios: {episodios}")
    print(f"Recompensa promedio: {np.mean(recompensas):.1f}")
    print(f"Recompensa máxima: {max(recompensas):.1f}")
    print(f"Recompensa mínima: {min(recompensas):.1f}")
    print(f"Pasos promedio: {np.mean(pasos_lista):.1f}")

    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deep RL con Stable-Baselines3")
    parser.add_argument(
        "--algoritmo", "-a", default="ppo", choices=["dqn", "ppo", "a2c"], help="Algoritmo a usar"
    )
    parser.add_argument(
        "--timesteps", "-t", type=int, default=200_000, help="Timesteps de entrenamiento"
    )
    parser.add_argument("--tamano", type=int, default=5, help="Tamaño del grid")
    parser.add_argument("--obstaculos", type=int, default=3, help="Número de obstáculos")
    parser.add_argument("--probar", "-p", type=str, help="Probar modelo guardado (ruta al .zip)")
    parser.add_argument("--episodios", "-e", type=int, default=5, help="Episodios para probar")
    parser.add_argument("--sin-render", action="store_true", help="No mostrar visualización")

    args = parser.parse_args()

    if args.probar:
        # Modo prueba
        probar_modelo_guardado(args.probar, episodios=args.episodios, render=not args.sin_render)
    else:
        # Modo entrenamiento
        entrenar_agente(
            algoritmo=args.algoritmo,
            timesteps=args.timesteps,
            tamano_grid=args.tamano,
            obstaculos=args.obstaculos,
        )
