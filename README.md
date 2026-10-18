# Proyecto TPM: Monitor de Coyuntura y Proyección a 24 Meses

## 📌 Descripción del Proyecto
Este proyecto analiza la trayectoria de la Tasa de Política Monetaria (TPM) del Banco Central de Chile mediante una **Regla de Taylor adaptada a una economía abierta**. El sistema integra la ingesta automatizada de 12 series macroeconómicas desde las APIs oficiales del Banco Central de Chile (BCCh) y la Reserva Federal de EE.UU. (FRED), almacenándolas en una base de datos relacional SQLite para su posterior análisis y modelación.

## 👥 Integrantes
* **Sebastián Rozas** (Líder de Infraestructura, SQL y Git)
* **Natalia** (Especialista en Extracción de Datos y APIs)
* **Sofía** (Analista Macroeconómica de Coyuntura y Visualización)

## 📁 Estructura del Repositorio
```text
TPM/
├── data/               # Base de datos relacional SQLite (tpm.db)
├── notebooks/          # Cuadernos Jupyter con análisis de coyuntura
│   └── 01_analisis_coyuntura.ipynb
├── src/                # Scripts de Python para extracción e ingesta
├── sql/                # Scripts de creación de esquemas y consultas Window Functions
├── requirements.txt    # Librerías y dependencias necesarias
└── README.md           # Guía de reproducibilidad

git clone [https://github.com/SebaRozas/TPM.git](https://github.com/SebaRozas/TPM.git)
cd TPM
pip install -r requirements.txt
