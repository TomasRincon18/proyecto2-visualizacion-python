# %% [markdown]
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
