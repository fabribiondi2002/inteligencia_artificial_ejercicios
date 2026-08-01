"""Ejemplo 4: Agente con Aprendizaje por Refuerzo (Q-Learning)

Este ejemplo demuestra cómo un agente puede APRENDER la política óptima
mediante Machine Learning en lugar de reglas programadas manualmente.

Conceptos:
- Q-Learning (Reinforcement Learning)
- Exploración vs. Explotación (ε-greedy)
- Q-table (estado-acción → valor)
- Sistema de recompensas
- Entrenamiento de agentes
"""

import pickle
import random
import time
from collections import defaultdict
from dataclasses import dataclass

import numpy as np


@dataclass
class EstadoGrid:
    """Representa el estado del entorno.

    Attributes
    ----------
    posicion : Tuple[int, int]
        Posición actual (x, y)
    suciedad : set
        Conjunto de posiciones con suciedad
    obstaculos : set
        Conjunto de posiciones con obstáculos

    """

    posicion: tuple[int, int]
    suciedad: frozenset
    obstaculos: frozenset

    def __hash__(self):
        """Permite usar el estado como key en diccionario."""
        return hash((self.posicion, self.suciedad, self.obstaculos))

    def __eq__(self, otro):
        """Igualdad de estados."""
        return (
            self.posicion == otro.posicion
            and self.suciedad == otro.suciedad
            and self.obstaculos == otro.obstaculos
        )


class EntornoGrid:
    """Entorno: Grid NxN con obstáculos y suciedad.

    El agente debe navegar evitando obstáculos y limpiando suciedad.
    """

    # Acciones posibles
    ARRIBA = 0
    ABAJO = 1
    IZQUIERDA = 2
    DERECHA = 3
    ASPIRAR = 4

    ACCIONES = [ARRIBA, ABAJO, IZQUIERDA, DERECHA, ASPIRAR]
    NOMBRES_ACCIONES = {
        ARRIBA: "↑ ARRIBA",
        ABAJO: "↓ ABAJO",
        IZQUIERDA: "← IZQUIERDA",
        DERECHA: "→ DERECHA",
        ASPIRAR: "● ASPIRAR",
    }

    # Sistema de recompensas
    RECOMPENSA_LIMPIAR = 10
    RECOMPENSA_MOVIMIENTO = -1
    RECOMPENSA_OBSTACULO = -5
    RECOMPENSA_LIMPIO = 0
    RECOMPENSA_COMPLETAR = 50

    def __init__(
        self, tamano: int = 5, num_obstaculos: int = 3, probabilidad_suciedad: float = 0.3
    ):
        """Inicializa el entorno.

        Parameters
        ----------
        tamano : int
            Tamaño del grid (NxN)
        num_obstaculos : int
            Número de obstáculos aleatorios
        probabilidad_suciedad : float
            Probabilidad de que una celda tenga suciedad inicialmente

        """
        self.tamano = tamano
        self.num_obstaculos = num_obstaculos
        self.probabilidad_suciedad = probabilidad_suciedad

        self.reset()

    def reset(self) -> EstadoGrid:
        """Reinicia el entorno a un estado inicial aleatorio.

        Returns
        -------
        EstadoGrid
            Estado inicial

        """
        # Posición inicial del agente (esquina superior izquierda)
        self.posicion_agente = (0, 0)

        # Generar obstáculos aleatorios (no en posición inicial)
        self.obstaculos = set()
        while len(self.obstaculos) < self.num_obstaculos:
            x = random.randint(0, self.tamano - 1)
            y = random.randint(0, self.tamano - 1)
            if (x, y) != self.posicion_agente:
                self.obstaculos.add((x, y))

        # Generar suciedad aleatoria
        self.suciedad = set()
        for x in range(self.tamano):
            for y in range(self.tamano):
                if (x, y) not in self.obstaculos and random.random() < self.probabilidad_suciedad:
                    self.suciedad.add((x, y))

        self.pasos = 0
        self.recompensa_acumulada = 0

        return self._obtener_estado()

    def _obtener_estado(self) -> EstadoGrid:
        """Retorna el estado actual."""
        return EstadoGrid(
            posicion=self.posicion_agente,
            suciedad=frozenset(self.suciedad),
            obstaculos=frozenset(self.obstaculos),
        )

    def step(self, accion: int) -> tuple[EstadoGrid, float, bool]:
        """Ejecuta una acción en el entorno.

        Parameters
        ----------
        accion : int
            Acción a ejecutar (ARRIBA, ABAJO, etc.)

        Returns
        -------
        Tuple[EstadoGrid, float, bool]
            (nuevo_estado, recompensa, terminado)

        """
        self.pasos += 1
        recompensa = 0

        if accion == self.ASPIRAR:
            # Intentar aspirar
            if self.posicion_agente in self.suciedad:
                self.suciedad.remove(self.posicion_agente)
                recompensa = self.RECOMPENSA_LIMPIAR

                # Bonus por completar todo
                if len(self.suciedad) == 0:
                    recompensa += self.RECOMPENSA_COMPLETAR
            else:
                recompensa = self.RECOMPENSA_LIMPIO

        else:
            # Intentar moverse
            x, y = self.posicion_agente
            nueva_pos = self._calcular_nueva_posicion(x, y, accion)

            # Verificar si es válido
            if self._es_posicion_valida(nueva_pos):
                self.posicion_agente = nueva_pos
                recompensa = self.RECOMPENSA_MOVIMIENTO
            else:
                # Chocó con obstáculo o pared
                recompensa = self.RECOMPENSA_OBSTACULO

        self.recompensa_acumulada += recompensa

        # Termina si no hay más suciedad o pasaron muchos pasos
        terminado = len(self.suciedad) == 0 or self.pasos >= 100

        return self._obtener_estado(), recompensa, terminado

    def _calcular_nueva_posicion(self, x: int, y: int, accion: int) -> tuple[int, int]:
        """Calcula la nueva posición según la acción."""
        if accion == self.ARRIBA:
            return (x, y - 1)
        elif accion == self.ABAJO:
            return (x, y + 1)
        elif accion == self.IZQUIERDA:
            return (x - 1, y)
        elif accion == self.DERECHA:
            return (x + 1, y)
        return (x, y)

    def _es_posicion_valida(self, pos: tuple[int, int]) -> bool:
        """Verifica si una posición es válida."""
        x, y = pos
        # Dentro del grid y sin obstáculo
        return 0 <= x < self.tamano and 0 <= y < self.tamano and pos not in self.obstaculos

    def render(self) -> None:
        """Muestra el estado actual del entorno en consola."""
        print("\n" + "═" * (self.tamano * 4 + 1))
        for y in range(self.tamano):
            fila = "║"
            for x in range(self.tamano):
                pos = (x, y)
                if pos == self.posicion_agente:
                    fila += " 🤖"
                elif pos in self.obstaculos:
                    fila += " 🧱"
                elif pos in self.suciedad:
                    fila += " 💩"
                else:
                    fila += " · "
                fila += " "
            print(fila + "║")
        print("═" * (self.tamano * 4 + 1))
        print(
            f"Suciedad restante: {len(self.suciedad)} | Pasos: {self.pasos} | Recompensa: {self.recompensa_acumulada:.1f}"
        )


class AgenteQLearning:
    """Agente que aprende mediante Q-Learning.

    Mantiene una Q-table que mapea (estado, acción) → valor esperado.
    """

    def __init__(
        self,
        acciones: list[int],
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
    ):
        """Inicializa el agente Q-Learning.

        Parameters
        ----------
        acciones : List[int]
            Lista de acciones posibles
        alpha : float
            Learning rate (tasa de aprendizaje)
        gamma : float
            Discount factor (factor de descuento)
        epsilon : float
            Exploration rate inicial
        epsilon_min : float
            Exploration rate mínimo
        epsilon_decay : float
            Tasa de decaimiento de epsilon

        """
        self.acciones = acciones
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        # Q-table: {estado: {accion: valor}}
        self.q_table = defaultdict(lambda: defaultdict(float))

        # Estadísticas
        self.recompensas_por_episodio = []
        self.pasos_por_episodio = []

    def elegir_accion(self, estado: EstadoGrid) -> int:
        """Elige una acción usando estrategia ε-greedy.

        Parameters
        ----------
        estado : EstadoGrid
            Estado actual

        Returns
        -------
        int
            Acción elegida

        """
        # Exploración: acción aleatoria
        if random.random() < self.epsilon:
            return random.choice(self.acciones)

        # Explotación: mejor acción según Q-table
        q_values = [self.q_table[estado][a] for a in self.acciones]
        max_q = max(q_values)

        # Si hay empate, elegir aleatoriamente entre las mejores
        mejores_acciones = [a for a in self.acciones if self.q_table[estado][a] == max_q]
        return random.choice(mejores_acciones)

    def actualizar_q(
        self,
        estado: EstadoGrid,
        accion: int,
        recompensa: float,
        nuevo_estado: EstadoGrid,
        terminado: bool,
    ) -> None:
        """Actualiza la Q-table usando la ecuación de Q-Learning.

        Q(s,a) = Q(s,a) + α × [r + γ × max(Q(s',a')) - Q(s,a)]

        Parameters
        ----------
        estado : EstadoGrid
            Estado actual
        accion : int
            Acción tomada
        recompensa : float
            Recompensa recibida
        nuevo_estado : EstadoGrid
            Estado resultante
        terminado : bool
            Si el episodio terminó

        """
        q_actual = self.q_table[estado][accion]

        if terminado:
            # Si terminó, no hay valor futuro
            q_objetivo = recompensa
        else:
            # Mejor valor futuro posible
            max_q_futuro = max([self.q_table[nuevo_estado][a] for a in self.acciones])
            q_objetivo = recompensa + self.gamma * max_q_futuro

        # Actualizar Q-value
        self.q_table[estado][accion] = q_actual + self.alpha * (q_objetivo - q_actual)

    def decaer_epsilon(self) -> None:
        """Reduce epsilon (menos exploración con el tiempo)."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def entrenar(self, entorno: EntornoGrid, episodios: int = 1000, verbose: bool = True) -> None:
        """Entrena el agente durante N episodios.

        Parameters
        ----------
        entorno : EntornoGrid
            Entorno de entrenamiento
        episodios : int
            Número de episodios
        verbose : bool
            Mostrar progreso

        """
        print("=" * 70)
        print("🎓 ENTRENAMIENTO CON Q-LEARNING")
        print("=" * 70)
        print(f"Episodios: {episodios}")
        print(f"Alpha (learning rate): {self.alpha}")
        print(f"Gamma (discount): {self.gamma}")
        print(f"Epsilon: {self.epsilon} → {self.epsilon_min}")
        print("=" * 70 + "\n")

        for episodio in range(episodios):
            estado = entorno.reset()
            recompensa_total = 0
            pasos = 0
            terminado = False

            while not terminado:
                # 1. Elegir acción
                accion = self.elegir_accion(estado)

                # 2. Ejecutar acción
                nuevo_estado, recompensa, terminado = entorno.step(accion)

                # 3. Aprender (actualizar Q-table)
                self.actualizar_q(estado, accion, recompensa, nuevo_estado, terminado)

                recompensa_total += recompensa
                pasos += 1
                estado = nuevo_estado

            # Decaer epsilon
            self.decaer_epsilon()

            # Guardar estadísticas
            self.recompensas_por_episodio.append(recompensa_total)
            self.pasos_por_episodio.append(pasos)

            # Mostrar progreso
            if verbose and (episodio % 100 == 0 or episodio == episodios - 1):
                promedio_recompensa = np.mean(self.recompensas_por_episodio[-100:])
                print(
                    f"Episodio {episodio:4d} | "
                    f"Recompensa: {recompensa_total:6.1f} | "
                    f"Promedio últimos 100: {promedio_recompensa:6.1f} | "
                    f"Epsilon: {self.epsilon:.3f} | "
                    f"Q-states: {len(self.q_table)}"
                )

        print("\n" + "=" * 70)
        print("✅ ENTRENAMIENTO COMPLETADO")
        print("=" * 70)
        print(f"Estados explorados: {len(self.q_table)}")
        print(
            f"Recompensa promedio últimos 100 episodios: {np.mean(self.recompensas_por_episodio[-100:]):.1f}"
        )

    def ejecutar_episodio(
        self, entorno: EntornoGrid, render: bool = True, delay: float = 0.5
    ) -> tuple[float, int]:
        """Ejecuta un episodio usando la política aprendida (sin exploración).

        Parameters
        ----------
        entorno : EntornoGrid
            Entorno de ejecución
        render : bool
            Mostrar visualización
        delay : float
            Tiempo entre acciones (segundos)

        Returns
        -------
        Tuple[float, int]
            (recompensa_total, pasos)

        """
        estado = entorno.reset()
        recompensa_total = 0
        pasos = 0
        terminado = False

        if render:
            print("\n" + "=" * 70)
            print("🤖 EJECUTANDO POLÍTICA APRENDIDA (sin exploración)")
            print("=" * 70)
            entorno.render()

        # Guardar epsilon original
        epsilon_original = self.epsilon
        self.epsilon = 0  # Sin exploración

        while not terminado:
            # Elegir mejor acción
            accion = self.elegir_accion(estado)

            if render:
                time.sleep(delay)
                print(f"\nAcción: {EntornoGrid.NOMBRES_ACCIONES[accion]}")

            # Ejecutar
            nuevo_estado, recompensa, terminado = entorno.step(accion)
            recompensa_total += recompensa
            pasos += 1

            if render:
                entorno.render()

            estado = nuevo_estado

        # Restaurar epsilon
        self.epsilon = epsilon_original

        if render:
            print("\n" + "=" * 70)
            print(f"{'✅ COMPLETADO' if len(entorno.suciedad) == 0 else '⏱️ TIMEOUT'}")
            print(f"Recompensa total: {recompensa_total:.1f}")
            print(f"Pasos: {pasos}")
            print("=" * 70)

        return recompensa_total, pasos

    def guardar_modelo(self, ruta: str = "modelo_qlearning.pkl") -> None:
        """Guarda la Q-table en un archivo."""
        with open(ruta, "wb") as f:
            pickle.dump(dict(self.q_table), f)
        print(f"💾 Modelo guardado en '{ruta}'")

    def cargar_modelo(self, ruta: str = "modelo_qlearning.pkl") -> None:
        """Carga la Q-table desde un archivo."""
        with open(ruta, "rb") as f:
            self.q_table = defaultdict(lambda: defaultdict(float), pickle.load(f))
        print(f"📂 Modelo cargado desde '{ruta}'")


def comparar_antes_despues(entorno: EntornoGrid, agente: AgenteQLearning) -> None:
    """Compara rendimiento antes y después del entrenamiento."""
    print("\n" + "=" * 70)
    print("📊 COMPARACIÓN: ANTES vs. DESPUÉS DEL ENTRENAMIENTO")
    print("=" * 70)

    # Crear nuevo agente sin entrenar
    agente_random = AgenteQLearning(EntornoGrid.ACCIONES)
    agente_random.epsilon = 1.0  # Completamente random

    print("\n1️⃣ AGENTE SIN ENTRENAR (acciones aleatorias):")
    recompensa_random, pasos_random = agente_random.ejecutar_episodio(entorno, render=False)
    print(f"   Recompensa: {recompensa_random:.1f} | Pasos: {pasos_random}")

    print("\n2️⃣ AGENTE ENTRENADO (política aprendida):")
    recompensa_entrenado, pasos_entrenado = agente.ejecutar_episodio(entorno, render=False)
    print(f"   Recompensa: {recompensa_entrenado:.1f} | Pasos: {pasos_entrenado}")

    print("\n📈 MEJORA:")
    mejora = recompensa_entrenado - recompensa_random
    print(f"   Recompensa: +{mejora:.1f} puntos ({mejora/abs(recompensa_random)*100:.1f}% mejor)")


if __name__ == "__main__":
    # Configuración
    TAMANO_GRID = 5
    NUM_OBSTACULOS = 3
    EPISODIOS_ENTRENAMIENTO = 1000

    # Crear entorno
    entorno = EntornoGrid(
        tamano=TAMANO_GRID, num_obstaculos=NUM_OBSTACULOS, probabilidad_suciedad=0.3
    )

    # Crear agente
    agente = AgenteQLearning(
        acciones=EntornoGrid.ACCIONES,
        alpha=0.1,
        gamma=0.9,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.995,
    )

    # FASE 1: Entrenar
    agente.entrenar(entorno, episodios=EPISODIOS_ENTRENAMIENTO)

    # FASE 2: Ejecutar política aprendida
    print("\n")
    agente.ejecutar_episodio(entorno, render=True, delay=0.3)

    # FASE 3: Comparación
    comparar_antes_despues(entorno, agente)

    # Guardar modelo
    print("\n")
    agente.guardar_modelo()
