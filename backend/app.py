from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import datetime

app = Flask(__name__)
CORS(app)

# ---------------- MONGODB SETUP ----------------
client = None
users_collection = None
sensor_collection = None

try:
    from pymongo import MongoClient

    MONGO_URI = os.environ.get("MONGO_URI")

    if MONGO_URI:
        client = MongoClient(MONGO_URI)
        db = client["smart_irrigation"]

        users_collection = db["users"]
        sensor_collection = db["sensor_data"]

        print("✅ MongoDB Connected")
    else:
        print("⚠️ No MongoDB URI found")

except Exception as e:
    print("❌ MongoDB Error:", e)

# ---------------- FALLBACK STORAGE ----------------
users = []

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Smart Irrigation Backend Running ✅"

# ---------------- DATA API ----------------
@app.route("/data")
def get_data():
    try:
        data = {
            "status": "Success",
            "ttn": {"soil_moisture": 45, "temperature": 30},
            "flow": {"flow_rate": 18, "pressure": 2.5},
            "weather": {
                "temperature": 31,
                "rainfall": 5,
                "humidity": 72
            },
            "decision": "Irrigation not required",
            "water_use_efficiency": 75,
            "time": str(datetime.datetime.now())
        }

        # SAVE ONLY IF DB EXISTS (FIXED)
        if sensor_collection is not None:
            try:
                sensor_collection.insert_one(data)
            except Exception as e:
                print("DB INSERT ERROR:", e)

        return jsonify(data)

    except Exception as e:
        print("DATA ERROR:", e)
        return jsonify({"status": "Error", "message": str(e)})

# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    try:
        if sensor_collection is not None:
            data = list(
                sensor_collection.find({}, {"_id": 0})
                .sort("time", -1)
                .limit(10)
            )
            return jsonify(data)

        return jsonify([])

    except Exception as e:
        print("HISTORY ERROR:", e)
        return jsonify([])

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "Error", "message": "No data"})

        email = data.get("email")
        password = data.get("password")

        # MONGODB LOGIN (FIXED)
        if users_collection is not None:
            user = users_collection.find_one({
                "email": email,
                "password": password
            })

            if user:
                return jsonify({"status": "Success"})
            else:
                return jsonify({"status": "Failed"})

        # FALLBACK LOGIN
        for user in users:
            if user["email"] == email and user["password"] == password:
                return jsonify({"status": "Success"})

        return jsonify({"status": "Failed"})

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"status": "Error", "message": str(e)})

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "Error", "message": "No data"})

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        # MONGODB SIGNUP (FIXED)
        if users_collection is not None:
            existing = users_collection.find_one({"email": email})

            if existing:
                return jsonify({"status": "Failed", "message": "User exists"})

            users_collection.insert_one({
                "name": name,
                "email": email,
                "password": password
            })

            return jsonify({"status": "Success"})

        # FALLBACK SIGNUP
        for user in users:
            if user["email"] == email:
                return jsonify({"status": "Failed"})

        users.append({
            "name": name,
            "email": email,
            "password": password
        })

        return jsonify({"status": "Success"})

    except Exception as e:
        print("SIGNUP ERROR:", e)
        return jsonify({"status": "Error", "message": str(e)})