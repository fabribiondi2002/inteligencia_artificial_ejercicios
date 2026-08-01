"""Ejemplo 2: Aspiradora - Agente Reactivo Simple con Múltiples Percepciones

Este ejemplo demuestra un agente con percepciones más complejas
y múltiples acciones posibles.

Conceptos:
- Percepciones compuestas
- Múltiples acciones
- Entorno con posiciones discretas
- Limitaciones del agente reactivo simple
"""

import random
from dataclasses import dataclass
from typing import Literal


@dataclass
class Percepcion:
    """Percepción del agente aspiradora.

    Attributes
    ----------
    posicion : str
        Posición actual ('A' o 'B')
    hay_suciedad : bool
        True si hay suciedad en la posición actual

    """

    posicion: str
    hay_suciedad: bool

    def __str__(self) -> str:
        estado = "Sucio" if self.hay_suciedad else "Limpio"
        return f"Pos:{self.posicion}, {estado}"


class EntornoAspirador:
    """Entorno: Dos habitaciones que pueden estar limpias o sucias.

    El entorno mantiene el estado de las habitaciones y la posición
    de la aspiradora.
    """

    def __init__(self, habitacion_a_sucia: bool = True, habitacion_b_sucia: bool = True):
        """Inicializa el entorno.

        Parameters
        ----------
        habitacion_a_sucia : bool
            Estado inicial de habitación A
        habitacion_b_sucia : bool
            Estado inicial de habitación B

        """
        self.habitaciones = {"A": habitacion_a_sucia, "B": habitacion_b_sucia}
        self.posicion_agente = "A"
        self.acciones_ejecutadas = []
        self.historial_estados = [self._obtener_estado()]

    def _obtener_estado(self) -> str:
        """Retorna representación del estado actual."""
        a = "Sucio" if self.habitaciones["A"] else "Limpio"
        b = "Sucio" if self.habitaciones["B"] else "Limpio"
        return f"[A:{a}, B:{b}, @{self.posicion_agente}]"

    def percibir(self) -> Percepcion:
        """Retorna la percepción actual.

        Returns
        -------
        Percepcion
            Posición actual y estado de suciedad

        """
        return Percepcion(
            posicion=self.posicion_agente, hay_suciedad=self.habitaciones[self.posicion_agente]
        )

    def ejecutar_accion(self, accion: str) -> bool:
        """Ejecuta una acción en el entorno.

        Parameters
        ----------
        accion : str
            'ASPIRAR', 'DERECHA', 'IZQUIERDA', 'NADA'

        Returns
        -------
        bool
            True si la acción fue exitosa

        """
        self.acciones_ejecutadas.append(accion)

        if accion == "ASPIRAR":
            self.habitaciones[self.posicion_agente] = False
        elif accion == "DERECHA":
            if self.posicion_agente == "A":
                self.posicion_agente = "B"
        elif accion == "IZQUIERDA":
            if self.posicion_agente == "B":
                self.posicion_agente = "A"
        elif accion == "NADA":
            pass  # No hacer nada
        else:
            return False

        self.historial_estados.append(self._obtener_estado())
        return True

    def esta_limpio(self) -> bool:
        """Verifica si todas las habitaciones están limpias."""
        return not any(self.habitaciones.values())

    def ensuciar_aleatorio(self, probabilidad: float = 0.1) -> None:
        """Ensucia aleatoriamente una habitación (simula entorno dinámico).

        Parameters
        ----------
        probabilidad : float
            Probabilidad de ensuciar una habitación

        """
        for hab in self.habitaciones:
            if random.random() < probabilidad:
                self.habitaciones[hab] = True


class AspiradoraSimple:
    """Agente Reactivo Simple: Aspiradora

    Usa reglas simples basadas solo en la percepción actual.
    NO mantiene estado interno.
    """

    def __init__(self):
        """Inicializa el agente."""
        self.acciones_tomadas = 0

    def decidir_accion(
        self, percepcion: Percepcion
    ) -> Literal["ASPIRAR", "DERECHA", "IZQUIERDA", "NADA"]:
        """Decide la acción basándose en la percepción actual.

        Reglas:
        1. Si hay suciedad aquí → ASPIRAR
        2. Si estoy en A y limpio → DERECHA
        3. Si estoy en B y limpio → IZQUIERDA

        Parameters
        ----------
        percepcion : Percepcion
            Percepción actual

        Returns
        -------
        str
            Acción a realizar

        """
        self.acciones_tomadas += 1

        # Regla 1: Limpiar si hay suciedad
        if percepcion.hay_suciedad:
            return "ASPIRAR"

        # Regla 2 y 3: Moverse si está limpio
        if percepcion.posicion == "A":
            return "DERECHA"
        else:  # posicion == 'B'
            return "IZQUIERDA"


class AspiradoraMejorada:
    """Agente Reactivo Simple Mejorado: Aspiradora con sensor global

    Puede percibir el estado de TODAS las habitaciones.
    Añade regla de terminación.
    """

    def __init__(self):
        """Inicializa el agente."""
        self.acciones_tomadas = 0

    def decidir_accion(
        self, percepcion: Percepcion, estado_global: dict
    ) -> Literal["ASPIRAR", "DERECHA", "IZQUIERDA", "NADA"]:
        """Decide la acción con conocimiento global del entorno.

        Parameters
        ----------
        percepcion : Percepcion
            Percepción local
        estado_global : dict
            Estado completo de todas las habitaciones

        Returns
        -------
        str
            Acción a realizar

        """
        self.acciones_tomadas += 1

        # Regla 1: Limpiar si hay suciedad aquí
        if percepcion.hay_suciedad:
            return "ASPIRAR"

        # Regla 2: Si todo está limpio, no hacer nada
        if not any(estado_global.values()):
            return "NADA"

        # Regla 3: Ir a la habitación sucia más cercana
        if percepcion.posicion == "A" and estado_global["B"]:
            return "DERECHA"
        elif percepcion.posicion == "B" and estado_global["A"]:
            return "IZQUIERDA"

        # Si la habitación actual está limpia, explorar
        return "DERECHA" if percepcion.posicion == "A" else "IZQUIERDA"


def simular_aspiradora_simple(pasos: int = 10) -> None:
    """Simula el agente aspiradora simple.

    Parameters
    ----------
    pasos : int
        Número máximo de pasos

    """
    print("=" * 70)
    print("SIMULACIÓN: Aspiradora Reactiva Simple")
    print("=" * 70)

    entorno = EntornoAspirador(habitacion_a_sucia=True, habitacion_b_sucia=True)
    agente = AspiradoraSimple()

    print(f"Estado inicial: {entorno._obtener_estado()}\n")

    for paso in range(pasos):
        # Percibir
        percepcion = entorno.percibir()

        # Decidir
        accion = agente.decidir_accion(percepcion)

        # Actuar
        entorno.ejecutar_accion(accion)

        # Mostrar
        print(f"Paso {paso}: {percepcion} → {accion:10s} → {entorno._obtener_estado()}")

        # Verificar si terminó
        if entorno.esta_limpio():
            print(f"\n¡Todo limpio en {paso + 1} pasos!")
            break

    # Estadísticas
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS")
    print("=" * 70)
    acciones = entorno.acciones_ejecutadas
    print(f"Acciones totales: {len(acciones)}")
    print(f"  ASPIRAR: {acciones.count('ASPIRAR')}")
    print(f"  DERECHA: {acciones.count('DERECHA')}")
    print(f"  IZQUIERDA: {acciones.count('IZQUIERDA')}")


def simular_aspiradora_mejorada(pasos: int = 15) -> None:
    """Simula el agente aspiradora mejorada.

    Parameters
    ----------
    pasos : int
        Número máximo de pasos

    """
    print("\n" + "=" * 70)
    print("SIMULACIÓN: Aspiradora Mejorada (con sensor global)")
    print("=" * 70)

    entorno = EntornoAspirador(habitacion_a_sucia=True, habitacion_b_sucia=True)
    agente = AspiradoraMejorada()

    print(f"Estado inicial: {entorno._obtener_estado()}\n")

    for paso in range(pasos):
        # Percibir (con conocimiento global)
        percepcion = entorno.percibir()
        estado_global = entorno.habitaciones.copy()

        # Decidir
        accion = agente.decidir_accion(percepcion, estado_global)

        # Actuar
        entorno.ejecutar_accion(accion)

        # Mostrar
        print(f"Paso {paso}: {percepcion} → {accion:10s} → {entorno._obtener_estado()}")

        # Verificar si terminó
        if entorno.esta_limpio() and accion == "NADA":
            print(f"\n¡Completado en {paso + 1} pasos! (sin oscilación)")
            break

    # Estadísticas
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS")
    print("=" * 70)
    acciones = entorno.acciones_ejecutadas
    print(f"Acciones totales: {len(acciones)}")
    print(f"  ASPIRAR: {acciones.count('ASPIRAR')}")
    print(f"  DERECHA: {acciones.count('DERECHA')}")
    print(f"  IZQUIERDA: {acciones.count('IZQUIERDA')}")
    print(f"  NADA: {acciones.count('NADA')}")


def comparar_tabla_comportamiento() -> None:
    """Muestra tabla de comportamiento completo del agente simple."""
    print("\n" + "=" * 70)
    print("TABLA DE COMPORTAMIENTO - Aspiradora Simple")
    print("=" * 70)
    print(f"{'Estado':<25} {'Percepción':<15} {'Acción':<12} {'Resultado'}")
    print("-" * 70)

    # Todos los estados posibles
    estados = [
        (["A:Sucio", "B:Sucio", "@A"], ("A", True), "ASPIRAR", ["A:Limpio", "B:Sucio", "@A"]),
        (["A:Limpio", "B:Sucio", "@A"], ("A", False), "DERECHA", ["A:Limpio", "B:Sucio", "@B"]),
        (["A:Limpio", "B:Sucio", "@B"], ("B", True), "ASPIRAR", ["A:Limpio", "B:Limpio", "@B"]),
        (["A:Limpio", "B:Limpio", "@B"], ("B", False), "IZQUIERDA", ["A:Limpio", "B:Limpio", "@A"]),
        (["A:Limpio", "B:Limpio", "@A"], ("A", False), "DERECHA", ["A:Limpio", "B:Limpio", "@B"]),
        (["A:Sucio", "B:Limpio", "@A"], ("A", True), "ASPIRAR", ["A:Limpio", "B:Limpio", "@A"]),
        (["A:Sucio", "B:Limpio", "@B"], ("B", False), "IZQUIERDA", ["A:Sucio", "B:Limpio", "@A"]),
        (["A:Limpio", "B:Sucio", "@B"], ("B", True), "ASPIRAR", ["A:Limpio", "B:Limpio", "@B"]),
    ]

    for estado, percep, accion, resultado in estados:
        estado_str = f"[{','.join(estado)}]"
        percep_str = f"Pos:{percep[0]}, {'Sucio' if percep[1] else 'Limpio'}"
        resultado_str = f"[{','.join(resultado)}]"
        print(f"{estado_str:<25} {percep_str:<15} {accion:<12} {resultado_str}")


if __name__ == "__main__":
    # Mostrar tabla de comportamiento
    comparar_tabla_comportamiento()

    # Simular aspiradora simple
    print()
    simular_aspiradora_simple(pasos=10)

    # Simular aspiradora mejorada
    simular_aspiradora_mejorada(pasos=15)
