# Proyecto: de la regresión regularizada al portafolio óptimo

Fundamentos de Econometría (ECO515), Universidad Panamericana, Otoño 2026.

**Equipos de hasta 3 personas.** Entregas por Blackboard. La fecha la indica el profesor.

El enunciado completo, con los ejercicios en papel, está en `ProyectoRegularizacion_FundamentosEconometria_Otono2026.pdf`.

## Qué vas a responder

1. **Regresión lineal, Ridge, Lasso y Elastic Net:** ¿en qué mejora la regularización a MCO y en qué casos no? Incluye una **tabla MANOVA**.
2. **Multicolinealidad:** ¿cómo evadirla, y cuándo no hace falta?
3. **PCA a partir de un vector aleatorio:** obtén los componentes de tres maneras: con la teoría, con una muestra y con un vector inicial aleatorio.
4. **Markowitz:** deduce e implementa la solución cerrada, y compruébala fuera de muestra.

## Qué vas a entregar

| # | Entregable | Formato |
|---|---|---|
| 1 | Notebook completo, corrido de principio a fin sin errores | `Proyecto_Alumnos.ipynb` |
| 2 | Dashboard interactivo publicado | Enlace público |
| 3 | Repositorio de GitHub con el código | Enlace público |

## Paso 1. Preparar el ambiente

En la página del repositorio, pulsa **Use this template > Create a new repository** y elige visibilidad pública. Eso te da tu propia copia, que después usarás para publicar el dashboard. Clónala y crea el ambiente:

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
cd TU-REPOSITORIO
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac o Linux:
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook Proyecto_Alumnos.ipynb
```

También puedes resolver el notebook en Google Colab, con el enlace de `README.md`: los datos se descargan solos. **Guarda tu copia en Drive**, porque Colab no conserva los cambios del original. Streamlit no se puede probar en Colab: el dashboard debe hacerse en tu computadora.

## Paso 2. Resolver el notebook

1. Escribe la matrícula de un integrante en `SEMILLA`. Esa matrícula define tus sectores y tus datos: **no la cambies después**.
2. Avanza en orden, celda por celda.
3. Completa cada `# TU CÓDIGO AQUÍ` y borra la línea `raise NotImplementedError`.
4. Revisa que las comprobaciones salgan con ✅.
5. Contesta cada ✍️ con tus cifras.

Tiempo estimado: de 8 a 12 horas de trabajo en equipo. La celda del Monte Carlo tarda unos minutos la primera vez.

### Errores frecuentes

| Síntoma | Causa probable |
|---|---|
| `NotImplementedError` | Falta completar ese paso o borrar la línea |
| `NameError` más abajo | Cambiaste el nombre de una variable, o te saltaste una celda |
| Lasso deja todos los coeficientes en cero | `alpha` demasiado grande, o `X` sin estandarizar |
| Tu Wilks no coincide con `statsmodels` | Una matriz $H$ está mal: revisa la comprobación $H+E=T$ |
| El método de la potencia da un vector con signo opuesto | Es correcto: $a$ y $-a$ son la misma dirección |
| El Sharpe fuera de muestra es mucho menor que en entrenamiento | Es normal, y es justo lo que debes analizar |
| `partially initialized module 'streamlit'` | Un archivo tuyo se llama `streamlit.py`: renómbralo |

## Paso 3. Construir el dashboard

Elige **una** opción. Ambas valen lo mismo.

| | Opción A: Streamlit | Opción B: página HTML |
|---|---|---|
| Archivo | `dashboard/app.py` | `dashboard/generar_html.py` |
| Calcula en vivo | Sí | No: recorre resultados ya calculados |
| Publicación | Streamlit Community Cloud | GitHub Pages |
| Recomendada si | Quieres que el usuario elija libremente | Quieres una página simple que no se "duerma" |

La sección final del notebook guarda tus resultados en `dashboard/resultados/`. Ambas plantillas ya incluyen un ejemplo que funciona.

**Requisitos mínimos del dashboard:**

- Una sección por cada una de las 4 partes, cada una con al menos un control interactivo que cambie un resultado.
- En la Parte 4, al menos dos controles.
- Tu tabla MANOVA y tu conclusión de la Parte 1.
- Comparación dentro y fuera de muestra en las Partes 1 y 4.
- Cada gráfica con título, ejes con unidades y una frase que diga qué concluir de ella.
- Nombres del equipo y fuente de los datos.

### Opción A: publicar con Streamlit

```bash
# Prueba local, desde la raíz del repositorio
streamlit run dashboard/app.py
```

1. Sube tus cambios a tu repositorio público: `git add -A`, `git commit -m "Dashboard"` y `git push`.
2. Entra a <https://share.streamlit.io> con tu cuenta de GitHub.
3. Elige *Create app*, tu repositorio y la rama `main`. En *Main file path* escribe `dashboard/app.py`.
4. Abre el enlace en una ventana de incógnito para comprobar que es público.

### Opción B: publicar con GitHub Pages

```bash
# Desde la raíz del repositorio
python dashboard/generar_html.py
```

1. Abre `docs/index.html` en tu navegador y revisa que funcione.
2. Sube tus cambios a tu repositorio público: `git add -A`, `git commit -m "Dashboard"` y `git push`.
3. En *Settings > Pages*, elige *Deploy from a branch*, la rama `main` y la carpeta `/docs`.
4. Tras un par de minutos, abre `https://TU-USUARIO.github.io/TU-REPOSITORIO/` en una ventana de incógnito.

## Rúbrica (100 puntos)

| Criterio | Puntos | Excelente |
|---|---|---|
| Parte 1: Regularización | 15 | Comparación correcta dentro y fuera de muestra, sin fuga de información |
| Parte 1: Tabla MANOVA | 10 | Matrices a mano que coinciden con `statsmodels`; revisa supuestos y distingue significancia de tamaño de efecto |
| Parte 2: Multicolinealidad | 15 | Diagnóstico completo; elige el remedio según el objetivo: interpretar o predecir |
| Parte 3: PCA | 15 | Las tres vías coinciden; explica la convergencia y da lectura financiera |
| Parte 4: Markowitz | 15 | Solución cerrada verificada; evalúa fuera de muestra y reconoce sus limitaciones |
| Interpretación y memorándum | 10 | Usa las cifras de su equipo; el comité entendería el memorándum |
| Dashboard | 15 | Publicado, cumple los requisitos y un tercero lo entiende sin ayuda |
| Reproducibilidad | 5 | `Restart & Run All` corre sin errores con la semilla declarada |

Las comprobaciones ✅ no garantizan los puntos: revisan la coherencia del cálculo, no la interpretación.

**Reglas de integridad.** Cada equipo tiene sus propios datos: respuestas con cifras de otra semilla reciben cero en esa parte. Puedes usar herramientas de IA, pero debes poder explicar en clase cualquier línea de tu código.

## Datos

Rendimientos mensuales de 30 portafolios de industria ponderados por valor, y factores Fama-French, de la [Kenneth R. French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html), 2000-01 a 2026-09, en porcentaje. El conjunto Longley viene incluido en `statsmodels`.
