"""
Smart Irrigation Water Prediction Model Training
ADVANCED version
This script engineers 10 new features and trains a more complex model.
It must be paired with 'predict_advanced.html'.
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_percentage_error
import tensorflowjs as tfjs
import json
import os
import sys

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("=" * 70)
print("🌾 SMART IRRIGATION - ML MODEL TRAINING")
print("=" * 70)

# Configuration
DATASET_PATH = 'datasets/irrigation_dataset.csv'
MODEL_SAVE_PATH = 'model_advanced' # <-- Save to a new folder
RANDOM_SEED = 42

# --- Step 1: Load Dataset ---
print("\n📂 Step 1: Loading dataset...")
try:
    df = pd.read_csv(DATASET_PATH)
    print(f"   ✅ Dataset loaded successfully")
    
    # 🌟 CRITICAL FIX: UNIT SCALING 🌟
    # The raw target values are ~20 times too small for daily L/ha.
    # We multiply by 20.0 to correct the magnitude for training.
    df['water_requirement_liters_per_hectare'] = df['water_requirement_liters_per_hectare'] * 20.0
    
    print(f"   📊 Total samples: {len(df)}")
except FileNotFoundError:
    print(f"   ❌ Error: '{DATASET_PATH}' not found!")
    print(f"   💡 Please run 'adapt_data.py' first to create this file.")
    exit(1)

# --- Step 2: Preprocessing (Encoding) ---
print("\n🔧 Step 2: Preprocessing data...")
label_encoder = LabelEncoder()
df['crop_encoded'] = label_encoder.fit_transform(df['crop_type'])
crop_classes = label_encoder.classes_.tolist()
print(f"   ✅ Crop types encoded: {len(crop_classes)} types")

# --- Step 3: Advanced Feature Engineering ---
print("\n🧠 Step 3: Engineering advanced features...")

def create_features(data):
    # Use a small epsilon to avoid division by zero
    epsilon = 1e-6
    
    # Create a copy to avoid changing the original dataframe
    df_feat = data.copy()
    
    # 1. Climate Ratios
    df_feat['temp_humidity_ratio'] = df_feat['temperature_celsius'] / (df_feat['humidity_percent'] + epsilon)
    df_feat['humidity_rainfall_ratio'] = df_feat['humidity_percent'] / (df_feat['rainfall_mm'] + epsilon)

    # 2. Interactions
    df_feat['temp_moisture_interaction'] = df_feat['temperature_celsius'] * df_feat['soil_moisture_percent']
    df_feat['moisture_humidity_product'] = df_feat['soil_moisture_percent'] * df_feat['humidity_percent']
    df_feat['moisture_rainfall_product'] = df_feat['soil_moisture_percent'] * df_feat['rainfall_mm']

    # 3. Water Source / Stress Indicators
    df_feat['water_saturation_deficit'] = (100 - df_feat['humidity_percent']) * (df_feat['temperature_celsius'] / 25)
    df_feat['soil_water_deficit'] = (100 - df_feat['soil_moisture_percent'])
    df_feat['net_water_input'] = df_feat['rainfall_mm'] - (df_feat['temperature_celsius'] / 5) # Simple rain vs evaporation

    # 4. Polynomial features
    df_feat['temp_squared'] = df_feat['temperature_celsius']**2
    df_feat['moisture_squared'] = df_feat['soil_moisture_percent']**2
    
    return df_feat

df_engineered = create_features(df)
print(f"   ✅ 10 new features created.")

# Define ALL 7 features in the correct order
# This order MUST be matched in the JavaScript
feature_columns = [
    # Original 5
    'crop_encoded',
    'soil_moisture_percent',
    'temperature_celsius',
    'humidity_percent',
    'rainfall_mm',
    # New 10
    'temp_humidity_ratio',
    'humidity_rainfall_ratio',
    'temp_moisture_interaction',
    'moisture_humidity_product',
    'moisture_rainfall_product',
    'water_saturation_deficit',
    'soil_water_deficit',
    'net_water_input',
    'temp_squared',
    'moisture_squared'
]

X = df_engineered[feature_columns].values
y = df_engineered['water_requirement_liters_per_hectare'].values.reshape(-1, 1)

print(f"   ✅ Final feature count: {X.shape[1]}")

# --- Step 4: Data Preparation ---
print("\n🎯 Step 4: Splitting and Scaling Data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_SEED, shuffle=True
)

print(f"   - Training samples: {len(X_train)}")
print(f"   - Testing samples: {len(X_test)}")

scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)
y_train_scaled = scaler_y.fit_transform(y_train)
y_test_scaled = scaler_y.transform(y_test)

print(f"   ✅ Data normalized using StandardScaler")

# --- Step 5: Build Neural Network ---
print("\n🏗️ Step 5: Building neural network architecture...")

model = keras.Sequential([
    # Input shape is 15 (for our 15 features)
    keras.layers.Dense(256, activation='relu', input_shape=(len(feature_columns),)),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.4),
    
    keras.layers.Dense(128, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    
    keras.layers.Dense(64, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.2),
    
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='linear')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='huber', # Huber loss is more robust to outliers
    metrics=['mae']
)

print(f"   ✅ Model created with input_shape=(15,)")

# --- Step 6: Train Model ---
print("\n🚀 Step 6: Training advanced model...")

early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=25, # More patience for a complex model
    restore_best_weights=True,
    verbose=0
)

class TrainingProgress(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % 20 == 0 or epoch == 0:
            print(f"   Epoch {epoch+1:3d}: loss={logs['loss']:.4f}, val_loss={logs['val_loss']:.4f}")

history = model.fit(
    X_train_scaled, y_train_scaled,
    validation_split=0.2,
    epochs=250, # Train for a bit longer
    batch_size=32,
    callbacks=[early_stopping],
    verbose=0
)

epochs_trained = len(history.history['loss'])
print(f"\n   ✅ Training completed!")
print(f"   - Total epochs: {epochs_trained}")

# --- Step 7: Evaluate Model ---
print("\n📈 Step 7: Evaluating model performance...")

y_pred_scaled = model.predict(X_test_scaled, verbose=0)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
y_test_original = scaler_y.inverse_transform(y_test_scaled)

r2 = r2_score(y_test_original, y_pred)
mape = mean_absolute_percentage_error(y_test_original, y_pred) * 100
mae = np.mean(np.abs(y_test_original - y_pred))
rmse = np.sqrt(np.mean((y_test_original - y_pred)**2))
accuracy = max(0, (1 - mape/100) * 100)
errors = np.abs(y_test_original - y_pred)
max_error = np.max(errors)
median_error = np.median(errors)

print(f"\n   {'='*60}")
print(f"   📊 ADVANCED MODEL PERFORMANCE")
print(f"   {'='*60}")
print(f"   ⭐ Accuracy:    {accuracy:.1f}%")
print(f"   📈 R² Score:    {r2:.4f}")
print(f"   📊 MAE:         {mae:.0f} L/ha")
print(f"   📉 RMSE:        {rmse:.0f} L/ha")
print(f"   🎯 Max Error:   {max_error:.0f} L/ha")
print(f"   🎯 Median Error: {median_error:.0f} L/ha")
print(f"   {'='*60}")

# --- Step 8: Save Model ---
print("\n💾 Step 8: Saving model for web deployment...")

os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
tfjs.converters.save_keras_model(model, MODEL_SAVE_PATH)
print(f"   ✅ Model saved to '{MODEL_SAVE_PATH}/' folder")

# Save preprocessing parameters
scalers_info = {
    'scaler_X_mean': scaler_X.mean_.tolist(),
    'scaler_X_scale': scaler_X.scale_.tolist(),
    'scaler_y_mean': scaler_y.mean_.tolist(),
    'scaler_y_scale': scaler_y.scale_.tolist(),
    'crop_classes': crop_classes,
    'feature_columns': feature_columns,
    'model_metrics': {
        'r2_score': float(r2),
        'accuracy': float(accuracy),
        'mae': float(mae),
        'mape': float(mape),
        'rmse': float(rmse),
        'max_error': float(max_error),
        'median_error': float(median_error)
    },
    'training_info': {
        'total_samples': len(df),
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'epochs_trained': epochs_trained,
        'features': feature_columns
    }
}

scalers_path = os.path.join(MODEL_SAVE_PATH, 'scalers.json')
with open(scalers_path, 'w') as f:
    json.dump(scalers_info, f, indent=2)

print(f"   ✅ Scalers saved to '{scalers_path}'")
print("\n" + "=" * 70)
print("✅ ADVANCED MODEL TRAINING COMPLETE!")
print(f"   Your new 15-feature model is saved in the '{MODEL_SAVE_PATH}/' folder.")
print("=" * 70 + "\n")