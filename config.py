"""Configuración básica para la aplicación del clima."""
import os

# Coloca aquí tu API key de OpenWeatherMap.
# Puedes reemplazar el valor por la clave real o establecerla como variable de entorno OPENWEATHER_API_KEY.
API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "733285f73f4b152a0b891974fe21cbea")

# URL base para obtener el clima actual desde OpenWeatherMap.
BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"

# URL para obtener el pronóstico de 5 días / 3 horas.
FORECAST_URL: str = "https://api.openweathermap.org/data/2.5/forecast"

# URL para obtener datos de calidad del aire.
AIR_POLLUTION_URL: str = "https://api.openweathermap.org/data/2.5/air_pollution"
# Coloca aquí tu API key de OpenWeatherMap. 
# Puedes reemplazar el valor por la clave real o establecerla como variable de entorno OPENWEATHER_API_KEY.
API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "733285f73f4b152a0b891974fe21cbea")

# URL base para obtener el clima actual desde OpenWeatherMap.
BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
