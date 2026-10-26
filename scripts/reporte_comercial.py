"""Genera un resumen por destino a partir de un CSV (datos demo por defecto)."""

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["fecha", "destino", "toneladas", "precio_usd_t"]


def generar_reporte(entrada: Path, salida: Path) -> pd.DataFrame:
    datos = pd.read_csv(entrada)
    faltantes = set(REQUIRED) - set(datos.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas: {', '.join(sorted(faltantes))}")
    if datos.empty or datos[REQUIRED].isna().any().any():
        raise ValueError("El archivo debe contener filas completas, sin valores vacíos.")
    pd.to_datetime(datos["fecha"], format="%Y-%m-%d", errors="raise")
    datos["destino"] = datos["destino"].astype(str).str.strip()
    if datos["destino"].eq("").any():
        raise ValueError("El destino no puede estar vacío.")
    for columna in ["toneladas", "precio_usd_t"]:
        datos[columna] = pd.to_numeric(datos[columna], errors="raise")
        if not datos[columna].map(lambda valor: float("-inf") < valor < float("inf")).all():
            raise ValueError(f"{columna} debe contener números finitos.")
    if datos["toneladas"].le(0).any() or datos["precio_usd_t"].lt(0).any():
        raise ValueError("Las toneladas deben ser positivas y el precio no negativo.")

    datos["valor_usd"] = datos["toneladas"] * datos["precio_usd_t"]
    resumen = datos.groupby("destino", as_index=False).agg(
        toneladas=("toneladas", "sum"), valor_usd=("valor_usd", "sum")
    )
    resumen["precio_promedio_usd_t"] = resumen["valor_usd"] / resumen["toneladas"]
    resumen = resumen.sort_values("toneladas", ascending=False).reset_index(drop=True)
    salida.parent.mkdir(parents=True, exist_ok=True)
    resumen.to_csv(salida, index=False, encoding="utf-8-sig", float_format="%.2f")
    return resumen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data/examples/ventas_demo.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "data/output/resumen_destinos.csv")
    args = parser.parse_args()
    try:
        resumen = generar_reporte(args.input, args.output)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(resumen.to_string(index=False))
    print(f"\nReporte guardado en: {args.output.resolve()}")


if __name__ == "__main__":
    main()
