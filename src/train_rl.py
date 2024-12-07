import tensorflow as tf
import numpy as np
from rl_environment import FoodDeliveryEnv

def build_dqn(input_dim, output_dim):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation="relu", input_dim=input_dim),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(output_dim, activation="linear")
    ])
    model.compile(optimizer="adam", loss="mse")
    return model

def train_dqn():
    env = FoodDeliveryEnv()
    model = build_dqn(env.observation_space.shape[0], env.action_space.n)

    episodes = 500
    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0

        while not done:
            action = np.random.randint(0, env.action_space.n)
            next_state, reward, done, _ = env.step(action)
            total_reward += reward
            state = next_state

        print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")

    model.save("../models/trained_model.h5")
    print("Model training complete and saved.")

if __name__ == "__main__":
    train_dqn()
