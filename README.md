# PythonWork

Base práctica para análisis comercial, preparación de datos para Power BI y automatizaciones en Python.

## Estructura

| Ruta | Uso |
| --- | --- |
| `scripts/` | Procesos ejecutables: limpieza, transformación y reportes. |
| `notebooks/` | Exploración y prototipos en Jupyter. |
| `data/examples/` | Datos ficticios versionados para ejecutar los ejemplos. |
| `data/input/` | Archivos de entrada locales (ignorados por Git). |
| `data/output/` | Reportes generados locales (ignorados por Git). |

## Preparación

Requiere Python 3.10 o superior. Desde la carpeta del repositorio:

```bash
python -m venv .venv
```

Activa el entorno en Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

O en Windows (CMD):

```bat
.venv\Scripts\activate.bat
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Primer reporte con pandas

```bash
python scripts/reporte_comercial.py
```

Usa datos **completamente ficticios**, calcula valor USD por operación
(`toneladas × precio_usd_t`) y agrupa por destino. Exporta toneladas, valor USD
y precio promedio ponderado por toneladas a `data/output/resumen_destinos.csv`.
Brasil debe sumar 1.500 toneladas, USD 390.000 y USD 260/t.
El ejemplo completo suma 5.000 toneladas y USD 1.320.000.

Para tus propios datos:

```bash
python scripts/reporte_comercial.py --input data/input/ventas.csv --output data/output/resumen_destinos.csv
```

El CSV debe usar coma como separador, punto decimal y estas columnas:

| Columna | Formato |
| --- | --- |
| `fecha` | AAAA-MM-DD |
| `destino` | Texto no vacío |
| `toneladas` | Número positivo |
| `precio_usd_t` | Número no negativo |

Cada fila representa una operación; no incluyas subtotales. El script rechaza
columnas faltantes, filas incompletas, fechas inválidas y cantidades inválidas.
El archivo de salida se reemplaza en cada ejecución. Sin argumentos, las rutas
se resuelven desde el repositorio, incluso al ejecutar desde otra carpeta;
las rutas explícitas se interpretan desde el directorio actual.

## Cómo crecer

- **Power BI:** importa el CSV de salida con Obtener datos → Texto/CSV.
  Configura toneladas, valor y precio como números decimales. Para un precio
  agregado, divide la suma del valor USD por la suma de toneladas.
- **SQL:** agrega consultas en una futura carpeta `sql/` y una conexión
  mediante variables de entorno cuando el primer proyecto lo necesite.
- **Notebooks:** instala opcionalmente `python -m pip install jupyterlab`,
  ejecuta `python -m jupyterlab` y guarda tus exploraciones en `notebooks/`.
  Mueve los procesos repetibles a `scripts/`.
- **Automatización:** programa el mismo comando con el Programador de tareas
  de Windows cuando el flujo ya funcione manualmente.

Este repositorio es público: usa `data/examples/` solo para muestras ficticias.
Los datos locales y `.env` están excluidos por `.gitignore`; revisa siempre
`git status` antes de subir cambios y no incluyas credenciales ni información comercial.
