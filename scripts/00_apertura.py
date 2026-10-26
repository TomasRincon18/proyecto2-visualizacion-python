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
# reproducible para el análisis.