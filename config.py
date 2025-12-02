"""Configuración básica para la aplicación del clima."""
import os

# Coloca aquí tu API key de OpenWeatherMap. 
# Puedes reemplazar el valor por la clave real o establecerla como variable de entorno OPENWEATHER_API_KEY.
API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "TU_API_KEY_AQUI")

# URL base para obtener el clima actual desde OpenWeatherMap.
BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
