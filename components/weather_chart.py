"""Gráfico de temperatura vs día."""
from __future__ import annotations

import flet as ft

from theme import WeatherTheme
from utils import get_day_name


def create_weather_chart(chart_data: list[dict]) -> ft.Container:
    points = []
    for entry in chart_data:
        label = get_day_name(entry.get("label"))
        value = entry.get("value") or 0
        points.append(ft.LineChartDataPoint(x=len(points), y=value, tooltip=f"{label}: {value:.1f}°"))

    series = [
        ft.LineChartData(
            color=WeatherTheme.ACCENT_SOFT,
            stroke_width=3,
            curved=True,
            data_points=points,
        )
    ]

    return ft.Container(
        expand=True,
        padding=16,
        bgcolor=WeatherTheme.CARD_COLOR,
        border_radius=WeatherTheme.RADIUS,
        shadow=WeatherTheme.BOX_SHADOW,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Pronóstico del Clima", weight=ft.FontWeight.W_700),
                ft.LineChart(
                    width=520,
                    height=240,
                    data_series=series,
                    left_axis=ft.ChartAxis(labels_size=32),
                    bottom_axis=ft.ChartAxis(
                        labels=[ft.ChartAxisLabel(value=i, label=ft.Text(get_day_name(entry.get("label")))) for i, entry in enumerate(chart_data)],
                        labels_size=32,
                    ),
                    tooltip_bgcolor=WeatherTheme.ACCENT_SOFT,
                ),
            ],
        ),
    )
