# %% [markdown]
# # Generación de la presentación web del proyecto
#
# Construye `entregables/Proyecto2_Presentacion.html`: página profesional de
# scroll con narrativa, evidencias (figuras Seaborn embebidas en base64) y los
# **dos gráficos Plotly interactivos en vivo**, 100% sin internet (plotly.js,
# figuras y datos van dentro del archivo).
#
# Regenerable: si cambia un gráfico, se vuelve a ejecutar este script.

# %% tags=["hide-input"]
from pathlib import Path
import base64
import runpy
import plotly.graph_objects as go
import plotly.io as pio

# ------------------------------------------------------------------ Rutas
def _base():
    for c in [Path("."), Path(".."), Path("Proyecto2")]:
        if (c / "entregables").exists() and (c / "scripts").exists():
            return c
    return Path(".")

BASE = _base()
FIG = BASE / "recursos" / "figuras"
ENT = BASE / "entregables"

# ------------------------------------------------------- Figuras Plotly
# Ejecuta 04_plotly.py con show() anulado para obtener las dos figuras en vivo.
_show_orig = go.Figure.show
go.Figure.show = lambda self, *a, **k: None
try:
    ns = runpy.run_path(str(BASE / "scripts" / "04_plotly.py"))
finally:
    go.Figure.show = _show_orig
fig_pais, fig_rank = ns["fig_pais"], ns["fig_rank"]
json_pais, json_rank = fig_pais.to_json(), fig_rank.to_json()
print(f"Plotly: scatter {len(json_pais)/1e3:.0f} KB · ranking {len(json_rank)/1e3:.0f} KB")

# --------------------------------------------------- Assets offline (b64)
def b64(nombre: str) -> str:
    return base64.b64encode((FIG / nombre).read_bytes()).decode()

img = {
    "fig1": b64("fig1_barras_evaluacion_por_region.png"),
    "fig2": b64("fig2_composicion_por_region.png"),
    "fig3": b64("fig3_strip_paises_por_region.png"),
    "fig4": b64("fig4_scatter_apoyo_social.png"),
}

import plotly
plotly_js = (Path(plotly.__file__).parent / "package_data" / "plotly.min.js").read_text(encoding="utf-8")
print(f"plotly.js: {len(plotly_js)/1e6:.1f} MB · figuras b64: {sum(len(v) for v in img.values())/1e6:.1f} MB")

# ------------------------------------------------------------------ CSS
CSS = """
:root{
  --ink:#0F172A; --slate:#64748B; --line:#E2E8F0; --soft:#F8FAFC;
  --blue:#1D4ED8; --blue2:#0173B2; --blue-deep:#1E3A8A;
  --mena:#CC78BC; --ok:#029E73;
  --white:#fff; --radius:16px;
  --shadow:0 8px 30px rgba(15,23,42,.10);
  --shadow-lg:0 24px 70px rgba(15,23,42,.22);
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:"SF Mono",Consolas,Menlo,monospace;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:var(--font);color:var(--ink);background:var(--white);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:var(--blue);text-decoration:none}
.wrap{max-width:1120px;margin:0 auto;padding:0 32px}
section{scroll-margin-top:24px}

/* ---------- progreso de lectura ---------- */
#progress{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--blue2),var(--blue));z-index:120;transition:width .1s linear}

/* ---------- nav lateral scroll-spy ---------- */
#sidenav{position:fixed;left:22px;top:50%;transform:translateY(-50%);z-index:110;display:flex;flex-direction:column;gap:14px}
#sidenav a{display:flex;align-items:center;gap:10px;color:var(--slate);font-size:12px;font-weight:600}
#sidenav .dot{width:9px;height:9px;border-radius:50%;background:var(--line);border:2px solid var(--slate);transition:all .3s}
#sidenav .lbl{opacity:0;transform:translateX(-6px);transition:all .3s;white-space:nowrap;background:var(--ink);color:#fff;padding:3px 10px;border-radius:20px}
#sidenav a:hover .lbl{opacity:1;transform:none}
#sidenav a.active .dot{background:var(--blue);border-color:var(--blue);transform:scale(1.5)}
#sidenav a.active{color:var(--blue)}
@media(max-width:1240px){#sidenav{display:none}}

/* ---------- hero ---------- */
.hero{min-height:92vh;display:flex;align-items:center;background:radial-gradient(1200px 600px at 80% -10%,#2445a8 0%,transparent 60%),linear-gradient(160deg,#0F172A 0%,#132a52 55%,#0F172A 100%);color:#fff;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;inset:0;background:
  radial-gradient(420px 420px at 88% 78%,rgba(204,120,188,.16),transparent 70%),
  radial-gradient(300px 300px at 12% 20%,rgba(1,115,178,.22),transparent 70%);pointer-events:none}
.hero .wrap{position:relative;z-index:2;padding-top:70px;padding-bottom:70px}
.kicker{font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:#8ab4ff;font-weight:700;margin-bottom:18px}
.hero h1{font-size:clamp(34px,5vw,58px);line-height:1.12;font-weight:800;max-width:900px;letter-spacing:-.02em}
.hero h1 em{font-style:normal;color:#ffd479}
.hero .sub{margin-top:22px;font-size:clamp(15px,1.6vw,19px);color:#c6d2e8;max-width:720px}
.meta{margin-top:34px;display:flex;flex-wrap:wrap;gap:12px}
.meta span{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);padding:8px 16px;border-radius:30px;font-size:13.5px;font-weight:600;backdrop-filter:blur(4px)}
.scroll-hint{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);color:#9fb4d8;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;z-index:2;animation:bob 2.2s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(8px)}}

/* ---------- secciones ---------- */
.sec{padding:92px 0}
.sec.tinted{background:var(--soft);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.kick{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--blue);background:rgba(29,78,216,.09);padding:5px 14px;border-radius:30px;margin-bottom:16px}
h2{font-size:clamp(26px,3.2vw,38px);line-height:1.2;font-weight:800;letter-spacing:-.015em;margin-bottom:18px}
h3{font-size:19px;font-weight:750;margin-bottom:10px}
.lead{font-size:17.5px;color:#334155;max-width:780px}
.lead b{color:var(--ink)}
p{margin-bottom:14px;color:#334155}
.muted{color:var(--slate);font-size:14.5px}

/* ---------- pregunta destacada ---------- */
.question{margin-top:34px;background:linear-gradient(135deg,var(--ink),var(--blue-deep));color:#fff;border-radius:var(--radius);padding:38px 40px;box-shadow:var(--shadow-lg);position:relative;overflow:hidden}
.question::before{content:"¿";position:absolute;right:22px;top:-30px;font-size:170px;font-weight:800;color:rgba(255,255,255,.07);line-height:1}
.question .tag{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:#ffd479;font-weight:800;margin-bottom:12px}
.question p{color:#e8eefc;font-size:clamp(18px,2.2vw,25px);font-weight:650;line-height:1.45;margin:0;position:relative;z-index:1}

/* ---------- KPIs ---------- */
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:36px}
.kpi{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:24px 22px;box-shadow:var(--shadow)}
.kpi .num{font-size:clamp(30px,3.4vw,42px);font-weight:800;color:var(--blue);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.kpi .cap{font-size:13.5px;color:var(--slate);font-weight:600;margin-top:4px}
@media(max-width:860px){.kpis{grid-template-columns:repeat(2,1fr)}}

/* ---------- tabla ---------- */
.tblwrap{margin-top:30px;overflow-x:auto;border-radius:var(--radius);box-shadow:var(--shadow)}
.tbl{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line)}
.tbl td,.tbl th{padding:13px 18px;text-align:left;font-size:14.5px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl tr:last-child td{border-bottom:none}
.tbl td:first-child{font-weight:750;color:var(--ink);background:var(--soft);width:150px;white-space:nowrap}
.tbl th{background:var(--blue-deep);color:#fff;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
.tbl code{background:#eef2ff;color:var(--blue-deep);padding:1px 6px;border-radius:5px;font-size:13px;font-family:var(--mono);word-break:break-all}
@media(max-width:640px){
  .tbl td,.tbl th{padding:9px 11px;font-size:13.5px}
  .tbl td:first-child{width:auto;white-space:normal}
}

/* ---------- checklist preparación ---------- */
.checks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:30px}
.check{display:flex;gap:14px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px;box-shadow:var(--shadow);min-width:0}
.check .mark{flex:none;width:26px;height:26px;border-radius:50%;background:rgba(2,158,115,.12);display:flex;align-items:center;justify-content:center;margin-top:1px}
.check .mark svg{width:15px;height:15px;stroke:var(--ok);stroke-width:3.2;fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:24;stroke-dashoffset:24;transition:stroke-dashoffset .6s ease .25s}
.check.in .mark svg{stroke-dashoffset:0}
.check b{display:block;font-size:15px;color:var(--ink);overflow-wrap:anywhere}
.check span{font-size:13.8px;color:var(--slate)}
@media(max-width:860px){.checks{grid-template-columns:1fr}}

/* ---------- evidencias: layout alternado ---------- */
.evidence{display:grid;grid-template-columns:minmax(300px,40%) 1fr;gap:46px;align-items:center}
.evidence.flip{grid-template-columns:1fr minmax(300px,40%)}
.evidence.flip .ev-text{order:2}
.evidence.flip .ev-fig{order:1}
.ev-text .kick{margin-bottom:12px}
.ev-text h2{font-size:clamp(23px,2.6vw,31px)}
.ev-text .note{margin-top:16px;background:#fff;border-left:3px solid var(--blue);padding:12px 16px;border-radius:0 10px 10px 0;font-size:14.5px;color:#334155;box-shadow:var(--shadow)}
.ev-text .note b{color:var(--ink)}
@media(max-width:960px){
  .evidence,.evidence.flip{grid-template-columns:1fr;gap:24px}
  .evidence.flip .ev-text{order:1}.evidence.flip .ev-fig{order:2}
}

/* ---------- figuras + lightbox ---------- */
.figcard{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:14px;box-shadow:var(--shadow);cursor:zoom-in;transition:transform .35s,box-shadow .35s;position:relative}
.figcard:hover{transform:translateY(-5px);box-shadow:var(--shadow-lg)}
.figcard .zoomtip{position:absolute;top:14px;right:16px;background:rgba(15,23,42,.78);color:#fff;font-size:11.5px;padding:4px 11px;border-radius:20px;opacity:0;transition:opacity .3s;pointer-events:none}
.figcard:hover .zoomtip{opacity:1}
#lightbox{position:fixed;inset:0;background:rgba(8,12,24,.93);z-index:200;display:none;align-items:center;justify-content:center;padding:36px;cursor:zoom-out}
#lightbox.open{display:flex}
#lightbox img{max-width:96vw;max-height:92vh;border-radius:10px;box-shadow:0 30px 90px rgba(0,0,0,.6);animation:zin .3s ease}
@keyframes zin{from{transform:scale(.94);opacity:.4}to{transform:none;opacity:1}}
#lightbox .close{position:absolute;top:22px;right:30px;color:#fff;font-size:34px;font-weight:300;cursor:pointer;line-height:1}

/* ---------- scrollytelling (fig3) ---------- */
.scrolly{display:grid;grid-template-columns:1fr minmax(300px,370px);gap:44px;margin-top:34px}
.scrolly-fig{position:sticky;top:12vh;height:76vh;background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);display:flex;align-items:center;justify-content:center}
.scrolly-fig img{width:100%;height:100%;object-fit:contain;transform-origin:0 0;transition:transform .85s cubic-bezier(.22,.61,.36,1)}
.steps{display:flex;flex-direction:column;gap:0}
.step{min-height:78vh;display:flex;align-items:center}
.step .box{background:#fff;border:1px solid var(--line);border-radius:14px;padding:24px 26px;box-shadow:var(--shadow);opacity:.38;transform:translateY(10px);transition:all .5s}
.step.active .box{opacity:1;transform:none;border-color:var(--blue);box-shadow:0 12px 40px rgba(29,78,216,.16)}
.step .n{font-size:12px;font-weight:800;letter-spacing:.16em;color:var(--blue);text-transform:uppercase;margin-bottom:8px}
.step h3{font-size:17.5px}
.step p{font-size:14.6px;margin:0}
.step .hl{color:var(--mena);font-weight:750}
@media(max-width:960px){
  .scrolly{grid-template-columns:1fr;gap:16px}
  .scrolly-fig{height:46vh;top:8vh}
  .step{min-height:60vh}
}

/* ---------- plotly en vivo ---------- */
.livegrid{display:grid;grid-template-columns:1fr;gap:34px;margin-top:34px}
.livecard{background:#fff;border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden}
.livecard .head{padding:20px 26px 6px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.livecard h3{margin:0;font-size:17.5px}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{font-size:12px;font-weight:700;background:#eef2ff;color:var(--blue-deep);border:1px solid #dbe4ff;padding:4px 12px;border-radius:20px;white-space:nowrap}
.chip.g{background:#e7f7f1;color:#047857;border-color:#bfe8db}
.livecard .plot{padding:6px 10px 16px;min-height:540px}
.livecard .foot{padding:10px 26px 16px;font-size:13.5px;color:var(--slate);border-top:1px dashed var(--line)}

/* ---------- hallazgos ---------- */
.finds{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:34px}
.find{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:26px 22px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.find::before{content:"";position:absolute;left:0;top:0;height:100%;width:4px;background:linear-gradient(180deg,var(--blue2),var(--blue))}
.find .big{font-size:clamp(28px,3vw,38px);font-weight:800;color:var(--ink);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.find .big small{font-size:.55em;color:var(--slate);font-weight:700}
.find p{font-size:14px;margin:8px 0 0;color:var(--slate)}
@media(max-width:960px){.finds{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.finds{grid-template-columns:1fr}}

/* ---------- conclusiones 2 cols ---------- */
.cols2{display:grid;grid-template-columns:1.25fr 1fr;gap:34px;margin-top:30px}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:28px 30px;box-shadow:var(--shadow)}
.card.dark{background:linear-gradient(150deg,var(--ink),var(--blue-deep));border:none;color:#e8eefc}
.card.dark h3{color:#fff}
.card.dark p{color:#cdd8f2}
.card ul{list-style:none}
.card li{font-size:14.6px;color:#334155;padding-left:26px;position:relative;margin-bottom:11px}
.card.dark li{color:#cdd8f2}
.card li::before{content:"→";position:absolute;left:0;color:var(--blue);font-weight:800}
.card.dark li::before{content:"!";color:#ffd479}
@media(max-width:860px){.cols2{grid-template-columns:1fr}}

/* ---------- entregables ---------- */
.deliv{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:30px}
.deliv .check b{font-family:var(--mono);font-size:13.6px}
@media(max-width:860px){.deliv{grid-template-columns:1fr}}

footer{background:var(--ink);color:#93a4c3;padding:46px 0 40px;font-size:14px}
footer .wrap{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;align-items:center}
footer b{color:#fff}

/* ---------- reveal / animaciones ---------- */
.reveal{opacity:0;transform:translateY(28px);transition:opacity .75s cubic-bezier(.22,.61,.36,1),transform .75s cubic-bezier(.22,.61,.36,1)}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  .reveal{opacity:1;transform:none;transition:none}
  .scrolly-fig img{transition:none}
  .scroll-hint{animation:none}
  html{scroll-behavior:auto}
}
"""


# ------------------------------------------------------------------ HTML
BODY = """
<div id="progress"></div>

<nav id="sidenav">
  <a href="#inicio" data-sec="inicio"><span class="dot"></span><span class="lbl">Inicio</span></a>
  <a href="#problema" data-sec="problema"><span class="dot"></span><span class="lbl">El problema</span></a>
  <a href="#datos" data-sec="datos"><span class="dot"></span><span class="lbl">Los datos</span></a>
  <a href="#preparacion" data-sec="preparacion"><span class="dot"></span><span class="lbl">Preparación</span></a>
  <a href="#evidencias" data-sec="evidencias"><span class="dot"></span><span class="lbl">Evidencias</span></a>
  <a href="#exploracion" data-sec="exploracion"><span class="dot"></span><span class="lbl">Exploración en vivo</span></a>
  <a href="#hallazgos" data-sec="hallazgos"><span class="dot"></span><span class="lbl">Hallazgos</span></a>
  <a href="#conclusiones" data-sec="conclusiones"><span class="dot"></span><span class="lbl">Conclusiones</span></a>
  <a href="#entregables" data-sec="entregables"><span class="dot"></span><span class="lbl">Entregables</span></a>
</nav>

<!-- ============ HERO ============ -->
<header class="hero" id="inicio">
  <div class="wrap">
    <div class="kicker">Proyecto 2 · Visualización de Datos con Python</div>
    <h1>Bienestar por regiones: qué ocultan los <em>promedios</em> del World Happiness Report 2024</h1>
    <p class="sub">Un análisis exploratorio reproducible con Seaborn y Plotly que compara el bienestar
    <b>entre</b> las 10 regiones oficiales del reporte y <b>dentro</b> de cada una de ellas.</p>
    <div class="meta">
      <span>Juan Tomás Rincón</span>
      <span>Alejandro Pardo Costo</span>
      <span>143 países · 10 regiones</span>
      <span>Octubre 2026</span>
    </div>
  </div>
  <div class="scroll-hint">desliza para explorar ↓</div>
</header>

<!-- ============ EL PROBLEMA ============ -->
<section class="sec" id="problema">
  <div class="wrap">
    <div class="reveal">
      <span class="kick">El problema</span>
      <h2>Un número por país, y todo lo que desaparece detrás</h2>
      <p class="lead">El <b>World Happiness Report 2024</b> publica cómo evalúan su vida las personas de
      143 países en una escala de 0 a 10 (promedios 2021–2023), junto con una descomposición que reparte
      esa evaluación entre seis factores. Los rankings resumen cada país con un solo número… pero las
      <b>agregaciones regionales pueden ocultar brechas internas enormes</b>: dos regiones con el mismo
      promedio pueden estar formadas por países muy distintos entre sí.</p>
      <p class="lead">La comparación entre regiones solo es honesta si se miran a la vez el nivel, la
      composición y la dispersión interna. De ahí nace este informe.</p>
    </div>

    <div class="question reveal">
      <div class="tag">Pregunta analítica</div>
      <p>¿Qué diferencias en los indicadores de bienestar se identifican entre las regiones oficiales
      del World Happiness Report 2024, y cuánta variación se observa dentro de cada región?</p>
    </div>

    <p class="muted reveal" style="margin-top:22px"><b>Audiencia técnica:</b> investigadores y analistas de un
    organismo internacional que necesitan comparar regiones de forma justificada y reproducible.</p>
  </div>
</section>

<!-- ============ LOS DATOS ============ -->
<section class="sec tinted" id="datos">
  <div class="wrap">
    <div class="reveal">
      <span class="kick">Los datos</span>
      <h2>Fuente oficial, una sola vez</h2>
      <p class="lead">Todo el bienestar proviene exclusivamente del archivo oficial del reporte.
      Las regiones provienen de la taxonomía oficial del WHR (atributo de país; ningún dato de
      bienestar de otros años entra en el análisis).</p>
    </div>

    <div class="kpis reveal">
      <div class="kpi"><div class="num" data-count="143">0</div><div class="cap">países analizados</div></div>
      <div class="kpi"><div class="num" data-count="10">0</div><div class="cap">regiones oficiales</div></div>
      <div class="kpi"><div class="num" data-count="6">0</div><div class="cap">factores explicativos</div></div>
      <div class="kpi"><div class="num" data-text="0–10">0–10</div><div class="cap">escala Cantril</div></div>
    </div>

    <div class="tblwrap reveal">
    <table class="tbl">
      <tr><th>Elemento</th><th>Descripción</th></tr>
      <tr><td>Fuente</td><td><code>WHR24_Data_Figure_2.1.xls</code> — World Happiness Report 2024, archivo oficial <i>Data for Figure 2.1</i></td></tr>
      <tr><td>Cobertura</td><td>143 países; promedios trianuales <b>2021–2023</b>; escala Cantril de evaluación de vida 0–10 + intervalo de confianza del 95%</td></tr>
      <tr><td>Variables</td><td>Evaluación de vida + contribuciones de 6 factores (PIB per cápita, apoyo social, esperanza de vida saludable, libertad, generosidad, percepción de corrupción) y bloque <i>Dystopia + residuo</i> — todo en puntos de escalera</td></tr>
      <tr><td>Región</td><td>Taxonomía oficial de 10 regiones del WHR (construida por script reproducible desde archivos oficiales WHR21/WHR20, solo como atributo de país)</td></tr>
      <tr><td>Preparación</td><td>Homologación de 5 nombres de país · integridad verificada (contribuciones + residuo = evaluación ✓) · 3 países sin contribuciones documentados y sin imputar · tabla final 143 × 14</td></tr>
    </table>
    </div>
  </div>
</section>

<!-- ============ PREPARACIÓN ============ -->
<section class="sec" id="preparacion">
  <div class="wrap">
    <div class="reveal">
      <span class="kick">Preparación</span>
      <h2>Antes de graficar: verificar</h2>
      <p class="lead">El notebook documenta cada paso; aquí está el resumen de las comprobaciones
      que se ejecutan en cada corrida.</p>
    </div>
    <div class="checks reveal">
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>Fuente oficial importada</b><span>WHR24_Data_Figure_2.1.xls verificado: 143 filas, 11 columnas, formato y tipos correctos.</span></div></div>
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>Integridad del modelo ✓</b><span>Las 6 contribuciones + residuo reproducen la evaluación de vida (diferencia máxima 0.00005).</span></div></div>
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>Regiones 143/143</b><span>Taxonomía oficial asignada a todos los países; homologación de 5 nombres entre ediciones verificada con anti-join.</span></div></div>
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>Faltantes documentados</b><span>Bahréin, Tayikistán y Palestina: conservados para evaluación de vida, excluidos de composición (140/143), sin imputar.</span></div></div>
    </div>
  </div>
</section>

<!-- ============ EVIDENCIAS 1 y 2 ============ -->
<section class="sec tinted" id="evidencias">
  <div class="wrap">
    <div class="reveal" style="margin-bottom:44px">
      <span class="kick">Evidencias · Seaborn</span>
      <h2>Cuatro lecturas de la misma pregunta</h2>
      <p class="lead">Cada gráfico llena un vacío distinto: nivel, composición, variación interna y
      asociación. Haz clic en cualquier figura para ampliarla.</p>
    </div>

    <div class="evidence reveal" style="margin-bottom:72px">
      <div class="ev-text">
        <span class="kick">Evidencia 1 · Nivel</span>
        <h2>¿Cuánto difieren las regiones?</h2>
        <p>Las medianas van de <b>6.96</b> (Norteamérica y ANZ) a <b>3.98</b> (Asia Meridional):
        casi <b>3 puntos en una escala de 10</b>. Solo tres regiones superan la mediana global
        de 5.79; las tres últimas quedan claramente por debajo.</p>
        <div class="note"><b>Por qué este gráfico:</b> es la comparación directa — barras con el valor
        exacto, sin formas que exijan explicación previa.</div>
      </div>
      <div class="ev-fig">
        <figure class="figcard" data-img="__IMG1__">
          <span class="zoomtip">clic para ampliar</span>
          <img src="__IMG1__" alt="Evaluación de vida por región: barras de mediana">
        </figure>
      </div>
    </div>

    <div class="evidence flip reveal">
      <div class="ev-text">
        <span class="kick">Evidencia 2 · Composición</span>
        <h2>¿De qué se arma cada barra?</h2>
        <p>En <b>todas</b> las regiones el PIB y el apoyo social son los bloques más grandes;
        generosidad y corrupción aportan menos de 0.6 puntos juntos. <b>Oriente Medio y Norte de
        África tiene la menor contribución de libertad de toda la tabla (0.49)</b>.</p>
        <div class="note"><b>Hallazgo de modelo:</b> entre <b>1.0 y 2.1 puntos</b> de cada barra
        (bloque gris) quedan <b>fuera de los seis indicadores</b> — el residuo es comparable a
        varios factores juntos.</div>
      </div>
      <div class="ev-fig">
        <figure class="figcard" data-img="__IMG2__">
          <span class="zoomtip">clic para ampliar</span>
          <img src="__IMG2__" alt="Composición del bienestar por región: barras apiladas">
        </figure>
      </div>
    </div>
  </div>
</section>

<!-- ============ EV 3: SCROLLYTELLING ============ -->
<section class="sec" id="variacion">
  <div class="wrap">
    <div class="reveal">
      <span class="kick">Evidencia 3 · Variación interna</span>
      <h2>Lo que el promedio regional esconde</h2>
      <p class="lead">Cada punto es un país. Sigue leyendo: la figura se acerca sola a los dos
      extremos de la dispersión.</p>
    </div>

    <div class="scrolly">
      <div class="scrolly-fig">
        <img id="fig3zoom" src="__IMG3__" alt="Evaluación de vida por país y región (strip plot)">
      </div>
      <div class="steps">
        <div class="step" data-s="1" data-cx="0.5" data-cy="0.5">
          <div class="box">
            <div class="n">Vista general</div>
            <h3>143 países, 10 regiones</h3>
            <p>Los puntos están agrupados por región y ordenados por su mediana (de arriba abajo).
            Los rombos negros marcan la mediana de cada región; la línea punteada, la mediana global (5.79).</p>
          </div>
        </div>
        <div class="step" data-s="1.9" data-cx="0.60" data-cy="0.70">
          <div class="box">
            <div class="n">Zoom · heterogénea</div>
            <h3>MENA: 4.63 puntos dentro de una misma región</h3>
            <p>De <span class="hl">Líbano (2.71)</span> a <span class="hl">Israel (7.34)</span>: la
            penúltima y la quinta posición del ranking mundial conviven en la misma región. Su mediana
            (4.98) resume países que no se parecen entre sí.</p>
          </div>
        </div>
        <div class="step" data-s="1.9" data-cx="0.45" data-cy="0.24">
          <div class="box">
            <div class="n">Zoom · homogénea</div>
            <h3>Norteamérica y ANZ: apenas 0.33 puntos</h3>
            <p>Sus 4 países caben en un tercio de punto (6.72–7.06). Aquí el promedio sí representa
            a la región. <b>La variación interna no sigue el nivel</b>: no es raro que las regiones
            más ricas sean también las más parecidas por dentro.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============ EV 4: asociación ============ -->
<section class="sec tinted">
  <div class="wrap">
    <div class="evidence reveal">
      <div class="ev-text">
        <span class="kick">Evidencia 4 · Asociación</span>
        <h2>¿Se sostiene dentro de cada región?</h2>
        <p>Apoyo social y evaluación de vida se relacionan fuertemente entre todos los países
        (<b>r = 0.81</b>), pero al mirar <b>dentro</b> de cada región la relación se debilita de
        forma desigual: de <b>0.83</b> en Norteamérica/ANZ a <b>0.14</b> en Asia Oriental.</p>
        <div class="note"><b>Cautela inferencial:</b> el eje es un componente del total (relación
        parte–todo) y la relación es asociación, no causalidad.</div>
      </div>
      <div class="ev-fig">
        <figure class="figcard" data-img="__IMG4__">
          <span class="zoomtip">clic para ampliar</span>
          <img src="__IMG4__" alt="Apoyo social y evaluación de vida: dispersión con recta global">
        </figure>
      </div>
    </div>
  </div>
</section>

<!-- ============ EXPLORACIÓN EN VIVO ============ -->
<section class="sec" id="exploracion">
  <div class="wrap">
    <div class="reveal">
      <span class="kick">Evidencias · Plotly en vivo</span>
      <h2>Explora tú mismo</h2>
      <p class="lead">Los dos gráficos interactivos del proyecto, funcionando <b>dentro de esta
      página</b> — mismas paletas, mismos datos, sin salir del navegador.</p>
    </div>

    <div class="livegrid reveal">
      <div class="livecard">
        <div class="head">
          <h3>Evaluación de vida por país</h3>
          <div class="chips">
            <span class="chip">↑ desplegable: cambia el indicador</span>
            <span class="chip g">clic en la leyenda: filtra regiones</span>
            <span class="chip">hover: valor por país</span>
          </div>
        </div>
        <div class="plot" id="plot1"></div>
        <div class="foot">Seis relaciones indicador ↔ evaluación en un solo espacio, cada una con su
        recta de ajuste global. Filtra una región y compara cuánto se separa de la tendencia.</div>
      </div>

      <div class="livecard">
        <div class="head">
          <h3>Países líderes y rezagados por indicador</h3>
          <div class="chips">
            <span class="chip">↑ desplegable: 7 indicadores</span>
            <span class="chip g">top 10 + bottom 10</span>
            <span class="chip">hover: país, región y valor</span>
          </div>
        </div>
        <div class="plot" id="plot2"></div>
        <div class="foot">El ranking cambia por completo con el indicador elegido: no existe un
        solo "país líder". Cambia de indicador y observa quién entra y quién sale.</div>
      </div>
    </div>
  </div>
</section>

<!-- ============ HALLAZGOS ============ -->
<section class="sec tinted" id="hallazgos">
  <div class="wrap">
    <div class="reveal">
      <span class="kick">Síntesis</span>
      <h2>Cuatro cifras que resumen el análisis</h2>
    </div>
    <div class="finds reveal">
      <div class="find"><div class="big" data-count="3" data-prefix="≈ " data-suffix=" pts">0</div>
        <p>entre las regiones de mayor y menor mediana (6.96 vs 3.98) en una escala de 10</p></div>
      <div class="find"><div class="big" data-count="4.63" data-dec="2">0</div>
        <p>puntos de rango dentro de MENA: de Líbano (2.71) a Israel (7.34)</p></div>
      <div class="find"><div class="big" data-count="0.81" data-dec="2">0</div>
        <p>correlación apoyo social↔evaluación entre países; dentro de Asia Oriental cae a 0.14</p></div>
      <div class="find"><div class="big" data-count="2.1" data-dec="1" data-prefix="1.0–">0</div>
        <p>puntos de cada barra que los seis indicadores no explican (residuo)</p></div>
    </div>
  </div>
</section>

<!-- ============ CONCLUSIONES ============ -->
<section class="sec" id="conclusiones">
  <div class="wrap">
    <div class="reveal">
      <span class="kick">Conclusiones</span>
      <h2>Respuesta a la pregunta</h2>
    </div>
    <div class="cols2 reveal">
      <div class="card dark">
        <h3>Qué responden los datos</h3>
        <p>Las regiones difieren en <b>cómo de alto</b> evalúan su vida los países (hasta 3 puntos),
        en <b>de qué se componen</b> esas valoraciones y en <b>cuánta diversidad interna</b> ocultan
        (rangos de 0.33 a 4.63 puntos).</p>
        <p>Comparar regiones exige mirar siempre las tres cosas. Descartar cualquiera lleva a
        lecturas parciales: el riesgo concreto es tratar un promedio regional como representativo
        de países que van de la mitad superior a la inferior del ranking mundial.</p>
      </div>
      <div class="card">
        <h3>Limitaciones</h3>
        <ul>
          <li>El archivo publica <b>contribuciones</b> del modelo, no indicadores crudos.</li>
          <li>3 países sin contribuciones (sin imputar); regiones de 4 a 35 países.</li>
          <li>Ventana 2021–2023: sin evolución temporal en este análisis.</li>
          <li>Toda relación es <b>asociación, no causalidad</b>; parte del vínculo es parte–todo.</li>
          <li>Entre 1.0 y 2.1 puntos por región quedan fuera de los seis factores.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- ============ ENTREGABLES ============ -->
<section class="sec tinted" id="entregables">
  <div class="wrap">
    <div class="reveal">
      <span class="kick">Reproducibilidad</span>
      <h2>Todo se puede verificar</h2>
      <p class="lead">El notebook se ejecuta de principio a fin en un kernel limpio, dos veces,
      sin pasos manuales. Esta página y los entregables se regeneran desde los mismos scripts.</p>
    </div>
    <div class="deliv reveal">
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>Proyecto2_Analisis.ipynb</b><span>Notebook ejecutado 2 veces · 18/18 celdas · 0 errores · Plotly embebidos interactivos.</span></div></div>
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>Proyecto2_Graficos_Interactivos.html</b><span>Los dos gráficos Plotly como archivo autónomo para presentación.</span></div></div>
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>Proyecto2_Informe.pdf</b><span>Informe de 3 páginas: pregunta, audiencia, datos, hallazgos y conclusiones.</span></div></div>
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>Proyecto2_Anexo_IA.pdf</b><span>Anexo de uso de IA de 1 página: herramientas, prompts y revisión crítica.</span></div></div>
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>datos/</b><span>Archivo oficial WHR24 + recurso de regiones generado por script + tablas preparadas.</span></div></div>
      <div class="check"><span class="mark"><svg viewBox="0 0 24 24"><polyline points="4 13 9 18 20 6"/></svg></span>
        <div><b>requirements.txt</b><span>Dependencias fijadas: el análisis se reconstruye desde cero.</span></div></div>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div><b>Proyecto 2 · Visualización de Datos 1</b> — World Happiness Report 2024</div>
    <div>Juan Tomás Rincón · Alejandro Pardo Costo</div>
    <div>Python (Seaborn + Plotly) · página 100 % offline</div>
  </div>
</footer>

<div id="lightbox"><span class="close">&times;</span><img alt="Figura ampliada"></div>
"""


# ------------------------------------------------------------------- JS
JS = """
(function(){
'use strict';
var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- progreso de lectura ---------- */
var bar = document.getElementById('progress');
function onScroll(){
  var h = document.documentElement;
  var p = h.scrollTop / (h.scrollHeight - h.clientHeight) * 100;
  bar.style.width = p + '%';
}
window.addEventListener('scroll', onScroll, {passive:true}); onScroll();

/* ---------- reveal on scroll ---------- */
var io = new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
}, {threshold:.14, rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.reveal').forEach(function(el){ io.observe(el); });

/* ---------- checks con tilde animada ---------- */
var ioC = new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); ioC.unobserve(e.target); } });
}, {threshold:.5});
document.querySelectorAll('.check').forEach(function(el){ ioC.observe(el); });

/* ---------- count-up ---------- */
function countUp(el){
  var target = parseFloat(el.dataset.count);
  var dec = parseInt(el.dataset.dec || '0', 10);
  var pre = el.dataset.prefix || '';
  var suf = el.dataset.suffix || '';
  if (el.dataset.text){ el.textContent = pre + el.dataset.text; return; }
  if (reduce){ el.textContent = pre + target.toFixed(dec) + suf; return; }
  var t0 = null, dur = 1400;
  function tick(t){
    if(!t0) t0 = t;
    var k = Math.min((t - t0) / dur, 1);
    var e = 1 - Math.pow(1 - k, 3);
    el.textContent = pre + (target * e).toFixed(dec) + suf;
    if(k < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
var ioN = new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ countUp(e.target); ioN.unobserve(e.target); } });
}, {threshold:.6});
document.querySelectorAll('[data-count]').forEach(function(el){ ioN.observe(el); });

/* ---------- nav lateral scroll-spy ---------- */
var links = Array.prototype.slice.call(document.querySelectorAll('#sidenav a'));
var secs = links.map(function(a){ return document.getElementById(a.dataset.sec); });
function spy(){
  var y = window.scrollY + window.innerHeight * 0.35, best = 0;
  secs.forEach(function(s, i){ if(s && s.offsetTop <= y) best = i; });
  links.forEach(function(a, i){ a.classList.toggle('active', i === best); });
}
window.addEventListener('scroll', spy, {passive:true}); spy();

/* ---------- lightbox de figuras ---------- */
var lb = document.getElementById('lightbox'), lbImg = lb.querySelector('img');
document.querySelectorAll('.figcard').forEach(function(fig){
  fig.addEventListener('click', function(){
    lbImg.src = fig.dataset.img;
    lb.classList.add('open');
  });
});
function closeLB(){ lb.classList.remove('open'); }
lb.addEventListener('click', closeLB);
document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeLB(); });

/* ---------- scrollytelling: zoom de la figura 3 ---------- */
var fig3 = document.getElementById('fig3zoom');
var steps = document.querySelectorAll('.step');
function applyZoom(st){
  var s = parseFloat(st.dataset.s), cx = parseFloat(st.dataset.cx), cy = parseFloat(st.dataset.cy);
  // transform: scale(s) translate(tx%, ty%) con origin 0 0  →  destino = s*(p + t) = 0.5 ⇒ t = 0.5/s - c
  var tx = (0.5 / s - cx) * 100, ty = (0.5 / s - cy) * 100;
  fig3.style.transform = 'scale(' + s + ') translate(' + tx.toFixed(2) + '%, ' + ty.toFixed(2) + '%)';
}
var ioS = new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(e.isIntersecting){
      steps.forEach(function(s){ s.classList.remove('active'); });
      e.target.classList.add('active');
      applyZoom(e.target);
    }
  });
}, {threshold:.55});
steps.forEach(function(s){ ioS.observe(s); });

/* ---------- Plotly en vivo ---------- */
var cfg = {responsive:true, displayModeBar:'hover', displaylogo:false,
            modeBarButtonsToRemove:['lasso2d','select2d','autoScale2d']};
try{
  Plotly.newPlot('plot1', __P1_DATA__, __P1_LAYOUT__, cfg);
  Plotly.newPlot('plot2', __P2_DATA__, __P2_LAYOUT__, cfg);
  requestAnimationFrame(function(){
    Plotly.Plots.resize('plot1'); Plotly.Plots.resize('plot2');
  });
}catch(err){
  console.error('Plotly:', err);
  document.querySelectorAll('.plot').forEach(function(d){
    d.innerHTML = '<p style="padding:30px;color:#64748B">Gráfico interactivo no disponible.</p>';
  });
}
})();
"""


# --------------------------------------------------------- Ensamblado final
html = (
    "<!DOCTYPE html>\n"
    '<html lang="es">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    "<title>Bienestar por regiones · Proyecto 2 · World Happiness Report 2024</title>\n"
    '<meta name="description" content="Análisis exploratorio reproducible del bienestar entre y '
    'dentro de las regiones del World Happiness Report 2024 — Seaborn y Plotly.">\n'
    "<style>" + CSS + "</style>\n</head>\n<body>\n"
    + BODY +
    "\n<script>" + plotly_js + "</script>\n"
    "<script>" + JS + "</script>\n"
    "</body>\n</html>\n"
)

# Placeholders de imágenes (base64) — se reemplazan por tamaño de cadena
for k, v in img.items():
    n = {"fig1": "__IMG1__", "fig2": "__IMG2__", "fig3": "__IMG3__", "fig4": "__IMG4__"}[k]
    html = html.replace(n, "data:image/png;base64," + v)

# Placeholders de las figuras Plotly (data y layout por separado)
import json as _json
p1 = _json.loads(json_pais); p2 = _json.loads(json_rank)
# Al incrustar: sin título interno (el encabezado de la card ya lo pone) y con
# altura explícita para que responsive no colapse el contenedor.
for p, h in ((p1, 560), (p2, 760)):
    p["layout"].pop("title", None)
    p["layout"].setdefault("height", h)
html = html.replace("__P1_DATA__", _json.dumps(p1["data"], ensure_ascii=False, separators=(",", ":")))
html = html.replace("__P1_LAYOUT__", _json.dumps(p1["layout"], ensure_ascii=False, separators=(",", ":")))
html = html.replace("__P2_DATA__", _json.dumps(p2["data"], ensure_ascii=False, separators=(",", ":")))
html = html.replace("__P2_LAYOUT__", _json.dumps(p2["layout"], ensure_ascii=False, separators=(",", ":")))

# Ningún placeholder sin resolver (solo los nuestros; plotly.js minificado
# puede contener tokens tipo __NPO__ que no son nuestros marcadores)
MIS_PLACEHOLDERS = ["__IMG1__", "__IMG2__", "__IMG3__", "__IMG4__",
                    "__P1_DATA__", "__P1_LAYOUT__", "__P2_DATA__", "__P2_LAYOUT__"]
huerfanos = [p for p in MIS_PLACEHOLDERS if p in html]
assert not huerfanos, f"Placeholders sin resolver: {huerfanos}"
import re as _re

salida = ENT / "Proyecto2_Presentacion.html"
salida.write_text(html, encoding="utf-8")
print(f"Presentación: {salida} ({salida.stat().st_size/1e6:.1f} MB)")
print("Secciones:", len(_re.findall(r'<section', html)), "| figuras embebidas:", len(_re.findall(r"data:image/png", html)))