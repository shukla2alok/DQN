import pandas as pd
import numpy as np

def generate_synthetic_data(num_orders=100, num_riders=10):
    np.random.seed(42)
    orders_data = {
        "order_id": range(1, num_orders + 1),
        "latitude": np.random.uniform(26.50, 27.17, num_orders),
        "longitude": np.random.uniform(80.50, 81.22, num_orders),
        "prep_time": np.random.randint(5, 15, num_orders),  # minutes
        "weight": np.random.uniform(0.5, 5, num_orders),  # kg
    }

    riders_data = {
        "rider_id": range(1, num_riders + 1),
        "capacity": [20] * num_riders,  # kg
        "location_lat": np.random.uniform(26.50, 27.17, num_riders),
        "location_lon": np.random.uniform(80.50, 81.22, num_riders),
    }

    orders_df = pd.DataFrame(orders_data)
    riders_df = pd.DataFrame(riders_data)
    orders_df.to_csv("../data/orders.csv", index=False)
    riders_df.to_csv("../data/riders.csv", index=False)
    print("Synthetic data generated and saved in /data/ directory.")

if __name__ == "__main__":
    generate_synthetic_data()
