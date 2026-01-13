print("Starting...")

print("Importing pandas...")
import pandas as pd
print("✅ Pandas OK")

print("Importing numpy...")
import numpy as np
print("✅ Numpy OK")

print("Importing sklearn...")
from sklearn.preprocessing import StandardScaler
print("✅ Sklearn OK")

print("Importing TensorFlow... (this may take 30-60 seconds)")
import tensorflow as tf
print("✅ TensorFlow OK")
print(f"TensorFlow version: {tf.__version__}")

print("Importing tensorflowjs...")
import tensorflowjs as tfjs
print("✅ TensorFlowJS OK")

print("\n🎉 All imports successful!")