"""Punto de entrada para la Dashboard del Clima."""
import flet as ft
from flet import colors

from weather_service import WeatherServiceError, get_current_weather


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


def build_stat_block(icon: str, label: str, value: str) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=18, color=colors.AMBER_200),
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(label, size=12, color=colors.GREY_400),
                        ft.Text(value, weight=ft.FontWeight.BOLD, size=14),
                    ],
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


def build_weather_card(data: dict) -> ft.Card:
    units = data.get("units", "metric")
    temp_main = format_temperature(data.get("temp"), units)
    temp_min = format_temperature(data.get("temp_min"), units)
    temp_max = format_temperature(data.get("temp_max"), units)
    feels_like = format_temperature(data.get("feels_like"), units)

    return ft.Card(
        elevation=8,
        color=colors.with_opacity(0.08, colors.WHITE),
        surface_tint_color=colors.BLUE_GREY_900,
        shape=ft.RoundedRectangleBorder(radius=24),
        content=ft.Container(
            padding=24,
            width=420,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[colors.with_opacity(0.7, colors.BLUE_900), colors.BLUE_GREY_900],
            ),
            border_radius=20,
            content=ft.Column(
                spacing=18,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        f"{data.get('city', '')}, {data.get('country', '')}",
                                        size=20,
                                        weight=ft.FontWeight.W_700,
                                    ),
                                    ft.Text(
                                        data.get("timestamp", "").strftime("%d %b %Y, %H:%M")
                                        if data.get("timestamp")
                                        else "",
                                        size=12,
                                        color=colors.GREY_400,
                                    ),
                                ],
                            ),
                            ft.Icon(ft.icons.LOCATION_ON_OUTLINED, color=colors.AMBER_200),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=16,
                        controls=[
                            ft.Image(
                                src=data.get("icon_url"),
                                width=96,
                                height=96,
                                fit=ft.ImageFit.CONTAIN,
                                error_content=ft.Icon(ft.icons.CLOUD_OUTLINED, size=72),
                            ),
                            ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text(temp_main, size=48, weight=ft.FontWeight.W_700),
                                    ft.Text(
                                        data.get("description", ""),
                                        size=16,
                                        color=colors.GREY_300,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            build_stat_block(ft.icons.ARROW_CIRCLE_DOWN_OUTLINED, "Mín", temp_min),
                            build_stat_block(ft.icons.ARROW_CIRCLE_UP_OUTLINED, "Máx", temp_max),
                            build_stat_block(ft.icons.DEVICE_THERMOSTAT, "Sensación", feels_like),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            build_stat_block(ft.icons.WATER_DROP_OUTLINED, "Humedad", f"{data.get('humidity', '-')}%"),
                            build_stat_block(ft.icons.AIR_OUTLINED, "Viento", format_wind(data.get("wind_speed"), units)),
                        ],
                    ),
                ],
            ),
        ),
    )


def main(page: ft.Page) -> None:
    page.title = "Dashboard del Clima"
    page.window_width = 480
    page.window_height = 720
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 24

    status_text = ft.Text(color=colors.RED_200, size=12)
    city_input = ft.TextField(
        label="Ciudad",
        hint_text="Ej: Madrid,ES",
        prefix_icon=ft.icons.SEARCH,
        autofocus=True,
        expand=True,
    )
    units_dropdown = ft.Dropdown(
        label="Unidades",
        options=[
            ft.dropdown.Option("metric", "Métrico (°C, m/s)"),
            ft.dropdown.Option("imperial", "Imperial (°F, mph)"),
        ],
        value="metric",
        width=200,
    )

    weather_container = ft.Container(content=None)

    progress_ring = ft.ProgressRing(visible=False, width=24, height=24)

    def set_status(message: str, color: str = colors.RED_200) -> None:
        status_text.value = message
        status_text.color = color
        status_text.update()

    def clear_status() -> None:
        status_text.value = ""
        status_text.update()

    def toggle_loading(is_loading: bool) -> None:
        progress_ring.visible = is_loading
        progress_ring.update()

    def update_weather_card(data: dict | None) -> None:
        weather_container.content = build_weather_card(data) if data else None
        weather_container.update()

    def handle_search(_: ft.ControlEvent) -> None:
        clear_status()
        city = city_input.value.strip() if city_input.value else ""
        if not city:
            set_status("Por favor ingresa una ciudad para buscar.")
            update_weather_card(None)
            return

        toggle_loading(True)
        page.update()

        try:
            weather = get_current_weather(city, units_dropdown.value)
        except ValueError as exc:
            set_status(str(exc))
            update_weather_card(None)
        except WeatherServiceError as exc:
            set_status(str(exc))
            update_weather_card(None)
        else:
            update_weather_card(weather)
            set_status("Actualizado correctamente", colors.GREEN_ACCENT_200)
        finally:
            toggle_loading(False)

    search_button = ft.ElevatedButton(
        text="Buscar", icon=ft.icons.SEARCH, on_click=handle_search, height=48
    )

    city_input.on_submit = handle_search

    controls_column = ft.Column(
        width=480,
        spacing=16,
        controls=[
            ft.Text("Dashboard del Clima", size=26, weight=ft.FontWeight.W_700),
            ft.Text(
                "Consulta el clima actual con un estilo moderno.",
                size=14,
                color=colors.GREY_400,
            ),
            ft.Container(
                padding=16,
                border_radius=20,
                bgcolor=colors.with_opacity(0.08, colors.WHITE),
                content=ft.Column(
                    spacing=12,
                    controls=[
                        ft.Row(
                            controls=[city_input],
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[units_dropdown, ft.Row([progress_ring, search_button], spacing=8)],
                        ),
                        status_text,
                    ],
                ),
            ),
            weather_container,
        ],
    )

    background = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#0f172a", "#1f2937", "#111827"],
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[controls_column],
        ),
    )

    page.add(background)


if __name__ == "__main__":
    ft.app(target=main)
