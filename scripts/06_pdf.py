# %% [markdown]
# # Generación de los documentos finales (PDF)
#
# Convierte los Markdown de entrega a PDF usando **pandoc** (Markdown → HTML)
# y **weasyprint** (HTML → PDF con hoja A4 vía CSS), sin necesidad de LaTeX.
#
# - `Proyecto2_Informe.md` → `Proyecto2_Informe.pdf` (máximo 3 páginas)
# - `Proyecto2_Anexo_IA.md` → `Proyecto2_Anexo_IA.pdf` (máximo 1 página)

# %% tags=["hide-input"]
from pathlib import Path
import pypandoc
import pymupdf  # para verificar el número de páginas

BASE = next(c for c in [Path("."), Path(".."), Path("Proyecto2")]
            if (c / "entregables" / "Proyecto2_Informe.md").exists())
ENT = BASE / "entregables"


def md_a_pdf(md: Path, pdf: Path, css: Path) -> int:
    """Markdown → HTML (pandoc) → PDF (weasyprint). Devuelve nº de páginas."""
    html = md.with_suffix(".html")
    pypandoc.convert_file(
        str(md), "html", outputfile=str(html),
        extra_args=[f"--css={css.name}", "--standalone", "--metadata", "lang=es"],
    )
    import subprocess
    subprocess.run(
        [str(Path.home() / ".local/bin/weasyprint"), str(html.name), str(pdf.name)],
        check=True, cwd=ENT, capture_output=True,
    )
    n_paginas = len(pymupdf.open(pdf))
    html.unlink()  # el HTML intermedio no es entregable
    return n_paginas


informe = md_a_pdf(ENT / "Proyecto2_Informe.md", ENT / "Proyecto2_Informe.pdf", ENT / "informe.css")
print(f"Proyecto2_Informe.pdf → {informe} páginas (máx. 3)")
assert informe <= 3, f"El informe excede las 3 páginas: {informe}"

anexo = md_a_pdf(ENT / "Proyecto2_Anexo_IA.md", ENT / "Proyecto2_Anexo_IA.pdf", ENT / "anexo.css")
print(f"Proyecto2_Anexo_IA.pdf → {anexo} página(s) (máx. 1)")
assert anexo <= 1, f"El anexo excede 1 página: {anexo}"