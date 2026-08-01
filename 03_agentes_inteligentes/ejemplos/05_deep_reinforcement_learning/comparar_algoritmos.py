"""Compara diferentes algoritmos de Deep RL en el mismo entorno.

Entrena y evalúa DQN, PPO y A2C para ver cuál funciona mejor.
"""

import time

import matplotlib.pyplot as plt
from entorno_gym import AspiradoraEnv
from stable_baselines3 import A2C, DQN, PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor


def entrenar_y_evaluar(algoritmo_nombre: str, timesteps: int = 30_000):
    """Entrena y evalúa un algoritmo."""
    print(f"\n{'='*70}")
    print(f"🤖 Entrenando {algoritmo_nombre}...")
    print("=" * 70)

    # Crear entorno
    env = Monitor(AspiradoraEnv())

    # Crear modelo según algoritmo
    if algoritmo_nombre == "DQN":
        model = DQN("MlpPolicy", env, verbose=0)
    elif algoritmo_nombre == "PPO":
        model = PPO("MlpPolicy", env, verbose=0)
    elif algoritmo_nombre == "A2C":
        model = A2C("MlpPolicy", env, verbose=0)

    # Entrenar con medición de tiempo
    start_time = time.time()
    model.learn(total_timesteps=timesteps, progress_bar=True)
    training_time = time.time() - start_time

    # Evaluar
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=20, deterministic=True)

    env.close()

    return {
        "algoritmo": algoritmo_nombre,
        "mean_reward": mean_reward,
        "std_reward": std_reward,
        "training_time": training_time,
    }


def comparar_todos(timesteps: int = 30_000):
    """Compara todos los algoritmos."""
    print("=" * 70)
    print("🏆 COMPARACIÓN DE ALGORITMOS")
    print("=" * 70)
    print(f"Timesteps por algoritmo: {timesteps:,}")
    print()

    algoritmos = ["DQN", "PPO", "A2C"]
    resultados = []

    for algo in algoritmos:
        resultado = entrenar_y_evaluar(algo, timesteps)
        resultados.append(resultado)

        print(f"\n✅ {algo} completado:")
        print(f"   Recompensa: {resultado['mean_reward']:.2f} ± {resultado['std_reward']:.2f}")
        print(f"   Tiempo: {resultado['training_time']:.1f}s")

    # Mostrar tabla comparativa
    print("\n" + "=" * 70)
    print("📊 TABLA COMPARATIVA")
    print("=" * 70)
    print(f"{'Algoritmo':<12} {'Recompensa':<20} {'Tiempo (s)':<12} {'Ganador'}")
    print("-" * 70)

    mejor_reward = max(r["mean_reward"] for r in resultados)

    for r in resultados:
        es_mejor = "🏆" if r["mean_reward"] == mejor_reward else ""
        print(
            f"{r['algoritmo']:<12} {r['mean_reward']:>6.2f} ± {r['std_reward']:<8.2f} "
            f"{r['training_time']:>10.1f}  {es_mejor}"
        )

    # Graficar
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico 1: Recompensas
    nombres = [r["algoritmo"] for r in resultados]
    rewards = [r["mean_reward"] for r in resultados]
    stds = [r["std_reward"] for r in resultados]

    ax1.bar(nombres, rewards, yerr=stds, capsize=5, alpha=0.7)
    ax1.set_ylabel("Recompensa Promedio")
    ax1.set_title("Rendimiento por Algoritmo")
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Tiempo
    tiempos = [r["training_time"] for r in resultados]
    ax2.bar(nombres, tiempos, alpha=0.7, color="orange")
    ax2.set_ylabel("Tiempo de Entrenamiento (s)")
    ax2.set_title("Eficiencia de Entrenamiento")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("comparacion_algoritmos.png", dpi=300, bbox_inches="tight")
    print("\n📊 Gráfico guardado: comparacion_algoritmos.png")
    plt.show()

    # Recomendación
    print("\n" + "=" * 70)
    print("💡 RECOMENDACIÓN")
    print("=" * 70)

    mejor = max(resultados, key=lambda x: x["mean_reward"])
    mas_rapido = min(resultados, key=lambda x: x["training_time"])

    print(
        f"🏆 Mejor rendimiento: {mejor['algoritmo']} "
        f"({mejor['mean_reward']:.2f} ± {mejor['std_reward']:.2f})"
    )
    print(f"⚡ Más rápido: {mas_rapido['algoritmo']} " f"({mas_rapido['training_time']:.1f}s)")

    if mejor["algoritmo"] == mas_rapido["algoritmo"]:
        print(f"\n✨ {mejor['algoritmo']} es el CLARO GANADOR (mejor y más rápido)")
    else:
        print(
            f"\n💭 {mejor['algoritmo']} para máximo rendimiento, "
            f"{mas_rapido['algoritmo']} para rapidez"
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Comparar algoritmos de Deep RL")
    parser.add_argument(
        "--timesteps", "-t", type=int, default=30_000, help="Timesteps por algoritmo"
    )

    args = parser.parse_args()

    comparar_todos(timesteps=args.timesteps)
