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
