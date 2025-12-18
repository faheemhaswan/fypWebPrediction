from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# --- Load the trained model ---
MODEL_FILE = 'optimized_irrigation_model.pkl'

try:
    with open(MODEL_FILE, 'rb') as file:
        model = pickle.load(file)
    # Model reloaded for compatibility
    print(f"✅ Model loaded successfully from '{MODEL_FILE}'")
except FileNotFoundError:
    print(f"❌ ERROR: '{MODEL_FILE}' not found. Please ensure the model file is in the same directory.")
    model = None

# --- Route: Serve the HTML page ---
@app.route('/')
def home():
    return render_template('predict.html')

# --- Route: Handle prediction requests ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please check server logs.'}), 500
    
    try:
        # Get JSON data from request
        data = request.json
        
        # Validate required fields
        required_fields = [
            'crop_type', 
            'soil_moisture_percent', 
            'temperature_celsius', 
            'humidity_percent', 
            'rainfall_mm', 
            'crop_water_base'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {missing_fields}'}), 400
        
        # Create DataFrame with the exact column order used during training
        input_df = pd.DataFrame([{
            'crop_type': data['crop_type'],
            'soil_moisture_percent': float(data['soil_moisture_percent']),
            'temperature_celsius': float(data['temperature_celsius']),
            'humidity_percent': float(data['humidity_percent']),
            'rainfall_mm': float(data['rainfall_mm']),
            'crop_water_base': float(data['crop_water_base'])
        }])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        # Return result
        return jsonify({
            'success': True,
            'water_requirement_liters_per_hectare': round(prediction, 2),
            'input_data': data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Route: Get crop base values (helper endpoint) ---
@app.route('/crop-info', methods=['GET'])
def crop_info():
    crop_rules = {
        'rice': 6500, 
        'maize': 5000, 
        'pomegranate': 4400, 
        'banana': 5100, 
        'mango': 4600, 
        'watermelon': 4700, 
        'papaya': 4850
    }
    return jsonify(crop_rules)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🌱 Irrigation Prediction API Server")
    print("="*50)
    print("Server running at: http://localhost:5000")
    print("API Endpoint: http://localhost:5000/predict")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)