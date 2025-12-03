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

    _en_
