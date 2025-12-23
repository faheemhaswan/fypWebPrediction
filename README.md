# 💧 AquaWise - Smart Irrigation System

<div align="center">

![AquaWise Logo](assets/aquawise_logo.png)

**AI-Powered Water Usage Prediction for Sustainable Agriculture**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Admin-orange.svg)](https://firebase.google.com/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-red.svg)](https://scikit-learn.org/)

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots)

</div>

---

## 📖 About The Project

**AquaWise** is an intelligent irrigation management system that leverages machine learning to predict optimal water usage for agricultural crops. By analyzing environmental factors such as temperature, humidity, rainfall, and soil moisture, AquaWise helps farmers make data-driven irrigation decisions, conserve water, and maximize crop yield.

### 🎯 Problem Statement
- Water scarcity affecting agricultural productivity
- Manual irrigation leading to water wastage
- Lack of data-driven decision making in farming
- Difficulty predicting optimal irrigation schedules

### 💡 Solution
AquaWise provides:
- **AI-powered water usage predictions** based on real-time environmental data
- **Smart irrigation recommendations** tailored to crop types and weather conditions
- **Historical tracking** of irrigation patterns and water consumption
- **Weather forecasting integration** for proactive irrigation planning

---

## ✨ Features

### 🔐 Authentication & Security
- **Firebase Authentication** - Secure user registration and login
- **OTP Email Verification** - Two-factor authentication for password reset
- **Session Management** - Secure user sessions with auto-logout

### 🌾 Smart Predictions
- **ML-Based Water Prediction** - Scikit-learn Random Forest model
- **Multi-Factor Analysis** - Temperature, humidity, rainfall, soil moisture, crop type
- **Real-Time Calculations** - Instant water usage predictions per hectare
- **Irrigation Recommendations** - AI-generated advice based on current conditions

### 📊 Dashboard & Analytics
- **Comprehensive Dashboard** - Real-time overview of system status
- **Historical Data Tracking** - View past predictions and irrigation patterns
- **Visual Analytics** - Charts and graphs for data visualization
- **Comparison Metrics** - Analyze water usage trends over time

### 🌤️ Weather Integration
- **OpenWeatherMap API** - Real-time weather data
- **5-Day Forecasts** - Plan irrigation schedules in advance
- **Location-Based** - GPS or manual location selection
- **Smart Recommendations** - Weather-aware irrigation advice

### ⚙️ User Management
- **Profile Management** - Update user information
- **Settings Dashboard** - Customize application preferences
- **Account Statistics** - Track usage and activity
- **Password Reset** - Secure password recovery with OTP

---

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic markup structure
- **CSS3** - Modern styling with animations and gradients
- **JavaScript (ES6+)** - Interactive user interface
- **Font Awesome** - Icon library
- **Google Fonts (Outfit)** - Typography

### Backend
- **Python 3.9+** - Core programming language
- **Flask** - Web framework and REST API
- **Flask-CORS** - Cross-Origin Resource Sharing

### Machine Learning
- **Scikit-learn** - Random Forest Regressor model
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Pickle** - Model serialization

### Database & Authentication
- **Firebase Admin SDK** - User authentication and management
- **Firebase Auth** - Secure authentication service

### APIs & Services
- **OpenWeatherMap API** - Weather data and forecasts
- **SMTP (Gmail)** - Email service for OTP delivery

### Development Tools
- **Git** - Version control
- **VS Code** - Code editor
- **Chrome DevTools** - Debugging and testing

---

## 📋 Prerequisites

Before installation, ensure you have:

- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **pip** - Python package manager (included with Python)
- **Git** - [Download](https://git-scm.com/downloads)
- **Firebase Account** - [Create](https://firebase.google.com/)
- **OpenWeatherMap API Key** - [Get Free Key](https://openweathermap.org/api)
- **Gmail Account** - For SMTP email service

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/faheemhaswan/fypWebPrediction.git
cd smart_irrigation_project
```

### 2. Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Firebase
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing
3. Generate Firebase Admin SDK private key:
   - Project Settings → Service Accounts → Generate New Private Key
4. Save the JSON file as `smart-irrigation-system-3a5ff-firebase-adminsdk-fbsvc-9a698da30d.json`
5. Place in project root directory

### 5. Configure Environment Variables
Create a `.env` file in the project root (optional, or use direct configuration):
```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-digit-app-password
WEATHER_API_KEY=your-openweathermap-api-key
```

**Note:** For Gmail SMTP, you need to:
1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password: [Google Account Security](https://myaccount.google.com/security)

### 6. Update API Configuration
In `weather.html`, update line 752:
```javascript
const WEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY';
```

---

## 💻 Usage

### Starting the Backend Server

#### Option 1: Using Batch File (Windows)
```bash
.\run_backend.bat
```

#### Option 2: Manual Start
```bash
# Activate virtual environment first
venv\Scripts\activate

# Run Flask server
python app.py
```

The server will start at `http://localhost:5000`

**Keep this terminal window open** while using the application.

### Opening the Frontend

1. Navigate to the project directory
2. Open `index.html` in your web browser
3. Or use a local server (recommended):
   ```bash
   # Python 3
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

### First-Time Setup

1. **Create Account**
   - Click "Sign Up" on the login page
   - Enter email and password (min 6 characters)
   - Agree to terms and conditions

2. **Login**
   - Use your registered email and password
   - Check "Remember Me" for persistent login

3. **Make Your First Prediction**
   - Go to "Predict" page
   - Enter crop details (type, area, soil moisture, etc.)
   - Click "Get Prediction"
   - View AI-generated water usage recommendation

---

## 📸 Screenshots

### Login & Authentication
![Login Page](screenshots/login.png)
*Secure login with modern UI*

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Real-time overview of irrigation system*

### Water Prediction
![Prediction](screenshots/prediction.png)
*AI-powered water usage calculations*

### Weather Forecast
![Weather](screenshots/weather.png)
*5-day weather forecast with irrigation recommendations*

### History Tracking
![History](screenshots/history.png)
*Track past predictions and irrigation patterns*

---

## 🗂️ Project Structure

```
smart_irrigation_project/
├── app.py                          # Flask backend API
├── run_backend.bat                 # Backend startup script
├── requirements.txt                # Python dependencies
├── optimized_irrigation_model.pkl  # Trained ML model
├── smart-irrigation-system-*.json  # Firebase credentials
│
├── index.html                      # Login/Signup page
├── dashboard.html                  # Main dashboard
├── predict.html                    # Water prediction interface
├── history.html                    # Prediction history
├── weather.html                    # Weather forecast
├── settings.html                   # User settings
│
├── assets/                         # Images and logos
│   ├── aquawise_logo.png
│   └── background.png
│
├── datasets/                       # Training data
│   ├── irrigation_dataset.csv
│   └── adapted_data.csv
│
├── model_advanced/                 # ML model files
│
└── venv/                          # Virtual environment
```

---

## 🔧 Configuration

### Email SMTP Settings
In `app.py`, update lines 120-125:
```python
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-16-digit-app-password'
```

### Weather API
Update `WEATHER_API_KEY` in `weather.html` (line 752)

### Default Location
In `weather.html`, modify lines 753-754:
```javascript
const DEFAULT_LAT = 4.1996;  // Your latitude
const DEFAULT_LON = 101.2570; // Your longitude
```

---

## 🤖 Machine Learning Model

### Model Details
- **Algorithm:** Random Forest Regressor
- **Training Data:** Historical irrigation data from agricultural studies
- **Features:** Temperature, Humidity, Rainfall, Soil Moisture, Crop Type, Growth Stage
- **Output:** Water requirement in liters per hectare

### Model Training
To retrain the model:
```bash
python train_model_advanced.py
```

The trained model is saved as `optimized_irrigation_model.pkl`

---

## 🌐 API Endpoints

### Authentication
- `POST /api/send-otp` - Send OTP to email
- `POST /api/verify-otp` - Verify OTP code
- `POST /api/reset-password` - Reset user password

### Predictions
- `POST /api/predict` - Get water usage prediction
  ```json
  {
    "temperature": 28.5,
    "humidity": 65.0,
    "rainfall": 10.0,
    "soil_moisture": 45.0,
    "crop_type": "Rice",
    "growth_stage": "Vegetative",
    "area": 2.5
  }
  ```

---

## 🐛 Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Check Firebase credentials file exists
- Verify all dependencies installed: `pip install -r requirements.txt`

### Email OTP not sending
- Check Gmail App Password is correct (16 digits, no spaces)
- Ensure 2FA is enabled on Google Account
- Verify SMTP settings in `app.py`

### Weather data not loading
- Verify OpenWeatherMap API key is valid
- Check internet connection
- Ensure API key is correctly set in `weather.html`

### Model prediction errors
- Ensure `optimized_irrigation_model.pkl` exists
- Check all input fields are filled correctly
- Verify numeric values are within valid ranges

---

## 📝 Future Enhancements

- [ ] Mobile application (iOS/Android)
- [ ] IoT sensor integration for real-time soil moisture
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Automated irrigation scheduling
- [ ] SMS/WhatsApp notifications
- [ ] Crop disease detection
- [ ] Integration with smart irrigation controllers

---

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenWeatherMap** - Weather data API
- **Firebase** - Authentication services
- **Scikit-learn** - Machine learning framework
- **Font Awesome** - Icon library
- **Google Fonts** - Typography

---

## 📞 Contact

**Faheem Haswan**
- GitHub: [@faheemhaswan](https://github.com/faheemhaswan)
- Email: faheem.hswn@gmail.com

**Project Link:** [https://github.com/faheemhaswan/fypWebPrediction](https://github.com/faheemhaswan/fypWebPrediction)

---

<div align="center">

**Made with ❤️ for sustainable agriculture**

⭐ Star this repository if you find it helpful!

</div>
