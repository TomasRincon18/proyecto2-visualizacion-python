# %% [markdown]
# # Bienestar por regiones: una mirada al World Happiness Report 2024
#
# **Informe analítico reproducible · Python (Seaborn y Plotly)**
#
# Integrantes: Juan Tomás Rincón · Alejandro Pardo Costo

# %% [markdown]
# ## Contexto
#
# El *World Happiness Report 2024* publica la evaluación de vida de 143 países
# (promedios 2021–2023, escala Cantril 0–10) y una descomposición que atribuye
# esa evaluación a seis factores: PIB per cápita, apoyo social, esperanza de
# vida saludable, libertad de elección, generosidad y percepción de corrupción.
# Las cifras se concentran con frecuencia en rankings globales, pero los
# promedios nacionales y regionales pueden ocultar diferencias internas
# relevantes.

# %% [markdown]
# ## Audiencia técnica
#
# Este informe se dirige a **investigadores y analistas del equipo de estudios
# comparativos de bienestar de un organismo internacional**, que necesita
# identificar cómo se distribuyen los indicadores de bienestar **entre** las
# regiones oficiales del reporte y **dentro** de cada una de ellas, para orientar
# comparaciones regionales justificadas y futuras investigaciones. Esta audiencia
# espera definiciones claras de variables, transformaciones documentadas,
# visualizaciones interpretables y un flujo que pueda reproducir completo.

# %% [markdown]
# ## Pregunta analítica
#
# > **¿Qué diferencias en los indicadores de bienestar se identifican entre las
# > regiones oficiales del World Happiness Report 2024, y cuánta variación se
# > observa dentro de cada región?**
#
# La pregunta tiene dos mitades que el informe responde en orden: primero
# **entre** regiones (nivel y composición), luego **dentro** de ellas
# (dispersión de los países que las integran).

# %% [markdown]
# ## Cómo está organizado el informe
#
# | Sección | Contenido | Responde |
# |---|---|---|
# | 1. Datos y preparación | Fuente oficial, verificación de integridad, regiones, variables y transformaciones | ¿Qué datos y con qué criterios? |
# | 2. Visualizaciones estáticas (Seaborn) | Nivel, composición, dispersión y asociación | Las cuatro caras de la pregunta |
# | 3. Visualizaciones interactivas (Plotly) | Exploración de la asociación y rankings de países | Profundizar en los hallazgos |
# | 4. Conclusiones | Respuesta a la pregunta, limitaciones y nuevas preguntas | ¿Qué se pudo responder? |
#
# **Nota metodológica.** Todos los datos de bienestar provienen exclusivamente
# de `WHR24_Data_Figure_2.1.xls` (fuente oficial). Las asociaciones que se
# muestran son descriptivas: **no se interpretan como relaciones causales**.

# %% [markdown]
# ---
# ## 1. Datos y preparación
#
# El análisis importa el archivo oficial, verifica su integridad,
# documenta los criterios de selección de variables y deja una tabla preparada y
# reproducible para el análisis.# %% [markdown]
# ### Construcción del recurso de regiones oficiales del WHR
#
# El archivo oficial `WHR24_Data_Figure_2.1.xls` **no incluye** la clasificación
# regional de los países. Para la Opción B del proyecto (diferencias entre
# regiones) necesitamos esa taxonomía.
#
# **Fuente de la taxonomía:** los propios archivos oficiales del World Happiness
# Report (figura 2.1) de ediciones anteriores, que sí incluían la columna
# `Regional indicator`:
# - `WHR21_Data_Figure_2.1.xls` (149 países) — fuente principal.
# - `WHR20_Data_Figure_2.1.xls` — solo para `Congo (Kinshasa)`, ausente en WHR21.
#
# La taxonomía regional del WHR es fija (10 regiones) y solo se usa aquí como
# **atributo de país**; ningún dato de bienestar proviene de otros años.
# El resultado es `datos/WHR24_regiones_oficiales.csv`, que se fusiona con el
# WHR24 en el notebook por nombre de país (con homologación de 5 nombres).

from pathlib import Path
import pandas as pd

# Rutas robustas: localizan datos/ desde la raíz, Proyecto2/ o notebook/
def _encontrar_base():
    for candidata in [Path("."), Path(".."), Path("Proyecto2")]:
        if (candidata / "datos" / "WHR24_Data_Figure_2.1.xls").exists():
            return candidata
    return Path(".")

BASE = _encontrar_base()
DATOS = BASE / "datos"

whr21 = pd.read_excel(DATOS / "WHR21_Data_Figure_2.1_fuente_regiones.xls")
whr20 = pd.read_excel(DATOS / "WHR20_Data_Figure_2.1_fuente_regiones.xls")

# 1. Regiones desde WHR21 (fuente principal)
regiones = whr21[["Country name", "Regional indicator"]].drop_duplicates()

# 2. Complemento desde WHR20: países del WHR24 ausentes en WHR21
whr24 = pd.read_excel(DATOS / "WHR24_Data_Figure_2.1.xls")
faltantes = set(whr24["Country name"]) - set(regiones["Country name"])
extra = whr20[whr20["Country name"].isin(faltantes)][
    ["Country name", "Regional indicator"]
]
regiones = pd.concat([regiones, extra], ignore_index=True)

# 3. Homologación de nombres (WHR24 → nombre en la taxonomía oficial)
homologacion = {
    "Czechia": "Czech Republic",
    "Eswatini": "Swaziland",
    "State of Palestine": "Palestinian Territories",
    "Turkiye": "Turkey",
}
regiones["pais_original"] = regiones["Country name"]
regiones["Country name"] = (
    regiones["Country name"].replace({v: k for k, v in homologacion.items()})
)
regiones = regiones[["Country name", "Regional indicator"]].drop_duplicates(
    subset="Country name"
)

# 4. Verificación: los 143 países del WHR24 deben tener región
cobertura = whr24[["Country name"]].merge(regiones, on="Country name", how="left")
sin_region = cobertura[cobertura["Regional indicator"].isna()]
assert len(sin_region) == 0, f"Sin región: {sin_region['Country name'].tolist()}"

salida = DATOS / "WHR24_regiones_oficiales.csv"
regiones.to_csv(salida, index=False, encoding="utf-8")
print(f"OK: {len(regiones)} países con región → {salida.name}")
print(regiones["Regional indicator"].value_counts().to_string())
# %% [markdown]
# **Pregunta analítica:** ¿Qué diferencias en los indicadores de bienestar se
# identifican entre las regiones oficiales del World Happiness Report 2024, y
# cuánta variación se observa dentro de cada región?
#
# Esta sección importa el archivo oficial, verifica su integridad, documenta los
# criterios de selección y transformación, y deja una tabla **preparada** para
# el análisis exploratorio.

# %% [markdown]
# ### Importación
#
# - **Fuente obligatoria:** `WHR24_Data_Figure_2.1.xls` (World Happiness Report
#   2024, "Data for Figure 2.1"), descargado de la página oficial
#   `files.worldhappiness.report`. Todos los datos de bienestar provienen de este
#   archivo.
# - **Archivo de apoyo:** `WHR24_regiones_oficiales.csv` contiene la taxonomía
#   regional oficial del WHR (10 regiones). El archivo WHR24 no incluye la región
#   de cada país, y este proyecto la necesita para la comparación por grupos. El
#   CSV se generó con `scripts/01_regiones_oficiales.py` a partir de los archivos
#   oficiales WHR21 y WHR20 (solo la columna de región; ningún dato de bienestar
#   proviene de otros años).

# %% tags=["hide-input"]
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.io as pio

# ------------------------------------------------------------- Configuración
# Rutas relativas robustas: localizan datos/ desde la raíz, Proyecto2/ o notebook/
def _encontrar_base():
    for candidata in [Path("."), Path(".."), Path("Proyecto2")]:
        if (candidata / "datos" / "WHR24_Data_Figure_2.1.xls").exists():
            return candidata
    return Path(".")

BASE = _encontrar_base()
DATOS = BASE / "datos"

# Paleta semántica por región (consistente en todo el proyecto)
PALETA_REGIONES = {
    "Western Europe": "#0173B2",
    "Central and Eastern Europe": "#56B4E9",
    "Commonwealth of Independent States": "#949494",
    "North America and ANZ": "#029E73",
    "Latin America and Caribbean": "#ECE133",
    "East Asia": "#DE8F05",
    "Southeast Asia": "#FBAFE4",
    "Middle East and North Africa": "#CC78BC",
    "South Asia": "#D55E00",
    "Sub-Saharan Africa": "#CA9161",
}
NOMBRE_CORTO = {
    "Western Europe": "Europa Occidental",
    "Central and Eastern Europe": "Europa Central y del Este",
    "Commonwealth of Independent States": "CEI",
    "North America and ANZ": "Norteamérica y ANZ",
    "Latin America and Caribbean": "Latinoamérica y Caribe",
    "East Asia": "Asia Oriental",
    "Southeast Asia": "Asia Sudoriental",
    "Middle East and North Africa": "Oriente Medio y N. de África",
    "South Asia": "Asia Meridional",
    "Sub-Saharan Africa": "África Subsahariana",
}
# Columnas originales → nombres cortos (legibles en gráficos)
COLS_CONTRIB = {
    "Explained by: Log GDP per capita": "contrib_pib",
    "Explained by: Social support": "contrib_apoyo_social",
    "Explained by: Healthy life expectancy": "contrib_esperanza_vida",
    "Explained by: Freedom to make life choices": "contrib_libertad",
    "Explained by: Generosity": "contrib_generosidad",
    "Explained by: Perceptions of corruption": "contrib_corrupcion",
}
NOMBRE_CONTRIB = {
    "contrib_pib": "PIB per cápita",
    "contrib_apoyo_social": "Apoyo social",
    "contrib_esperanza_vida": "Esperanza de vida saludable",
    "contrib_libertad": "Libertad de elección",
    "contrib_generosidad": "Generosidad",
    "contrib_corrupcion": "Percepción de corrupción",
}
COLS_CORTAS = {
    "Country name": "pais",
    "Ladder score": "evaluacion_vida",
    "upperwhisker": "ic_superior",
    "lowerwhisker": "ic_inferior",
    "Regional indicator": "region",
    "Dystopia + residual": "dystopia_residual",
}
DIVERGENTE = ["#C2410C", "#F1F5F9", "#1D4ED8"]  # naranja → gris → azul

# Estilo de gráficos
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update(
    {
        "figure.dpi": 110,
        "savefig.dpi": 300,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)
# Renderer de Plotly embebido en el notebook (gráficos interactivos reales)
pio.renderers.default = "notebook"

# %% [markdown]
# #### Carga y verificación de la fuente

# %%
whr = pd.read_excel(DATOS / "WHR24_Data_Figure_2.1.xls", engine="calamine")
regiones = pd.read_csv(DATOS / "WHR24_regiones_oficiales.csv")

print(f"Archivo WHR24: {whr.shape[0]} países, {whr.shape[1]} columnas")
print(f"Archivo de regiones: {regiones.shape[0]} países, {regiones.shape[1]} columnas")
whr.head(3)

# %% [markdown]
# **Estructura observada.** El archivo trae:
#
# - `Country name`: país.
# - `Ladder score`: evaluación de vida promedio 2021–2023 (escala Cantril 0–10).
# - `upperwhisker` / `lowerwhisker`: límites del intervalo de confianza del 95%.
# - 6 columnas `Explained by: ...`: **contribución de cada factor** (en puntos de
#   la escalera) a la evaluación de vida, según la descomposición oficial del
#   WHR.
# - `Dystopia + residual`: contribución del escenario "distopía" más el residuo
#   (lo no explicado por los seis factores).
#
# > **Nota metodológica:** el archivo WHR24 no incluye los *indicadores crudos*
# > (PIB, apoyo social, etc.) sino sus **contribuciones explicadas**. Toda la
# > comparación del proyecto se basa en estas contribuciones, que están en la
# > misma unidad (puntos de escalera) y por lo tanto son comparables entre sí.

# %%
# Tipos de datos y valores faltantes
info = pd.DataFrame({
    "tipo": whr.dtypes.astype(str),
    "no_nulos": whr.notna().sum(),
    "faltantes": whr.isna().sum(),
})
info[info["faltantes"] > 0]  # solo columnas con faltantes

# %% [markdown]
# ### Verificación de integridad
#
# Según el modelo del WHR, la suma de las seis contribuciones más
# `Dystopia + residual` debe reproducir el `Ladder score`. Comprobamos que la
# diferencia sea numéricamente nula.

# %%
cols_explicacion = list(COLS_CONTRIB) + ["Dystopia + residual"]
completas = whr[cols_explicacion].notna().all(axis=1)
whr["suma_explicacion"] = whr[cols_explicacion].sum(axis=1)
whr["dif_ladder"] = (whr["suma_explicacion"] - whr["Ladder score"]).abs()

dif_max = whr.loc[completas, "dif_ladder"].max()
print(f"Países con contribuciones completas: {completas.sum()} de {len(whr)}")
print(f"Diferencia máxima |suma − ladder|: {dif_max:.6f}")
print("✓ Integridad verificada: contribuciones + dystopia = evaluación de vida"
      if dif_max < 1e-3
      else "⚠ Revisar: la suma no reproduce el ladder")

# %% [markdown]
# ### Países con información incompleta
#
# Tres países no tienen valores en las columnas de contribución. **Criterio
# documentado:** se conservan en el dataset (su `Ladder score` e intervalo son
# válidos y se usan para las distribuciones y comparaciones de evaluación de
# vida), pero se **excluyen de los análisis que requieren las contribuciones**,
# porque no existe imputación oficial y fabricar un valor distorsionaría la
# comparación.

# %%
faltantes = whr[whr[cols_explicacion].isna().any(axis=1)]
print("Países sin contribuciones:")
print(faltantes[["Country name", "Ladder score"]].to_string(index=False))

# %% [markdown]
# ### Fusión con la región
#
# Unimos la taxonomía regional oficial del WHR por nombre de país. La homología
# de 5 nombres (cambios de nomenclatura entre ediciones del reporte) quedó
# resuelta al construir el CSV de regiones y se verifica aquí con un anti-join.

# %%
df = whr.merge(regiones, on="Country name", how="left")
sin_region = df[df["Regional indicator"].isna()]
print(f"Países sin región asignada: {len(sin_region)}")
assert len(sin_region) == 0, sin_region["Country name"].tolist()
print("✓ Los 143 países tienen región oficial asignada.")

# %% [markdown]
# ### Renombrado de columnas y tabla preparada
#
# Renombramos a nombres cortos en español para que los gráficos sean legibles, y
# marcamos los países con contribuciones completas.

# %%
df = df.rename(columns={**COLS_CORTAS, **COLS_CONTRIB})
df["contribuciones_completas"] = df[list(COLS_CONTRIB.values())].notna().all(axis=1)
df["region_corta"] = df["region"].map(NOMBRE_CORTO)

# Orden analítico de regiones: por mediana de evaluación de vida (mayor → menor)
orden_regiones = (
    df.groupby("region")["evaluacion_vida"].median().sort_values(ascending=False).index.tolist()
)
df["region"] = pd.Categorical(df["region"], categories=orden_regiones, ordered=True)

columnas_finales = [
    "pais", "region", "region_corta", "evaluacion_vida", "ic_inferior", "ic_superior",
    *COLS_CONTRIB.values(), "dystopia_residual", "contribuciones_completas",
]
df = df[columnas_finales].sort_values("evaluacion_vida", ascending=False).reset_index(drop=True)
df.to_csv(DATOS / "WHR24_preparado.csv", index=False, encoding="utf-8")

print(f"Tabla preparada: {df.shape[0]} países × {df.shape[1]} columnas")
print(f"Guardada en: {DATOS / 'WHR24_preparado.csv'}")
df.head(3)

# %% [markdown]
# ### Vista general del conjunto preparado
#
# Estas cifras orientan la lectura de los gráficos siguientes.

# %%
resumen = pd.DataFrame({
    "evaluacion_vida": df["evaluacion_vida"].describe()[["count", "min", "25%", "50%", "75%", "max"]].round(2),
})
print("Evaluación de vida (0–10):")
print(resumen.to_string())
print(f"\nRegiones: {df['region'].nunique()} | Países: {df['pais'].nunique()}")
print("\nPaíses por región:")
print(df["region_corta"].value_counts().reindex(
    [NOMBRE_CORTO[r] for r in orden_regiones]).to_string())

# %% [markdown]
# ### Exploración numérica inicial: medianas por región
#
# Primera lectura de la pregunta: ¿cómo se comparan las regiones en la evaluación
# de vida y en cada contribución? Esta tabla guiará la selección y el orden de
# los gráficos.

# %%
contribs = list(COLS_CONTRIB.values())
medianas = (
    df.groupby("region", observed=True)[["evaluacion_vida"] + contribs]
    .median()
    .reindex(orden_regiones)
    .rename(columns={"evaluacion_vida": "Evaluación de vida", **NOMBRE_CONTRIB})
    .round(2)
)
medianas.index = [NOMBRE_CORTO[r] for r in medianas.index]
medianas

# %% [markdown]
# **Lectura preliminar (asociativa, no causal).** Las regiones difieren tanto en
# el nivel de evaluación de vida como en la estructura de contribuciones: por
# ejemplo, Europa Occidental y Norteamérica/ANZ concentran altas contribuciones de
# PIB y apoyo social, mientras que regiones como África Subsahariana muestran
# contribuciones bajas y mayor heterogeneidad interna. Estas observaciones se
# examinarán gráficamente en las secciones siguientes.

# %% [markdown]
# ### Resumen de preparación
#
# | Decisión | Criterio |
# |---|---|
# | Fuente única de bienestar | `WHR24_Data_Figure_2.1.xls` (oficial) |
# | Regiones | Taxonomía oficial WHR (CSV generado por script reproducible) |
# | Integridad | Verificada: contribuciones + dystopia = ladder |
# | Faltantes | 3 países conservados para evaluación de vida; excluidos de contribuciones |
# | Unidad de análisis | Contribuciones en puntos de escalera (comparables entre sí) |
# | Orden de regiones | Por mediana de evaluación de vida (mayor → menor) |
# | Tabla preparada | `datos/WHR24_preparado.csv` (143 países) |
# %% [markdown]
# ## 2. Visualizaciones estáticas (Seaborn)
#
# Los siguientes cuatro gráficos responden, en conjunto, a la pregunta analítica:
# **¿Qué diferencias en los indicadores de bienestar se identifican entre las
# regiones oficiales del World Happiness Report 2024, y cuánta variación se
# observa dentro de cada región?**
#
# **Criterio comunicativo (antes de cada gráfico):** ¿qué necesita examinar el
# analista con esta visualización y qué aporta que no se haya mostrado ya?
#
# | # | Gráfico | Qué examina el analista | Por qué este gráfico |
# |---|---|---|---|
# | 1 | Barras de mediana por región | El nivel típico de cada región | Comparación directa entre grupos, sin formas que interpretar |
# | 2 | Barras apiladas de composición | De qué se arma ese nivel en cada región | Formato oficial del WHR; hace visible lo no explicado (residuo) |
# | 3 | Strip de países por región | Los países concretos y sus extremos | Devuelve el detalle país-level que el promedio regional oculta |
# | 4 | Dispersión apoyo social ↔ evaluación | Fuerza de la asociación global y regional | Contrasta la lectura agregada con la lectura dentro de cada región |
#
# **Criterio de color (Opción 1 — "color con función"):**
# - Región en el eje → el color *no* repite lo que el eje ya dice: datos en
#   neutro `#CBD5E1` y **un solo acento** (MENA, la región destacada del
#   análisis, con su color asignado `#CC78BC`, igual en toda la secuencia).
# - Partes de un todo (Gráfico 2) → escala de **un solo matiz** (azul de oscuro
#   a claro según el tamaño del aporte) + gris para lo no explicado.
# - Identificar grupos donde el eje no basta (gráfico 4) → paleta
#   **cualitativa** de las 10 regiones (base Okabe-Ito, segura para daltonismo).

# %% tags=["hide-input"]
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

# ------------------------------------------------------------------ Rutas
def _encontrar_base():
    """Carpeta que contiene datos/ — funciona desde Proyecto2/, su raíz o notebook/."""
    for candidata in [Path("."), Path(".."), Path("Proyecto2")]:
        if (candidata / "datos" / "WHR24_Data_Figure_2.1.xls").exists():
            return candidata
    return Path(".")

BASE = _encontrar_base()
DATOS = BASE / "datos"
FIGURAS = BASE / "recursos" / "figuras"
FIGURAS.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------- Paleta (Opción 1, fija)
NEUTRO = "#CBD5E1"                       # gris claro: datos no destacados
TEXTO = "#0F172A"                        # títulos
TEXTO_SEC = "#64748B"                    # ejes / notas
ACENTO_MENA = "#CC78BC"                  # color asignado a MENA (consistente)
PALETA_REGIONES = {
    "North America and ANZ": "#0173B2",
    "Western Europe": "#56B4E9",
    "Central and Eastern Europe": "#949494",
    "Latin America and Caribbean": "#ECE133",
    "East Asia": "#DE8F05",
    "Southeast Asia": "#FBAFE4",
    "Commonwealth of Independent States": "#029E73",
    "Middle East and North Africa": "#CC78BC",
    "Sub-Saharan Africa": "#CA9161",
    "South Asia": "#D55E00",
}
NOMBRE_CORTO = {
    "North America and ANZ": "Norteamérica y ANZ",
    "Western Europe": "Europa Occidental",
    "Central and Eastern Europe": "Europa Central y del Este",
    "Latin America and Caribbean": "Latinoamérica y Caribe",
    "East Asia": "Asia Oriental",
    "Southeast Asia": "Asia Sudoriental",
    "Commonwealth of Independent States": "CEI",
    "Middle East and North Africa": "Oriente Medio y N. de África",
    "Sub-Saharan Africa": "África Subsahariana",
    "South Asia": "Asia Meridional",
}

# Estilo: fondo neutro, sin esquinas superiores/derechas
sns.set_theme(style="whitegrid", context="notebook")
mpl.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 300,
    "axes.spines.top": False, "axes.spines.right": False,
    "text.color": TEXTO, "axes.labelcolor": TEXTO_SEC,
    "xtick.color": TEXTO_SEC, "ytick.color": TEXTO_SEC,
})

# ------------------------------------------------------------------ Datos
df = pd.read_csv(DATOS / "WHR24_preparado.csv")
orden = df.groupby("region")["evaluacion_vida"].median().sort_values(ascending=False).index
orden_corto = [NOMBRE_CORTO[r] for r in orden]
df["region_ord"] = pd.Categorical(df["region_corta"], categories=orden_corto, ordered=True)

DESTACADA = NOMBRE_CORTO["Middle East and North Africa"]   # mayor variación interna
COLOR_X_REGION = {
    NOMBRE_CORTO[r]: (ACENTO_MENA if NOMBRE_CORTO[r] == DESTACADA else NEUTRO)
    for r in orden
}
CONTRIB_ORDER = ["contrib_pib", "contrib_apoyo_social", "contrib_libertad",
                 "contrib_esperanza_vida", "contrib_generosidad", "contrib_corrupcion"]
NOMBRE_CONTRIB = {
    "contrib_pib": "PIB per cápita",
    "contrib_apoyo_social": "Apoyo social",
    "contrib_libertad": "Libertad de elección",
    "contrib_esperanza_vida": "Esperanza de vida saludable",
    "contrib_generosidad": "Generosidad",
    "contrib_corrupcion": "Percepción de corrupción",
}
FUENTE = "Fuente: World Happiness Report 2024 — Data for Figure 2.1 (promedios 2021–2023). Elaboración propia."


def nota_fuente(fig):
    fig.text(0.01, 0.012, FUENTE, fontsize=8, color=TEXTO_SEC, ha="left")


def guardar(fig, nombre):
    fig.savefig(FIGURAS / f"{nombre}.png", bbox_inches="tight", facecolor="white")


# %% [markdown]
# ### Gráfico 1 — Evaluación de vida por región
#
# **¿Qué necesita examinar el analista?** Cuánto difieren las regiones entre sí
# en su nivel de evaluación de vida: la comparación básica que enmarca la
# pregunta.
#
# **Por qué barras:** es la forma más directa y familiar de comparar grupos
# ordenados. La barra muestra la **mediana** de la región y el número da la
# cifra exacta. La variación *dentro* de cada región se examina en el
# Gráfico 3, con los datos de cada país.

# %% tags=["hide-input"]
# Mediana por región (el valor que representa la barra)
med_reg = (
    df.groupby("region_ord", observed=True)["evaluacion_vida"]
    .median().reindex(orden_corto)
)
i_mena = orden_corto.index(DESTACADA)

fig, ax = plt.subplots(figsize=(10, 6))
# Sin hue: cada barra ocupa todo su ancho (con hue, Seaborn lo divide entre 10)
sns.barplot(
    data=df, x="evaluacion_vida", y="region_ord",
    order=orden_corto, color=NEUTRO, width=0.8,
    estimator=np.median, errorbar=None, ax=ax,
)

# Acento: la región destacada conserva su color asignado
for rect in ax.patches:
    centro_y = rect.get_y() + rect.get_height() / 2
    if abs(centro_y - i_mena) < 0.3:
        rect.set_facecolor(ACENTO_MENA)

# Valor exacto de cada mediana al final de su barra
for i, valor in enumerate(med_reg):
    ax.text(valor + 0.08, i, f"{valor:.2f}",
            va="center", fontsize=9.5, color=TEXTO)

# Referencia: mediana global
ax.axvline(df["evaluacion_vida"].median(), color=TEXTO, ls="--", lw=1.2, alpha=0.7)
ax.set_xlim(0, 8.3)
ax.set_ylim(9.7, -0.85)
ax.text(df["evaluacion_vida"].median() + 0.08, -0.55,
        f"Mediana global ({df['evaluacion_vida'].median():.2f})",
        fontsize=9, color=TEXTO, va="center", ha="left")

from matplotlib.patches import Patch
ax.legend(
    handles=[
        Patch(facecolor=NEUTRO, edgecolor="none", label="Mediana por región"),
        Patch(facecolor=ACENTO_MENA, edgecolor="none", label="MENA"),
    ],
    loc="lower right", fontsize=9, frameon=True,
)

ax.set(
    title="Evaluación de vida por región",
    xlabel="Evaluación de vida (0–10)",
    ylabel="Región",
)
ax.tick_params(labelsize=9.5)
fig.text(0.01, 0.012, FUENTE + "  Barra = mediana.",
         fontsize=8, color=TEXTO_SEC, ha="left")
fig.tight_layout(rect=(0, 0.03, 1, 1))
guardar(fig, "fig1_barras_evaluacion_por_region")
plt.show()

# %% [markdown]
# **Interpretación (Gráfico 1).**
#
# Las barras ordenan las regiones por nivel de evaluación de vida: de
# Norteamérica y ANZ (mediana 6.96) a Asia Meridional (3.98), una distancia de
# casi 3 puntos en una escala de 10 —casi un tercio del rango posible—. Tres
# grupos se sitúan por encima de la mediana global (5.79) y los tres últimos
# claramente por debajo: CEI (5.58), Oriente Medio y Norte de África (4.98),
# África Subsahariana (4.38) y Asia Meridional (3.98). La comparación
# establece **cuánto difieren las regiones entre sí**; qué tan homogéneas son
# por dentro lo examina el Gráfico 3.
#
# *Cautela:* cada barra resume un promedio trianual de entre 4 y 35 países; las
# diferencias observadas no dicen nada sobre sus causas.

# %% [markdown]
# ### Gráfico 2 — Composición del bienestar por región
#
# **¿Qué necesita examinar el analista?** De qué se "arma" la evaluación de vida
# en cada región: cuánto aporta cada uno de los seis indicadores y cuánto queda
# fuera de ellos.
#
# **Por qué barras apiladas:** es el formato del gráfico oficial del propio
# World Happiness Report, así que resulta familiar. La barra completa es la
# evaluación media de la región; cada bloque es la aportación media de un
# indicador. Se usa una escala de azules de oscuro a claro según el tamaño
# habitual del aporte, y gris para lo que los seis indicadores **no** explican.

# %% tags=["hide-input"]
FACTORES = [
    ("contrib_pib", "PIB per cápita", "#1E3A8A"),
    ("contrib_apoyo_social", "Apoyo social", "#1D4ED8"),
    ("contrib_libertad", "Libertad de elección", "#3B82F6"),
    ("contrib_esperanza_vida", "Esperanza de vida saludable", "#60A5FA"),
    ("contrib_generosidad", "Generosidad", "#93C5FD"),
    ("contrib_corrupcion", "Percepción de corrupción", "#BFDBFE"),
    ("dystopia_residual", "Dystopia + residuo (no explicado)", "#94A3B8"),
]

medias = (
    df.groupby("region_ord", observed=True)[[c for c, _, _ in FACTORES]]
    .mean().reindex(orden_corto)
)

fig, ax = plt.subplots(figsize=(10, 6))
izq = np.zeros(len(orden_corto))
for col, etiqueta, color in FACTORES:
    ax.barh(orden_corto, medias[col].values, left=izq,
            color=color, height=0.62, edgecolor="white", linewidth=0.8,
            label=etiqueta)
    izq += medias[col].values

# Evaluación media total al final de cada barra
for i, total in enumerate(izq):
    ax.text(total + 0.09, i, f"{total:.2f}", va="center", fontsize=9, color=TEXTO)

ax.set_xlim(0, 8.3)
ax.axvline(df["evaluacion_vida"].median(), color=TEXTO, ls="--", lw=1.2, alpha=0.7)
ax.text(df["evaluacion_vida"].median() + 0.06, 9.45,
        f"Mediana global ({df['evaluacion_vida'].median():.2f})",
        fontsize=9, color=TEXTO, va="center", ha="left")
ax.set_ylim(9.7, -0.85)

ax.set(
    title="Composición del bienestar por región",
    xlabel="Contribución a la evaluación de vida (puntos)",
    ylabel="Región",
)
ax.tick_params(labelsize=9.5)
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8.5,
          frameon=True, title="Indicador", title_fontsize=9)
fig.text(0.01, 0.012, FUENTE + "  Barra = media; bloques = aportación media de cada indicador.",
         fontsize=8, color=TEXTO_SEC, ha="left")
fig.tight_layout(rect=(0, 0.03, 0.80, 1))
guardar(fig, "fig2_composicion_por_region")
plt.show()

# %% [markdown]
# **Interpretación (Gráfico 2).**
#
# La composición explica por qué las barras del Gráfico 1 son de distinta
# longitud. En **todas** las regiones el PIB y el apoyo social son los dos
# bloques más grandes (juntos, entre 1.5 y 3.3 puntos), y en **todas** la
# generosidad y la percepción de corrupción son casi residuales (juntos, menos de
# 0.6 puntos). Las diferencias de composición se leen en los bloques medios:
# **Oriente Medio y Norte de África tiene el bloque de libertad más pequeño de
# todas las regiones** (0.49 puntos), mientras que Asia Sudoriental tiene uno de
# los mayores (0.77) pese a tener evaluación media; y **Norteamérica/ANZ y Europa
# Occidental destacan en esperanza de vida y corrupción** (0.65–0.71 y 0.31–0.34).
# El bloque gris revela un hallazgo importante para las conclusiones: **entre
# 1.0 y 2.1 puntos de la evaluación no quedan explicados por los seis
# indicadores** —el "Dystopia + residuo" del modelo—, comparable en tamaño a
# varios indicadores juntos.
#
# *Cautela:* los bloques son **contribuciones del modelo del WHR**, no
# indicadores crudos, y sus sumas reproducen el ladder por construcción (verificado
# en la Sección 1). Se usan medias porque las contribuciones son aditivas; se
# excluyeron 3 países sin datos (Bahréin, Tayikistán, Palestina).

# %% [markdown]
# ### Gráfico 3 — Los países dentro de cada región (strip)
#
# **¿Qué necesita examinar el analista?** Qué países concretos producen los
# promedios y los rangos anteriores: los extremos reales y el tamaño de cada
# grupo. El Gráfico 1 resume con mediana; este gráfico **muestra los datos
# crudos** y cuánto se dispersan alrededor de esa mediana.
#
# **Por qué un stripplot:** devuelve la granularidad de país, hace visible el
# tamaño desigual de cada región (n = 4 … n = 35) y permite anotar los casos
# extremos, evitando que el lector confíe en promedios sin ver su base.

# %% tags=["hide-input"]
fig, ax = plt.subplots(figsize=(10, 6))
sns.stripplot(
    data=df, x="evaluacion_vida", y="region_ord",
    hue="region_ord", hue_order=orden_corto, palette=COLOR_X_REGION,
    order=orden_corto, jitter=0.16, size=6.5, alpha=0.9, legend=False, ax=ax,
)

# Mediana de cada región (rombo) — codificación adicional que no depende del color
medianas = df.groupby("region_ord", observed=True)["evaluacion_vida"].median().reindex(orden_corto)
ax.scatter(medianas.values, range(len(orden_corto)), marker="D", s=45,
           color=TEXTO, zorder=5, label="Mediana regional")

# Extremos anotados (casos que sostienen la lectura)
for pais, dx, dy in [("Finland", -0.12, 0.22), ("Afghanistan", 0.16, -0.34),
                     ("Israel", -0.16, 0.28), ("Lebanon", 0.16, -0.34)]:
    fila = df[df["pais"] == pais]
    if fila.empty:
        continue
    fila = fila.iloc[0]
    y = orden_corto.index(fila["region_corta"])
    ax.annotate(f"{pais} ({fila['evaluacion_vida']:.2f})",
                xy=(fila["evaluacion_vida"], y),
                xytext=(fila["evaluacion_vida"] + dx, y + dy),
                fontsize=8.5, color=TEXTO,
                arrowprops=dict(arrowstyle="-", color=TEXTO_SEC, lw=0.8))

ax.axvline(df["evaluacion_vida"].median(), color=TEXTO, ls="--", lw=1.2, alpha=0.7)
# n por región en las etiquetas del eje (fijando los ticks antes de etiquetar)
etiquetas = [t.get_text() for t in ax.get_yticklabels()]
posiciones = ax.get_yticks()
ax.set_yticks(posiciones)
ax.set_yticklabels(
    [f"{c}  (n={int((df['region_corta'] == c).sum())})" for c in etiquetas],
    fontsize=9.5,
)
ax.legend(loc="lower right", frameon=True, fontsize=9)
ax.set(
    title="Evaluación de vida por país y región",
    xlabel="Evaluación de vida (0–10)",
    ylabel="Región",
)
nota_fuente(fig)
fig.tight_layout(rect=(0, 0.03, 1, 1))
guardar(fig, "fig3_strip_paises_por_region")
plt.show()

# %% [markdown]
# **Interpretación (Gráfico 3).**
#
# El gráfico añade la variación dentro de cada región, que el Gráfico 1 no
# muestra. En **MENA**,
# los 17 países abarcan de Líbano (2.71) a Israel (7.34): una separación de 4.63
# puntos que equivale a recorrer casi todo el ranking mundial (posiciones 5.ª a
# 142.ª) dentro de una misma región. **Asia Meridional** (n = 6) combina el
# mínimo global, Afganistán (1.72), con Nepal (5.16). En el extremo opuesto,
# **Norteamérica y ANZ** (n = 4) y **Europa Occidental** muestran nubes compactas
# y alineadas con sus medianas. El gráfico también hace visible una asimetría
# muestral: África Subsahariana aporta 35 países y Norteamérica/ANZ solo 4, de
# modo que la comparación de dispersión entre regiones debe leerse con ese
# contraste de tamaños.
#
# *Cautela:* cada punto es un promedio nacional trianual con su incertidumbre
# propia (los intervalos de confianza del archivo original no se representan aquí
# para no saturar el gráfico); los extremos nombrados ilustran, no resumen, la
# distribución.

# %% [markdown]
# ### Gráfico 4 — Asociación entre apoyo social y evaluación de vida
#
# **¿Qué necesita examinar el analista?** Si la relación entre un indicador
# central (apoyo social) y la evaluación de vida se sostiene cuando se mira
# **dentro** de cada región, o si es un patrón que solo aparece al agregar
# países. Este es el gráfico donde el color *sí* trabaja: los puntos no llevan la
# región en el eje, así que la paleta cualitativa de las 10 regiones los identifica.
#
# **Por qué scatter + recta global:** permite ver simultáneamente la asociación
# agregada (recta) y la estructura interna (racimos regionales), que es donde la
# cautela inferencial es decisiva.

# %% tags=["hide-input"]
fig, ax = plt.subplots(figsize=(10, 6.4))
sns.scatterplot(
    data=df, x="contrib_apoyo_social", y="evaluacion_vida",
    hue="region_ord", hue_order=orden_corto,
    palette={k: PALETA_REGIONES[r] for k, r in zip(orden_corto, orden)},
    s=62, alpha=0.9, edgecolor="white", linewidth=0.5, ax=ax,
)
sns.regplot(
    data=df, x="contrib_apoyo_social", y="evaluacion_vida",
    scatter=False, ci=None, color=TEXTO, line_kws={"lw": 2, "ls": "--", "alpha": 0.8},
    ax=ax,
)
ax.text(0.985, 0.03, "Recta de ajuste global (r = 0.81)",
        transform=ax.transAxes, ha="right", fontsize=9, color=TEXTO, style="italic")

ax.set(
    title="Apoyo social y evaluación de vida",
    xlabel="Contribución del apoyo social (puntos)",
    ylabel="Evaluación de vida (0–10)",
)
leg = ax.legend(title="Región", loc="center left", bbox_to_anchor=(1.01, 0.5),
                frameon=True, fontsize=9, title_fontsize=10)
nota_fuente(fig)
fig.tight_layout(rect=(0, 0.03, 0.86, 1))
guardar(fig, "fig4_scatter_apoyo_social")
plt.show()

# %% [markdown]
# **Interpretación (Gráfico 4).**
#
# La recta global resume una asociación fuerte y positiva (r = 0.81): los países
# donde el apoyo social aporta más puntos tienden a evaluar su vida mejor. Los
# racimos regionales muestran que gran parte de esa relación opera **entre**
# regiones: Europa Occidental y Norteamérica/ANZ concentran la esquina
# alta-alta, África Subsahariana y Asia Meridional la baja-baja. Al mirar
# **dentro** de cada región, la asociación se debilita de forma desigual: es
# alta en Norteamérica/ANZ (r = 0.83) y Europa Occidental (0.78), moderada en
# Asia Sudoriental (0.77), pero casi nula en Asia Oriental (0.14) y débil en
# Latinoamérica (0.28). Es decir: **el patrón agregado no se sostiene por igual
# en todos los grupos**, un recordatorio de que la correlación global mezcla
# diferencias entre regiones con diferencias dentro de ellas.
#
# *Cautela inferencial:* (1) existe un vínculo **parte-todo**: el eje es un
# componente de la variable del eje y, por construcción, correlacionarse con el
# total es en parte mecánico; (2) la relación es **asociación, no causalidad**:
# nada aquí permite afirmar que aumentar el apoyo social elevaría la evaluación
# de vida; (3) r calculada sobre 140 países con contribuciones completas.

# %% [markdown]
# ### Síntesis de la Sección 2
#
# Los cuatro gráficos cubren la pregunta en capas complementarias sin repetirse:
#
# 1. **Nivel** de cada región (barras de mediana).
# 2. **Composición** del bienestar por región (barras apiladas, con el residuo no explicado).
# 3. **Detalle país y extremos** que sostienen los promedios (strip).
# 4. **Fuerza de la asociación** global vs. regional (scatter con recta).
#
# Todos usan el mismo orden de regiones y el mismo color semántico (MENA
# acentuada con `#CC78BC`, neutro `#CBD5E1` en el resto), cumpliendo el criterio
# de "color con función" de la Opción 1.
# %% [markdown]
# ## 3. Visualizaciones interactivas (Plotly)
#
# Dos gráficos con **propósitos analíticos diferenciados** que profundizan lo que
# los estáticos no pueden mostrar:
#
# | # | Gráfico | Interactividad | Qué permite examinar |
# |---|---|---|---|
# | 5 | Evaluación de vida por país | Desplegable de indicador + leyenda clicable para filtrar regiones + zoom/hover | Cómo cambia la relación indicador ↔ evaluación al elegir otro indicador o centrarse en una región |
# | 6 | Países líderes y rezagados por indicador | Desplegable de indicador (7 rankings) + leyenda de regiones + hover | Qué países lideran/cierran cada indicador y cómo cambia el orden al medir otra cosa |
#
# Ambos se muestran embebidos en el notebook (`fig.show()`) y se exportan a un
# **archivo HTML** de presentación.

# %% tags=["hide-input"]
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# Renderer: gráficos Plotly reales e interactivos dentro del notebook
pio.renderers.default = "notebook"

# ------------------------------------------------------------------ Rutas
def _encontrar_base():
    """Carpeta que contiene datos/ — funciona desde Proyecto2/, su raíz o notebook/."""
    for candidata in [Path("."), Path(".."), Path("Proyecto2")]:
        if (candidata / "datos" / "WHR24_preparado.csv").exists():
            return candidata
    return Path(".")

BASE = _encontrar_base()
DATOS = BASE / "datos"
ENTREGABLES = BASE / "entregables"
ENTREGABLES.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------- Paleta (misma que la Sección 2)
PALETA_REGIONES = {
    "North America and ANZ": "#0173B2",
    "Western Europe": "#56B4E9",
    "Central and Eastern Europe": "#949494",
    "Latin America and Caribbean": "#ECE133",
    "East Asia": "#DE8F05",
    "Southeast Asia": "#FBAFE4",
    "Commonwealth of Independent States": "#029E73",
    "Middle East and North Africa": "#CC78BC",
    "Sub-Saharan Africa": "#CA9161",
    "South Asia": "#D55E00",
}
NOMBRE_CORTO = {
    "North America and ANZ": "Norteamérica y ANZ",
    "Western Europe": "Europa Occidental",
    "Central and Eastern Europe": "Europa Central y del Este",
    "Latin America and Caribbean": "Latinoamérica y Caribe",
    "East Asia": "Asia Oriental",
    "Southeast Asia": "Asia Sudoriental",
    "Commonwealth of Independent States": "CEI",
    "Middle East and North Africa": "Oriente Medio y N. de África",
    "Sub-Saharan Africa": "África Subsahariana",
    "South Asia": "Asia Meridional",
}
CONTRIB_ORDER = ["contrib_pib", "contrib_apoyo_social", "contrib_libertad",
                 "contrib_esperanza_vida", "contrib_generosidad", "contrib_corrupcion"]
NOMBRE_CONTRIB = {
    "contrib_pib": "PIB per cápita",
    "contrib_apoyo_social": "Apoyo social",
    "contrib_libertad": "Libertad",
    "contrib_esperanza_vida": "Esperanza de vida",
    "contrib_generosidad": "Generosidad",
    "contrib_corrupcion": "Corrupción",
}
TEXTO = "#0F172A"
TEXTO_SEC = "#64748B"

# ------------------------------------------------------------------ Datos
df = pd.read_csv(DATOS / "WHR24_preparado.csv")
orden = df.groupby("region")["evaluacion_vida"].median().sort_values(ascending=False).index
orden_corto = [NOMBRE_CORTO[r] for r in orden]
df["region_ord"] = pd.Categorical(df["region_corta"], categories=orden_corto, ordered=True)
completas = df[df["contribuciones_completas"]].copy()   # 140 países con contribuciones

# %% [markdown]
# ### Gráfico 5 — Evaluación de vida por país
#
# **¿Qué necesita examinar el analista?** Si la relación entre cada indicador y
# la evaluación de vida se sostiene al mirar países concretos, eligiendo el
# indicador y la región que le interesan.
#
# **Qué aporta la interactividad (no decorativa):** el desplegable cambia el
# indicador del eje X (6 relaciones en un solo espacio); la leyenda filtra por
# región al hacer clic; el hover da el nombre del país y sus valores exactos;
# el zoom permite inspeccionar racimos. La recta de ajuste global cambia con el
# indicador y su hover muestra la correlación.

# %% tags=["hide-input"]
n_ind = len(CONTRIB_ORDER)
n_reg = len(orden_corto)
traces = []

for i, ind in enumerate(CONTRIB_ORDER):
    # Recta de ajuste global del indicador
    x_all, y_all = completas[ind].values, completas["evaluacion_vida"].values
    pendiente, ordenada = np.polyfit(x_all, y_all, 1)
    r_global = np.corrcoef(x_all, y_all)[0, 1]
    x_min, x_max = x_all.min(), x_all.max()

    for reg in orden_corto:
        sub = completas[completas["region_ord"] == reg]
        region_original = dict(zip(orden_corto, orden))[reg]
        traces.append(go.Scatter(
            x=sub[ind], y=sub["evaluacion_vida"], text=sub["pais"],
            mode="markers", name=reg,
            legendgroup=reg, showlegend=(i == 0),
            marker=dict(color=PALETA_REGIONES[region_original], size=9,
                        line=dict(width=0.5, color="white")),
            hovertemplate="<b>%{text}</b><br>Contribución: %{x:.2f} pts"
                          "<br>Evaluación: %{y:.2f}<extra>%{fullData.name}</extra>",
        ))
    traces.append(go.Scatter(
        x=[x_min, x_max],
        y=[pendiente * x_min + ordenada, pendiente * x_max + ordenada],
        mode="lines", name="Ajuste lineal global", showlegend=False,
        line=dict(color=TEXTO, width=2, dash="dash"),
        hovertemplate=f"Ajuste lineal global (r = {r_global:.2f})<extra></extra>",
    ))

# Botones de visibilidad: cada indicador = bloque de 10 regiones + 1 recta
botones = []
for i, ind in enumerate(CONTRIB_ORDER):
    base = i * (n_reg + 1)
    vis = [False] * len(traces)
    for j in range(n_reg + 1):
        vis[base + j] = True
    botones.append(dict(
        label=NOMBRE_CONTRIB[ind], method="update",
        args=[{"visible": vis},
              {"xaxis.title.text": f"{NOMBRE_CONTRIB[ind]} (puntos)"}],
    ))

fig_pais = go.Figure(data=traces, layout=dict(
    title=dict(text="Evaluación de vida por país", x=0.5, xanchor="center"),
    updatemenus=[dict(
        type="dropdown", direction="down", x=0.0, xanchor="left", y=1.16, yanchor="top",
        buttons=botones, font=dict(size=12),
        bgcolor="white", bordercolor="#CBD5E1", borderwidth=1,
    )],
    xaxis=dict(title="PIB per cápita (puntos)",
               gridcolor="#EDF2F7", zeroline=False),
    yaxis=dict(title="Evaluación de vida (0–10)", gridcolor="#EDF2F7", zeroline=False),
    legend=dict(title=dict(text="Región"), font=dict(size=11)),
    margin=dict(t=110, l=60, r=30, b=60),
    plot_bgcolor="white", paper_bgcolor="white",
    font=dict(color=TEXTO),
    annotations=[dict(
        text="Fuente: World Happiness Report 2024 — Data for Figure 2.1. "
             "Haga clic en la leyenda para filtrar regiones.",
        xref="paper", yref="paper", x=0, y=-0.16, showarrow=False,
        font=dict(size=10, color=TEXTO_SEC),
    )],
))
fig_pais.show()

# %% [markdown]
# **Interpretación (Gráfico 5).**
#
# Con el indicador inicial (PIB per cápita) la nube muestra una relación
# positiva: los países con mayor contribución del PIB tienden a evaluar su vida
# mejor, pero con mucha dispersión vertical —hay países con la misma contribución
# y evaluaciones distintas—. Al cambiar de indicador se comprueba que **no todos
# los indicadores se relacionan igual**: apoyo social presenta la nube más
# alineada (r = 0.81), mientras que generosidad apenas muestra patrón (r
# cercano a 0). Al filtrar por región con la leyenda, el racimo se acota y se
# hace visible lo que el Gráfico 4 resumía en cifras: **dentro de una región la
# relación es más débil que entre regiones**. La recta global sirve de referencia
# para medir cuánto se separa cada región de esa tendencia.
#
# *Cautela:* la recta y el r describen asociación entre países, no efectos
# causales; los 3 países sin contribuciones no aparecen en este gráfico.

# %% [markdown]
# ### Gráfico 6 — Países líderes y rezagados por indicador
#
# **¿Qué necesita examinar el analista?** Qué países concretos encabizan y
# cierran cada indicador, y cómo cambia ese orden al cambiar de indicador.
#
# **Qué aporta la interactividad:** el desplegable cambia el indicador (siete
# rankings en un solo espacio); la leyenda filtra por región; el hover entrega
# el país y su valor exacto. La utilidad analítica es comprobar que **el ranking
# depende del indicador elegido**: los países que lideran la evaluación no son
# necesariamente los que lideran cada componente.

# %% tags=["hide-input"]
INDICADORES = [("evaluacion_vida", "Evaluación de vida (0–10)")] + [
    (c, f"{NOMBRE_CONTRIB[c]} (puntos)") for c in CONTRIB_ORDER
]
N_TOP = 10

traces_rank = []
for ind, etiqueta in INDICADORES:
    d = df.dropna(subset=[ind]).sort_values(ind, ascending=False)
    top = d.head(N_TOP).iloc[::-1]          # ascendente → el líder arriba
    bot = d.tail(N_TOP).iloc[::-1]
    for sub, parte in [(top, "top"), (bot, "bottom")]:
        regiones_sub = sub["region"].map(
            dict(zip(orden, [PALETA_REGIONES[r] for r in orden])))
        traces_rank.append(go.Bar(
            x=sub[ind], y=sub["pais"], orientation="h",
            name=etiqueta, legendgroup=parte,
            showlegend=False,
            marker=dict(color=regiones_sub,
                        line=dict(width=0.5, color="white")),
            customdata=np.stack([sub["region"].map(NOMBRE_CORTO)], axis=-1),
            hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>"
                          + etiqueta + ": %{x:.2f}<extra></extra>",
            visible=(ind == "evaluacion_vida"),
        ))

n_bloques = len(INDICADORES)
botones_rank = []
for i, (ind, etiqueta) in enumerate(INDICADORES):
    vis = [False] * len(traces_rank)
    vis[2 * i] = True
    vis[2 * i + 1] = True
    botones_rank.append(dict(
        label=etiqueta.split(" (")[0], method="update",
        args=[{"visible": vis},
              {"xaxis.title.text": etiqueta}],
    ))

fig_rank = go.Figure(data=traces_rank, layout=dict(
    title=dict(text="Países líderes y rezagados por indicador", x=0.5, xanchor="center"),
    updatemenus=[dict(
        type="dropdown", direction="down", x=0.0, xanchor="left", y=1.16, yanchor="top",
        buttons=botones_rank, font=dict(size=12),
        bgcolor="white", bordercolor="#CBD5E1", borderwidth=1,
    )],
    barmode="overlay",
    xaxis=dict(title="Evaluación de vida (0–10)", gridcolor="#EDF2F7", zeroline=False),
    yaxis=dict(title="", tickfont=dict(size=10), autorange="reversed"),
    margin=dict(t=110, l=140, r=30, b=50),
    plot_bgcolor="white", paper_bgcolor="white",
    font=dict(color=TEXTO),
    height=760,
    annotations=[dict(
        text="Fuente: World Happiness Report 2024 — Data for Figure 2.1. "
             "Color = región (leyenda del Gráfico 5). Top 10 y bottom 10 del indicador.",
        xref="paper", yref="paper", x=0, y=-0.09, showarrow=False,
        font=dict(size=10, color=TEXTO_SEC),
    )],
))
fig_rank.show()

# %% [markdown]
# **Interpretación (Gráfico 6).**
#
# El ranking de líderes y rezagados cambia por completo según el indicador
# elegido, y ese es su aporte: **no existe un solo "país líder"**. En
# evaluación de vida dominan los países nórdicos (Finlandia 7.74, Dinamarca
# 7.58, Islandia 7.53); en PIB per cápita aparecen Luxemburgo (2.14), Irlanda
# (2.13) y Singapur (2.12), este último también primero en percepción de
# corrupción (0.58); en generosidad encabezan Myanmar (0.40) e Indonesia
# (0.40) —países de evaluación media-baja—; y en esperanza de vida saludable
# lideran Hong Kong (0.86), Japón (0.78) y Corea del Sur (0.77), ninguno de
# ellos entre los cinco primeros en evaluación general. El contraste entre el bloque superior y el
# inferior de cada indicador hace visible cuánto separa a los extremos —y cuán
# distinto es el orden según lo que se mida—, profundizando en los datos a
# nivel país, algo que los gráficos regionales no muestran.
#
# *Cautela:* son contribuciones del modelo WHR (parte del ladder), no niveles
# absolutos; ordenar por ellas no implica que el indicador cause la posición
# general del país.

# %% [markdown]
# ### Exportación a HTML
#
# Un único archivo con ambas visualizaciones para la presentación (mismo código
# que genera las figuras del notebook).

# %% tags=["hide-input"]
html_pais = pio.to_html(fig_pais, full_html=False, include_plotlyjs=True)
html_rank = pio.to_html(fig_rank, full_html=False, include_plotlyjs=False)
html_total = (
    "<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"utf-8\">"
    "<title>Proyecto 2 — Visualizaciones interactivas (Plotly)</title>"
    "<style>body{font-family:sans-serif;margin:24px;color:#0F172A}"
    "h1{font-size:18px}section{margin-bottom:40px}</style></head>\n<body>\n"
    "<h1>Proyecto 2 — Visualizaciones interactivas · World Happiness Report 2024</h1>\n"
    f"<section>{html_pais}</section>\n<section>{html_rank}</section>\n"
    "</body>\n</html>\n"
)
salida = ENTREGABLES / "Proyecto2_Graficos_Interactivos.html"
salida.write_text(html_total, encoding="utf-8")
print(f"HTML guardado: {salida} ({salida.stat().st_size / 1e6:.1f} MB)")
# %% [markdown]
# ---
# ## 4. Conclusiones
#
# ### Respuesta a la pregunta analítica
#
# **¿Qué diferencias entre las regiones oficiales?** Diferencias grandes y de dos
# tipos. En **nivel**, las medianas de evaluación de vida van desde 6.96 en
# Norteamérica y ANZ hasta 3.98 en Asia Meridional: casi 3 puntos en una escala
# de 10, con solo tres regiones por encima de la mediana global (5.79). En
# **composición**, todas las regiones se apoyan en el PIB y el apoyo social como
# bloques más grandes y todas aportan poco por generosidad y percepción de
# corrupción; las diferencias están en los bloques medios —la menor contribución
# de libertad de toda la tabla es la de Oriente Medio y Norte de África (0.49
# puntos), mientras que Asia Sudoriental llega a 0.77 pese a su nivel
# intermedio— y en un hallazgo de modelo: **entre 1.0 y 2.1 puntos de cada
# barra no quedan explicados por los seis indicadores** (Dystopia + residuo).
#
# **¿Cuánta variación dentro de cada región?** La variación interna es tan
# relevante como la diferencia entre regiones, y no es proporcional al nivel:
# Norteamérica y ANZ se mueve en apenas 0.33 puntos entre sus cuatro países,
# mientras que **Oriente Medio y Norte de África abarca 4.63 puntos** —de
# Líbano (2.71) a Israel (7.34)— y Asia Meridional, 3.44 —de Afganistán (1.72)
# a Nepal (5.16)—. En otras palabras: **el promedio regional es un resumen
# fiel en las regiones homogéneas y engañoso en las heterogéneas**, donde
# conviven países de extremos opuestos del ranking mundial.
#
# **Síntesis:** las regiones difieren en cuánto valora su población su vida, en
# de qué están hechas esas valoraciones y en cuánta diversidad interna ocultan.
# Quien compara regiones debe mirar siempre las tres cosas: nivel, composición y
# dispersión.

# %% [markdown]
# ### Limitaciones del análisis
#
# 1. **Contribuciones, no indicadores crudos.** El archivo WHR24 publica la
#    aportación de cada factor al ladder, no los valores originales de PIB,
#    apoyo social, etc.; el análisis describe cómo se compone la evaluación, no
#    los niveles materiales de cada país.
# 2. **Datos faltantes.** 3 de 143 países (Bahréin, Tayikistán y Palestina) no
#    tienen contribuciones: se conservan para evaluación de vida y se excluyen
#    de los análisis de composición, sin imputar.
# 3. **Tamaños muestrales desiguales.** Las regiones van de 4 a 35 países; la
#    dispersión de una región grande tiene más oportunidad de aparecer que la
#    de una pequeña.
# 4. **Ventana temporal.** Todo se resume en promedios 2021–2023: el informe no
#    analiza evolución ni años individuales.
# 5. **Asociación, no causalidad.** Ningún gráfico sustenta afirmaciones
#    causales; en el caso de apoyo social y evaluación existe además un vínculo
#    parte-todo (la contribución es componente del total).
# 6. **Residuo no explicado.** Entre 1.0 y 2.1 puntos por región quedan fuera
#    de los seis factores: las conclusiones de composición son una lectura
#    parcial del modelo.

# %% [markdown]
# ### Nuevas preguntas de investigación
#
# - ¿Qué variables —fuera de los seis factores del modelo— explican el bloque
#   de *Dystopia + residuo*, y por qué pesa más en unas regiones que en otras?
# - ¿Se sostienen las diferencias de nivel y dispersión en la serie anual
#   2012–2023, o son propias del trienio 2021–2023?
# - ¿Cómo cambia la comparación regional si se usan datos individuales (edad,
#   género) en lugar de promedios nacionales?
# - ¿Por qué la asociación entre apoyo social y evaluación es fuerte entre
#   regiones pero casi nula dentro de algunas (Asia Oriental, r = 0.14)?

# %% [markdown]
# ### Reproducibilidad
#
# El notebook se ejecuta de principio a fin sin pasos manuales: requiere únicamente
# los archivos de `datos/` (fuente oficial + recurso de regiones generado por
# script) y las dependencias de `requirements.txt`. Todas las transformaciones
# están documentadas en la Sección 1 y cada visualización conserva su fuente al
# pie.