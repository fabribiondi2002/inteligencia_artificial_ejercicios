"""Entorno de aspiradora compatible con OpenAI Gym/Gymnasium.

Este entorno puede ser usado directamente con Stable-Baselines3
y cualquier otra librería de RL que siga el estándar Gym.
"""

import random

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class AspiradoraEnv(gym.Env):
    """Entorno de aspiradora compatible con Gymnasium.

    El agente debe navegar un grid y limpiar toda la suciedad,
    evitando obstáculos.

    Observation Space:
        Box con shape (grid_size * grid_size + 2,) conteniendo:
        - Grid aplanado con codificación:
          0.0 = celda vacía
          0.5 = obstáculo
          1.0 = suciedad
        - Posición X normalizada [0, 1]
        - Posición Y normalizada [0, 1]

    Action Space:
        Discrete(5):
        - 0: Arriba
        - 1: Abajo
        - 2: Izquierda
        - 3: Derecha
        - 4: Aspirar

    Rewards:
        +10: Limpiar suciedad
        -1: Movimiento
        -5: Chocar con obstáculo
        +50: Completar (limpiar todo)
    """

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self,
        tamano: int = 5,
        num_obstaculos: int = 3,
        probabilidad_suciedad: float = 0.3,
        max_steps: int = 100,
        render_mode: str | None = None,
    ):
        """Inicializa el entorno.

        Parameters
        ----------
        tamano : int
            Tamaño del grid (NxN)
        num_obstaculos : int
            Número de obstáculos
        probabilidad_suciedad : float
            Probabilidad inicial de suciedad por celda
        max_steps : int
            Máximo número de pasos por episodio
        render_mode : str, optional
            Modo de renderizado ("human" o "rgb_array")

        """
        super().__init__()

        self.tamano = tamano
        self.num_obstaculos = num_obstaculos
        self.probabilidad_suciedad = probabilidad_suciedad
        self.max_steps = max_steps
        self.render_mode = render_mode

        # Espacios de observación y acción
        obs_size = tamano * tamano + 2  # Grid + posición X,Y
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(obs_size,), dtype=np.float32)

        self.action_space = spaces.Discrete(5)

        # Estado interno
        self.grid = None
        self.posicion_agente = None
        self.obstaculos = set()
        self.suciedad = set()
        self.pasos = 0

        # Para render
        self.window = None
        self.clock = None

    def reset(
        self, seed: int | None = None, options: dict | None = None
    ) -> tuple[np.ndarray, dict]:
        """Reinicia el entorno.

        Returns
        -------
        observation : np.ndarray
            Observación inicial
        info : dict
            Información adicional

        """
        super().reset(seed=seed)

        # Posición inicial
        self.posicion_agente = (0, 0)
        self.pasos = 0

        # Generar obstáculos
        self.obstaculos = set()
        while len(self.obstaculos) < self.num_obstaculos:
            x = random.randint(0, self.tamano - 1)
            y = random.randint(0, self.tamano - 1)
            if (x, y) != self.posicion_agente:
                self.obstaculos.add((x, y))

        # Generar suciedad
        self.suciedad = set()
        for x in range(self.tamano):
            for y in range(self.tamano):
                if (x, y) not in self.obstaculos and random.random() < self.probabilidad_suciedad:
                    self.suciedad.add((x, y))

        # Construir observación
        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict]:
        """Ejecuta una acción.

        Parameters
        ----------
        action : int
            Acción a ejecutar (0-4)

        Returns
        -------
        observation : np.ndarray
            Nueva observación
        reward : float
            Recompensa recibida
        terminated : bool
            Si el episodio terminó (objetivo cumplido)
        truncated : bool
            Si el episodio fue truncado (límite de pasos)
        info : dict
            Información adicional

        """
        self.pasos += 1
        reward = 0.0
        terminated = False
        truncated = False

        if action == 4:  # ASPIRAR
            if self.posicion_agente in self.suciedad:
                self.suciedad.remove(self.posicion_agente)
                reward = 10.0

                # Bonus si completó todo
                if len(self.suciedad) == 0:
                    reward += 100.0  # Aumentado de 50 a 100
                    terminated = True
            else:
                reward = -1.0  # Penalización por aspirar celda limpia (antes 0)

        else:  # MOVIMIENTO
            x, y = self.posicion_agente
            nueva_pos = self._calcular_nueva_posicion(x, y, action)

            if self._es_posicion_valida(nueva_pos):
                self.posicion_agente = nueva_pos
                reward = -1.0  # Costo de movimiento
            else:
                # Chocó con obstáculo o pared
                reward = -5.0

        # Verificar si alcanzó límite de pasos
        if self.pasos >= self.max_steps:
            truncated = True

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def _get_obs(self) -> np.ndarray:
        """Construye la observación actual.

        Returns
        -------
        np.ndarray
            Vector de observación

        """
        # Grid codificado
        grid = np.zeros((self.tamano, self.tamano), dtype=np.float32)

        for x in range(self.tamano):
            for y in range(self.tamano):
                if (x, y) in self.obstaculos:
                    grid[y, x] = 0.5  # Obstáculo
                elif (x, y) in self.suciedad:
                    grid[y, x] = 1.0  # Suciedad

        # Aplanar grid
        grid_flat = grid.flatten()

        # Posición normalizada
        pos_x = self.posicion_agente[0] / (self.tamano - 1)
        pos_y = self.posicion_agente[1] / (self.tamano - 1)

        # Concatenar todo
        obs = np.concatenate([grid_flat, [pos_x, pos_y]])

        return obs.astype(np.float32)

    def _get_info(self) -> dict:
        """Retorna información adicional del entorno."""
        return {
            "suciedad_restante": len(self.suciedad),
            "pasos": self.pasos,
            "posicion": self.posicion_agente,
        }

    def _calcular_nueva_posicion(self, x: int, y: int, action: int) -> tuple[int, int]:
        """Calcula nueva posición según acción."""
        if action == 0:  # ARRIBA
            return (x, y - 1)
        elif action == 1:  # ABAJO
            return (x, y + 1)
        elif action == 2:  # IZQUIERDA
            return (x - 1, y)
        elif action == 3:  # DERECHA
            return (x + 1, y)
        return (x, y)

    def _es_posicion_valida(self, pos: tuple[int, int]) -> bool:
        """Verifica si una posición es válida."""
        x, y = pos
        return 0 <= x < self.tamano and 0 <= y < self.tamano and pos not in self.obstaculos

    def render(self):
        """Renderiza el entorno."""
        if self.render_mode == "human":
            self._render_text()
        elif self.render_mode == "rgb_array":
            return self._render_rgb()

    def _render_text(self):
        """Renderizado en modo texto."""
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
        print(f"Suciedad: {len(self.suciedad)} | Pasos: {self.pasos}")

    def _render_rgb(self) -> np.ndarray:
        """Renderizado como array RGB (para video)."""
        # Tamaño de celda en pixels
        cell_size = 50
        img_size = self.tamano * cell_size

        # Crear imagen RGB
        img = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255

        for x in range(self.tamano):
            for y in range(self.tamano):
                x_pixel = x * cell_size
                y_pixel = y * cell_size

                pos = (x, y)

                if pos in self.obstaculos:
                    # Negro para obstáculos
                    img[y_pixel : y_pixel + cell_size, x_pixel : x_pixel + cell_size] = [50, 50, 50]
                elif pos in self.suciedad:
                    # Marrón para suciedad
                    img[y_pixel : y_pixel + cell_size, x_pixel : x_pixel + cell_size] = [
                        139,
                        69,
                        19,
                    ]

                if pos == self.posicion_agente:
                    # Azul para agente
                    center_y = y_pixel + cell_size // 2
                    center_x = x_pixel + cell_size // 2
                    radius = cell_size // 3

                    y_coords, x_coords = np.ogrid[:img_size, :img_size]
                    mask = (x_coords - center_x) ** 2 + (y_coords - center_y) ** 2 <= radius**2
                    img[mask] = [0, 0, 255]

        return img

    def close(self):
        """Cierra el entorno."""
        if self.window is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()


if __name__ == "__main__":
    # Test del entorno
    env = AspiradoraEnv(render_mode="human")

    print("🧪 Testeando entorno...")
    print(f"Observation space: {env.observation_space}")
    print(f"Action space: {env.action_space}")

    obs, info = env.reset()
    print(f"\n📊 Observación inicial shape: {obs.shape}")
    print(f"📊 Info: {info}")

    env.render()

    print("\n🎮 Ejecutando acciones aleatorias...")
    for i in range(10):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

        print(f"\nPaso {i+1}: Acción={action}, Reward={reward:.1f}")
        env.render()

        if terminated or truncated:
            print("\n✅ Episodio terminado!")
            break

    env.close()
    print("\n✅ Test completado!")
