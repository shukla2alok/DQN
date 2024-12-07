import gym
from gym import spaces
import numpy as np

class FoodDeliveryEnv(gym.Env):
    def __init__(self, num_riders=5, num_orders=10):
        super(FoodDeliveryEnv, self).__init__()
        self.num_riders = num_riders
        self.num_orders = num_orders
        self.orders = np.random.rand(self.num_orders, 5)  # Dummy order features
        self.riders = np.random.rand(self.num_riders, 3)  # Dummy rider features

        # Action space: Assign orders to riders (discrete actions)
        self.action_space = spaces.Discrete(self.num_riders)

        # Observation space: order and rider status
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.num_orders + self.num_riders,), dtype=np.float32)

        self.current_order = 0
        self.state = self.reset()

    def reset(self):
        # Reset the environment to an initial state
        self.current_order = 0
        return np.concatenate((self.orders[self.current_order], self.riders.flatten()))

    def step(self, action):
        reward = self.calculate_reward(action)
        self.current_order += 1
        done = self.current_order >= self.num_orders
        next_state = np.concatenate((self.orders[self.current_order], self.riders.flatten())) if not done else None
        return next_state, reward, done, {}

    def calculate_reward(self, action):
        # Placeholder: reward logic based on distance, time, fuel cost, etc.
        distance = np.linalg.norm(self.orders[self.current_order, :2] - self.riders[action, :2])
        return -distance

    def render(self, mode="human"):
        pass
