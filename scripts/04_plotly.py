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
# **¿Qué necesita examinar el analista?** Qué países concretos encabezan y
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
salida = ENTREGABLES / "Equipo3_Proyecto2_Graficos_Interactivos.html"
salida.write_text(html_total, encoding="utf-8")
print(f"HTML guardado: {salida} ({salida.stat().st_size / 1e6:.1f} MB)")
