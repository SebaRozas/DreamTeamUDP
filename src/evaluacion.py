import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def rmse(y_real, y_pred):
    """Calcula la Raíz del Error Cuadrático Medio (penaliza errores grandes en % de TPM)."""
    y_real_arr = np.asarray(y_real, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    return float(np.sqrt(mean_squared_error(y_real_arr, y_pred_arr)))


def mae(y_real, y_pred):
    """Calcula el Error Absoluto Medio (desviación promedio en puntos porcentuales de TPM)."""
    y_real_arr = np.asarray(y_real, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    return float(mean_absolute_error(y_real_arr, y_pred_arr))


def r2_oos(y_real, y_pred, y_ref):
    """Calcula R² fuera de muestra: 1 - MSE_modelo / MSE_referencia (> 0 gana al benchmark)."""
    y_real_arr = np.asarray(y_real, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    y_ref_arr = np.asarray(y_ref, dtype=float)

    mse_modelo = mean_squared_error(y_real_arr, y_pred_arr)
    mse_referencia = mean_squared_error(y_real_arr, y_ref_arr)

    if mse_referencia == 0:
        raise ValueError("El MSE de referencia es 0; no se puede calcular R² fuera de muestra.")

    return float(1.0 - (mse_modelo / mse_referencia))


def benchmark_ingenuo(y):
    """Caminata aleatoria: pronostica que la TPM de este mes es igual a la del mes anterior."""
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    return y.shift(1)


def walk_forward(df, inicio, ajustar_predecir, paso=12):
    """Validación walk-forward con ventana expansiva reestimando cada `paso` meses sin fuga futura."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un pd.DataFrame ordenado cronológicamente.")
    if inicio <= 0 or inicio >= len(df):
        raise ValueError(f"inicio ({inicio}) debe estar entre 1 y {len(df) - 1}.")

    pronosticos_bloques = []

    for b in range(inicio, len(df), paso):
        train = df.iloc[:b]
        test = df.iloc[b : b + paso]
        pred_bloque = ajustar_predecir(train, test)

        if isinstance(pred_bloque, pd.Series):
            serie_bloque = pred_bloque.reindex(test.index)
        else:
            serie_bloque = pd.Series(np.asarray(pred_bloque, dtype=float), index=test.index)

        pronosticos_bloques.append(serie_bloque)

    return pd.concat(pronosticos_bloques)


def tabla_metricas(y_real, dict_pronosticos, y_ref):
    """Construye el DataFrame comparativo con RMSE, MAE y R2_oos alineando los meses válidos."""
    s_real = pd.Series(y_real, name="real")
    s_ref = pd.Series(y_ref, name="referencia")

    filas = []
    for nombre_modelo, y_pred in dict_pronosticos.items():
        idx = s_real.index if not isinstance(y_pred, pd.Series) else y_pred.index
        s_pred = pd.Series(y_pred, index=idx)
        comp = pd.concat([s_real, s_pred.rename("pred"), s_ref], axis=1).dropna()

        filas.append(
            {
                "Modelo": nombre_modelo,
                "RMSE": rmse(comp["real"], comp["pred"]),
                "MAE": mae(comp["real"], comp["pred"]),
                "R2_oos": r2_oos(comp["real"], comp["pred"], comp["referencia"]),
            }
        )

    return pd.DataFrame(filas).set_index("Modelo")


if __name__ == "__main__":
    from sklearn.base import clone
    from sklearn.linear_model import Ridge

    rng = np.random.default_rng(42)
    fechas = pd.period_range("2011-01", periods=180, freq="M")
    tpm_sim = [4.5]
    for _ in range(179):
        shock = rng.choice([-0.25, 0.0, 0.0, 0.25])
        tpm_sim.append(np.clip(0.95 * tpm_sim[-1] + 0.25 + shock, 0.5, 11.25))

    df_test = pd.DataFrame({"TPM": tpm_sim}, index=fechas)
    df_test["TPM_lag1"] = df_test["TPM"].shift(1)
    df_test = df_test.dropna()

    inicio_oos = len(df_test) - 48
    modelo_base = Ridge(alpha=1.0)

    def predecir_ridge(train, test):
        mod = clone(modelo_base)
        mod.fit(train[["TPM_lag1"]], train["TPM"])
        return mod.predict(test[["TPM_lag1"]])

    pred_ridge = walk_forward(df_test, inicio=inicio_oos, ajustar_predecir=predecir_ridge, paso=12)
    pred_ingenuo = benchmark_ingenuo(df_test["TPM"]).loc[pred_ridge.index]
    y_real_oos = df_test["TPM"].loc[pred_ridge.index]

    resultados = tabla_metricas(
        y_real=y_real_oos,
        dict_pronosticos={
            "Benchmark Ingenuo (RW)": pred_ingenuo,
            "Modelo Prueba (Ridge AR1)": pred_ridge,
        },
        y_ref=pred_ingenuo,
    )

    print("=== Prueba unitaria de src/evaluacion.py ===")
    print(resultados.round(4))

    import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def rmse(y_real, y_pred):
    """Calcula la Raíz del Error Cuadrático Medio (penaliza errores grandes en % de TPM)."""
    y_real_arr = np.asarray(y_real, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    return float(np.sqrt(mean_squared_error(y_real_arr, y_pred_arr)))


def mae(y_real, y_pred):
    """Calcula el Error Absoluto Medio (desviación promedio en puntos porcentuales de TPM)."""
    y_real_arr = np.asarray(y_real, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    return float(mean_absolute_error(y_real_arr, y_pred_arr))


def r2_oos(y_real, y_pred, y_ref):
    """Calcula R² fuera de muestra: 1 - MSE_modelo / MSE_referencia (> 0 gana al benchmark)."""
    y_real_arr = np.asarray(y_real, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    y_ref_arr = np.asarray(y_ref, dtype=float)

    mse_modelo = mean_squared_error(y_real_arr, y_pred_arr)
    mse_referencia = mean_squared_error(y_real_arr, y_ref_arr)

    if mse_referencia == 0:
        raise ValueError("El MSE de referencia es 0; no se puede calcular R² fuera de muestra.")

    return float(1.0 - (mse_modelo / mse_referencia))


def benchmark_ingenuo(y):
    """Caminata aleatoria: pronostica que la TPM de este mes es igual a la del mes anterior."""
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    return y.shift(1)


def walk_forward(df, inicio, ajustar_predecir, paso=12):
    """Validación walk-forward con ventana expansiva reestimando cada `paso` meses sin fuga futura."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df debe ser un pd.DataFrame ordenado cronológicamente.")
    if inicio <= 0 or inicio >= len(df):
        raise ValueError(f"inicio ({inicio}) debe estar entre 1 y {len(df) - 1}.")

    pronosticos_bloques = []

    for b in range(inicio, len(df), paso):
        train = df.iloc[:b]
        test = df.iloc[b : b + paso]
        pred_bloque = ajustar_predecir(train, test)

        if isinstance(pred_bloque, pd.Series):
            serie_bloque = pred_bloque.reindex(test.index)
        else:
            serie_bloque = pd.Series(np.asarray(pred_bloque, dtype=float), index=test.index)

        pronosticos_bloques.append(serie_bloque)

    return pd.concat(pronosticos_bloques)


def tabla_metricas(y_real, dict_pronosticos, y_ref):
    """Construye el DataFrame comparativo con RMSE, MAE y R2_oos alineando los meses válidos."""
    s_real = pd.Series(y_real, name="real")
    s_ref = pd.Series(y_ref, name="referencia")

    filas = []
    for nombre_modelo, y_pred in dict_pronosticos.items():
        idx = s_real.index if not isinstance(y_pred, pd.Series) else y_pred.index
        s_pred = pd.Series(y_pred, index=idx)
        comp = pd.concat([s_real, s_pred.rename("pred"), s_ref], axis=1).dropna()

        filas.append(
            {
                "Modelo": nombre_modelo,
                "RMSE": rmse(comp["real"], comp["pred"]),
                "MAE": mae(comp["real"], comp["pred"]),
                "R2_oos": r2_oos(comp["real"], comp["pred"], comp["referencia"]),
            }
        )

    return pd.DataFrame(filas).set_index("Modelo")


if __name__ == "__main__":
    from sklearn.base import clone
    from sklearn.linear_model import Ridge

    rng = np.random.default_rng(42)
    fechas = pd.period_range("2011-01", periods=180, freq="M")
    tpm_sim = [4.5]
    for _ in range(179):
        shock = rng.choice([-0.25, 0.0, 0.0, 0.25])
        tpm_sim.append(np.clip(0.95 * tpm_sim[-1] + 0.25 + shock, 0.5, 11.25))

    df_test = pd.DataFrame({"TPM": tpm_sim}, index=fechas)
    df_test["TPM_lag1"] = df_test["TPM"].shift(1)
    df_test = df_test.dropna()

    inicio_oos = len(df_test) - 48
    modelo_base = Ridge(alpha=1.0)

    def predecir_ridge(train, test):
        mod = clone(modelo_base)
        mod.fit(train[["TPM_lag1"]], train["TPM"])
        return mod.predict(test[["TPM_lag1"]])

    pred_ridge = walk_forward(df_test, inicio=inicio_oos, ajustar_predecir=predecir_ridge, paso=12)
    pred_ingenuo = benchmark_ingenuo(df_test["TPM"]).loc[pred_ridge.index]
    y_real_oos = df_test["TPM"].loc[pred_ridge.index]

    resultados = tabla_metricas(
        y_real=y_real_oos,
        dict_pronosticos={
            "Benchmark Ingenuo (RW)": pred_ingenuo,
            "Modelo Prueba (Ridge AR1)": pred_ridge,
        },
        y_ref=pred_ingenuo,
    )

    print("=== Prueba unitaria de src/evaluacion.py ===")
    print(resultados.round(4))
    