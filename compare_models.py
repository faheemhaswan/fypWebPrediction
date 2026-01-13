import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import os

# Configuration
# Configuration
DATASET_PATH = 'datasets/irrigation_dataset.csv'
RESULTS_FILE = 'model_comparison_results.txt'
PLOT_FILE = 'assets/model_comparison.png'
RANDOM_SEED = 42

# Ensure assets directory exists
os.makedirs('assets', exist_ok=True)

print("=" * 70, flush=True)
print(" MODEL PERFORMANCE COMPARISON", flush=True)
print("=" * 70, flush=True)

# --- Step 1: Load Dataset ---
print("\n Step 1: Loading dataset...", flush=True)
if not os.path.exists(DATASET_PATH):
    # Fallback to local path if datasets folder not found (handling different execution contexts)
    if os.path.exists('irrigation_dataset.csv'):
        DATASET_PATH = 'irrigation_dataset.csv'
    else:
        print(f" Error: '{DATASET_PATH}' not found!", flush=True)
        exit(1)

df = pd.read_csv(DATASET_PATH)
print(f"    Dataset loaded successfully: {len(df)} samples", flush=True)

# CLEANUP: Remove potential duplicate header (row index 0)
if df.iloc[0]['crop_type'] == 'crop_type':
    print("    Detected duplicate header row. Removal...", flush=True)
    df = df.drop(0).reset_index(drop=True)

# Ensure numeric types
cols_to_numeric = [
    'soil_moisture_percent', 'temperature_celsius', 'humidity_percent', 
    'rainfall_mm', 'water_requirement_liters_per_hectare'
]
for col in cols_to_numeric:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()
print(f"    Samples after cleaning: {len(df)}", flush=True)

# CRITICAL FIX: UNIT SCALING
# Matching logic from train_model_advanced.py
df['water_requirement_liters_per_hectare'] = df['water_requirement_liters_per_hectare'] * 20.0

# --- Step 2: Preprocessing ---
print("\n Step 2: Preprocessing data...", flush=True)
label_encoder = LabelEncoder()
df['crop_encoded'] = label_encoder.fit_transform(df['crop_type'])

# --- Step 3: Feature Engineering ---
# Matching logic from train_model_advanced.py
print("\n Step 3: Engineering features...", flush=True)
def create_features(data):
    epsilon = 1e-6
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
    df_feat['net_water_input'] = df_feat['rainfall_mm'] - (df_feat['temperature_celsius'] / 5)

    # 4. Polynomial features
    df_feat['temp_squared'] = df_feat['temperature_celsius']**2
    df_feat['moisture_squared'] = df_feat['soil_moisture_percent']**2
    
    return df_feat

df_engineered = create_features(df)

feature_columns = [
    'crop_encoded', 'soil_moisture_percent', 'temperature_celsius', 'humidity_percent', 'rainfall_mm',
    'temp_humidity_ratio', 'humidity_rainfall_ratio', 'temp_moisture_interaction', 
    'moisture_humidity_product', 'moisture_rainfall_product', 'water_saturation_deficit', 
    'soil_water_deficit', 'net_water_input', 'temp_squared', 'moisture_squared'
]

X = df_engineered[feature_columns].values
y = df_engineered['water_requirement_liters_per_hectare'].values

# --- Step 4: Split and Scale ---
print("\n Step 4: Splitting and Scaling...", flush=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_SEED)

scaler_X = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)

# Define models
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=RANDOM_SEED),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=RANDOM_SEED)
}

results = []

print("\n Step 5: Training and Evaluating Models...", flush=True)
for name, model in models.items():
    print(f"    - Training {name}...", flush=True)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    # Metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
    accuracy = max(0, 100 - mape) # Simple accuracy proxy
    
    results.append({
        "Model": name,
        "R2 Score": r2,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "Accuracy (%)": accuracy
    })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# --- Step 6: Output Results ---
print("\n Step 6: Results Summary", flush=True)
print(results_df.to_string(index=False), flush=True)

with open(RESULTS_FILE, 'w') as f:
    f.write("Model Performance Comparison\n")
    f.write("============================\n\n")
    f.write(results_df.to_string(index=False))
    f.write("\n\n")
    for res in results:
        f.write(f"Model: {res['Model']}\n")
        f.write(f"  R2 Score: {res['R2 Score']:.4f}\n")
        f.write(f"  MAE:      {res['MAE']:.2f}\n")
        f.write(f"  RMSE:     {res['RMSE']:.2f}\n")
        f.write(f"  Accuracy: {res['Accuracy (%)']:.2f}%\n")
        f.write("-" * 30 + "\n")

print(f"\n    Results saved to '{RESULTS_FILE}'", flush=True)

# --- Step 7: Visualization ---
print("\n Step 7: Generating Visualization...", flush=True)

# Melt for easier plotting
melted_df = results_df.melt(id_vars="Model", value_vars=["R2 Score", "Accuracy (%)"], var_name="Metric", value_name="Value")

plt.figure(figsize=(12, 6))

# Plot R2 and Accuracy
plt.subplot(1, 2, 1)
sns.barplot(x="Model", y="R2 Score", data=results_df, palette="viridis")
plt.title("R2 Score Comparison")
plt.ylim(0, 1.1)
for i, v in enumerate(results_df["R2 Score"]):
    plt.text(i, v + 0.02, f"{v:.3f}", ha='center')

plt.subplot(1, 2, 2)
sns.barplot(x="Model", y="RMSE", data=results_df, palette="magma")
plt.title("RMSE Comparison (Lower is Better)")
for i, v in enumerate(results_df["RMSE"]):
    plt.text(i, v + 50, f"{v:.0f}", ha='center')

plt.tight_layout()
plt.savefig(PLOT_FILE)
print(f"    Plot saved to '{PLOT_FILE}'", flush=True)

print("\nDONE.", flush=True)
