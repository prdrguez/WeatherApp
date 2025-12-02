"""Funciones para consultar el clima actual desde OpenWeatherMap."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import requests

from config import API_KEY, BASE_URL


class WeatherServiceError(Exception):
    """Errores específicos del servicio de clima."""


def _build_icon_url(icon_code: str | None) -> str:
    if not icon_code:
        return ""
    return f"https://openweathermap.org/img/wn/{icon_code}@4x.png"


def get_current_weather(city: str, units: str = "metric", lang: str = "es") -> Dict[str, Any]:
    """Obtiene el clima actual para una ciudad.

    Args:
        city: Nombre de la ciudad a consultar, por ejemplo "Buenos Aires,AR".
        units: Unidades de medida: "metric" (°C, m/s) o "imperial" (°F, mph).
        lang: Idioma para las descripciones del clima.

    Returns:
        Diccionario con los campos listos para mostrar en la UI.

    Raises:
        ValueError: Si la API key no está configurada o faltan datos de entrada.
        WeatherServiceError: Si la API responde con un error o los datos no son válidos.
    """

    if not city or not city.strip():
        raise ValueError("Por favor ingresa una ciudad para consultar el clima.")

    if not API_KEY or API_KEY == "TU_API_KEY_AQUI":
        raise ValueError(
            "API key no configurada. Establece la variable de entorno OPENWEATHER_API_KEY "
            "o reemplaza API_KEY en config.py."
        )

    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
        "lang": lang,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as exc:  # problemas de red
        raise WeatherServiceError("No se pudo conectar al servicio de clima.") from exc

    if response.status_code != 200:
        try:
            error_message = response.json().get("message", "Error desconocido")
        except ValueError:
            error_message = response.text or "Error desconocido"
        raise WeatherServiceError(f"Error desde la API: {error_message}")

    data = response.json()
    weather_list = data.get("weather", [])
    weather_info = weather_list[0] if weather_list else {}
    main_info = data.get("main", {})
    wind_info = data.get("wind", {})

    try:
        return {
            "city": data["name"],
            "country": data.get("sys", {}).get("country", ""),
            "temp": main_info.get("temp"),
            "temp_min": main_info.get("temp_min"),
            "temp_max": main_info.get("temp_max"),
            "feels_like": main_info.get("feels_like"),
            "description": weather_info.get("description", "").capitalize(),
            "humidity": main_info.get("humidity"),
            "wind_speed": wind_info.get("speed"),
            "icon_url": _build_icon_url(weather_info.get("icon")),
            "timestamp": datetime.fromtimestamp(data.get("dt", 0)),
            "units": units,
        }
    except KeyError as exc:  # falta de campos esenciales
        raise WeatherServiceError("Respuesta incompleta de la API de clima.") from exc
