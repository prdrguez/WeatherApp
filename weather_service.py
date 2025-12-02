"""Funciones para consultar datos de clima y componer el dashboard."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

import requests

from config import AIR_POLLUTION_URL, API_KEY, BASE_URL, FORECAST_URL


class WeatherServiceError(Exception):
    """Errores específicos del servicio de clima."""


def _build_icon_url(icon_code: str | None) -> str:
    if not icon_code:
        return ""
    return f"https://openweathermap.org/img/wn/{icon_code}@4x.png"


def _ensure_api_key() -> None:
    if not API_KEY or API_KEY == "TU_API_KEY_AQUI":
        raise ValueError(
            "API key no configurada. Establece la variable de entorno OPENWEATHER_API_KEY "
            "o reemplaza API_KEY en config.py."
        )


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

    _ensure_api_key()

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
    sys_info = data.get("sys", {})
    coord_info = data.get("coord", {})

    try:
        return {
            "city": data["name"],
            "country": sys_info.get("country", ""),
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
            "visibility": data.get("visibility"),
            "pressure": main_info.get("pressure"),
            "sunrise": datetime.fromtimestamp(sys_info.get("sunrise", 0)) if sys_info.get("sunrise") else None,
            "sunset": datetime.fromtimestamp(sys_info.get("sunset", 0)) if sys_info.get("sunset") else None,
            "lat": coord_info.get("lat"),
            "lon": coord_info.get("lon"),
        }
    except KeyError as exc:  # falta de campos esenciales
        raise WeatherServiceError("Respuesta incompleta de la API de clima.") from exc


def _fetch_forecast(city: str, units: str, lang: str = "es") -> List[Dict[str, Any]]:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
        "lang": lang,
    }
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
    parsed = []
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
    grouped: dict[str, list[Dict[str, Any]]] = defaultdict(list)
    for entry in forecast:
        grouped[entry["datetime"].date()].append(entry)

    daily = []
    for date_key, entries in grouped.items():
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


def _build_chart_data(daily: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {"label": entry["date"], "value": entry.get("temp")}
        for entry in daily
    ]


def _build_rain_probability(daily: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result = []
    for entry in daily:
        probability = int((entry.get("pop", 0) or 0) * 100)
        result.append({"date": entry["date"], "probability": probability})
    return result


def _get_air_quality(lat: float | None, lon: float | None) -> Dict[str, Any]:
    if lat is None or lon is None:
        return {
            "aqi": None,
            "label": "Sin datos",
            "value": None,
            "components": {},
        }

    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    try:
        response = requests.get(AIR_POLLUTION_URL, params=params, timeout=10)
    except requests.RequestException:
        return {
            "aqi": None,
            "label": "Sin conexión",
            "value": None,
            "components": {},
        }

    if response.status_code != 200:
        return {
            "aqi": None,
            "label": "No disponible",
            "value": None,
            "components": {},
        }

    data = response.json()
    first = data.get("list", [{}])[0]
    aqi_value = first.get("main", {}).get("aqi")
    components = first.get("components", {}) if isinstance(first, dict) else {}
    labels = {1: "Bueno", 2: "Aceptable", 3: "Moderado", 4: "Pobre", 5: "Muy Pobre"}
    return {
        "aqi": aqi_value,
        "label": labels.get(aqi_value, "Sin datos"),
        "value": aqi_value,
        "components": components,
    }


def get_dashboard_weather(city: str, units: str = "metric", lang: str = "es") -> Dict[str, Any]:
    """Devuelve toda la información necesaria para el dashboard."""

    current = get_current_weather(city, units, lang)
    forecast_raw = _fetch_forecast(city, units, lang)
    daily = _aggregate_daily(forecast_raw)
    chart_data = _build_chart_data(daily)
    rain_probability = _build_rain_probability(daily)
    air_quality = _get_air_quality(current.get("lat"), current.get("lon"))

    return {
        "current": current,
        "forecast": daily,
        "chart_data": chart_data,
        "air_quality": air_quality,
        "rain_probability": rain_probability,
    }

