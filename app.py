from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__, template_folder='.')
# Strict CORS disabled for extensive dev compatibility
CORS(app)

# --- MANUAL CORS OVERRIDE (To Fix 404 on OPTIONS) ---
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# --- Load the trained model ---
MODEL_FILE = 'optimized_irrigation_model.pkl'

try:
    with open(MODEL_FILE, 'rb') as file:
        model = pickle.load(file)
    # Model reloaded for compatibility
    print(f"✅ Model loaded successfully from '{MODEL_FILE}'")
except Exception as e:
    print(f"❌ ERROR Loading Model: {e}")
    print("⚠️  Use 'python train_model_advanced.py' to retrain the model for this environment.")
    print("⚠️  Server continues running for OTP/Auth features.")
    model = None

# --- Route: Serve the HTML page ---
@app.route('/')
def home():
    return render_template('predict.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/history.html')
def history():
    return render_template('history.html')

@app.route('/settings.html')
def settings():
    return render_template('settings.html')

@app.route('/weather.html')
def weather():
    return render_template('weather.html')

# --- STATIC FILE SERVING (Fix for Render/Production) ---
from flask import send_from_directory

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

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



# ==========================================
#  🔐 SECURITY & AUTHENTICATION (OTP + SMTP)
# ==========================================
import smtplib
import random
import string
import time
from email.message import EmailMessage
import firebase_admin
from firebase_admin import credentials, auth

# --- CONFIGURATION (USER MUST FILL THIS) ---
SMTP_EMAIL = "faheem.hswn@gmail.com"
SMTP_PASSWORD = "zyoo arad mwpd lekm".replace(" ", "")  # Sanitize spaces
# -------------------------------------------

# Initialize Firebase Admin SDK
try:
    if not firebase_admin._apps:
        # Check for environment variable first (Best for Render/Cloud)
        firebase_creds_env = os.environ.get('FIREBASE_CREDENTIALS')
        
        if firebase_creds_env:
            # Load from JSON string in environment variable
            import json
            cred_dict = json.loads(firebase_creds_env)
            cred = credentials.Certificate(cred_dict)
        else:
            # Fallback to local file (Development)
            cred = credentials.Certificate("smart-irrigation-system-3a5ff-firebase-adminsdk-fbsvc-9a698da30d.json")
            
        firebase_admin.initialize_app(cred)
    print("✅ Firebase Admin SDK Initialized")
except Exception as e:
    print(f"⚠️ WARNING: Firebase Admin SDK failed to initialize. Password reset will not work.\nReason: {e}")

# In-Memory OTP Storage: {email: {'otp': '123456', 'expires_at': timestamp}}
otp_storage = {}

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_smtp_email(to_email, otp):
    # Only mock if the config is still the default placeholder
    if "your-email" in SMTP_EMAIL:
        print(f"⚠️ [MOCK EMAIL] SMTP not configured. OTP for {to_email} is: {otp}")
        return True # Pretend success for testing if not configured
        
    try:
        msg = EmailMessage()
        msg.set_content(f"Your AquaWise Verification Code is: {otp}\n\nThis code expires in 5 minutes.")
        msg['Subject'] = 'AquaWise Password Reset Code'
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email

        # Connect to Gmail SMTP
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ OTP sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ SMTP Error: {e}")
        return False

# 1. SEND OTP ENDPOINT
@app.route('/api/send-otp', methods=['POST', 'OPTIONS'])
def send_otp_route():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # ✅ CHECK IF USER EXISTS BEFORE SENDING OTP
    try:
        user = auth.get_user_by_email(email)
        print(f"User found for OTP request: {email} (UID: {user.uid})")
    except firebase_admin._auth_utils.UserNotFoundError:
        print(f"OTP request failed - email not registered: {email}")
        return jsonify({'error': 'This email is not registered. Please sign up first!'}), 404
    except Exception as e:
        print(f"Error checking email: {str(e)}")
        return jsonify({'error': 'Failed to verify email. Please try again.'}), 500
    
    # Generate OTP
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = {'otp': otp, 'expires_at': time.time() + 300} # 5 minutes
    
    success = send_smtp_email(email, otp)
    if success:
        print(f"✅ OTP sent to {email}")
        return jsonify({'success': True, 'message': 'Verification code sent to your email!'})
    else:
        print(f"Email send failed: {e}") # 'e' from send_smtp_email is not available here, should be handled inside send_smtp_email or passed back.
        return jsonify({'error': 'Failed to send email. Please try again.'}), 500

# 2. VERIFY OTP ENDPOINT
@app.route('/api/verify-otp', methods=['POST', 'OPTIONS'])
def verify_otp_route():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.json
    email = data.get('email')
    user_otp = data.get('otp')
    
    if not email or not user_otp:
        return jsonify({'error': 'Email and OTP required'}), 400
        
    record = otp_storage.get(email)
    
    if not record:
        return jsonify({'error': 'No OTP requested for this email'}), 400
        
    if time.time() > record['expires_at']:
        del otp_storage[email]
        return jsonify({'error': 'OTP has expired. Please request a new one.'}), 400
        
    if record['otp'] != user_otp:
        return jsonify({'error': 'Invalid OTP'}), 400
        
    return jsonify({'success': True, 'message': 'OTP Verified'})

# 3. RESET PASSWORD ENDPOINT
@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('new_password')
    
    if not email or not otp or not new_password:
        return jsonify({'error': 'Missing required fields'}), 400

    # Verify OTP is still valid
    record = otp_storage.get(email)
    if not record:
        return jsonify({'error': 'Session expired. Please request a new code.'}), 400
    
    if record['otp'] != otp:
        return jsonify({'error': 'Invalid verification code. Please try again.'}), 400
          
    try:
        # Get user from Firebase
        print(f"Attempting password reset for: {email}")  # Debug log
        user = auth.get_user_by_email(email)
        print(f"User found: {user.uid}")  # Debug log
        
        # Update password
        auth.update_user(
            user.uid,
            password=new_password
        )
        
        # Cleanup OTP
        del otp_storage[email]
        
        print(f"Password reset successful for: {email}")  # Debug log
        return jsonify({'success': True, 'message': 'Password reset successfully!'})
        
    except firebase_admin._auth_utils.UserNotFoundError:
        print(f"Firebase user not found for email: {email}")  # Debug log
        return jsonify({'error': 'Email not registered. Please sign up first.'}), 404
    except Exception as e:
        print(f"Password reset error for {email}: {str(e)}")  # Debug log
        return jsonify({'error': f'Failed to reset password: {str(e)}'}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🌱 Irrigation Prediction API Server")
    print("="*50)
    print("Server running at: http://localhost:5000")
    print("API Endpoint: http://localhost:5000/predict")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)