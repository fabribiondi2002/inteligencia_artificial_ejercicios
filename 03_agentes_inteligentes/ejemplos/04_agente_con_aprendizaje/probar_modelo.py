"""Script para probar un modelo Q-Learning guardado.

Carga la Q-table entrenada desde archivo y ejecuta episodios
sin necesidad de re-entrenar.
"""

import sys

# Necesario para que pickle pueda deserializar EstadoGrid correctamente
# cuando se guarda desde otro script
import __main__
from agente_qlearning import AgenteQLearning, EntornoGrid, EstadoGrid

__main__.EstadoGrid = EstadoGrid


def probar_modelo_guardado(
    archivo: str = "modelo_qlearning.pkl", num_episodios: int = 5, render: bool = True
) -> None:
    """Carga un modelo guardado y lo prueba.

    Parameters
    ----------
    archivo : str
        Ruta al archivo .pkl con el modelo
    num_episodios : int
        Número de episodios a ejecutar
    render : bool
        Mostrar visualización

    """
    print("=" * 70)
    print("🔄 CARGANDO MODELO ENTRENADO")
    print("=" * 70)

    # Crear agente
    agente = AgenteQLearning(EntornoGrid.ACCIONES)

    # Cargar modelo guardado
    try:
        agente.cargar_modelo(archivo)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo}'")
        print("💡 Primero entrena un modelo ejecutando: python agente_qlearning.py")
        sys.exit(1)

    print("✅ Modelo cargado exitosamente")
    print(f"📊 Estados en Q-table: {len(agente.q_table)}")
    print()

    # Crear entorno
    entorno = EntornoGrid(tamano=5, num_obstaculos=3, probabilidad_suciedad=0.3)

    # Probar en múltiples episodios
    recompensas = []
    pasos_lista = []

    for ep in range(num_episodios):
        print(f"\n{'='*70}")
        print(f"🎮 EPISODIO {ep + 1}/{num_episodios}")
        print("=" * 70)

        recompensa, pasos = agente.ejecutar_episodio(
            entorno, render=render, delay=0.2 if render else 0
        )

        recompensas.append(recompensa)
        pasos_lista.append(pasos)

    # Estadísticas finales
    print("\n" + "=" * 70)
    print("📊 ESTADÍSTICAS DE TODOS LOS EPISODIOS")
    print("=" * 70)

    import numpy as np

    print(f"Episodios ejecutados: {num_episodios}")
    print(f"Recompensa promedio: {np.mean(recompensas):.1f}")
    print(f"Recompensa máxima: {max(recompensas):.1f}")
    print(f"Recompensa mínima: {min(recompensas):.1f}")
    print(f"Pasos promedio: {np.mean(pasos_lista):.1f}")
    print()

    # Detalle por episodio
    print("Detalle por episodio:")
    for i, (r, p) in enumerate(zip(recompensas, pasos_lista, strict=False), 1):
        resultado = "✅ Completó" if r > 0 else "⏱️ Timeout"
        print(f"  Ep {i}: Recompensa={r:6.1f}, Pasos={p:3d} - {resultado}")


def continuar_entrenamiento(
    archivo: str = "modelo_qlearning.pkl", episodios_extra: int = 500
) -> None:
    """Carga un modelo y continúa entrenándolo.

    Parameters
    ----------
    archivo : str
        Ruta al modelo guardado
    episodios_extra : int
        Episodios adicionales de entrenamiento

    """
    print("=" * 70)
    print("🔄 CONTINUANDO ENTRENAMIENTO DE MODELO GUARDADO")
    print("=" * 70)

    # Crear y cargar agente
    agente = AgenteQLearning(
        EntornoGrid.ACCIONES,
        alpha=0.1,
        gamma=0.9,
        epsilon=0.3,  # Menos exploración que al inicio
        epsilon_min=0.01,
        epsilon_decay=0.995,
    )

    try:
        agente.cargar_modelo(archivo)
        print(f"✅ Modelo base cargado: {len(agente.q_table)} estados\n")
    except FileNotFoundError:
        print("⚠️  No se encontró modelo previo, entrenando desde cero\n")

    # Crear entorno
    entorno = EntornoGrid(tamano=5, num_obstaculos=3)

    # Continuar entrenamiento
    agente.entrenar(entorno, episodios=episodios_extra, verbose=True)

    # Guardar modelo mejorado
    agente.guardar_modelo("modelo_qlearning_mejorado.pkl")
    print("\n💾 Modelo mejorado guardado como 'modelo_qlearning_mejorado.pkl'")


def comparar_modelos() -> None:
    """Compara rendimiento de diferentes modelos guardados."""
    print("=" * 70)
    print("📊 COMPARACIÓN DE MODELOS")
    print("=" * 70)

    modelos = ["modelo_qlearning.pkl", "modelo_qlearning_mejorado.pkl"]

    entorno = EntornoGrid(tamano=5, num_obstaculos=3)

    for modelo in modelos:
        try:
            agente = AgenteQLearning(EntornoGrid.ACCIONES)
            agente.cargar_modelo(modelo)

            print(f"\n🔍 Probando: {modelo}")
            print(f"   Estados: {len(agente.q_table)}")

            # Probar 10 episodios
            recompensas = []
            for _ in range(10):
                r, _ = agente.ejecutar_episodio(entorno, render=False)
                recompensas.append(r)

            import numpy as np

            print(f"   Recompensa promedio: {np.mean(recompensas):.1f}")
            print(f"   Desv. estándar: {np.std(recompensas):.1f}")

        except FileNotFoundError:
            print(f"\n⚠️  {modelo} no encontrado")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Probar modelos Q-Learning guardados")
    parser.add_argument(
        "--archivo", "-f", default="modelo_qlearning.pkl", help="Archivo del modelo a cargar"
    )
    parser.add_argument(
        "--episodios", "-e", type=int, default=3, help="Número de episodios a ejecutar"
    )
    parser.add_argument("--sin-render", action="store_true", help="No mostrar visualización")
    parser.add_argument(
        "--continuar", "-c", action="store_true", help="Continuar entrenamiento del modelo"
    )
    parser.add_argument("--comparar", action="store_true", help="Comparar diferentes modelos")

    args = parser.parse_args()

    if args.comparar:
        comparar_modelos()
    elif args.continuar:
        continuar_entrenamiento(args.archivo, episodios_extra=500)
    else:
        probar_modelo_guardado(
            archivo=args.archivo, num_episodios=args.episodios, render=not args.sin_render
        )
