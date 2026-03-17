from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# Home route (frontend open)
@app.route("/")
def home():
    return send_file("farmer.html")


# Crop data
crops = {
    "cotton": {"pesticide": "Imidacloprid", "dose": 200, "water": 150},
    "wheat": {"pesticide": "Chlorpyrifos", "dose": 180, "water": 140},
    "rice": {"pesticide": "Cartap Hydrochloride", "dose": 220, "water": 160},
    "onion": {"pesticide": "Mancozeb", "dose": 150, "water": 120},
    "soybean": {"pesticide": "Lambda-cyhalothrin", "dose": 170, "water": 130},
    "sugarcane": {"pesticide": "Thiamethoxam", "dose": 250, "water": 200}
}

# Get crop data
@app.route("/crop/<name>")
def crop(name):
    name = name.lower()
    if name in crops:
        return jsonify(crops[name])
    return jsonify({"error": "Crop not found"})


# Spray calculation
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

    area = float(data["area"])
    dose = float(data["dose"])
    water = float(data["water"])
    tank = float(data["tank"])

    totalMed = area * dose
    totalWater = area * water

    tankCount = totalWater / tank if tank != 0 else 0
    perTank = totalMed / tankCount if tankCount != 0 else 0

    return jsonify({
        "medicine": round(totalMed, 2),
        "water": round(totalWater, 2),
        "tanks": round(tankCount, 1),
        "perTank": round(perTank, 2)
    })


# Weather
@app.route("/weather")
def weather():
    rain = random.choice([True, False])

    if rain:
        return jsonify({
            "weather": "Rain expected",
            "advice": "Avoid spraying today"
        })

    return jsonify({
        "weather": "Clear weather",
        "advice": "Good for spraying"
    })


# Disease detect
@app.route("/disease")
def disease():
    diseases = [
        "Leaf Spot",
        "Powdery Mildew",
        "Rust Disease",
        "Bacterial Blight",
        "Healthy Leaf"
    ]

    result = random.choice(diseases)

    return jsonify({
        "disease": result,
        "solution": "Neem Oil Spray"
    })


# Railway run config
if __name__ == "__main__":
    port = int(os.environ.get("PORT"))
    app.run(host="0.0.0.0", port=port)
