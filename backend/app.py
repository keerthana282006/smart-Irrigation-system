from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import urllib3
from pymongo import MongoClient
import os

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

# ---------------- MongoDB SAFE CONNECTION ----------------
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    print("❌ MONGO_URI not found. Running without DB.")
    client = None
else:
    try:
        client = MongoClient(MONGO_URI)
        db = client["smart_irrigation"]
        sensor_collection = db["sensor_data"]
        users_collection = db["users"]
        print("✅ MongoDB Connected Successfully")
    except Exception as e:
        print("❌ MongoDB Connection Failed:", e)
        client = None

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
# DATA API (FULLY SAFE)
# ---------------------------------------------------
@app.route("/data")
def get_data():
    try:
        # -------- SAFE TTN --------
        try:
            ttn = get_ttn_data()
        except Exception as e:
            print("TTN Error:", e)
            ttn = None

        # -------- SAFE FLOW --------
        try:
            flow = get_flownex_data()
        except Exception as e:
            print("Flow Error:", e)
            flow = None

        # -------- WEATHER --------
        weather = {
            "temperature": 31,
            "rainfall": 5,
            "humidity": 72
        }

        # -------- DEFAULTS --------
        if not ttn:
            ttn = {"soil_moisture": 45, "temperature": 30}

        if not flow:
            flow = {"flow_rate": 18, "pressure": 2.5}

        # -------- SAFE IRRIFRAME --------
        try:
            irriframe = get_irriframe_data(ttn["soil_moisture"])
        except Exception as e:
            print("Irriframe Error:", e)
            irriframe = {"status": "default"}

        # -------- LOGIC --------
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

        # -------- SAVE ONLY IF DB --------
        if client:
            try:
                sensor_collection.insert_one(save_data)
            except Exception as e:
                print("DB Insert Error:", e)

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
        print("CRASH:", e)
        return jsonify({
            "status": "Error",
            "message": str(e)
        })

# ---------------------------------------------------
# HISTORY API
# ---------------------------------------------------
@app.route("/history")
def history():
    if not client:
        return jsonify([])

    try:
        data = list(
            sensor_collection.find({}, {"_id": 0})
            .sort("time", -1)
            .limit(10)
        )
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    if not client:
        return jsonify({"status": "Error", "message": "Database not connected"})

    data = request.get_json()

    try:
        user = users_collection.find_one({
            "email": data.get("email"),
            "password": data.get("password")
        })

        if user:
            return jsonify({"status": "Success"})
        else:
            return jsonify({"status": "Failed"})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

# ---------------------------------------------------
# SIGNUP
# ---------------------------------------------------
@app.route("/signup", methods=["POST"])
def signup():
    if not client:
        return jsonify({"status": "Error", "message": "Database not connected"})

    data = request.get_json()

    try:
        existing_user = users_collection.find_one({"email": data.get("email")})

        if existing_user:
            return jsonify({"status": "Failed", "message": "User exists"})

        users_collection.insert_one({
            "name": data.get("name"),
            "email": data.get("email"),
            "password": data.get("password")
        })

        return jsonify({"status": "Success"})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

# ---------------------------------------------------
# RUN SERVER (RENDER SAFE)
# ---------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)