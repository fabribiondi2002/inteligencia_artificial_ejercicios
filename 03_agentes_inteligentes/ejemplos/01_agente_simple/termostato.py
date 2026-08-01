"""Ejemplo 1: Termostato - Agente Reactivo Simple

Este ejemplo demuestra un agente reactivo simple que mantiene
la temperatura de una habitación usando reglas básicas.

Conceptos:
- Agente reactivo simple
- Percepciones y acciones
- Reglas condición-acción
- Análisis PEAS
"""

import random
from typing import Literal


class Habitacion:
    """Entorno: Habitación con temperatura variable.

    La temperatura cambia según las acciones del termostato y
    tiende naturalmente hacia la temperatura ambiente.
    """

    def __init__(self, temperatura_inicial: float = 15.0, temperatura_ambiente: float = 18.0):
        """Inicializa la habitación.

        Parameters
        ----------
        temperatura_inicial : float
            Temperatura inicial de la habitación
        temperatura_ambiente : float
            Temperatura ambiente exterior (a la que tiende naturalmente)

        """
        self.temperatura = temperatura_inicial
        self.temperatura_ambiente = temperatura_ambiente
        self.historial_temperatura = [temperatura_inicial]
        self.historial_acciones = []

    def actualizar(self, accion: str) -> None:
        """Actualiza la temperatura según la acción del termostato.

        Parameters
        ----------
        accion : str
            'HEAT': aumenta temperatura +1°C
            'COOL': disminuye temperatura -1°C
            'OFF': temperatura tiende al ambiente

        """
        if accion == "HEAT":
            self.temperatura += 1.0
        elif accion == "COOL":
            self.temperatura -= 1.0
        elif accion == "OFF":
            # Tiende gradualmente a la temperatura ambiente
            diferencia = self.temperatura_ambiente - self.temperatura
            self.temperatura += diferencia * 0.1  # 10% hacia ambiente

        # Añadir pequeño ruido aleatorio (simulando apertura de puertas, etc.)
        self.temperatura += random.uniform(-0.2, 0.2)

        # Registrar historial
        self.historial_temperatura.append(self.temperatura)
        self.historial_acciones.append(accion)

    def obtener_temperatura(self) -> float:
        """Retorna la temperatura actual."""
        return self.temperatura


class TermostatoSimple:
    """Agente Reactivo Simple: Termostato

    Mantiene la temperatura en un rango confortable usando reglas simples.
    No mantiene estado interno - solo reacciona a la percepción actual.
    """

    def __init__(self, temp_min: float = 20.0, temp_max: float = 22.0):
        """Inicializa el termostato.

        Parameters
        ----------
        temp_min : float
            Temperatura mínima deseada
        temp_max : float
            Temperatura máxima deseada

        """
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.decisiones_tomadas = 0

    def percibir(self, entorno: Habitacion) -> float:
        """Percibe la temperatura actual del entorno.

        Parameters
        ----------
        entorno : Habitacion
            El entorno a percibir

        Returns
        -------
        float
            Temperatura actual

        """
        return entorno.obtener_temperatura()

    def decidir_accion(self, temperatura: float) -> Literal["HEAT", "COOL", "OFF"]:
        """Decide la acción basándose en la temperatura actual.

        Reglas:
        - Si T < T_min → HEAT (calentar)
        - Si T > T_max → COOL (enfriar)
        - Si T_min ≤ T ≤ T_max → OFF (apagar)

        Parameters
        ----------
        temperatura : float
            Temperatura percibida

        Returns
        -------
        str
            Acción a realizar

        """
        self.decisiones_tomadas += 1

        if temperatura < self.temp_min:
            return "HEAT"
        elif temperatura > self.temp_max:
            return "COOL"
        else:
            return "OFF"

    def actuar(self, entorno: Habitacion, accion: str) -> None:
        """Ejecuta la acción en el entorno.

        Parameters
        ----------
        entorno : Habitacion
            Entorno donde actuar
        accion : str
            Acción a ejecutar

        """
        entorno.actualizar(accion)


def simular_termostato(pasos: int = 50, temp_inicial: float = 15.0, mostrar_cada: int = 5) -> None:
    """Simula el funcionamiento del termostato.

    Parameters
    ----------
    pasos : int
        Número de pasos de simulación
    temp_inicial : float
        Temperatura inicial de la habitación
    mostrar_cada : int
        Mostrar estado cada N pasos

    """
    # Crear entorno y agente
    habitacion = Habitacion(temperatura_inicial=temp_inicial)
    termostato = TermostatoSimple(temp_min=20.0, temp_max=22.0)

    print("=" * 60)
    print("SIMULACIÓN: Termostato Reactivo Simple")
    print("=" * 60)
    print("Objetivo: Mantener temperatura entre 20-22°C")
    print(f"Temperatura inicial: {temp_inicial}°C")
    print(f"Temperatura ambiente: {habitacion.temperatura_ambiente}°C")
    print("=" * 60)

    # Ciclo de simulación
    for paso in range(pasos):
        # 1. PERCIBIR
        temp_actual = termostato.percibir(habitacion)

        # 2. DECIDIR
        accion = termostato.decidir_accion(temp_actual)

        # 3. ACTUAR
        termostato.actuar(habitacion, accion)

        # Mostrar estado
        if paso % mostrar_cada == 0:
            print(f"Paso {paso:3d}: T={temp_actual:5.2f}°C → " f"Acción: {accion:4s}")

    # Estadísticas finales
    print("=" * 60)
    print("ESTADÍSTICAS FINALES")
    print("=" * 60)

    temperaturas = habitacion.historial_temperatura
    acciones = habitacion.historial_acciones

    temp_promedio = sum(temperaturas) / len(temperaturas)
    temp_min_alcanzada = min(temperaturas)
    temp_max_alcanzada = max(temperaturas)

    # Contar acciones
    num_heat = acciones.count("HEAT")
    num_cool = acciones.count("COOL")
    num_off = acciones.count("OFF")

    # Tiempo en rango objetivo
    en_rango = sum(1 for t in temperaturas if 20.0 <= t <= 22.0)
    porcentaje_en_rango = (en_rango / len(temperaturas)) * 100

    print(f"Temperatura promedio: {temp_promedio:.2f}°C")
    print(f"Rango alcanzado: [{temp_min_alcanzada:.2f}, {temp_max_alcanzada:.2f}]°C")
    print(f"Tiempo en rango objetivo: {porcentaje_en_rango:.1f}%")
    print("\nAcciones tomadas:")
    print(f"  HEAT (calentar): {num_heat}")
    print(f"  COOL (enfriar):  {num_cool}")
    print(f"  OFF (apagar):    {num_off}")
    print(f"  Total:           {len(acciones)}")


def demo_reglas() -> None:
    """Demuestra las reglas del termostato con diferentes temperaturas."""
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN DE REGLAS")
    print("=" * 60)

    termostato = TermostatoSimple(temp_min=20.0, temp_max=22.0)

    temperaturas_prueba = [15.0, 18.0, 20.0, 21.0, 22.0, 25.0, 28.0]

    print("Objetivo: Mantener entre 20-22°C\n")
    for temp in temperaturas_prueba:
        accion = termostato.decidir_accion(temp)
        print(f"Temperatura: {temp:5.1f}°C → Acción: {accion}")


if __name__ == "__main__":
    # Demostrar reglas
    demo_reglas()

    # Ejecutar simulación
    print()
    simular_termostato(pasos=50, temp_inicial=15.0, mostrar_cada=5)

    # Experimento adicional
    print("\n" + "=" * 60)
    print("EXPERIMENTO: Inicio con temperatura muy alta")
    print("=" * 60)
    simular_termostato(pasos=50, temp_inicial=30.0, mostrar_cada=5)
