"""Plantilla del dashboard (Opción A: Streamlit).

Ejecutar desde la carpeta kit_alumnos:  streamlit run dashboard/app.py
La pestaña 1 ya funciona como ejemplo. Completa todo lo marcado con TODO.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

AQUI = Path(__file__).parent
FACTORES = ["Mkt-RF", "SMB", "HML", "RF"]

st.set_page_config(page_title="Mi proyecto", layout="wide")


@st.cache_data  # evita recalcular cada vez que se mueve un control
def cargar_datos():
    return pd.read_csv(AQUI.parent / "datos" / "industrias_ff30_mensual.csv", index_col="fecha")


datos = cargar_datos()
sectores = [c for c in datos.columns if c not in FACTORES]
excesos = datos[sectores].sub(datos["RF"], axis=0)
corte = int(0.75 * len(datos))
entrena, prueba = datos.index[:corte], datos.index[corte:]

st.title("TODO: título de tu proyecto")
st.caption("TODO: nombres de los integrantes y semilla del equipo")

tab1, tab2, tab3, tab4 = st.tabs(["1. Regularización y MANOVA", "2. Multicolinealidad", "3. PCA", "4. Markowitz"])

with tab1:
    st.subheader("Ejemplo: Ridge frente a MCO")
    objetivo = st.selectbox("Sector a replicar", sectores)
    log_lambda = st.slider("log10(lambda)", -2.0, 4.0, 2.0, 0.1)
    otros = [s for s in sectores if s != objetivo]
    X_a, y_a = excesos.loc[entrena, otros], excesos.loc[entrena, objetivo]
    X_b, y_b = excesos.loc[prueba, otros], excesos.loc[prueba, objetivo]
    ridge = make_pipeline(StandardScaler(), Ridge(alpha=10 ** log_lambda)).fit(X_a, y_a)
    mco = make_pipeline(StandardScaler(), LinearRegression()).fit(X_a, y_a)
    rmse = lambda m: float(np.sqrt(np.mean((y_b - m.predict(X_b)) ** 2)))
    col1, col2 = st.columns(2)
    col1.metric("RMSE de prueba, Ridge", f"{rmse(ridge):.3f}")
    col2.metric("RMSE de prueba, MCO", f"{rmse(mco):.3f}")
    fig = go.Figure()
    fig.add_bar(x=otros, y=mco[-1].coef_, name="MCO", marker_color="#8a8f98")
    fig.add_bar(x=otros, y=ridge[-1].coef_, name="Ridge", marker_color="#2a78d6")
    fig.update_layout(title="Coeficientes estandarizados", xaxis_title="Sector", yaxis_title="Coeficiente")
    st.plotly_chart(fig)

    # TODO: agrega Lasso y Elastic Net con un selector de método.
    # TODO: agrega un control para la ventana de entrenamiento.
    # TODO: muestra tu tabla MANOVA: pd.read_csv(AQUI / "resultados" / "tabla_manova.csv")
    # TODO: muestra las tablas del Monte Carlo y tu conclusión en una o dos frases.

with tab2:
    st.info("TODO: al menos un control. Idea: elegir regresoras de Longley y ver cómo cambian el VIF y el número de condición.")

with tab3:
    st.info("TODO: al menos un control. Idea: un deslizador de iteraciones del método de la potencia, con el vector v_t sobre la nube de datos.")

with tab4:
    st.info("TODO: al menos dos controles. Idea: elegir sectores y la tasa libre de riesgo, y permitir o no ventas en corto; mostrar la frontera, los pesos y el Sharpe fuera de muestra.")
