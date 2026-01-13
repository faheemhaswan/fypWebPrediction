import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle # Added for the next step: saving the model

# --- Configuration ---
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, '../../data/datasets/irrigation_dataset.csv')
TARGET_VARIABLE = 'water_requirement_liters_per_hectare'
RANDOM_STATE = 42
MODEL_OUTPUT_FILE = os.path.join(BASE_DIR, 'models/optimized_irrigation_model.pkl') # File to save the trained model
# ---------------------

print("### Starting Full Data Engineering and ML Pipeline ###")
print("-" * 50)

# --- A. Data Loading and Engineering ---
try:
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded '{INPUT_FILE}' with {len(df)} samples.")
except FileNotFoundError:
    print(f"ERROR: '{INPUT_FILE}' not found. Please ensure the raw data is in the same directory.")
    exit()

# 1. Rename columns to standardized, clean names
df.rename(columns={
    'label': 'crop_type',
    'temperature': 'temperature_celsius',
    'humidity': 'humidity_percent',
    'rainfall': 'rainfall_mm'
}, inplace=True)

# 2. Normalize and check for consistency
df['crop_type'] = df['crop_type'].str.lower().str.strip()
print("Normalized 'crop_type' to lowercase.")

# --- CRITICAL FIX: Ensure calculation columns are numeric ---
numeric_cols_to_check = ['temperature_celsius', 'humidity_percent', 'rainfall_mm']

for col in numeric_cols_to_check:
    # Coerce errors: non-numeric values become NaN
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Impute (fill) resulting NaNs with the mean of the column
df.fillna(df.mean(numeric_only=True), inplace=True)
print("Ensured all calculation columns are numeric and handled initial non-numeric data.")
# -----------------------------------------------------------


# 3. Generate a synthetic 'soil_moisture_percent' column
df['soil_moisture_percent'] = np.round(np.random.uniform(30.0, 70.0, size=len(df)), 1)
print("Generated synthetic 'soil_moisture_percent' column.")

# 4. Define the rules and engineered features (Base Water Requirement)
CROP_RULES_FULL = {
    'rice': 6500, 'maize': 5000, 'pomegranate': 4400, 'banana': 5100, 
    'mango': 4600, 'watermelon': 4700, 'papaya': 4850
}

# --- FEATURE ENGINEERING: Create the numerical 'crop_water_base' feature ---
df['crop_water_base'] = df['crop_type'].map(CROP_RULES_FULL).fillna(4000)
print("Engineered 'crop_water_base' feature (numerical category proxy).")

# 5. Calculate the dynamic target variable: 'water_requirement_liters_per_hectare'
def calculate_water(row):
    crop_base_water = CROP_RULES_FULL.get(row['crop_type'], 4000)
    
    # --- HARD TYPE CONVERSION ADDED HERE ---
    temp_celsius = float(row['temperature_celsius'])
    soil_moisture = float(row['soil_moisture_percent'])
    rainfall = float(row['rainfall_mm'])
    humidity = float(row['humidity_percent'])
    
    # Dynamic calculation using environmental factors
    water_req = (
        crop_base_water +
        (temp_celsius * 15) -
        (soil_moisture * 20) -
        (rainfall * 50) +
        (humidity * 10)
    )
    
    # Add random noise for realism
    noise = np.random.normal(0, 150)
    water_req = int(water_req + noise)
    
    return max(500, water_req)

df[TARGET_VARIABLE] = df.apply(calculate_water, axis=1)
print(f"Calculated dynamic '{TARGET_VARIABLE}'.")

# 6. Keep only the final columns needed for modeling
final_columns = [
    'crop_type', 
    'soil_moisture_percent', 
    'temperature_celsius', 
    'humidity_percent', 
    'rainfall_mm',
    'crop_water_base', 
    TARGET_VARIABLE
]
df_final = df[final_columns].copy()

print("-" * 50)

# ---------------------------------------------------------------------------------------------------
## START ML PIPELINE
# ---------------------------------------------------------------------------------------------------

# B. Data Preparation and Splitting
X = df_final.drop(columns=[TARGET_VARIABLE])
Y = df_final[TARGET_VARIABLE]
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=RANDOM_STATE
)

# Define Preprocessing Steps
numerical_features = [
    'soil_moisture_percent', 'temperature_celsius', 'humidity_percent', 
    'rainfall_mm', 'crop_water_base'
]
categorical_features = ['crop_type']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

# C. Optimized Model Training (Grid Search)
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1))
])

param_grid = {
    'regressor__n_estimators': [100, 200], 
    'regressor__max_depth': [10, None],
    'regressor__min_samples_split': [2, 5]
}

print("Starting Grid Search for Hyperparameter Optimization...")
grid_search = GridSearchCV(
    model_pipeline, 
    param_grid, 
    cv=3,
    scoring='neg_mean_absolute_error',
    verbose=0, 
    n_jobs=-1
)

grid_search.fit(X_train, Y_train)
best_model = grid_search.best_estimator_

# D. Evaluation
Y_pred_optimized = best_model.predict(X_test)
mae_optimized = mean_absolute_error(Y_test, Y_pred_optimized)
r2_optimized = r2_score(Y_test, Y_pred_optimized)

print("\n✅ Grid Search Complete.")
print(f"Best Hyperparameters Found: {grid_search.best_params_}")
print("\n" + "=" * 70)
print("🎯 MODEL PERFORMANCE REPORT".center(70))
print("=" * 70)
print(f"\n📊 Dataset Information:")
print(f"   • Total Samples: {len(df):,}")
print(f"   • Training Set: {len(X_train):,} samples ({len(X_train)/len(df)*100:.1f}%)")
print(f"   • Test Set: {len(X_test):,} samples ({len(X_test)/len(df)*100:.1f}%)")
print(f"   • Features Used: {X.shape[1]}")

print(f"\n🌟 Model Accuracy Metrics:")
print(f"   ┌─────────────────────────────────────────────┐")
print(f"   │  Model Accuracy (R²):  {r2_optimized*100:5.2f}%          │")
print(f"   │  Average Error (MAE):  {mae_optimized:6.2f} liters    │")
print(f"   └─────────────────────────────────────────────┘")

# Interpretation
if r2_optimized >= 0.95:
    quality = "🏆 EXCELLENT"
    interpretation = "Your model is highly accurate!"
elif r2_optimized >= 0.85:
    quality = "✅ VERY GOOD"
    interpretation = "Your model performs well."
elif r2_optimized >= 0.70:
    quality = "👍 GOOD"
    interpretation = "Your model is acceptable."
else:
    quality = "⚠️  NEEDS IMPROVEMENT"
    interpretation = "Consider more training data."

print(f"\n📈 Model Quality: {quality}")
print(f"   {interpretation}")
print(f"\n💡 What This Means:")
print(f"   • On average, predictions are within ±{mae_optimized:.0f} liters of actual values")
print(f"   • The model explains {r2_optimized*100:.2f}% of the variation in water requirements")

print("\n" + "=" * 70)

# E. Save the Model (Next Logical Step)
with open(MODEL_OUTPUT_FILE, 'wb') as file:
    pickle.dump(best_model, file)
print(f"✅ Model saved successfully to '{MODEL_OUTPUT_FILE}'")
print(f"🚀 Model is ready for deployment and real-time predictions!")
print("=" * 70 + "\n")