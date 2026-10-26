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
