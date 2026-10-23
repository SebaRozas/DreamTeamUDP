# Proyecto TPM: Monitor de Coyuntura y Proyección a 24 Meses

## Descripción del Proyecto
Este proyecto analiza la trayectoria de la Tasa de Política Monetaria (TPM) del Banco Central de Chile mediante una Regla de Taylor adaptada a una economía abierta. El sistema integra la ingesta automatizada de series macroeconómicas desde las APIs oficiales del Banco Central de Chile (BCCh) y la Reserva Federal de St. Louis (FRED), almacenándolas en una base de datos relacional SQLite para su posterior análisis y modelación.

Pregunta de investigación: ¿cuál es la trayectoria proyectada para la TPM a 24 meses mediante una Regla de Taylor adaptada a economía abierta, y cómo la condicionan la Fed y la persistencia inflacionaria?

## Integrantes
* Sebastián Rozas 
* Natalia Luco 
* Sofía Vergara

## Estructura del Repositorio
```text
DreamTeamUDP/
├── data/               # Base SQLite coyuntura.db 
├── notebooks/
│   └── 01_analisis_coyuntura.ipynb   # Análisis de coyuntura
├── src/
│   ├── config.py             # Catálogo de series y rutas
│   ├── extraccion.py         # Descarga desde APIs BCCh y FRED
│   ├── carga_db.py           # Crea el esquema y carga la base
│   └── exportar_powerbi.py   # Crea la vista para el monitor Power BI
├── sql/
│   ├── 01_esquema.sql        # 3 tablas: temas, series, observaciones
│   └── Consultas.sql         # JOIN, GROUP BY y funciones de ventana
├── .env.example        # Plantilla de credenciales
├── requirements.txt
└── README.md
```

##  Requisitos
* Python 3.11 o superior
* `sqlite3` en la terminal
* Credenciales gratuitas de las APIs:
  * BCCh: registro en https://si3.bcentral.cl/Siete/es/Siete/API
  * FRED: API key en https://fred.stlouisfed.org/docs/api/api_key.html

## Reproducción paso a paso

¡1. Clonar el repositorio e instalar dependencias
```bash
git clone https://github.com/SebaRozas/DreamTeamUDP.git
cd DreamTeamUDP
python3 -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Configurar credenciales

Copiar la plantilla y completar con las credenciales propias:
```bash
cp .env.example .env
```
Luego editar `.env` con `BCCH_USUARIO`, `BCCH_PASSWORD` y `FRED_API_KEY`. El archivo `.env` está en `.gitignore` y **nunca** debe subirse a GitHub.

3. Extraer las series y cargar la base de datos

La extracción usa una fecha de corte fija para que todos obtengan exactamente la misma base:
```bash
python src/carga_db.py --hasta 2026-08-31
```
Esto descarga las series desde las APIs, crea `data/coyuntura.db` con el esquema de `sql/01_esquema.sql` y carga las observaciones. Revisar en la salida que todas las series aparezcan con `[OK]`.

Fecha de corte del Hito 2 es 2026-08-31. Si se omite `--hasta`, se usa la fecha de hoy y la base cambia cada día.

4. Verificar las consultas SQL
```bash
sqlite3 data/coyuntura.db
.read sql/Consultas.sql
.quit
```
No debe aparecer ningún `Error`.

5. Ejecutar el notebook de análisis

Abrir `notebooks/01_analisis_coyuntura.ipynb` y ejecutar todas las celdas. El notebook lee los datos desde `data/coyuntura.db`.

6. (Opcional) Preparar la vista para Power BI
```bash
python src/exportar_powerbi.py
```
Crea la vista `vista_monitor` en la base; Power BI se conecta a `data/coyuntura.db`.

### Probar sin credenciales
Para verificar que el pipeline funciona antes de tener las claves de las APIs:
```bash
python src/carga_db.py --demo --hasta 2026-08-31
```
Los datos del modo demo son sintéticos y sin significado económico osea que sirven solo para probar el pipeline, nunca para analizar.
