# AquaWise - Smart Irrigation Prediction System

<div align="center">

![AquaWise Logo](assets/aquawise_logo.png)

**AI-Powered Water Usage Prediction for Sustainable Agriculture**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Admin-orange.svg)](https://firebase.google.com/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-red.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots)

</div>

---

## 📖 About The Project

**AquaWise** is an intelligent irrigation management system that leverages machine learning to predict optimal water usage for agricultural crops. By analyzing environmental factors such as temperature, humidity, rainfall, and soil moisture, AquaWise helps farmers make data-driven irrigation decisions, conserve water, and maximize crop yield.

### 🎯 Problem Statement
- **Water Scarcity:** Increasing demand and limited supply affect agricultural productivity.
- **Inefficient Practices:** Manual irrigation often leads to over-watering or under-watering.
- **Lack of Data:** Farmers struggle to make informed decisions without real-time environmental insights.
- **Planning Challenges:** Difficulty in predicting optimal irrigation schedules based on future weather.

### 💡 Solution
AquaWise provides a comprehensive solution:
- **AI-Powered Predictions:** Utilizes a Random Forest Regressor model to calculate precise water requirements.
- **Smart Recommendations:** Tailored advice based on specific crop types and growth stages.
- **Historical Analytics:** Tracks irrigation patterns and water consumption over time.
- **Integrated Weather Forecasts:** 5-day weather data to support proactive planning.
- **User-Centric Design:** Modern, responsive interface with intuitive dashboards.

---

## ✨ Features

### 🔐 Robust Authentication
- **Secure Login/Signup:** Firebase Authentication ensures user data privacy.
- **Email Verification:** Two-factor authentication for password resets via SMTP OTP.
- **Session Management:** Secure, persistent user sessions with auto-logout.

### 🌾 Intelligent Predictions
- **ML Engine:** Scikit-learn Random Forest model trained on agricultural datasets.
- **Multi-Factor Analysis:** Considers temperature, humidity, rainfall, soil moisture, crop type, and field size.
- **Real-Time Calculation:** Instant water usage predictions in liters per hectare.
- **Actionable Advice:** AI-generated recommendations for optimal irrigation strategies.

### 📊 comprehensive Analytics Dashboard
- **Visual Overview:** Real-time system status and key metrics at a glance.
- **Historical Data:** detailed records of past predictions and irrigation activities.
- **Trend Analysis:** Charts and graphs to visualize water usage patterns.
- **Efficiency Metrics:** Comparative analysis of actual vs. predicted water usage.

### 🌤️ Weather Integration
- **Real-Time Data:** Integration with OpenWeatherMap API for current conditions.
- **5-Day Forecast:** Detailed weather predictions to aid longer-term planning.
- **Location Awareness:** Automatic or manual location selection for precise weather data.
- **Smart Alerts:** Weather-based notifications for rainfall or extreme conditions.

### ⚙️ User Management
- **Profile Customization:** Update personal details and display preferences.
- **Settings Dashboard:** Configure default crop types, field sizes, and notification preferences.
- **Data Management:** Tools to export history or reset account data.

---

## 🛠️ Tech Stack

### Frontend
- **HTML5 & CSS3:** Semantic structure with modern, responsive styling using custom CSS variables and glassmorphism effects.
- **JavaScript (ES6+):** Dynamic client-side logic for interactivity and API communication.
- **Font Awesome:** Comprehensive icon library for visual enhancement.
- **Google Fonts:** 'Outfit' and 'Plus Jakarta Sans' for professional typography.

### Backend
- **Python 3.9+:** Robust server-side logic and ML integration.
- **Flask:** Lightweight and efficient web framework for the RESTful API.
- **Flask-CORS:** Handling Cross-Origin Resource Sharing for secure frontend-backend communication.

### Machine Learning
- **Scikit-learn:** Implementation of the Random Forest Regressor algorithm.
- **Pandas & NumPy:** Efficient data manipulation and numerical analysis.
- **Pickle:** Model serialization for deployment.

### Database & Services
- **Firebase:** Real-time database and secure user authentication.
- **OpenWeatherMap API:** Third-party service for accurate weather data.
- **SMTP (Gmail):** Email service for OTP delivery and notifications.

### Development Tools
- **Git:** Version control system.
- **VS Code:** Integrated Development Environment.

---

## 📋 Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.9 or higher:** [Download Python](https://www.python.org/downloads/)
- **pip:** Python package manager (included with Python).
- **Git:** [Download Git](https://git-scm.com/downloads)
- **Firebase Account:** A valid Firebase project configuration.
- **OpenWeatherMap API Key:** A free API key for weather data.
- **Gmail Account:** An App Password for SMTP functionality.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/faheemhaswan/fypWebPrediction.git
cd smart_irrigation_project
```

### 2. Set Up Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Firebase
1.  Go to the [Firebase Console](https://console.firebase.google.com/).
2.  Create a project or select an existing one.
3.  Navigate to **Project Settings > Service Accounts**.
4.  Click **Generate New Private Key**.
5.  Rename the downloaded JSON file to `smart-irrigation-system-3a5ff-firebase-adminsdk-fbsvc-9a698da30d.json` and place it in the project root.

### 5. Configure Environment Variables
Create a `.env` file or update the configuration directly in `app.py`:
```python
# app.py settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-app-password'
```

### 6. Update API Keys
In `weather.html` (and other relevant files), update the API key:
```javascript
const WEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY';
```

---

## 💻 Usage

### Starting the Application

#### Option 1: Quick Start (Windows)
Run the provided batch script:
```bash
.\run_backend.bat
```

#### Option 2: Manual Start
1.  Activate your virtual environment.
2.  Run the Flask server:
    ```bash
    python app.py
    ```
3.  The backend API will start at `http://localhost:5000`.

### Accessing the Interface
1.  For the best experience, use a local web server for the frontend files.
    ```bash
    python -m http.server 8000
    ```
2.  Open your browser and navigate to `http://localhost:8000`.
3.  Log in or sign up to start using AquaWise.

---

## 📸 Screenshots

*(Screenshots to be added here)*

- **Login Page:** Secure access point.
- **Dashboard:** Central hub for all activities.
- **Prediction Tool:** Input parameters and get results.
- **Weather Forecast:** Upcoming weather conditions.

---

## 🗂️ Project Structure

```
smart_irrigation_project/
├── app.py                          # Main Flask application and API routes
├── run_backend.bat                 # Windows startup script
├── requirements.txt                # Python package dependencies
├── optimized_irrigation_model.pkl  # Trained Random Forest model
├── smart-irrigation-system-*.json  # Firebase Admin SDK credentials
│
├── index.html                      # Landing page (Login/Signup)
├── dashboard.html                  # User Dashboard
├── predict.html                    # Prediction Interface
├── history.html                    # Prediction History & Analytics
├── weather.html                    # Weather Forecast Page
├── settings.html                   # User Settings & Profile
├── 404.html                        # Error Page
│
├── css/                            # Stylesheets
│   └── style.css
├── assets/                         # Images, icons, and static assets
│   ├── aquawise_logo.png
│   ├── background.png
│   └── professional-ui.css         # Shared UI styles
│
├── datasets/                       # Data used for training and testing
│   ├── irrigation_dataset.csv
│   └── adapted_data.csv
│
├── model_advanced/                 # Advanced model training scripts and artifacts
├── retrain_model.py                # Utility script for model retraining
└── venv/                           # Python Virtual Environment
```

---

## 🔧 Maintenance

### Retraining the Model
If you need to update the model with new data or fix compatibility issues:
1.  Ensure your dataset is in the `datasets/` folder.
2.  Run the retraining script:
    ```bash
    python retrain_model.py
    ```
3.  The `optimized_irrigation_model.pkl` file will be updated.

### Troubleshooting
-   **Server Errors:** Check the terminal output for Python tracebacks.
-   **API Issues:** Verify your network connection and API keys.
-   **Database:** Ensure your Firebase security rules allow read/write access as configured.

---

## 👥 Contributing

Contributions are welcome!
1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/NewFeature`).
3.  Commit your changes (`git commit -m 'Add some NewFeature'`).
4.  Push to the branch (`git push origin feature/NewFeature`).
5.  Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

**Muhammad Faheem Bin Haswanorrizam**
-   **Student ID:** CDCS2306B
-   **Course:** CSP650
-   **GitHub:** [@faheemhaswan](https://github.com/faheemhaswan)
-   **Email:** faheem.hswn@gmail.com

**Project Link:** [https://github.com/faheemhaswan/fypWebPrediction](https://github.com/faheemhaswan/fypWebPrediction)
