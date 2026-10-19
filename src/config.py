"""
Configuración central del proyecto.

Las credenciales se leen desde el archivo .env (NUNCA subir credenciales a GitHub).
Copien .env.example a .env y completen sus claves.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Rutas del proyecto
RAIZ = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ / "data"
RUTA_DB = RUTA_DATOS / "coyuntura.db"
RUTA_SQL = RAIZ / "sql"

# Cargar credenciales desde .env
load_dotenv(RAIZ / ".env")

# --- Banco Central de Chile ---
# Registro gratuito en: https://si3.bcentral.cl/Siete/es/Siete/API
BCCH_USUARIO = os.getenv("BCCH_USUARIO", "")
BCCH_PASSWORD = os.getenv("BCCH_PASSWORD", "")

# --- FRED (Reserva Federal de St. Louis) ---
# API key gratuita en: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = os.getenv("FRED_API_KEY", "")

# ============================================================
# CATÁLOGO DE SERIES DEL PROYECTO
# Cada equipo debe editar este catálogo con sus propias series.
# Los códigos del BCCh se buscan en https://si3.bcentral.cl/siete
# (el código aparece en la ficha de cada serie).
# ============================================================
# Catálogo DreamTeam (Hito 1) - variable objetivo: TPM
# Códigos verificados manualmente en https://si3.bcentral.cl/siete el 26-08-2026.
# Los dos marcados TODO no se pudieron confirmar por búsqueda automática:
# hay que copiarlos a mano desde la ficha de la serie en si3.bcentral.cl/siete.
SERIES_BCCH = [
    # (codigo, nombre, frecuencia, unidad, id_tema)
    ("F022.TPM.TIN.D001.NO.Z.D", "Tasa de Política Monetaria (TPM)", "D", "% anual", 4),
    ("F074.IPC.VAR.Z.Z.C.M", "IPC, variación mensual (calcular interanual con LAG 12 en SQL)", "M", "var. % mensual", 2),
    ("F089.EDEP.POR.91EI24.M", "Expectativas de inflación a 2 años (EEE)", "M", "% anual", 2),
    ("F032.IMC.IND.Z.Z.EP18.Z.Z.0.M", "Imacec (índice)", "M", "índice 2018=100", 1),
    ("F049.DES.TAS.INE9.10.M", "Tasa de desempleo nacional", "M", "%", 1),
    ("F073.TCO.PRE.Z.D", "Tipo de cambio nominal observado (CLP/USD)", "D", "CLP/USD", 5),
    ("F019.PPB.PRE.40.M", "Precio del cobre refinado BML", "M", "US$/libra", 5),
    ("F074.IPC.IND.Z.EP23.C.M", "IPC empalmado oficial", "M", "índice", 2),
    ("G089.IME.IND.A3.M", "IMCE - Índice Mensual de Confianza Empresarial", "M", "índice", 6),
]

SERIES_FRED = [
    # (codigo, nombre, frecuencia, unidad, id_tema)
    ("FEDFUNDS", "Fed Funds Rate (tasa de política EE.UU.)", "M", "% anual", 6),
    ("DGS10", "Bono del Tesoro EE.UU. a 10 años", "D", "% anual", 6),
    ("DCOILWTICO", "Petróleo WTI", "D", "USD/barril", 6),
    ("CPIAUCSL", "IPC Estados Unidos (US CPI)", "M", "índice", 6),
]






