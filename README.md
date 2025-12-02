# WeatherApp

Aplicación de escritorio en Python + Flet para consultar el clima actual con un diseño de dashboard moderno y modular.

## Requisitos

- Python 3.10+
- Dependencias listadas en `requirements.txt` (Flet y requests).

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Configuración de la API

El proyecto usa la API de [OpenWeatherMap](https://openweathermap.org/). Configura tu API key así:

1. Crea un archivo `.env` o exporta una variable de entorno:
   ```bash
   export OPENWEATHER_API_KEY="TU_API_KEY"
   ```
2. Alternativamente, edita `config.py` y reemplaza el valor de `API_KEY` por tu clave.

## Ejecución

Puedes iniciar la app de dos formas:

```bash
python main.py
```

o

```bash
flet run main.py
```

Escribe una ciudad (por ejemplo, `Madrid,ES` o `Buenos Aires,AR`), elige unidades métricas o imperiales y presiona **Buscar** para ver el clima actual.

## Estructura principal

- `config.py`: Configuración base y claves de API.
- `theme.py`: Colores y estilos reutilizables.
- `utils.py`: Formateadores y utilidades generales.
- `weather_service.py`: Lógica de consulta y parseo de datos de OpenWeatherMap.
- `components/`: Conjunto de tarjetas y gráficos (clima, lluvia, AQI, etc.).
- `pages/home.py`: Construye el layout del dashboard completo.
- `main.py`: Punto de entrada y orquestación de la página.
- `requirements.txt`: Dependencias del proyecto.
