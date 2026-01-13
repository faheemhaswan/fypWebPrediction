"""
Quick fix script to create a compatible model for the current environment
This creates a simple working model that matches the expected interface
"""

import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

print("=" * 70)
print("🔧 Creating Compatible ML Model")
print("=" * 70)

# Create a simple but functional model
model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)

# Create dummy training data that matches the expected input format
# Features: crop_type (encoded), soil_moisture, temperature, humidity, rainfall, crop_water_base
np.random.seed(42)
n_samples = 1000

# Generate realistic synthetic data
crop_types_encoded = np.random.randint(0, 7, n_samples)  # 7 crop types
soil_moisture = np.random.uniform(20, 80, n_samples)
temperature = np.random.uniform(20, 35, n_samples)
humidity = np.random.uniform(40, 90, n_samples)
rainfall = np.random.uniform(0, 10, n_samples)
crop_water_base = np.random.choice([4000, 4400, 4600, 4700, 4850, 5000, 5100, 6500], n_samples)

X = np.column_stack([crop_types_encoded, soil_moisture, temperature, humidity, rainfall, crop_water_base])

# Generate realistic target values (water requirement in L/ha)
# Base formula similar to the rules in the frontend
y = (
    crop_water_base +
    (temperature * 15) -
    (soil_moisture * 20) -
    (rainfall * 50) +
    (humidity * 10) +
    np.random.normal(0, 200, n_samples)  # Add some noise
)
y = np.clip(y, 500, 10000)  # Realistic bounds

# Train the model
print("\n📊 Training model with 1000 synthetic samples...")
model.fit(X, y)

# Save the model
# Save the model
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, 'models/optimized_irrigation_model.pkl')
with open(MODEL_FILE, 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Model saved successfully to '{MODEL_FILE}'")
print(f"📈 Model R² Score on training data: {model.score(X, y):.3f}")
print("\n✨ Done! You can now restart the backend server.")
print("=" * 70)
