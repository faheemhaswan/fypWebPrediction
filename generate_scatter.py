import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = 'assets'
OUTPUT_FILE = 'prediction_vs_actual.png'

def generate_scatter_plot():
    print("="*60)
    print(" GENERATING PREDICTION VS ACTUAL SCATTER PLOT")
    print("="*60)

    # 1. Load Data (Same logic as verify_data.py)
    try:
        print(" Loading and preparing data...")
        DATASET_PATH = 'datasets/irrigation_dataset.csv'
        df = pd.read_csv(DATASET_PATH)
        
        # Handle double header or bad rows if present (like in heatmap generation)
        # However, verify_data.py didn't seem to have the cleaning I added to heatmap.
        # But for robustness, let's coerce numeric columns.
        
        if 'label' in df.columns:
            df.rename(columns={
                'label': 'crop_type',
                'temperature': 'temperature_celsius',
                'humidity': 'humidity_percent',
                'rainfall': 'rainfall_mm'
            }, inplace=True)
            
        df['crop_type'] = df['crop_type'].str.lower().str.strip()
        
        cols = ['temperature_celsius', 'humidity_percent', 'rainfall_mm']
        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows that failed conversion (like headers)
        df.dropna(subset=cols, inplace=True) 
        df.fillna(df.mean(numeric_only=True), inplace=True)
        
        # Synthetic Soil Moisture
        np.random.seed(42)
        df['soil_moisture_percent'] = np.round(np.random.uniform(30.0, 70.0, size=len(df)), 1)
        
        CROP_RULES = {
            'rice': 6500, 'maize': 5000, 'pomegranate': 4400, 'banana': 5100, 
            'mango': 4600, 'watermelon': 4700, 'papaya': 4850
        }
        df['crop_water_base'] = df['crop_type'].map(CROP_RULES).fillna(4000)
        
        # Calculate True Target
        def calculate_water(row):
            base = CROP_RULES.get(row['crop_type'], 4000)
            req = (base + float(row['temperature_celsius'])*15 - 
                   float(row['soil_moisture_percent'])*20 - 
                   float(row['rainfall_mm'])*50 + 
                   float(row['humidity_percent'])*10)
            return max(500, int(req))

        df['true_target'] = df.apply(calculate_water, axis=1)
        
        # Features expected by optimized_irrigation_model.pkl
        # Based on verify_data.py line 81
        X = df[['crop_type', 'soil_moisture_percent', 'temperature_celsius', 'humidity_percent', 'rainfall_mm', 'crop_water_base']]
        y_true = df['true_target']
        
        print(f"   Samples: {len(df)}")

    except Exception as e:
        print(f" Error preparing data: {e}")
        return

    # 2. Load Model
    try:
        print(" Loading model...")
        MODEL_PATH = 'optimized_irrigation_model.pkl'
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        print(f" Error loading model: {e}")
        return

    # 3. Predict
    print(" Running predictions...")
    try:
        y_pred = model.predict(X)
    except Exception as e:
        print(f" Prediction error: {e}")
        return

    # 4. Plot
    print(" creating scatter plot...")
    plt.figure(figsize=(10, 8))
    
    # Scatter points
    sns.scatterplot(x=y_true, y=y_pred, alpha=0.6, edgecolor=None, color='#2ecc71', s=50, label='Predictions')
    
    # Perfect alignment line
    min_val = min(min(y_true), min(y_pred))
    max_val = max(max(y_true), max(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Fit')
    
    plt.xlabel('Actual Water Requirement (L/ha)', fontsize=12)
    plt.ylabel('Predicted Water Requirement (L/ha)', fontsize=12)
    plt.title('Prediction vs Actual Accuracy', fontsize=16)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add metrics annotation
    from sklearn.metrics import r2_score, mean_absolute_error
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    
    plt.annotate(f'R² = {r2:.3f}\nMAE = {mae:.1f}', 
                 xy=(0.05, 0.95), xycoords='axes fraction',
                 fontsize=12, backgroundcolor='white',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

    # 5. Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f" Plot saved to '{save_path}'")
    print("="*60)

if __name__ == "__main__":
    generate_scatter_plot()
