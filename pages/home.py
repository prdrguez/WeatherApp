"""Página principal del dashboard."""
from __future__ import annotations

from typing import Callable

import flet as ft

from components.aqi_card import create_aqi_card
from components.info_card import (
    create_city_chip,
    create_info_card,
    create_main_weather_card,
    create_sun_card,
    create_weather_day_card,
)
from components.rain_chart import create_rain_probability_chart
from components.weather_chart import create_weather_chart
from theme import WeatherTheme
from utils import format_datetime, format_temperature, format_wind, get_day_name, safe_get


class HomePage:
    """Orquesta el layout del dashboard principal."""

    def __init__(
        self,
        page: ft.Page,
        weather_data: dict,
        on_search_callback: Callable[[str], None],
        on_refresh_callback: Callable[[], None],
    ) -> None:
        self.page = page
        self.weather_data = weather_data
        self.on_search_callback = on_search_callback
        self.on_refresh_callback = on_refresh_callback

    def _build_forecast_cards(self) -> ft.Row:
        forecast = self.weather_data.get("forecast", [])
        current_units = safe_get(self.weather_data.get("current", {}), "units", "metric")
        cards = []
        for entry in forecast[:5]:
            cards.append(
                create_weather_day_card(
                    day_name=get_day_name(entry.get("date")),
                    icon_url=entry.get("icon_url", ""),
                    temp=entry.get("temp"),
                    description=entry.get("description", ""),
                    units=current_units,
                )
            )
        return ft.Row(spacing=12, controls=cards, wrap=True)

    def _build_metrics(self) -> ft.Wrap:
        current = self.weather_data.get("current", {})
        units = safe_get(current, "units", "metric")
        metrics = [
            create_info_card("Humedad", f"{safe_get(current, 'humidity', '-')}%", ft.Icons.WATER_DROP_OUTLINED),
            create_info_card("Viento", format_wind(current.get("wind_speed"), units), ft.Icons.AIR_OUTLINED),
            create_info_card("Visibilidad", f"{safe_get(current, 'visibility', '-')} m", ft.Icons.VISIBILITY_OUTLINED),
            create_info_card("Presión", f"{safe_get(current, 'pressure', '-')} hPa", ft.Icons.SPEED_OUTLINED),
            create_info_card("Índice UV", str(safe_get(current, 'uvi', '-')), ft.Icons.WB_SUNNY_OUTLINED),
            create_info_card("Precipitación", f"{safe_get(current, 'precipitation', '-')}%", ft.Icons.UMBRELLA_OUTLINED),
        ]
        return ft.Wrap(spacing=12, run_spacing=12, controls=metrics)

    def build(self) -> ft.Control:
        current = self.weather_data.get("current", {})
        units = safe_get(current, "units", "metric")
        chart_data = self.weather_data.get("chart_data", [])
        rain_probability = self.weather_data.get("rain_probability", [])
        air_quality = self.weather_data.get("air_quality", {})

        favorites = [
            (current.get("city", "Ciudad"), current.get("temp")),
            ("Arequipa", None),
            ("London", None),
            ("Cusco", None),
        ]

        main_card = create_main_weather_card(
            city_value=current.get("city", ""),
            weather_data=current,
            units=units,
            favorites=favorites,
            on_search=self.on_search_callback,
            on_refresh=self.on_refresh_callback,
        )

        sunrise = format_datetime(current.get("sunrise"))
        sunset = format_datetime(current.get("sunset"))

        layout = ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    spacing=16,
                    wrap=True,
                    controls=[main_card, ft.Column(spacing=12, controls=[self._build_forecast_cards()])],
                ),
                ft.Row(
                    spacing=16,
                    wrap=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        create_weather_chart(chart_data),
                        create_sun_card(sunrise or "-", sunset or "-"),
                    ],
                ),
                ft.Row(
                    spacing=16,
                    wrap=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(spacing=12, controls=[self._build_metrics(), create_rain_probability_chart(rain_probability)]),
                        create_aqi_card(air_quality),
                    ],
                ),
            ],
        )

        return ft.Container(
            expand=True,
            padding=WeatherTheme.PADDING,
            gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=WeatherTheme.BG_GRADIENT),
            content=layout,
        )
