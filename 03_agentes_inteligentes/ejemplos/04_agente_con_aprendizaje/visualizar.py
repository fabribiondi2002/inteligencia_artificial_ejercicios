"""Herramientas de visualización para el agente Q-Learning.

Genera gráficos del proceso de aprendizaje:
- Curva de aprendizaje (recompensa vs. episodio)
- Política aprendida (mapa de calor)
- Evolución de epsilon
"""

import matplotlib.pyplot as plt
import numpy as np
from agente_qlearning import AgenteQLearning, EntornoGrid, EstadoGrid


def graficar_curva_aprendizaje(agente: AgenteQLearning, guardar: bool = True) -> None:
    """Grafica la curva de aprendizaje del agente.

    Parameters
    ----------
    agente : AgenteQLearning
        Agente entrenado
    guardar : bool
        Si guardar la imagen

    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    episodios = range(len(agente.recompensas_por_episodio))
    recompensas = agente.recompensas_por_episodio

    # Gráfico 1: Recompensa por episodio
    ax1.plot(episodios, recompensas, alpha=0.3, color="blue", label="Recompensa por episodio")

    # Promedio móvil
    ventana = 50
    if len(recompensas) >= ventana:
        promedio = np.convolve(recompensas, np.ones(ventana) / ventana, mode="valid")
        ax1.plot(
            range(ventana - 1, len(recompensas)),
            promedio,
            color="red",
            linewidth=2,
            label=f"Promedio móvil ({ventana} ep.)",
        )

    ax1.set_xlabel("Episodio", fontsize=12)
    ax1.set_ylabel("Recompensa Total", fontsize=12)
    ax1.set_title("Curva de Aprendizaje - Recompensa por Episodio", fontsize=14, fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Pasos por episodio
    pasos = agente.pasos_por_episodio
    ax2.plot(episodios, pasos, alpha=0.3, color="green", label="Pasos por episodio")

    if len(pasos) >= ventana:
        promedio_pasos = np.convolve(pasos, np.ones(ventana) / ventana, mode="valid")
        ax2.plot(
            range(ventana - 1, len(pasos)),
            promedio_pasos,
            color="orange",
            linewidth=2,
            label=f"Promedio móvil ({ventana} ep.)",
        )

    ax2.set_xlabel("Episodio", fontsize=12)
    ax2.set_ylabel("Número de Pasos", fontsize=12)
    ax2.set_title("Eficiencia - Pasos por Episodio", fontsize=14, fontweight="bold")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if guardar:
        plt.savefig("curva_aprendizaje.png", dpi=300, bbox_inches="tight")
        print("📊 Gráfico guardado: 'curva_aprendizaje.png'")

    plt.show()


def graficar_politica_grid(
    agente: AgenteQLearning, entorno: EntornoGrid, guardar: bool = True
) -> None:
    """Visualiza la política aprendida en un grid.

    Muestra flechas indicando la mejor acción en cada celda.

    Parameters
    ----------
    agente : AgenteQLearning
        Agente entrenado
    entorno : EntornoGrid
        Entorno
    guardar : bool
        Si guardar la imagen

    """
    # Crear grid para visualización
    estado = entorno.reset()
    tamano = entorno.tamano

    fig, ax = plt.subplots(figsize=(10, 10))

    # Mapeo de acciones a flechas
    flechas = {
        EntornoGrid.ARRIBA: "↑",
        EntornoGrid.ABAJO: "↓",
        EntornoGrid.IZQUIERDA: "←",
        EntornoGrid.DERECHA: "→",
        EntornoGrid.ASPIRAR: "●",
    }

    # Mapeo de acciones a colores
    colores_acciones = {
        EntornoGrid.ARRIBA: "blue",
        EntornoGrid.ABAJO: "green",
        EntornoGrid.IZQUIERDA: "orange",
        EntornoGrid.DERECHA: "red",
        EntornoGrid.ASPIRAR: "purple",
    }

    # Para cada celda del grid
    for x in range(tamano):
        for y in range(tamano):
            pos = (x, y)

            # Color de fondo según tipo de celda
            if pos in entorno.obstaculos:
                ax.add_patch(plt.Rectangle((x, y), 1, 1, color="black", alpha=0.8))
                ax.text(x + 0.5, y + 0.5, "🧱", ha="center", va="center", fontsize=20)
            else:
                # Crear estado para esta posición
                estado_temp = EstadoGrid(
                    posicion=pos, suciedad=estado.suciedad, obstaculos=estado.obstaculos
                )

                # Obtener mejor acción según Q-table
                if estado_temp in agente.q_table:
                    q_values = {a: agente.q_table[estado_temp][a] for a in EntornoGrid.ACCIONES}
                    mejor_accion = max(q_values, key=q_values.get)
                    mejor_valor = q_values[mejor_accion]

                    # Color según valor Q
                    color_fondo = plt.cm.RdYlGn((mejor_valor + 10) / 20)  # Normalizar
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color_fondo, alpha=0.3))

                    # Dibujar flecha
                    ax.text(
                        x + 0.5,
                        y + 0.5,
                        flechas[mejor_accion],
                        ha="center",
                        va="center",
                        fontsize=30,
                        color=colores_acciones[mejor_accion],
                        fontweight="bold",
                    )

                    # Mostrar valor Q
                    ax.text(
                        x + 0.5,
                        y + 0.2,
                        f"{mejor_valor:.1f}",
                        ha="center",
                        va="center",
                        fontsize=8,
                        color="black",
                        alpha=0.7,
                    )
                else:
                    # Estado no explorado
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color="gray", alpha=0.2))
                    ax.text(
                        x + 0.5, y + 0.5, "?", ha="center", va="center", fontsize=20, color="gray"
                    )

    # Configuración del gráfico
    ax.set_xlim(0, tamano)
    ax.set_ylim(0, tamano)
    ax.set_aspect("equal")
    ax.invert_yaxis()  # Y crece hacia abajo
    ax.set_xticks(range(tamano + 1))
    ax.set_yticks(range(tamano + 1))
    ax.grid(True, color="black", linewidth=2)
    ax.set_title(
        "Política Aprendida - Mejor Acción por Celda", fontsize=16, fontweight="bold", pad=20
    )

    # Leyenda
    leyenda_texto = (
        "↑↓←→ = Movimiento\n"
        "● = Aspirar\n"
        "🧱 = Obstáculo\n"
        "? = No explorado\n"
        "Números = Valor Q"
    )
    ax.text(
        tamano + 0.5,
        tamano / 2,
        leyenda_texto,
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    plt.tight_layout()

    if guardar:
        plt.savefig("politica_aprendida.png", dpi=300, bbox_inches="tight")
        print("📊 Gráfico guardado: 'politica_aprendida.png'")

    plt.show()


def graficar_estadisticas_q_table(agente: AgenteQLearning, guardar: bool = True) -> None:
    """Visualiza estadísticas de la Q-table.

    Parameters
    ----------
    agente : AgenteQLearning
        Agente entrenado
    guardar : bool
        Si guardar la imagen

    """
    # Extraer todos los valores Q
    todos_q_values = []
    q_por_accion = {a: [] for a in EntornoGrid.ACCIONES}

    for estado, acciones in agente.q_table.items():
        for accion, valor in acciones.items():
            todos_q_values.append(valor)
            q_por_accion[accion].append(valor)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Gráfico 1: Distribución de valores Q
    ax1.hist(todos_q_values, bins=50, color="skyblue", edgecolor="black", alpha=0.7)
    ax1.axvline(
        np.mean(todos_q_values),
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Media: {np.mean(todos_q_values):.2f}",
    )
    ax1.set_xlabel("Valor Q", fontsize=12)
    ax1.set_ylabel("Frecuencia", fontsize=12)
    ax1.set_title("Distribución de Valores Q", fontsize=14, fontweight="bold")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Box plot por acción
    nombres_acciones = [EntornoGrid.NOMBRES_ACCIONES[a] for a in EntornoGrid.ACCIONES]
    valores_por_accion = [q_por_accion[a] for a in EntornoGrid.ACCIONES]

    bp = ax2.boxplot(valores_por_accion, labels=nombres_acciones, patch_artist=True)

    # Colorear cajas
    colores = ["lightblue", "lightgreen", "lightyellow", "lightcoral", "plum"]
    for patch, color in zip(bp["boxes"], colores, strict=False):
        patch.set_facecolor(color)

    ax2.set_ylabel("Valor Q", fontsize=12)
    ax2.set_title("Valores Q por Acción", fontsize=14, fontweight="bold")
    ax2.grid(True, alpha=0.3, axis="y")
    ax2.tick_params(axis="x", rotation=45)

    plt.tight_layout()

    if guardar:
        plt.savefig("estadisticas_qtable.png", dpi=300, bbox_inches="tight")
        print("📊 Gráfico guardado: 'estadisticas_qtable.png'")

    plt.show()


def visualizar_todo(agente: AgenteQLearning, entorno: EntornoGrid) -> None:
    """Genera todas las visualizaciones.

    Parameters
    ----------
    agente : AgenteQLearning
        Agente entrenado
    entorno : EntornoGrid
        Entorno

    """
    print("\n" + "=" * 70)
    print("📊 GENERANDO VISUALIZACIONES")
    print("=" * 70 + "\n")

    graficar_curva_aprendizaje(agente, guardar=True)
    graficar_politica_grid(agente, entorno, guardar=True)
    graficar_estadisticas_q_table(agente, guardar=True)

    print("\n" + "=" * 70)
    print("✅ Visualizaciones completadas")
    print("=" * 70)


if __name__ == "__main__":
    # Este script se puede usar de forma independiente
    from agente_qlearning import AgenteQLearning, EntornoGrid

    print("Entrenando agente para visualización...")

    entorno = EntornoGrid(tamano=5, num_obstaculos=3)
    agente = AgenteQLearning(EntornoGrid.ACCIONES)
    agente.entrenar(entorno, episodios=1000, verbose=False)

    visualizar_todo(agente, entorno)
