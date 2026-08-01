import gymnasium as gym

env = gym.make("MountainCar-v0", render_mode="human")
obs, info = env.reset(seed=0)

terminated = truncated = False
while not (terminated or truncated):
    action = 2  # empuja a la derecha
    obs, reward, terminated, truncated, info = env.step(action)

env.close()
