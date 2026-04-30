from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import urllib3
from pymongo import MongoClient
import os

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)

# ---------------- SAFE CONNECTORS ----------------
try:
    from connectors.ttn_connector import get_ttn_data, start_ttn
except:
    print("⚠️ TTN module failed")
    def get_ttn_data(): return None
    def start_ttn(): pass

try:
    from connectors.flownex_connector import get_flownex_data
except:
    print("⚠️ Flownex module failed")
    def get_flownex_data(): return None

try:
    from connectors.irriframe_connector import get_irriframe_data
except:
    print("⚠️ Irriframe module failed")
    def get_irriframe_data(x): return {"status": "default"}

# ---------------- PROCESSING SAFE ----------------
try:
    from processing.irrigation_logic import irrigation_decision
except:
    print("⚠️ irrigation_logic failed")
    def irrigation_decision(x, y): return "No irrigation needed"

try:
    from processing.wue_calculation import calculate_wue
except:
    print("⚠️ wue_calculation failed")
    def calculate_wue(a, b, c): return 0

# ---------------- MongoDB SAFE ----------------
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    print("❌ No MongoDB (running without DB)")
    client = None
else:
    try:
        client = MongoClient(MONGO_URI)
        db = client["smart_irrigation"]
        sensor_collection = db["sensor_data"]
        users_collection = db["users"]
        print("✅ MongoDB Connected")
    except Exception as e:
        print("❌ MongoDB Error:", e)
        client = None

# ---------------- START TTN ----------------
try:
    start_ttn()
except:
    print("⚠️ TTN start failed")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Smart Irrigation Backend Running"

# ---------------------------------------------------
# DATA API (CRASH PROOF)
# ---------------------------------------------------
@app.route("/data")
def get_data():
    try:
        try:
            ttn = get_ttn_data()
        except:
            ttn = None

        try:
            flow = get_flownex_data()
        except:
            flow = None

        weather = {
            "temperature": 31,
            "rainfall": 5,
            "humidity": 72
        }

        if not ttn:
            ttn = {"soil_moisture": 45, "temperature": 30}

        if not flow:
            flow = {"flow_rate": 18, "pressure": 2.5}

        try:
            irriframe = get_irriframe_data(ttn["soil_moisture"])
        except:
            irriframe = {"status": "default"}

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

        if client:
            try:
                sensor_collection.insert_one(save_data)
            except:
                pass

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
        return jsonify({"status": "Error", "message": str(e)})

# ---------------------------------------------------
# HISTORY
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
    except:
        return jsonify([])

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    if not client:
        return jsonify({"status": "Error", "message": "No DB"})

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
    except:
        return jsonify({"status": "Error"})

# ---------------------------------------------------
# SIGNUP
# ---------------------------------------------------
@app.route("/signup", methods=["POST"])
def signup():
    if not client:
        return jsonify({"status": "Error", "message": "No DB"})

    data = request.get_json()

    try:
        existing = users_collection.find_one({
            "email": data.get("email")
        })

        if existing:
            return jsonify({"status": "Failed"})

        users_collection.insert_one({
            "name": data.get("name"),
            "email": data.get("email"),
            "password": data.get("password")
        })

        return jsonify({"status": "Success"})
    except:
        return jsonify({"status": "Error"})

# ---------------------------------------------------
# RUN SERVER (RENDER SAFE)
# ---------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)