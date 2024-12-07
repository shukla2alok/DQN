import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
import tensorflow as tf
from tensorflow.keras.losses import MeanSquaredError
from geopy.distance import geodesic

# Load the trained model with the loss function explicitly set
model = tf.keras.models.load_model(
    '../models/trained_model.h5',
    custom_objects={'mse': MeanSquaredError()}
)

# OSRM API URL
OSRM_API_URL = "http://router.project-osrm.org/route/v1/driving/"


def get_route(start_lon, start_lat, end_lon, end_lat):
    # Check if the distance between the start and end points is significant enough for routing
    distance = geodesic((start_lat, start_lon), (end_lat, end_lon)).km
    if distance < 0.1:  # if the distance is less than 100 meters
        print("The start and end points are too close. Skipping route generation.")
        return None

    # Continue with the route request
    url = f"{OSRM_API_URL}{start_lon},{start_lat};{end_lon},{end_lat}?overview=false&geometries=polyline"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Log the response to debug
        print("OSRM Response:", data)

        if 'routes' in data and len(data['routes']) > 0:
            if 'geometry' in data['routes'][0]:
                route_geometry = data['routes'][0]['geometry']
                return route_geometry
            else:
                print("No geometry found in the route data.")
        else:
            print("No valid routes found.")
    else:
        print(f"Error fetching data from OSRM API: {response.status_code}")
    return None


def decode_polyline(polyline):
    """Decode polyline string to a list of latitude, longitude points."""
    points = []
    index, lat, lng = 0, 0, 0
    while index < len(polyline):
        shift, result = 0, 0
        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat
        shift, result = 0, 0
        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng
        points.append((lat / 1e5, lng / 1e5))
    return points


def plot_routes():
    # Create the visuals directory if it doesn't exist
    src_path = "../src"
    if not os.path.exists(src_path):
        os.makedirs(src_path)

    # Load the data
    orders = pd.read_csv("../data/orders.csv")
    riders = pd.read_csv("../data/riders.csv")

    # Plot orders and riders locations
    plt.figure(figsize=(10, 8))
    plt.scatter(orders['longitude'], orders['latitude'], color='blue', label='Orders')
    plt.scatter(riders['location_lon'], riders['location_lat'], color='red', label='Riders')

    # Draw routes between each rider and their nearest order (for simplicity, using the first order and first rider)
    for i in range(min(len(orders), len(riders))):
        start_lon, start_lat = riders.iloc[i]['location_lon'], riders.iloc[i]['location_lat']
        end_lon, end_lat = orders.iloc[i]['longitude'], orders.iloc[i]['latitude']

        # Fetch route from OSRM
        route_geometry = get_route(start_lon, start_lat, end_lon, end_lat)

        if route_geometry:
            # Decode polyline geometry into lat/lon points
            route_points = decode_polyline(route_geometry)
            route_lons, route_lats = zip(*route_points)
            plt.plot(route_lons, route_lats, color='green', linewidth=2)

    # Add labels and title
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Rider and Order Distribution with Optimized Routes")
    plt.legend()

    # Save the plot in the 'src' folder
    plt.savefig(os.path.join(src_path, "rider_routes.png"))
    print(f"Route visualization saved as {os.path.join(src_path, 'rider_routes.png')}")


if __name__ == "__main__":
    plot_routes()
