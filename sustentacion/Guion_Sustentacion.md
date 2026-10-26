# Guion de sustentación — Proyecto 2
**Duración máxima: 10 minutos · Se sustenta desde el Notebook (sin diapositivas)**
Integrantes: Juan Tomás Rincón · Alejandro Pardo Costo

> **Regla de oro:** no leer el notebook. Mirar al público, usar el cursor para
> señalar el gráfico y dejar que el código hable solo. Si el tiempo aprieta,
> recortar el minuto 1 (datos), nunca los minutos de Plotly (es donde se valora
> la interacción).

---

## 1. Guion cronometrado

### ▸ 0:00–1:00 — Contexto, audiencia y pregunta
**Pantalla:** celda de apertura → "Pregunta analítica".

- (30 s) "El World Happiness Report resume a cada país con un solo número, pero
  **los promedios regionales pueden ocultar brechas internas enormes**: dos
  regiones con el mismo promedio pueden estar hechas de países muy distintos."
- (20 s) Audiencia: "investigadores y analistas de un organismo internacional que
  necesitan comparar regiones de forma **justificada y reproducible**."
- (10 s) Leer la pregunta textualmente y señalar sus dos mitades: **entre**
  regiones y **dentro** de cada región. "Todo el informe sigue ese orden."

### ▸ 1:00–2:00 — Fuente, variables y transformaciones
**Pantalla:** Sección 1 (outputs visibles).

- Fuente única: "`WHR24_Data_Figure_2.1.xls`, archivo oficial. 143 países,
  promedios 2021–2023, escala 0–10."
- **Integridad verificada**: "contribuciones + residuo = evaluación de vida;
  diferencia máxima 0.00005" → señalizar el ✓.
- Regiones: "el archivo oficial **no trae región**; usamos la taxonomía oficial
  del WHR desde archivos oficiales, solo como atributo de país — ningún dato de
  bienestar de otro año entra" (143/143 con homologación de 5 nombres).
- Faltantes: "3 países sin contribuciones — sin imputar; conservados donde su
  dato existe y excluidos de composición (140/143)."
- Nota si preguntan de medianas/medias: **mediana** para nivel (robusta),
  **media** para composición (porque las contribuciones son aditivas).

### ▸ 2:00–5:00 — Seaborn: patrones, relaciones y diferencias
**Pantalla:** Secciones de los Gráficos 1–4 (~45 s cada uno).

| Gráfico | Qué decir (1 idea + 1 cifra + conexión con la pregunta) |
|---|---|
| **G1 — Barras de mediana** | "Diferencia **entre** regiones: de 6.96 a 3.98, casi 3 puntos en una escala de 10; mediana global 5.79. Es la comparación directa." |
| **G2 — Composición apilada** | "No solo difieren en nivel: difieren en **cómo se componen**. PIB y apoyo social dominan en todas; MENA tiene la menor aportación de libertad (0.49); y **entre 1.0 y 2.1 puntos no los explican los seis factores** (bloque gris)." |
| **G3 — Strip de países** | "Aquí está la segunda mitad de la pregunta: **dentro** de cada región. MENA va de Líbano (2.71) a Israel (7.34): 4.63 puntos — del penúltimo al quinto del ranking. Norteamérica/ANZ apenas 0.33. El promedio regional representa a unas y engaña a otras." |
| **G4 — Scatter apoyo social** | "¿Se sostiene la relación? Entre todos los países r = 0.81, pero **dentro** de cada región va de 0.83 a 0.14. Cautela: es asociación, no causalidad, y hay vínculo parte-todo." |

### ▸ 5:00–8:00 — Plotly: interacción en vivo (¡el momento clave!)
**Pantalla:** Gráficos 5 y 6. **Interactuar de verdad**, sin miedo:

1. **G5 — desplegable:** abrir el selector del eje X → elegir **"Apoyo social"**
   → "la nube se alinea, r = 0.81" → cambiar a **"Generosidad"** → "casi sin
   patrón: no todos los indicadores se relacionan igual".
2. **G5 — leyenda:** clic en **"Oriente Medio y N. de África"** para ocultar/
   mostrar la región → "el racimo se acota: dentro de una región la relación
   cambia" → volver a mostrar.
3. **G5 — hover:** pasar sobre 1–2 países mostrando país, región y valor exacto.
4. **G6 — desplegable:** de "Evaluación de vida" a **"Generosidad"** → señalar
   cómo el podio cambia por completo: "Finlandia lidera la evaluación, Luxemburgo
   el PIB, Myanmar la generosidad, Hong Kong la esperanza de vida — **no existe
   un solo país líder**, depende de lo que se mida."
5. Decir el valor analítico (lo que pide la rúbrica): "el estático **comunica**
   el hallazgo; el interactivo permite al analista **verificarlo por su cuenta**:
   elegir el indicador, filtrar su región y leer los valores exactos."

> **Si Plotly falla:** respaldo en `entregables/Proyecto2_Graficos_Interactivos.html`
> (mismas figuras). Si el notebook va lento: respaldo en `Proyecto2_Presentacion.html`.

### ▸ 8:00–10:00 — Síntesis, limitaciones y respuesta
**Pantalla:** celda de Conclusiones.

- **Respuesta en dos partes:** "Entre regiones: hasta 3 puntos de diferencia y
  distinta composición. Dentro: rangos de 0.33 a 4.63 puntos. **Las tres
  cosas —nivel, composición y dispersión— hacen falta para comparar regiones sin
  engañarse.**"
- **Limitaciones (decirlas, no esconderlas):** contribuciones y no indicadores
  crudos; regiones de 4 a 35 países; ventana 2021–2023; asociación, no causalidad;
  parte de la varianza queda fuera del modelo.
- **Cierre de reproducibilidad:** "el notebook se ejecuta de principio a fin en
  un kernel limpio — lo verificamos dos veces, 0 errores — y todos los recursos
  están en la carpeta de entrega con `requirements.txt`."

---

## 2. Preguntas probables de la docente (+ respuestas)

1. **¿Por qué usan contribuciones y no los indicadores crudos?**
   → El archivo oficial WHR24 *solo* publica contribuciones; es la unidad del
   modelo del reporte. Lo declaramos como limitación y por eso hablamos de
   "composición", no de niveles materiales.

2. **¿De dónde salen las regiones si el archivo no las trae?**
   → De la taxonomía oficial del WHR (archivos oficiales WHR21/WHR20 usados
   *únicamente* como atributo de país; ningún dato de bienestar de otros años).
   Está generado por script reproducible y documentado en el notebook.

3. **¿Cómo verifican la integridad de los datos?**
   → Suma de las 6 contribuciones + Dystopia/residuo = evaluación de vida, con
   diferencia máxima 0.00005 en 140 países. Se ejecuta en cada corrida.

4. **¿Qué hicieron con los 3 países faltantes?**
   → Sin imputación (fabricaría datos). Conservados para evaluación de vida,
   excluidos solo de los análisis de composición; documentados.

5. **¿Por qué mediana en un gráfico y media en otro?**
   → Mediana para nivel de vida (robusta ante extremos); media para composición,
   porque las contribuciones son aditivas: la suma de medias reproduce el ladder.

6. **¿No es circular correlacionar una contribución con el total?**
   → Sí existe vínculo parte-todo y lo declaramos en la interpretación del G4:
   por eso la lectura es **comparativa** (¿cómo cambia entre regiones?) y no
   "el apoyo social causa la evaluación".

7. **¿Por qué este diseño de gráficos?**
   → Criterio comunicativo: 4 estáticos sin redundancia, cada uno responde una
   parte de la pregunta (nivel, composición, dispersión, asociación) y los 2
   interactivos añaden exploración que el estático no da. Tipos simples
   (barras, puntos, nube) porque la audiencia debe entenderlos sin explicación.

8. **¿Es causal lo que muestran?**
   → No. Todo es descriptivo y asociativo; está escrito en la nota metodológica,
   en cada interpretación y en conclusiones.

9. **¿Por qué una sola región en color?**
   → El color tiene función: donde el eje ya nombra las regiones, el color no
   repite — usamos un acento único (MENA, la más heterogénea) coherente en todo
   el proyecto; el color categórico solo aparece donde identifica grupos (G4,
   Plotly).

10. **¿Cómo sabemos que es reproducible?**
    → `requirements.txt`, rutas robustas, notebook = informe completo, y doble
    ejecución en kernel limpio con 0 errores (verificado, no supuesto).

---

## 3. Ruta de demo — orden exacto de interacción

**Antes de entrar (check de 5 minutos):**
- [ ] Notebook **ya ejecutado de punta a punta** (no ejecutar celdas sueltas en vivo)
- [ ] Kernel limpio: no guardar cambios accidentales (Ctrl+S → puede alterar outputs)
- [ ] Zoom del navegador **110–125%** (legibilidad en proyector)
- [ ] Cerrar notificaciones y demás pestañas
- [ ] Probar los 2 desplegables de Plotly una vez antes de empezar

**Durante (el recorrido):**
1. Título + pregunta analítica (apertura)
2. Sección 1: importación → integridad ✓ → regiones → tabla 143×14
3. G1 barras → G2 composición → G3 strip → G4 scatter
4. Plotly G5: desplegable (PIB → Apoyo social → Generosidad) → leyenda (ocultar/
   mostrar MENA) → hover de 2 países
5. Plotly G6: desplegable (Evaluación → Generosidad) → señalar el cambio de podio
6. Conclusiones → limitaciones → cierre
7. *(Opcional, si sobra tiempo)* abrir `Proyecto2_Presentacion.html` como
   "la misma historia en formato web" — es un plus, no sustituye el notebook

**Anticipar problemas:**
- Plotly no carga → HTML de respaldo en `entregables/`
- Mucha gente alrededor → proyectar el notebook, no acercar portátil
- Pregunta que no saben → "no lo tenemos verificado; es una buena pregunta de
  seguimiento" es una respuesta válida y mejor que improvisar

---

*Material interno del equipo — no es una diapositiva ni se proyecta durante la sustentación.*
