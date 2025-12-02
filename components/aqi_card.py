"""Tarjeta de calidad de aire."""
from __future__ import annotations

import flet as ft

from theme import WeatherTheme


def create_aqi_card(aqi_data: dict) -> ft.Container:
    value = aqi_data.get("value") or aqi_data.get("aqi")
    label = aqi_data.get("label", "Sin datos")
    components = aqi_data.get("components", {})

    pollutants = []
    for key in ["pm10", "pm2_5", "o3", "co", "so2", "no2"]:
        val = components.get(key)
        pollutants.append(ft.Text(f"{key.upper()}: {val if val is not None else '-'}", size=12))

    return ft.Container(
        bgcolor=WeatherTheme.CARD_COLOR,
        padding=16,
        width=320,
        border_radius=WeatherTheme.RADIUS,
        shadow=WeatherTheme.BOX_SHADOW,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Resumen de Calidad del Aire", weight=ft.FontWeight.W_700),
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.CircleAvatar(
                            radius=32,
                            bgcolor=WeatherTheme.ACCENT_SOFT,
                            content=ft.Text(str(value) if value is not None else "-", weight=ft.FontWeight.W_800),
                        ),
                        ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(label, size=16, weight=ft.FontWeight.W_600),
                                ft.Text("Valores en µg/m³", size=12, color=WeatherTheme.TEXT_SECONDARY),
                            ],
                        ),
                    ],
                ),
                ft.Wrap(spacing=8, run_spacing=6, controls=pollutants),
            ],
        ),
    )
