from rl_environment import FoodDeliveryEnv
import tensorflow as tf
import numpy as np

def evaluate_model():
    # Load the trained model
    try:
        model = tf.keras.models.load_model("../models/trained_model.h5")
    except FileNotFoundError:
        print("Trained model not found. Please run 'train_rl.py' first.")
        return

    # Initialize the environment
    env = FoodDeliveryEnv()
    state = env.reset()
    done = False
    total_reward = 0

    print("Evaluating the trained model...")
    while not done:
        # Use the model to predict the best action
        q_values = model.predict(state.reshape(1, -1), verbose=0)
        action = np.argmax(q_values)

        # Perform the action in the environment
        next_state, reward, done, _ = env.step(action)
        total_reward += reward
        state = next_state

    print(f"Total reward achieved during evaluation: {total_reward}")

if __name__ == "__main__":
    evaluate_model()
