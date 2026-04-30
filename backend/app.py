from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import urllib3
from pymongo import MongoClient

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Connectors
from connectors.ttn_connector import get_ttn_data, start_ttn
from connectors.flownex_connector import get_flownex_data
from connectors.irriframe_connector import get_irriframe_data

# Processing
from processing.irrigation_logic import irrigation_decision
from processing.wue_calculation import calculate_wue

app = Flask(__name__)
CORS(app)

# ---------------- MongoDB ----------------
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["smart_irrigation"]
sensor_collection = db["sensor_data"]
users_collection = db["users"]

print("✅ MongoDB Connected Successfully")

# ---------------- Start TTN ----------------
try:
    start_ttn()
except:
    print("⚠️ TTN not connected")

# ---------------- Home ----------------
@app.route("/")
def home():
    return "Smart Irrigation Backend Running"

# ---------------------------------------------------
# DATA API
# ---------------------------------------------------
@app.route("/data")
def get_data():
    try:
        ttn = get_ttn_data()
        flow = get_flownex_data()

        weather = {
            "temperature": 31,
            "rainfall": 5,
            "humidity": 72
        }

        if not ttn:
            ttn = {"soil_moisture": 45, "temperature": 30}

        if not flow:
            flow = {"flow_rate": 18, "pressure": 2.5}

        irriframe = get_irriframe_data(ttn["soil_moisture"])

        decision = irrigation_decision(
            ttn["soil_moisture"], weather
        )

        wue = calculate_wue(
            2500,
            flow["flow_rate"],
            weather["rainfall"]
        )

        save_data = {
            "soil_moisture": ttn["soil_moisture"],
            "temperature": ttn["temperature"],
            "flow_rate": flow["flow_rate"],
            "pressure": flow["pressure"],
            "weather_temp": weather["temperature"],
            "rainfall": weather["rainfall"],
            "humidity": weather["humidity"],
            "decision": decision,
            "water_use_efficiency": wue,
            "time": datetime.datetime.now()
        }

        sensor_collection.insert_one(save_data)

        return jsonify({
            "status": "Success",
            "ttn": ttn,
            "flow": flow,
            "weather": weather,
            "irriframe": irriframe,
            "decision": decision,
            "water_use_efficiency": wue,
            "time": str(datetime.datetime.now())
        })

    except Exception as e:
        return jsonify({
            "status": "Error",
            "message": str(e)
        })

# ---------------------------------------------------
# HISTORY API
# ---------------------------------------------------
@app.route("/history")
def history():
    data = list(
        sensor_collection.find({}, {"_id": 0})
        .sort("time", -1)
        .limit(10)
    )
    return jsonify(data)

# ---------------------------------------------------
# LOGIN (POST)
# ---------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({
        "email": email,
        "password": password
    })

    if user:
        return jsonify({
            "status": "Success",
            "message": "Login Successful"
        })
    else:
        return jsonify({
            "status": "Failed",
            "message": "Invalid Login"
        })

# ---------------------------------------------------
# SIGNUP (POST)
# ---------------------------------------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    existing_user = users_collection.find_one({"email": email})

    if existing_user:
        return jsonify({
            "status": "Failed",
            "message": "User already exists"
        })

    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    return jsonify({
        "status": "Success",
        "message": "Signup successful"
    })

# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)