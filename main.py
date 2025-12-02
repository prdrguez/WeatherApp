"""Punto de entrada para la Dashboard del Clima moderna."""
from __future__ import annotations

import flet as ft

from pages.home import HomePage
from theme import WeatherTheme
from weather_service import WeatherServiceError, get_dashboard_weather


def main(page: ft.Page) -> None:
    page.title = "Dashboard del Clima"
    page.window_width = 1200
    page.window_height = 900
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    status_text = ft.Text(color=ft.colors.RED_200, size=12)
    content_host = ft.Container(expand=True)
    loading_overlay = ft.Container(
        visible=False,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.with_opacity(0.25, ft.colors.BLACK),
        content=ft.ProgressRing(width=64, height=64, color=WeatherTheme.ACCENT_SOFT),
    )

    units_dropdown = ft.Dropdown(
        label="Unidades",
        options=[
            ft.dropdown.Option("metric", "Métrico (°C, m/s)"),
            ft.dropdown.Option("imperial", "Imperial (°F, mph)"),
        ],
        value="metric",
        width=220,
    )

    current_city = {"value": "Buenos Aires,AR"}

    def set_status(message: str, color: str = ft.colors.RED_200) -> None:
        status_text.value = message
        status_text.color = color
        status_text.update()

    def clear_status() -> None:
        set_status("")

    def render_dashboard(data: dict) -> None:
        home = HomePage(page, data, on_search_callback=handle_search, on_refresh_callback=handle_refresh)
        content_host.content = home.build()
        page.update()

    def load_weather(city: str, units: str) -> None:
        clear_status()
        loading_overlay.visible = True
        page.update()
        try:
            data = get_dashboard_weather(city, units)
        except ValueError as exc:
            set_status(str(exc))
            return
        except WeatherServiceError as exc:
            set_status(str(exc))
            return
        else:
            set_status("Datos actualizados", ft.colors.GREEN_ACCENT_200)
            render_dashboard(data)
        finally:
            loading_overlay.visible = False
            page.update()

    def handle_search(city: str) -> None:
        if not city:
            set_status("Ingresa una ciudad para buscar.")
            return
        current_city["value"] = city
        load_weather(city, units_dropdown.value)

    def handle_refresh() -> None:
        load_weather(current_city["value"], units_dropdown.value)

    def handle_units_change(e: ft.ControlEvent) -> None:
        handle_refresh()

    units_dropdown.on_change = handle_units_change

    header = ft.Container(
        padding=16,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Dashboard del Clima", size=24, weight=ft.FontWeight.W_800),
                        ft.Text("Consulta el clima actual y próximo en un vistazo.", size=13, color=WeatherTheme.TEXT_SECONDARY),
                    ],
                ),
                ft.Row(spacing=12, controls=[units_dropdown, status_text]),
            ],
        ),
    )

    layout = ft.Column(spacing=0, controls=[header, content_host])
    page.add(
        ft.Stack(
            controls=[layout, loading_overlay],
            expand=True,
        )
    )

    # Cargar datos iniciales
    handle_refresh()


if __name__ == "__main__":
    ft.app(target=main)
