"""Funciones para consultar datos de clima y componer el dashboard."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

import requests

from config import API_KEY, BASE_URL, FORECAST_URL, AIR_POLLUTION_URL


class WeatherServiceError(Exception):
    """Errores específicos del servicio de clima."""


# ---------------------------------------------------------------------------
# Helpers generales
# ---------------------------------------------------------------------------

def _build_icon_url(icon_code: str | None) -> str:
    """Construye la URL del ícono de OpenWeatherMap."""
    if not icon_code:
        return ""
    return f"https://openweathermap.org/img/wn/{icon_code}@4x.png"


def _ensure_api_key() -> None:
    """Verifica que la API key esté configurada."""
    if not API_KEY or API_KEY == "TU_API_KEY_AQUI":
        raise ValueError(
            "API key no configurada. Establece la variable de entorno "
            "OPENWEATHER_API_KEY o reemplaza API_KEY en config.py."
        )


# ---------------------------------------------------------------------------
# Clima actual
# ---------------------------------------------------------------------------

def get_current_weather(
    city: str,
    units: str = "metric",
    lang: str = "es",
) -> Dict[str, Any]:
    """Obtiene el clima actual para una ciudad.

    Args:
        city: Nombre de la ciudad (ej. 'Buenos Aires,AR').
        units: 'metric' (°C, m/s) o 'imperial' (°F, mph).
        lang: Idioma de las descripciones.

    Raises:
        ValueError: Si hay parámetros inválidos o falta la API key.
        WeatherServiceError: Si la API falla o devuelve datos inválidos.
    """
    if not city or not city.strip():
        raise ValueError("Por favor ingresa una ciudad para consultar el clima.")

    _ensure_api_key()

    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
        "lang": lang,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException as exc:
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
    sys_info = data.get("sys", {})
    coord_info = data.get("coord", {})

    try:
        return {
            "city": data.get("name", city),
            "country": sys_info.get("country", ""),
            "temp": main_info.get("temp"),
            "temp_min": main_info.get("temp_min"),
            "temp_max": main_info.get("temp_max"),
            "feels_like": main_info.get("feels_like"),
            "description": weather_info.get("description", "").capitalize(),
            "humidity": main_info.get("humidity"),
            "wind_speed": wind_info.get("speed"),
            "icon_url": _build_icon_url(weather_info.get("icon")),
            "timestamp": datetime.fromtimestamp(data.get("dt", 0))
            if data.get("dt")
            else datetime.now(),
            "units": units,
            # Extras para el dashboard:
            "visibility": data.get("visibility"),
            "pressure": main_info.get("pressure"),
            "sunrise": datetime.fromtimestamp(sys_info.get("sunrise", 0))
            if sys_info.get("sunrise")
            else None,
            "sunset": datetime.fromtimestamp(sys_info.get("sunset", 0))
            if sys_info.get("sunset")
            else None,
            "lat": coord_info.get("lat"),
            "lon": coord_info.get("lon"),
        }
    except KeyError as exc:
        raise WeatherServiceError("Respuesta incompleta de la API de clima.") from exc


# ---------------------------------------------------------------------------
# Pronóstico 5 días y datos derivados
# ---------------------------------------------------------------------------

def _fetch_forecast(city: str, units: str, lang: str = "es") -> List[Dict[str, Any]]:
    """Obtiene el pronóstico de 5 días / 3 horas y lo parsea a una lista simple."""
    _ensure_api_key()

    params = {"q": city, "appid": API_KEY, "units": units, "lang": lang}

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
    except requests.RequestException as exc:
        raise WeatherServiceError("No se pudo obtener el pronóstico de clima.") from exc

    if response.status_code != 200:
        try:
            error_message = response.json().get("message", "Error desconocido")
        except ValueError:
            error_message = response.text or "Error desconocido"
        raise WeatherServiceError(f"Error en pronóstico: {error_message}")

    data = response.json()
    forecast_list = data.get("list", [])

    parsed: List[Dict[str, Any]] = []
    for item in forecast_list:
        dt = datetime.fromtimestamp(item.get("dt", 0))
        weather = item.get("weather", [{}])[0] if item.get("weather") else {}
        parsed.append(
            {
                "datetime": dt,
                "temp": item.get("main", {}).get("temp"),
                "description": weather.get("description", ""),
                "icon_url": _build_icon_url(weather.get("icon")),
                "pop": item.get("pop", 0),
            }
        )

    return parsed


def _aggregate_daily(forecast: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Agrupa la lista de pronóstico en entradas diarias (1 por día)."""
    grouped: dict[datetime.date, list[Dict[str, Any]]] = defaultdict(list)
    for entry in forecast:
        grouped[entry["datetime"].date()].append(entry)

    daily: List[Dict[str, Any]] = []
    for date_key, entries in grouped.items():
        # Preferimos la lectura alrededor del mediodía
        target = None
        for e in entries:
            if e["datetime"].hour == 12:
                target = e
                break
        if not target:
            target = entries[len(entries) // 2]

        daily.append(
            {
                "date": target["datetime"],
                "temp": target.get("temp"),
                "description": target.get("description", "").capitalize(),
                "icon_url": target.get("icon_url", ""),
                "pop": target.get("pop", 0),
            }
        )

    daily.sort(key=lambda x: x["date"])
    return daily


def _build_chart_data(daily: List_
