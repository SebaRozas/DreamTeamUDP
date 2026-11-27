"""
Busca códigos de series mensuales en el catálogo de la API del BCCh.

Uso desde la raíz del repositorio:
    python src/buscar_series.py "sin volátiles" "no minero" "expectativas"

Imprime código, primera y última observación y título de cada serie cuyo
título contiene TODAS las palabras de alguno de los términos buscados.
Sirve para elegir códigos con historia suficiente antes de editar config.py.
"""
import sys

try:
    import config
    from extraccion import URL_BCCH, pedir_json
except ImportError:  # permite ejecutar desde la raíz del repo
    from src import config  # type: ignore
    from src.extraccion import URL_BCCH, pedir_json  # type: ignore


def buscar(terminos: list[str]) -> None:
    params = {"user": config.BCCH_USUARIO, "pass": config.BCCH_PASSWORD,
              "function": "SearchSeries", "frequency": "MONTHLY"}
    catalogo = pedir_json(URL_BCCH, params).get("SeriesInfos", [])
    for termino in terminos:
        palabras = termino.lower().split()
        print(f"\n=== {termino} ===")
        for s in catalogo:
            titulo = s.get("spanishTitle", "")
            if all(p in titulo.lower() for p in palabras):
                print(f"{s['seriesId']:<40} {s.get('firstObservation','')[:10]} -> "
                      f"{s.get('lastObservation','')[:10]}  {titulo[:110]}")


if __name__ == "__main__":
    buscar(sys.argv[1:] or ["sin volátiles", "no minero", "expectativas inflación"])
