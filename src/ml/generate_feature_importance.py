print("1. Start script...", flush=True)

import pandas as pd
import numpy as np
import pickle
import os
print("2. Imported basics", flush=True)

import matplotlib.pyplot as plt
import seaborn as sns
print("3. Imported plotting libs", flush=True)

OUTPUT_DIR = 'assets'
OUTPUT_FILE = 'feature_importance.png'
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, 'models/optimized_irrigation_model.pkl')

def generate_feature_importance():
    print("="*60, flush=True)
    print(" GENERATING FEATURE IMPORTANCE PLOT", flush=True)
    print("="*60, flush=True)

    # 1. Load Model
    if not os.path.exists(MODEL_FILE):
        print(f" Error: Model file '{MODEL_FILE}' not found.", flush=True)
        return

    try:
        print(f" Loading model from '{MODEL_FILE}'...", flush=True)
        with open(MODEL_FILE, 'rb') as f:
            pipeline = pickle.load(f)
        print(" Model loaded successfully.", flush=True)
    except Exception as e:
        print(f" Error loading model: {e}", flush=True)
        return

    # 2. Extract Importances
    print(" Extracting importances...", flush=True)
    try:
        # Access the regressor step
        regressor = pipeline.named_steps['regressor']
        importances = regressor.feature_importances_
        print(f" Raw importances: {importances}", flush=True)
        
        # Access the preprocessor step to get feature names
        preprocessor = pipeline.named_steps['preprocessor']
        
        print(" Extracting feature names...", flush=True)
        # Get feature names from the column transformer
        # scikit-learn >= 1.0 supports get_feature_names_out
        feature_names = preprocessor.get_feature_names_out()
        
        # Clean feature names (remove "num__" and "cat__" prefixes)
        clean_names = []
        for name in feature_names:
            # Handle standard sklearn output format like "num__feature_name"
            if "__" in name:
                clean_names.append(name.split("__")[1])
            else:
                clean_names.append(name)
        
        print(f" Feature names: {clean_names}", flush=True)
                
    except Exception as e:
        print(f" Error extracting features: {e}", flush=True)
        print(" Using fallback feature names based on adapt_data.py structure...", flush=True)
        return

    if len(clean_names) != len(importances):
        print(f" Mismatch: {len(clean_names)} names vs {len(importances)} importance values.", flush=True)
        return

    # 3. Create DataFrame
    df_imp = pd.DataFrame({'Feature': clean_names, 'Importance': importances})
    df_imp = df_imp.sort_values(by='Importance', ascending=False)
    
    print("\n Top 5 Features:", flush=True)
    print(df_imp.head(5), flush=True)

    # 4. Plot
    print(" creating plot...", flush=True)
    plt.figure(figsize=(12, 8))
    
    # Use a color palette where the top item is distinct if possible, or just a nice palette
    sns.barplot(data=df_imp.head(10), x='Importance', y='Feature', hue='Feature', legend=False, palette='mako')
    
    plt.title('Feature Importance Factors', fontsize=16, pad=20)
    plt.xlabel('Relative Importance (0-1)', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # 5. Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f" Plot saved to '{save_path}'", flush=True)
    print("="*60, flush=True)

if __name__ == "__main__":
    generate_feature_importance()
