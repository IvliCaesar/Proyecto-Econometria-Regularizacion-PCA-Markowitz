"""Plantilla del dashboard (Opción B: página HTML estática).

Ejecutar desde la carpeta kit_alumnos:  python dashboard/generar_html.py
Crea docs/index.html, que se publica con GitHub Pages. La página no calcula en vivo: los
controles (deslizadores y menús de Plotly) cambian entre resultados ya calculados aquí.
Completa todo lo marcado con TODO.
"""
from html import escape
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

AQUI = Path(__file__).parent
FACTORES = ["Mkt-RF", "SMB", "HML", "RF"]
datos = pd.read_csv(AQUI.parent / "datos" / "industrias_ff30_mensual.csv", index_col="fecha")
sectores = [c for c in datos.columns if c not in FACTORES]
excesos = datos[sectores].sub(datos["RF"], axis=0)
entrena = datos.index[: int(0.75 * len(datos))]


def figura_ridge(objetivo):
    """Ejemplo: un deslizador de Plotly que recorre valores de lambda ya calculados."""
    otros = [s for s in sectores if s != objetivo]
    X, y = excesos.loc[entrena, otros], excesos.loc[entrena, objetivo]
    log_lambdas = np.arange(-1, 4.01, 0.5)
    fig = go.Figure()
    for k, log_l in enumerate(log_lambdas):
        coef = make_pipeline(StandardScaler(), Ridge(alpha=10 ** log_l)).fit(X, y)[-1].coef_
        fig.add_bar(x=otros, y=coef, visible=(k == 0), marker_color="#2a78d6", name=f"log10(lambda) = {log_l:.1f}")
    pasos = [
        dict(method="update", label=f"{log_l:.1f}", args=[{"visible": [j == k for j in range(len(log_lambdas))]}])
        for k, log_l in enumerate(log_lambdas)
    ]
    fig.update_layout(
        title=f"Ridge: coeficientes para replicar {objetivo}", xaxis_title="Sector", yaxis_title="Coeficiente estandarizado",
        yaxis_range=[-0.8, 1.2], sliders=[dict(steps=pasos, currentvalue=dict(prefix="log10(lambda) = "), pad=dict(t=70))],
    )
    return fig


# TODO: cambia "Fin" por tu sector objetivo y agrega una figura interactiva por cada parte.
SECCIONES = [
    ("1. Regularización y MANOVA", figura_ridge("Fin"), "TODO: explica en dos frases qué muestra esta figura."),
    # ("2. Multicolinealidad", tu_figura, "Tu explicación"),
    # ("3. PCA", tu_figura, "Tu explicación"),
    # ("4. Markowitz", tu_figura, "Tu explicación"),
]

cuerpo = []
for k, (titulo, fig, texto) in enumerate(SECCIONES):
    html_fig = fig.to_html(full_html=False, include_plotlyjs="cdn" if k == 0 else False)
    cuerpo.append(f"<h2>{escape(titulo)}</h2><p>{escape(texto)}</p>{html_fig}")

ruta_manova = AQUI / "resultados" / "tabla_manova.csv"
if ruta_manova.exists():
    cuerpo.append("<h2>Tabla MANOVA</h2>" + pd.read_csv(ruta_manova).round(4).to_html(index=False, na_rep=""))

pagina = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mi proyecto</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 1050px; margin: 0 auto; padding: 16px; color: #222; background: #fff; }}
table {{ border-collapse: collapse; font-size: 14px; display: block; overflow-x: auto; }}
td, th {{ border-bottom: 1px solid #ddd; padding: 4px 10px; text-align: right; }}
</style></head><body>
<h1>TODO: título de tu proyecto</h1>
<p>TODO: nombres de los integrantes y semilla del equipo</p>
{''.join(cuerpo)}
</body></html>"""

salida = AQUI.parent / "docs" / "index.html"
salida.parent.mkdir(exist_ok=True)
salida.write_text(pagina, encoding="utf-8")
print("Página creada en", salida.resolve())
