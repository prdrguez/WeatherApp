"""Componentes de tarjetas y chips para el dashboard."""
from __future__ import annotations

from typing import Callable, Iterable

import flet as ft

from theme import WeatherTheme
from utils import UNITS_LABELS, format_temperature, format_wind


def create_info_card(title: str, value: str, icon: str, subtitle: str | None = None) -> ft.Container:
    subtitle_control = ft.Text(subtitle, size=12, color=WeatherTheme.TEXT_SECONDARY) if subtitle else None
    return ft.Container(
        padding=12,
        width=180,
        bgcolor=WeatherTheme.CARD_COLOR,
        border_radius=WeatherTheme.RADIUS,
        shadow=WeatherTheme.BOX_SHADOW,
        content=ft.Column(
            spacing=6,
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(title, size=14, weight=ft.FontWeight.W_600),
                        ft.Icon(icon, color=WeatherTheme.ACCENT_SOFT),
                    ],
                ),
                ft.Text(value, size=20, weight=ft.FontWeight.W_700),
                subtitle_control,
            ],
        ),
    )


def create_city_chip(city: str, temperature: float | int | None, units: str, on_click: Callable[[ft.ControlEvent], None]) -> ft.Chip:
    temp_label = format_temperature(temperature, units)
    return ft.Chip(
        label=ft.Row(
            spacing=6,
            controls=[ft.Text(city), ft.Text(temp_label, color=WeatherTheme.TEXT_SECONDARY, size=12)],
        ),
        bgcolor=ft.Colors.with_opacity(0.15, WeatherTheme.ACCENT_SOFT),
        on_click=on_click,
    )


def create_weather_day_card(day_name: str, icon_url: str, temp: float | int | None, description: str, units: str) -> ft.Container:
    return ft.Container(
        width=120,
        padding=12,
        bgcolor=WeatherTheme.CARD_COLOR,
        border_radius=WeatherTheme.RADIUS,
        shadow=WeatherTheme.BOX_SHADOW,
        content=ft.Column(
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(day_name, weight=ft.FontWeight.BOLD),
                ft.Image(src=icon_url, width=56, height=56, fit=ft.ImageFit.CONTAIN),
                ft.Text(format_temperature(temp, units), size=18, weight=ft.FontWeight.W_600),
                ft.Text(description, size=12, color=WeatherTheme.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
            ],
        ),
    )


def create_main_weather_card(
    city_value: str,
    weather_data: dict,
    units: str,
    favorites: Iterable[tuple[str, float | int | None]] | None,
    on_search: Callable[[str], None],
    on_refresh: Callable[[], None],
) -> ft.Container:
    temp_main = format_temperature(weather_data.get("temp"), units)
    description = weather_data.get("description", "")

    city_field = ft.TextField(
        value=city_value,
        label="Ciudad",
        prefix_icon=ft.Icons.LOCATION_ON_OUTLINED,
        border_radius=WeatherTheme.RADIUS,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        filled=True,
        on_submit=lambda e: on_search(e.control.value),
    )

    refresh_button = ft.IconButton(
        icon=ft.Icons.REFRESH,
        icon_color=WeatherTheme.TEXT_PRIMARY,
        on_click=lambda _: on_refresh(),
        tooltip="Actualizar",
    )

    search_button = ft.ElevatedButton(
        text="Buscar",
        icon=ft.Icons.SEARCH,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        color=WeatherTheme.TEXT_PRIMARY,
        on_click=lambda _: on_search(city_field.value),
    )

    chips = []
    if favorites:
        for city_name, temp in favorites:
            chips.append(
                create_city_chip(
                    city_name,
                    temp,
                    units,
                    on_click=lambda e, city=city_name: on_search(city),
                )
            )

    return ft.Container(
        padding=20,
        width=520,
        bgcolor=WeatherTheme.ACCENT_ORANGE,
        border_radius=24,
        shadow=WeatherTheme.BOX_SHADOW,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[city_field, refresh_button],
                ),
                ft.Text("Última actualización, Hoy", size=12, color=ft.Colors.WHITE70),
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    controls=[
                        ft.Text(temp_main, size=46, weight=ft.FontWeight.W_800, color=ft.Colors.WHITE),
                        ft.Text(description, size=16, color=ft.Colors.WHITE70),
                        search_button,
                    ],
                ),
                ft.Wrap(run_spacing=8, spacing=8, controls=chips),
            ],
        ),
    )


def create_sun_card(sunrise: str, sunset: str) -> ft.Container:
    return ft.Container(
        width=220,
        padding=16,
        bgcolor=WeatherTheme.CARD_COLOR,
        border_radius=WeatherTheme.RADIUS,
        shadow=WeatherTheme.BOX_SHADOW,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Amanecer y Atardecer", weight=ft.FontWeight.W_700),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, color=WeatherTheme.ACCENT_SOFT),
                        ft.Column(
                            controls=[
                                ft.Text(f"Amanecer: {sunrise}", size=13),
                                ft.Text(f"Atardecer: {sunset}", size=13),
                            ]
                        ),
                    ],
                ),
            ],
        ),
    )
