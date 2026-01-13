"""Test script to verify model loads in Flask context"""
import pickle

MODEL_FILE = 'optimized_irrigation_model.pkl'

print("Testing model load...")
try:
    with open(MODEL_FILE, 'rb') as file:
        model = pickle.load(file)
    print(f"✅ SUCCESS! Model loaded: {type(model).__name__}")
    print(f"✅ Model has {model.n_estimators} trees")
    
    # Test a prediction
    import numpy as np
    test_input = np.array([[0, 50, 25, 70, 2, 5000]])  # Sample input
    prediction = model.predict(test_input)
    print(f"✅ Test prediction: {prediction[0]:.1f} L/ha")
    print("\n🎉 Model is fully functional!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
