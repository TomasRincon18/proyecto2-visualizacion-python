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