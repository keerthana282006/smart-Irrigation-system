from flask import Flask, jsonify
from flask_cors import CORS
import datetime
import urllib3

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Connectors
from connectors.ttn_connector import get_ttn_data, start_ttn
from connectors.flownex_connector import get_flownex_data
from connectors.irriframe_connector import get_irriframe_data
from connectors.weather_connector import get_weather

# Processing
from processing.irrigation_logic import irrigation_decision
from processing.wue_calculation import calculate_wue
from processing.irrigation_graph import generate_irrigation_graph
from processing.project_table import generate_project_table
from processing.novelty_engine import smart_novelty_system

app = Flask(__name__)
CORS(app)

# Backend URL
BASE_URL = "https://smart-irrigation-system-3-ny8u.onrender.com"

# Start TTN Cloud
try:
    start_ttn()
except:
    print("TTN not connected")


@app.route("/")
def home():
    return "Smart Irrigation Backend Running"


@app.route("/data")
def get_data():
    try:
        ttn = get_ttn_data()
        flow = get_flownex_data()
        weather = get_weather()

        if not ttn:
            ttn = {"soil_moisture": 45, "temperature": 30}

        if not flow:
            flow = {"flow_rate": 18, "pressure": 2.5}

        if not weather:
            weather = {
                "temperature": 31,
                "rainfall": 5,
                "humidity": 72
            }

        irriframe = get_irriframe_data(ttn.get("soil_moisture", 45))

        decision = irrigation_decision(
            ttn.get("soil_moisture", 45),
            weather
        )

        wue = calculate_wue(
            2500,
            flow.get("flow_rate", 18),
            weather.get("rainfall", 5)
        )

        novelty = smart_novelty_system(
            ttn.get("soil_moisture", 45),
            weather.get("rainfall", 5),
            weather.get("temperature", 31)
        )

        generate_irrigation_graph()
        generate_project_table()

        return jsonify({
            "status": "Success",
            "ttn": ttn,
            "flow": flow,
            "weather": weather,
            "irriframe": irriframe,
            "decision": decision,
            "water_use_efficiency": wue,
            "novelty": novelty,
            "graph": f"{BASE_URL}/static/live_graph.png",
            "table": f"{BASE_URL}/static/project_table.png",
            "time": str(datetime.datetime.now())
        })

    except Exception as e:
        return jsonify({
            "status": "Error",
            "message": str(e)
        })


@app.route("/graph")
def graph():
    generate_irrigation_graph()
    return jsonify({
        "graph": f"{BASE_URL}/static/live_graph.png"
    })


@app.route("/table")
def table():
    generate_project_table()
    return jsonify({
        "table": f"{BASE_URL}/static/project_table.png"
    })


@app.route("/novelty")
def novelty():
    result = smart_novelty_system(45, 5, 30)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)