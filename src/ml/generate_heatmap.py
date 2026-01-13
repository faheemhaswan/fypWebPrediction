
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import LabelEncoder

# Set style
sns.set_theme(style="white")

# Configuration
# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, '../../data/datasets/irrigation_dataset.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, '../web/static/assets')
OUTPUT_FILE = 'correlation_heatmap.png'

def generate_heatmap():
    print("="*60)
    print(" GENERATING CORRELATION HEATMAP")
    print("="*60)

    # 1. Load Dataset
    if not os.path.exists(DATASET_PATH):
        print(f" Error: Dataset not found at '{DATASET_PATH}'")
        return

    print(f" Loading dataset from '{DATASET_PATH}'...")
    df = pd.read_csv(DATASET_PATH)
    print(f"   Shape: {df.shape}")

    # 2. Preprocessing
    # Encode 'crop_type' if it exists and is categorical
    if 'crop_type' in df.columns:
        print(" Encoding 'crop_type'...")
        le = LabelEncoder()
        df['crop_encoded'] = le.fit_transform(df['crop_type'])
        # Drop original string column for correlation calculation
        df_corr = df.drop(columns=['crop_type'])
    else:
        df_corr = df

        df_corr = df

    # 3. Clean and Calculate Correlation
    print(" Cleaning data...")
    # Force convert to numeric, turning errors (like the second header row) into NaN
    for col in df_corr.columns:
        if col != 'crop_encoded': # Skip the encoded categorical column if we want, but even that should be fine
             df_corr[col] = pd.to_numeric(df_corr[col], errors='coerce')
    
    # Drop rows with NaN (this will remove the second header row)
    df_corr = df_corr.dropna()
    print(f"   Cleaned Shape: {df_corr.shape}")

    print(" Calculating correlation matrix...")
    corr = df_corr.corr()

    # 4. Generate Heatmap
    print(" creating heatmap...")
    plt.figure(figsize=(12, 10))
    
    # Create a mask for the upper triangle
    mask =  None # np.triu(np.ones_like(corr, dtype=bool)) # Optional: masking upper triangle

    heatmap = sns.heatmap(
        corr, 
        annot=True, 
        fmt=".2f", 
        cmap='coolwarm',
        vmin=-1, 
        vmax=1, 
        center=0,
        square=True, 
        linewidths=.5, 
        cbar_kws={"shrink": .5}
    )

    plt.title('Feature Correlation Matrix', fontsize=16)
    plt.tight_layout()

    # 5. Save Image
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f" Heatmap saved to '{save_path}'")
    print("="*60)

if __name__ == "__main__":
    generate_heatmap()
