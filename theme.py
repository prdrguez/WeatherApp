"""Tema y constantes de estilo para la app de clima."""
from __future__ import annotations

import flet as ft


class WeatherTheme:
    """Colores y dimensiones reutilizables."""

    # Colores base
    BG_GRADIENT = ["#0f172a", "#1f2937", "#111827"]
    CARD_COLOR = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
    CARD_TINT = ft.Colors.BLUE_GREY_900
    ACCENT_ORANGE = "#f97316"
    ACCENT_SOFT = "#fb923c"

    # Texto
    TEXT_PRIMARY = ft.Colors.WHITE
    TEXT_SECONDARY = ft.Colors.GREY_400

    # Dimensiones
    PADDING = 16
    RADIUS = 16
    ELEVATION = 6

    # Sombras
    BOX_SHADOW = ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK))
