from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import urllib3
import certifi

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ------------------ CONNECTORS ------------------
from connectors.ttn_connector import get_ttn_data, start_ttn
from connectors.flownex_connector import get_flownex_data
from connectors.irriframe_connector import get_irriframe_data
from connectors.weather_connector import get_weather

# ------------------ PROCESSING ------------------
from processing.irrigation_logic import irrigation_decision
from processing.wue_calculation import calculate_wue
from processing.irrigation_graph import generate_irrigation_graph
from processing.project_table import generate_project_table
from processing.novelty_engine import smart_novelty_system

# ------------------ APP ------------------
app = Flask(__name__)
CORS(app)

# ------------------ MONGODB ------------------
MONGO_URL = "mongodb+srv://keerthana:test123@cluster0.zpsdux7.mongodb.net/smart_irrigation?retryWrites=true&w=majority"

users_collection = None
sensor_collection = None

try:
    client = MongoClient(
        MONGO_URL,
        tls=True,
        tlsCAFile=certifi.where()
    )

    db = client["smart_irrigation"]

    users_collection = db["users"]
    sensor_collection = db["sensor_data"]

    print("✅ MongoDB Connected")

except Exception as e:
    print("❌ MongoDB Error:", e)

# ------------------ BASE URL ------------------
BASE_URL = "http://localhost:5000"

# ------------------ START TTN ------------------
try:
    start_ttn()
except Exception as e:
    print("⚠️ TTN not connected:", e)

# =====================================================
# 🔐 AUTH MODULE
# =====================================================

@app.route("/signup", methods=["POST"])
def signup():
    if users_collection is None:
        return jsonify({"status": "error", "message": "Database not connected"})

    try:
        data = request.json

        name = data.get("name")
        email = data.get("email").lower().strip()
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"status": "error", "message": "All fields required"})

        if users_collection.find_one({"email": email}):
            return jsonify({"status": "error", "message": "User already exists"})

        hashed_password = generate_password_hash(password)

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

        return jsonify({"status": "success", "message": "Signup successful"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/login", methods=["POST"])
def login():
    if users_collection is None:
        return jsonify({"status": "error", "message": "Database not connected"})

    try:
        data = request.json

        email = data.get("email").lower().strip()
        password = data.get("password")

        user = users_collection.find_one({"email": email})

        if not user:
            return jsonify({"status": "error", "message": "User not found"})

        if not check_password_hash(user["password"], password):
            return jsonify({"status": "error", "message": "Invalid password"})

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "name": user["name"],
                "email": user["email"]
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# =====================================================
# 🌱 IRRIGATION MODULE
# =====================================================

@app.route("/")
def home():
    return "Smart Irrigation Backend Running ✅"


@app.route("/data")
def get_data():
    try:
        ttn = get_ttn_data() or {"soil_moisture": 45, "temperature": 30}
        flow = get_flownex_data() or {"flow_rate": 18, "pressure": 2.5}
        weather = get_weather() or {
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

        # Save to DB safely
        if sensor_collection:
            sensor_collection.insert_one({
                "ttn": ttn,
                "flow": flow,
                "weather": weather,
                "time": datetime.datetime.now()
            })

        return jsonify({
            "status": "success",
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
            "status": "error",
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


# =====================================================
# 🚀 RUN
# =====================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)