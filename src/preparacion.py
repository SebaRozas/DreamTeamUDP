# Base mensual del proyecto: la usan todos los notebooks para que las cifras coincidan.
import sqlite3
import pandas as pd
import config

# Nombres cortos por código (buscar por palabras confundía la TPM con la Fed)
NOMBRES = {
    "F022.TPM.TIN.D001.NO.Z.D": "TPM",
    "F089.IPC.V12.15.M": "EEE_23m",
    "F032.IMC.IND.Z.Z.EP18.Z.Z.0.M": "Imacec",
    "F032.IMC.IND.Z.Z.EP18.N03.Z.0.M": "Imacec_NM",
    "F049.DES.TAS.INE9.10.M": "Desempleo",
    "F073.TCO.PRE.Z.D": "Dolar",
    "F019.PPB.PRE.40.M": "Cobre",
    "F074.IPC.IND.Z.EP23.C.M": "IPC",
    "G073.IPCSV.IND.2023.M": "IPC_SV",
    "FEDFUNDS": "FedFunds",
    "DCOILWTICO": "WTI",
    "CPIAUCSL": "CPI_US",
}


def cargar_panel_mensual():
    conn = sqlite3.connect(config.RUTA_DB)
    obs = pd.read_sql_query("SELECT id_serie, fecha, valor FROM observaciones", conn)
    conn.close()

    obs["fecha"] = pd.to_datetime(obs["fecha"])
    df = obs.pivot(index="fecha", columns="id_serie", values="valor").sort_index()

    # Cierre de mes: en las diarias (TPM, dólar, WTI) queda el último dato del mes
    df = df.resample("ME").last()
    df.index = df.index.to_period("M")
    df = df.rename(columns=NOMBRES)[list(NOMBRES.values())]
    df.columns.name = None

    # Variación interanual solo en índices; las tasas quedan en nivel
    for col in ["IPC", "IPC_SV", "CPI_US", "Imacec", "Imacec_NM"]:
        df[col + "_ia"] = 100 * (df[col] / df[col].shift(12) - 1)

    # Sin ffill ni dropna ya que el último mes puede venir incompleto 
    return df


if __name__ == "__main__":
    print(cargar_panel_mensual().tail(6).round(2))