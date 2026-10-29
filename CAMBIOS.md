# Cambios para la entrega final (26-oct-2026)

Tomás: este es el resumen de lo que se cambió en el repo antes de entregar y por qué.
Ninguna cifra ni conclusión cambió: la tabla preparada (`datos/WHR24_preparado.csv`)
quedó idéntica byte a byte a la que tenías.

## 1. Solo el archivo oficial (sección 4 de las instrucciones)
La instrucción no permite "datos de otros años", y usábamos WHR20 y WHR21 para sacar la región.
- Se eliminaron `datos/WHR20_...xls`, `datos/WHR21_...xls`, `datos/WHR24_regiones_oficiales.csv`
  y `scripts/01_regiones_oficiales.py`.
- La región ahora se asigna en el notebook con un diccionario `REGIONES_PAISES` (región → países),
  con los nombres tal como vienen en el archivo 2024. Ya no hace falta homologar nombres.
- El notebook valida la agrupación: cada país tiene una sola región y los conteos por región
  coinciden con la **tabla 18 del Statistical Appendix del WHR 2024**
  (20, 17, 10, 9, 6, 6, 19, 4, 17, 35 = 143). Si algo no cuadra, se detiene.
- El apéndice se movió a `recursos/referencias/` (es documento de consulta, no un dato).
- Se actualizaron el informe, la presentación, el guion de sustentación y la limitación 7.

## 2. Notebook (`notebook/Equipo3_Proyecto2_Analisis.ipynb`)
- Corre en **VS Code y en Colab**: primera celda `%pip install`; si no encuentra `datos/`, descarga el
  `.xls` oficial (y si el servidor bloquea la descarga, usa la copia idéntica de este repo, mismo MD5).
  Renderer de Plotly `colab` en Colab y `notebook` en VS Code.
- La celda Markdown del inicio de la Sección 1 tenía pegado el código del script de regiones; se arregló.
- La paleta por región de la celda de configuración no coincidía con la de Seaborn/Plotly; quedó una sola.
- Gráfico 4: se corrigió la clasificación de las r por región ("moderada" para 0.77 era incoherente) y
  se agregó la advertencia de regiones con pocos países.
- "Promedio trianual" se reescribió: el archivo 2024 trae un solo valor por país calculado con las
  encuestas 2021–2023; así no parece que usemos otros años.
- Errata: "encabizan" → "encabezan".

## 3. Presentación (`entregables/Equipo3_Proyecto2_Presentacion.html`, se genera con `scripts/07_presentacion.py`)
- **Zoom de la figura de puntos por país:** apuntaba a la caja y no a la imagen (`object-fit: contain`
  dejaba franjas), así que cortaba a Israel y en Norteamérica mostraba un recuadro vacío. Ahora la caja
  tiene la proporción de la imagen, los centros se recalcularon y el desplazamiento se limita.
- Textos en tono técnico para la audiencia: "Explora tú mismo" → "Análisis a nivel de país", nueva
  portada, y otros títulos.
- La evidencia 4 ahora explica cómo leer el gráfico y su implicación (la r global de 0.81 no se repite
  dentro de las regiones: 0.78 en Europa Occidental, 0.37 en África Subsahariana, 0.28 en Latinoamérica).

## 4. Nombres y estructura
- Entregables con la convención `Equipo3_Proyecto2_*` (notebook, HTML, informe, anexo, presentación).
  PDFs regenerados con `scripts/06_pdf.py` (informe 3 páginas, anexo 1 página).
- Se eliminaron los scripts que duplicaban el notebook (`00`, `02`, `03`, `05` y
  `notebook/Proyecto2_Analisis.py`): el notebook es la única fuente. Quedan `04_plotly.py`
  (lo usa la presentación), `06_pdf.py` y `07_presentacion.py`.

## 4b. Corrección del Gráfico 5 (dispersión con menú de indicador)
- **Antes:** al abrir se mostraban los 6 indicadores a la vez (6 líneas punteadas y 840 puntos
  encimados con ejes distintos), porque las trazas no tenían `visible` inicial. Al elegir un indicador
  la leyenda desaparecía (solo las trazas del primer indicador tenían `showlegend`) y el `legendgroup`
  compartido hacía que al filtrar una región se ocultaran también sus países en los otros indicadores;
  el eje conservaba el rango anterior.
- **Ahora:** se abre solo con PIB per cápita; cada opción muestra 1 recta, 140 países y la leyenda de
  10 regiones, y el eje se reajusta (`xaxis.autorange`). Probado en Chromium con las 6 opciones.

## 4c. Revisión de cifras y del residuo (para la sustentación)
- **Residuo:** decíamos que "entre 1.0 y 2.1 puntos de cada barra no los explican los seis factores".
  Es impreciso: la columna `Dystopia + residual` incluye una **base fija de 1.58** (Distopía, igual
  para todos los países, según el apéndice del WHR 2024). Descontada la base, el residuo medio por
  región va de **−0.57 (Asia Meridional)** a **+0.48 (Latinoamérica y Caribe)**: Latinoamérica evalúa
  su vida mejor de lo que predicen sus factores. Se corrigió en notebook (estructura del archivo,
  Gráfico 2 y su leyenda, conclusiones, limitación 6, nuevas preguntas), informe, presentación
  (nota de la evidencia 2, cifra principal, limitaciones) y guion.
- **"Solo tres regiones por encima de la mediana global"** era falso: son **seis** (las medianas de
  Asia Oriental 6.02 y Asia Sudoriental 5.98 también la superan). Corregido en notebook, informe y presentación.
- **Gráfico 2:** PIB + apoyo social va de 1.66 a 3.32 (decía 1.5–3.3); la esperanza de vida no es
  exclusiva de Norteamérica/Europa Occidental (Asia Oriental 0.68), así que solo se mantiene lo de corrupción.
- **Gráfico 3:** Europa Occidental no es "compacta" (abarca 1.81 puntos); las más compactas son
  Norteamérica y ANZ (0.33), Asia Oriental (1.19) y CEI (1.32). También en el zoom de la presentación.
- Gráfico 4 / guion: se aclara que las r de regiones con 4 y 6 países son inestables.
- Todas las demás cifras citadas (medianas, extremos, rankings del Gráfico 6, integridad) se verificaron contra los datos.

## 5. Carpeta `entregables/` = lo que pide la sección 7
```
entregables/
├── Equipo3_Proyecto2_Analisis.ipynb            (1) notebook ejecutado
├── Equipo3_Proyecto2_Graficos_Interactivos.html (2) HTML de Plotly
├── Equipo3_Proyecto2_Informe.pdf               (3) PDF ≤ 3 páginas
├── Equipo3_Proyecto2_Datos/WHR24_Data_Figure_2.1.xls  (4) archivo original
├── Equipo3_Proyecto2_Anexo_IA.pdf              (5) anexo de IA ≤ 1 página
└── Complementarios/Equipo3_Proyecto2_Presentacion.html  (apoyo, no obligatorio)
```
Los Markdown y CSS de origen de los PDF se movieron a `recursos/fuentes_pdf/`.
El notebook de trabajo sigue en `notebook/`; después de ejecutarlo se copia a `entregables/`.

## Cómo regenerar todo
1. Ejecutar el notebook completo (genera `datos/WHR24_preparado.csv`, las figuras y el HTML de Plotly).
2. `python scripts/07_presentacion.py` → presentación (en `entregables/Complementarios/`).
3. `python scripts/06_pdf.py` → informe y anexo en PDF.
4. Copiar `notebook/Equipo3_Proyecto2_Analisis.ipynb` y `datos/WHR24_Data_Figure_2.1.xls` a `entregables/`.
