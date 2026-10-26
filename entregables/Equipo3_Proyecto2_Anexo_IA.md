---
title: "Anexo — Uso de inteligencia artificial"
subtitle: "Equipo 3 · Proyecto 2 · Visualización de Datos con Python"
---

# Herramientas y propósito

Todo el trabajo se desarrolló con un **asistente de IA basado en LLM dentro del agente de codificación OpenCode** (extracción de PDFs, planificación, generación y depuración de código Seaborn/Plotly, redacción y conversión de documentos), **siempre bajo indicación directa del equipo**, que aprobó cada decisión analítica y de diseño.

# Prompts empleados (los principales)

| # | Prompt (equipo) | Propósito |
|---|---|---|
| 1 | *"Analiza las instrucciones del Proyecto 2, haz un plan por fases y hazme preguntas"* | Planificación del trabajo |
| 2 | *"Dame 3 opciones de pregunta analítica con pros y contras y tu mejor recomendación"* | Selección de la pregunta (se eligió la de comparación regional) |
| 3 | **Paleta de colores:** *"Escogemos la mejor paleta; no saturar el proyecto de muchos colores, usa la skill de colorimetría e investiga por tu cuenta sobre teoría del color"* | Sistema de color del proyecto |
| 4 | *"Los títulos deben ser generales, no descriptivos; gráficos más sencillos; ejes más simplificados"* | Rediseño de legibilidad |
| 5 | *"Especifica que el rosado es MENA; no redundar sobre la región porque ya se ve en el eje"* | Ajuste de leyenda |
| 6 | *"La nueva gráfica es redundante con la figura 3, cámbiala"; "deben ser fáciles de entender"* | Eliminación de redundancias entre gráficos |

**Prompts de color (obligatorios):** el prompt 3 disparó la sección de colorimetría de la skill instalada (`colorimetria-dataviz`): la IA investigó fuentes (Okabe-Ito 2008; Tol, *Colour Schemes* SRON/EPS/TN/09-002, 2021; R Journal 2023), encontró el límite documentado de **8 categorías distinguibles** —nuestro dataset tiene 10 regiones— y propuso 3 opciones. El equipo eligió la **Opción 1 "color con función"**: neutro `#CBD5E1` + acento MENA `#CC78BC` en gráficos con región en el eje; escala de un solo azul + gris para composición (partes de un todo); paleta cualitativa Okabe-Ito (10) solo donde el color identifica grupos; divergente naranja-gris-azul en el primer heatmap (luego eliminado por redundante). Cada color quedó con función explícita y verificación de daltonismo.

# Reflexión sobre la revisión crítica

- **Verificación numérica propia:** las 13 cifras de conclusiones e interpretaciones se contrastaron con los datos por script independiente (13/13); la integridad del dataset (contribuciones + residuo = ladder) se verificó antes de confiar en ella.
- **Correcciones impuestas por el equipo:** la IA propuso títulos-conclusión, un violin y un heatmap de z-scores; **el equipo los rechazó** por no ser sencillos, por redundancia (heatmap ↔ heatmap interactivo; barras con rango ↔ strip) y por saturación, y la IA reimplementó cada cambio.
- **Límites asumidos:** la IA no seleccionó datos ni tomó decisiones analíticas sin aprobación; pregunta, paleta y gráficos pasaron por revisión del equipo; se mantuvo la cautela inferencial (asociación ≠ causalidad).
- **Evidencia, no afirmación:** la ejecución del notebook final se verificó dos veces de principio a fin (kernel limpio, 0 errores).