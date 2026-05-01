import matplotlib
matplotlib.use('Agg')   # Fix GUI thread warning

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import datetime

from connectors.ttn_connector import get_ttn_data
from connectors.flownex_connector import get_flownex_data
from connectors.weather_connector import get_weather
import matplotlib
matplotlib.use("Agg")

# Store live values
dates = []
rainfall_data = []
water_data = []
soil_data = []


def generate_irrigation_graph(data=None):
    global dates, rainfall_data, water_data, soil_data

    try:
        # Get Live Data
        ttn = get_ttn_data()
        flow = get_flownex_data()
        weather = get_weather()

        # Extract Values
        soil = ttn.get("soil_moisture", 0)
        rainfall = weather.get("rainfall", 0)
        water = flow.get("flow_rate", 0)

    except:
        soil = 0
        rainfall = 0
        water = 0

    # Append Live Data
    dates.append(datetime.datetime.now().strftime("%H:%M:%S"))
    rainfall_data.append(rainfall)
    water_data.append(water)
    soil_data.append(soil)

    # Keep last 20 values only
    dates = dates[-20:]
    rainfall_data = rainfall_data[-20:]
    water_data = water_data[-20:]
    soil_data = soil_data[-20:]

    # Create Graph
    plt.figure(figsize=(12, 6))

    # Rainfall Bar
    plt.bar(dates, rainfall_data, label="Rainfall")

    # Water Flow Line
    plt.plot(dates, water_data, marker='o', label="Water Flow")

    # Soil Moisture Line
    plt.plot(dates, soil_data, marker='o', label="Soil Moisture")

    plt.title("Live Smart Irrigation Data")
    plt.xlabel("Time")
    plt.ylabel("Sensor Values")

    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save Graph
    if not os.path.exists("static"):
        os.makedirs("static")

    plt.savefig("static/live_graph.png")
    plt.close()

    return "static/live_graph.png"