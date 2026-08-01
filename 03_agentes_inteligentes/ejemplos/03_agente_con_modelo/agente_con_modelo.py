"""Ejemplo 3: Agente con Modelo del Mundo - Estado Interno

Este ejemplo demuestra un agente basado en modelos que mantiene
un estado interno para superar las limitaciones del agente reactivo simple.

Conceptos:
- Estado interno (memoria)
- Modelo del mundo
- Actualización de creencias
- Planificación básica
- Detección de terminación
"""

import random
from dataclasses import dataclass, field
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


@dataclass
class EstadoInterno:
    """Estado interno del agente - Modelo del mundo.

    Este es el "modelo" que el agente mantiene sobre el entorno.
    Se actualiza con cada percepción.

    Attributes
    ----------
    habitaciones_visitadas : Set[str]
        Conjunto de habitaciones que el agente ha visitado
    habitaciones_limpias : Set[str]
        Conjunto de habitaciones que el agente cree que están limpias
    posicion_actual : str
        Posición que el agente cree que tiene
    acciones_realizadas : List[str]
        Historial de acciones que el agente ha realizado
    habitaciones_conocidas : Set[str]
        Todas las habitaciones que el agente conoce

    """

    habitaciones_visitadas: set[str] = field(default_factory=set)
    habitaciones_limpias: set[str] = field(default_factory=set)
    posicion_actual: str = "A"
    acciones_realizadas: list[str] = field(default_factory=list)
    habitaciones_conocidas: set[str] = field(default_factory=lambda: {"A", "B"})

    def __str__(self) -> str:
        """Representación legible del estado interno."""
        visitadas = (
            ",".join(sorted(self.habitaciones_visitadas))
            if self.habitaciones_visitadas
            else "ninguna"
        )
        limpias = (
            ",".join(sorted(self.habitaciones_limpias)) if self.habitaciones_limpias else "ninguna"
        )
        return f"Visitadas={{{visitadas}}}, Limpias={{{limpias}}}"


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


class AspiradoraConModelo:
    """Agente Basado en Modelo: Aspiradora con estado interno

    Mantiene un modelo del mundo y toma decisiones basándose en:
    - Percepción actual
    - Estado interno (modelo del mundo)
    - Historial de acciones

    Este agente supera las limitaciones del agente reactivo simple.
    """

    def __init__(self):
        """Inicializa el agente con un modelo del mundo vacío."""
        self.estado = EstadoInterno()
        self.acciones_tomadas = 0

    def actualizar_modelo(self, percepcion: Percepcion) -> None:
        """Actualiza el modelo interno basándose en la percepción actual.

        Esta es la parte clave: el agente integra nueva información
        en su modelo del mundo.

        Parameters
        ----------
        percepcion : Percepcion
            Percepción actual del entorno

        """
        # Actualizar posición creída
        self.estado.posicion_actual = percepcion.posicion

        # Marcar habitación como visitada
        self.estado.habitaciones_visitadas.add(percepcion.posicion)

        # Actualizar creencia sobre limpieza
        if not percepcion.hay_suciedad:
            # Si no hay suciedad, marcar como limpia
            self.estado.habitaciones_limpias.add(percepcion.posicion)
        else:
            # Si hay suciedad, remover de limpias (si estaba)
            self.estado.habitaciones_limpias.discard(percepcion.posicion)

    def todo_limpio(self) -> bool:
        """Verifica si el agente cree que todo está limpio.

        Returns
        -------
        bool
            True si todas las habitaciones conocidas están limpias

        """
        return self.estado.habitaciones_limpias == self.estado.habitaciones_conocidas

    def hay_habitaciones_sin_visitar(self) -> bool:
        """Verifica si hay habitaciones que no se han visitado aún.

        Returns
        -------
        bool
            True si existen habitaciones no visitadas

        """
        return len(self.estado.habitaciones_visitadas) < len(self.estado.habitaciones_conocidas)

    def obtener_habitacion_no_visitada(self) -> str | None:
        """Retorna una habitación que no se ha visitado.

        Returns
        -------
        str | None
            Nombre de habitación o None si todas están visitadas

        """
        no_visitadas = self.estado.habitaciones_conocidas - self.estado.habitaciones_visitadas
        return next(iter(no_visitadas)) if no_visitadas else None

    def planificar_movimiento(self) -> Literal["DERECHA", "IZQUIERDA", "NADA"]:
        """Planifica el siguiente movimiento basándose en el modelo.

        Este método demuestra razonamiento simple:
        - Si hay habitaciones sin visitar, ir a ellas
        - Si hay habitaciones sucias conocidas, ir a ellas
        - Si todo está limpio, no moverse

        Returns
        -------
        str
            Acción de movimiento a realizar

        """
        # Si hay habitaciones sin visitar, ir a ellas
        if self.hay_habitaciones_sin_visitar():
            destino = self.obtener_habitacion_no_visitada()
            if destino:
                return self._mover_hacia(destino)

        # Buscar habitaciones que creemos que están sucias
        habitaciones_sucias = self.estado.habitaciones_conocidas - self.estado.habitaciones_limpias

        if habitaciones_sucias:
            # Ir a la habitación sucia más cercana
            destino = next(iter(habitaciones_sucias))
            return self._mover_hacia(destino)

        # Si todo está limpio, no moverse
        return "NADA"

    def _mover_hacia(self, destino: str) -> Literal["DERECHA", "IZQUIERDA"]:
        """Determina el movimiento necesario para llegar al destino.

        Parameters
        ----------
        destino : str
            Habitación destino

        Returns
        -------
        str
            'DERECHA' o 'IZQUIERDA'

        """
        if self.estado.posicion_actual == "A" and destino == "B":
            return "DERECHA"
        elif self.estado.posicion_actual == "B" and destino == "A":
            return "IZQUIERDA"
        else:
            # Ya estamos en el destino o no hay movimiento
            return "NADA"

    def decidir_accion(
        self, percepcion: Percepcion
    ) -> Literal["ASPIRAR", "DERECHA", "IZQUIERDA", "NADA"]:
        """Decide la acción basándose en el modelo interno.

        Flujo de decisión:
        1. Actualizar modelo con nueva percepción
        2. Si hay suciedad aquí → ASPIRAR
        3. Si todo está limpio → NADA
        4. Si hay trabajo por hacer → Planificar movimiento

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

        # PASO 1: Actualizar modelo del mundo
        self.actualizar_modelo(percepcion)

        # PASO 2: Regla 1 - Si hay suciedad, limpiar inmediatamente
        if percepcion.hay_suciedad:
            accion = "ASPIRAR"
            self.estado.acciones_realizadas.append(accion)
            return accion

        # PASO 3: Regla 2 - Si todo está limpio, detenerse
        if self.todo_limpio():
            accion = "NADA"
            self.estado.acciones_realizadas.append(accion)
            return accion

        # PASO 4: Regla 3 - Planificar movimiento basándose en el modelo
        accion = self.planificar_movimiento()
        self.estado.acciones_realizadas.append(accion)
        return accion


class AspiradoraConModeloDinamico:
    """Variante avanzada: Agente que maneja entornos dinámicos.

    Añade capacidad de re-visitar habitaciones periódicamente
    para detectar cambios en el entorno.
    """

    def __init__(self, ciclos_re_visita: int = 5):
        """Inicializa el agente.

        Parameters
        ----------
        ciclos_re_visita : int
            Cada cuántos pasos debe re-visitar habitaciones

        """
        self.estado = EstadoInterno()
        self.acciones_tomadas = 0
        self.ciclos_re_visita = ciclos_re_visita
        self.ultima_visita = {"A": 0, "B": 0}

    def actualizar_modelo(self, percepcion: Percepcion) -> None:
        """Actualiza modelo y registro de visitas."""
        self.estado.posicion_actual = percepcion.posicion
        self.estado.habitaciones_visitadas.add(percepcion.posicion)
        self.ultima_visita[percepcion.posicion] = self.acciones_tomadas

        if not percepcion.hay_suciedad:
            self.estado.habitaciones_limpias.add(percepcion.posicion)
        else:
            self.estado.habitaciones_limpias.discard(percepcion.posicion)

    def necesita_re_visita(self, habitacion: str) -> bool:
        """Verifica si una habitación necesita ser re-visitada."""
        pasos_desde_ultima = self.acciones_tomadas - self.ultima_visita.get(habitacion, 0)
        return pasos_desde_ultima >= self.ciclos_re_visita

    def decidir_accion(
        self, percepcion: Percepcion
    ) -> Literal["ASPIRAR", "DERECHA", "IZQUIERDA", "NADA"]:
        """Decide acción considerando re-visitas."""
        self.acciones_tomadas += 1
        self.actualizar_modelo(percepcion)

        if percepcion.hay_suciedad:
            return "ASPIRAR"

        # Verificar si hay habitaciones que necesitan re-visita
        for hab in self.estado.habitaciones_conocidas:
            if self.necesita_re_visita(hab):
                if hab != self.estado.posicion_actual:
                    return "DERECHA" if self.estado.posicion_actual == "A" else "IZQUIERDA"

        # Comportamiento normal
        if self.estado.habitaciones_limpias == self.estado.habitaciones_conocidas:
            return "NADA"

        return "DERECHA" if self.estado.posicion_actual == "A" else "IZQUIERDA"


def simular_agente_con_modelo(pasos: int = 10) -> None:
    """Simula el agente con modelo del mundo.

    Parameters
    ----------
    pasos : int
        Número máximo de pasos

    """
    print("=" * 70)
    print("SIMULACIÓN: Aspiradora con Modelo del Mundo")
    print("=" * 70)

    entorno = EntornoAspirador(habitacion_a_sucia=True, habitacion_b_sucia=True)
    agente = AspiradoraConModelo()

    print(f"Estado inicial: {entorno._obtener_estado()}\n")

    for paso in range(pasos):
        # Percibir
        percepcion = entorno.percibir()

        # Decidir (incluye actualización del modelo)
        accion = agente.decidir_accion(percepcion)

        # Actuar
        entorno.ejecutar_accion(accion)

        # Mostrar
        print(f"Paso {paso}: {percepcion} → {accion:10s} → {entorno._obtener_estado()}")
        print(f"  Modelo: {agente.estado}")

        # Verificar si terminó
        if entorno.esta_limpio() and accion == "NADA":
            print(f"\n✅ ¡Completado en {paso + 1} pasos! (agente se detuvo correctamente)")
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


def simular_entorno_dinamico(pasos: int = 20) -> None:
    """Simula el agente en un entorno dinámico que se ensucia aleatoriamente.

    Parameters
    ----------
    pasos : int
        Número máximo de pasos

    """
    print("\n" + "=" * 70)
    print("SIMULACIÓN: Entorno Dinámico (se ensucia aleatoriamente)")
    print("=" * 70)

    entorno = EntornoAspirador(habitacion_a_sucia=True, habitacion_b_sucia=False)
    agente = AspiradoraConModeloDinamico(ciclos_re_visita=5)

    print(f"Estado inicial: {entorno._obtener_estado()}\n")

    for paso in range(pasos):
        # Ensucia aleatoriamente (simula entorno dinámico)
        if paso > 0 and paso % 4 == 0:
            entorno.ensuciar_aleatorio(probabilidad=0.5)
            print("  ⚠️  Entorno cambió!")

        # Percibir
        percepcion = entorno.percibir()

        # Decidir
        accion = agente.decidir_accion(percepcion)

        # Actuar
        entorno.ejecutar_accion(accion)

        # Mostrar
        print(f"Paso {paso}: {percepcion} → {accion:10s} → {entorno._obtener_estado()}")

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


def comparar_agentes() -> None:
    """Compara el rendimiento del agente simple vs. con modelo."""
    print("\n" + "=" * 70)
    print("COMPARACIÓN: Agente Simple vs. Con Modelo")
    print("=" * 70)

    # Importar agente simple del ejemplo anterior (simulado)
    print("\n1. AGENTE REACTIVO SIMPLE:")
    print("   - Oscila infinitamente entre A y B después de limpiar")
    print("   - ~10+ acciones sin detenerse")
    print("   - No recuerda qué habitaciones limpió")

    print("\n2. AGENTE CON MODELO:")
    print("   - Se detiene cuando todo está limpio")
    print("   - 4 acciones exactas")
    print("   - Mantiene modelo del mundo")

    print("\n3. CONCLUSIÓN:")
    print("   ✅ El agente con modelo es MÁS EFICIENTE")
    print("   ✅ El agente con modelo es MÁS RACIONAL")
    print("   ✅ El agente con modelo es MÁS ROBUSTO")


if __name__ == "__main__":
    # Simulación básica
    simular_agente_con_modelo(pasos=10)

    # Simulación con entorno dinámico
    simular_entorno_dinamico(pasos=20)

    # Comparación
    comparar_agentes()
