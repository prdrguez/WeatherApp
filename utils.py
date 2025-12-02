"""Funciones auxiliares para formato de datos."""
from __future__ import annotations

from datetime import datetime
from typing import Any

UNITS_LABELS = {
    "metric": "°C",
    "imperial": "°F",
}


def format_temperature(value: float | int | None, units: str) -> str:
    if value is None:
        return "-"
    return f"{value:.1f}{UNITS_LABELS.get(units, '')}"


def format_wind(value: float | int | None, units: str) -> str:
    if value is None:
        return "-"
    speed_unit = "m/s" if units == "metric" else "mph"
    return f"{value:.1f} {speed_unit}"


def format_datetime(dt: datetime | None) -> str:
    if not dt:
        return ""
    return dt.strftime("%d %b %Y, %H:%M")


def get_day_name(dt: datetime | None) -> str:
    if not dt:
        return ""
    return dt.strftime("%a")


def safe_get(data: dict[str, Any], key: str, default: Any = "-") -> Any:
    value = data.get(key)
    return default if value is None else value
