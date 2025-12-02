"""Probabilidad de lluvia por día."""
from __future__ import annotations

import flet as ft

from theme import WeatherTheme
from utils import get_day_name


def create_rain_probability_chart(rain_data: list[dict]) -> ft.Container:
    bars = []
    for entry in rain_data:
        probability = entry.get("probability", 0)
        bars.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                spacing=8,
                controls=[
                    ft.Text(get_day_name(entry.get("date")), width=32),
                    ft.ProgressBar(value=probability / 100 if probability else 0, width=180, color=WeatherTheme.ACCENT_SOFT),
                    ft.Text(f"{probability}%", width=40),
                ],
            )
        )

    return ft.Container(
        width=320,
        padding=16,
        bgcolor=WeatherTheme.CARD_COLOR,
        border_radius=WeatherTheme.RADIUS,
        shadow=WeatherTheme.BOX_SHADOW,
        content=ft.Column(
            spacing=10,
            controls=[ft.Text("Probabilidad de Lluvia", weight=ft.FontWeight.W_700), *bars],
        ),
    )
