"""Script para probar modelos Deep RL guardados.

Carga un modelo entrenado con Stable-Baselines3 y ejecuta episodios.
"""

import argparse
import time

import numpy as np
from entorno_gym import AspiradoraEnv
from stable_baselines3 import A2C, DQN, PPO


def probar_modelo(model_path: str, episodios: int = 5, render: bool = True, delay: float = 0.2):
    """Prueba un modelo guardado.

    Parameters
    ----------
    model_path : str
        Ruta al modelo (.zip)
    episodios : int
        Número de episodios a ejecutar
    render : bool
        Mostrar visualización
    delay : float
        Delay entre pasos (segundos)

    """
    print("=" * 70)
    print(f"🔄 CARGANDO MODELO: {model_path}")
    print("=" * 70)

    # Detectar algoritmo del nombre del archivo
    model_path_lower = model_path.lower()

    try:
        if "dqn" in model_path_lower:
            print("📦 Algoritmo detectado: DQN")
            model = DQN.load(model_path)
        elif "ppo" in model_path_lower:
            print("📦 Algoritmo detectado: PPO")
            model = PPO.load(model_path)
        elif "a2c" in model_path_lower:
            print("📦 Algoritmo detectado: A2C")
            model = A2C.load(model_path)
        else:
            print("⚠️  No se pudo detectar el algoritmo, intentando PPO...")
            model = PPO.load(model_path)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{model_path}.zip'")
        print("💡 Primero entrena un modelo con: python agente_deep_rl.py --algoritmo ppo")
        return

    print("✅ Modelo cargado exitosamente\n")

    # Crear entorno
    env = AspiradoraEnv(render_mode="human" if render else None)

    recompensas = []
    pasos_lista = []
    completados = 0

    for ep in range(episodios):
        print(f"\n{'='*70}")
        print(f"🎮 EPISODIO {ep + 1}/{episodios}")
        print("=" * 70)

        obs, info = env.reset()
        total_reward = 0
        done = False
        steps = 0

        if render:
            env.render()
            time.sleep(delay)

        while not done and steps < 100:
            # Predecir acción (determinístico = sin exploración)
            action, _states = model.predict(obs, deterministic=True)

            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward
            steps += 1
            done = terminated or truncated

            if render:
                print(f"\nPaso {steps}: Acción={action}, Reward={reward:.1f}")
                env.render()
                time.sleep(delay)

        recompensas.append(total_reward)
        pasos_lista.append(steps)

        if info["suciedad_restante"] == 0:
            completados += 1

        print("\n📊 Resultado:")
        print(f"   - Recompensa total: {total_reward:.1f}")
        print(f"   - Pasos: {steps}")
        print(f"   - Suciedad restante: {info['suciedad_restante']}")
        print(f"   - {'✅ Completó!' if info['suciedad_restante'] == 0 else '⏱️ Timeout'}")

    # Estadísticas finales
    print("\n" + "=" * 70)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 70)

    print("\n📈 Rendimiento:")
    print(f"   - Episodios ejecutados: {episodios}")
    print(
        f"   - Episodios completados: {completados}/{episodios} ({100*completados/episodios:.1f}%)"
    )
    print(f"   - Recompensa promedio: {np.mean(recompensas):.1f} ± {np.std(recompensas):.1f}")
    print(f"   - Recompensa máxima: {max(recompensas):.1f}")
    print(f"   - Recompensa mínima: {min(recompensas):.1f}")
    print(f"   - Pasos promedio: {np.mean(pasos_lista):.1f}")

    print("\n📋 Detalle por episodio:")
    for i, (r, p) in enumerate(zip(recompensas, pasos_lista, strict=False), 1):
        estado = "✅" if r > 0 else "⏱️"
        print(f"   Episodio {i}: Recompensa={r:6.1f}, Pasos={p:3d}  {estado}")

    env.close()

    print("\n" + "=" * 70)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Probar modelos Deep RL guardados")
    parser.add_argument("--modelo", "-m", required=True, help="Ruta al modelo guardado (sin .zip)")
    parser.add_argument(
        "--episodios", "-e", type=int, default=5, help="Número de episodios a ejecutar"
    )
    parser.add_argument("--sin-render", action="store_true", help="No mostrar visualización")
    parser.add_argument(
        "--delay", "-d", type=float, default=0.2, help="Delay entre pasos en segundos"
    )

    args = parser.parse_args()

    probar_modelo(
        model_path=args.modelo,
        episodios=args.episodios,
        render=not args.sin_render,
        delay=args.delay,
    )
