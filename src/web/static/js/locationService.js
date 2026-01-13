/**
 * SHARED LOCATION SERVICE
 * Use this across predict.html and weather.html for consistent location detection
 * Save this as: locationService.js (in your root directory)
 */

const LocationService = {
  // Configuration
  ACCURACY_THRESHOLD: 50, // meters - only accept locations accurate to 50m or better
  TIMEOUT: 20000, // 20 seconds max wait for GPS fix
  REFRESH_INTERVAL: 300000, // Auto-refresh every 5 minutes
  WEATHER_API_KEY: '7941d1d68e6c2211e4eac4a66bab0097',

  // Current location state
  location: {
    latitude: null,
    longitude: null,
    accuracy: null,
    locationName: null,
    source: 'none', // 'auto', 'manual', or 'none'
    lastUpdate: null
  },

  // Weather data cache
  weatherData: {
    current: null,
    forecast: null,
    lastUpdate: null
  },

  /**
   * Initialize the location service
   * Call this once when page loads
   */
  init() {
    console.log('LocationService initialized');
    this.restoreLocationFromStorage();
    this.autoRefreshLocation();
  },

  /**
   * Get current location with high accuracy
   * Returns a Promise that resolves with location object
   */
  async getCurrentLocation() {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation not supported'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const accuracy = position.coords.accuracy;

          // CRITICAL: Reject inaccurate locations
          if (accuracy > this.ACCURACY_THRESHOLD) {
            console.warn(`Location rejected: Accuracy ${accuracy.toFixed(0)}m exceeds threshold ${this.ACCURACY_THRESHOLD}m`);
            reject(new Error(`Accuracy too low: ${accuracy.toFixed(0)}m (need ${this.ACCURACY_THRESHOLD}m or better)`));
            return;
          }

          // Location passed accuracy check
          this.location.latitude = position.coords.latitude;
          this.location.longitude = position.coords.longitude;
          this.location.accuracy = accuracy;
          this.location.source = 'auto';
          this.location.lastUpdate = new Date();

          console.log(`✅ High-accuracy location obtained: ${this.location.latitude.toFixed(6)}, ${this.location.longitude.toFixed(6)} (${accuracy.toFixed(0)}m)`);

          this.saveLocationToStorage();
          this.reverseGeocode();
          resolve(this.location);
        },
        (error) => {
          console.error('Geolocation error:', error);
          const errorMsg = this.getGeolocationsErrorMessage(error);
          reject(new Error(errorMsg));
        },
        {
          enableHighAccuracy: true, // Force GPS/cellular for accuracy
          timeout: this.TIMEOUT,
          maximumAge: 0 // Don't use cached location - get fresh fix
        }
      );
    });
  },

  /**
   * Perform reverse geocoding to get location name
   */
  async reverseGeocode() {
    if (!this.location.latitude || !this.location.longitude) {
      return;
    }

    const geoUrl = `https://api.openweathermap.org/geo/1.0/reverse?lat=${this.location.latitude}&lon=${this.location.longitude}&limit=1&appid=${this.WEATHER_API_KEY}`;

    try {
      const response = await fetch(geoUrl);
      if (!response.ok) throw new Error('Geo API failed');

      const data = await response.json();
      if (data && data.length > 0) {
        const geo = data[0];
        const city = geo.name || '';
        const state = geo.state || '';
        const country = geo.country || '';

        // Intelligent naming
        if (city && state) {
          this.location.locationName = `${city}, ${state}`;
        } else if (city) {
          this.location.locationName = `${city}, ${country}`;
        } else if (state) {
          this.location.locationName = `${state}, ${country}`;
        } else {
          this.location.locationName = country;
        }
      }

      this.saveLocationToStorage();
      console.log(`📍 Location name: ${this.location.locationName}`);
    } catch (error) {
      console.warn('Reverse geocoding failed:', error);
      this.location.locationName = `${this.location.latitude.toFixed(4)}, ${this.location.longitude.toFixed(4)}`;
    }
  },

  /**
   * Fetch weather data for current location
   */
  async fetchWeatherData() {
    if (!this.location.latitude || !this.location.longitude) {
      return null;
    }

    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${this.location.latitude}&lon=${this.location.longitude}&appid=${this.WEATHER_API_KEY}&units=metric`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Weather API failed');

      this.weatherData.current = await response.json();
      this.weatherData.lastUpdate = new Date();
      this.saveWeatherToStorage();
      return this.weatherData.current;
    } catch (error) {
      console.error('Weather fetch error:', error);
      return null;
    }
  },

  /**
   * Fetch 5-day forecast for current location
   */
  async fetchForecastData() {
    if (!this.location.latitude || !this.location.longitude) {
      return null;
    }

    const url = `https://api.openweathermap.org/data/2.5/forecast?lat=${this.location.latitude}&lon=${this.location.longitude}&appid=${this.WEATHER_API_KEY}&units=metric`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Forecast API failed');

      this.weatherData.forecast = await response.json();
      this.weatherData.lastUpdate = new Date();
      this.saveWeatherToStorage();
      return this.weatherData.forecast;
    } catch (error) {
      console.error('Forecast fetch error:', error);
      return null;
    }
  },

  /**
   * Get all weather data (current + forecast) in one call
   */
  async getAllWeatherData() {
    const current = await this.fetchWeatherData();
    const forecast = await this.fetchForecastData();
    return { current, forecast };
  },

  /**
   * Auto-refresh location every 5 minutes
   */
  autoRefreshLocation() {
    setInterval(() => {
      this.getCurrentLocation().catch(err => console.warn('Auto-refresh location failed:', err));
    }, this.REFRESH_INTERVAL);
  },

  /**
   * Save location to localStorage for persistence
   */
  saveLocationToStorage() {
    localStorage.setItem('userLocation', JSON.stringify({
      latitude: this.location.latitude,
      longitude: this.location.longitude,
      accuracy: this.location.accuracy,
      locationName: this.location.locationName,
      source: this.location.source,
      lastUpdate: this.location.lastUpdate
    }));
  },

  /**
   * Restore location from localStorage
   */
  restoreLocationFromStorage() {
    const stored = localStorage.getItem('userLocation');
    if (stored) {
      const data = JSON.parse(stored);
      this.location = { ...data };
      console.log('📍 Location restored from storage');
    }
  },

  /**
   * Save weather to localStorage for persistence
   */
  saveWeatherToStorage() {
    localStorage.setItem('weatherData', JSON.stringify({
      current: this.weatherData.current,
      forecast: this.weatherData.forecast,
      lastUpdate: this.weatherData.lastUpdate
    }));
  },

  /**
   * Restore weather from localStorage
   */
  restoreWeatherFromStorage() {
    const stored = localStorage.getItem('weatherData');
    if (stored) {
      const data = JSON.parse(stored);
      this.weatherData = { ...data };
      console.log('🌤️ Weather data restored from storage');
    }
  },

  /**
   * Get friendly error message
   */
  getGeolocationsErrorMessage(error) {
    switch (error.code) {
      case error.PERMISSION_DENIED:
        return 'Location access denied. Please enable location permissions.';
      case error.TIMEOUT:
        return `Location request timed out (${this.TIMEOUT / 1000}s). Could not get accurate fix. Try again outdoors.`;
      case error.POSITION_UNAVAILABLE:
        return 'Location data unavailable.';
      default:
        return 'An unexpected geolocation error occurred.';
    }
  },

  /**
   * Check if location is valid and recent
   */
  isLocationValid(maxAgeMins = 5) {
    if (!this.location.latitude || !this.location.longitude) {
      return false;
    }
    
    if (this.location.lastUpdate) {
      const ageMs = Date.now() - new Date(this.location.lastUpdate).getTime();
      const ageMinutes = ageMs / 60000;
      return ageMinutes < maxAgeMins;
    }

    return true;
  },

  /**
   * Get formatted location string for display
   */
  getDisplayLocation() {
    if (this.location.locationName) {
      return this.location.locationName;
    }
    if (this.location.latitude && this.location.longitude) {
      return `${this.location.latitude.toFixed(6)}, ${this.location.longitude.toFixed(6)}`;
    }
    return 'Location not detected';
  },

  /**
   * Get formatted coordinates string
   */
  getCoordinatesString() {
    if (this.location.latitude && this.location.longitude) {
      return `Lat: ${this.location.latitude.toFixed(6)}, Lon: ${this.location.longitude.toFixed(6)}`;
    }
    return 'Lat: --, Lon: --';
  },

  /**
   * Get accuracy string
   */
  getAccuracyString() {
    if (this.location.accuracy !== null) {
      return `Accuracy: ${this.location.accuracy.toFixed(0)} meters`;
    }
    return 'Accuracy: --';
  }
};

// Initialize when script loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => LocationService.init());
} else {
  LocationService.init();
}