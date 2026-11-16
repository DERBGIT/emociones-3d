# -*- coding: utf-8 -*-
"""
Genera GLOSARIO.md (en la raiz del proyecto) a partir de app/glosario.json (Emociones 3D 5.0).

Organizacion: una seccion por familia (centro, octantes, ejes y planos) y, dentro de ella,
una ficha por grado (sutil, moderado, desbordante) con todos los textos, para revisarlos con calma.

Uso:
  python tools/glosario_md.py
"""
import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
GLOSARIO = RAIZ / "app" / "glosario.json"
SALIDA = RAIZ / "GLOSARIO.md"

CAMPOS = [("nombre_low", "Nombre cotidiano (LOW)"), ("resumen_low", "Resumen cotidiano"), ("nombre_high", "Nombre profundo (HIGH)"),
          ("evaluacion", "Evaluación"), ("senales", "Señales corporales"), ("impulso", "Impulso"), ("pensamientos", "Pensamientos"),
          ("regula", "Regulación"), ("reencuadra", "Reencuadre"), ("acomp_validar", "Acompañar: validar"),
          ("acomp_evitar", "Acompañar: evitar"), ("examen", "Examen / discernimiento")]


def main():
    g = json.loads(GLOSARIO.read_text(encoding="utf-8"))
    out = [f"# Glosario de Emociones 3D (versión {g.get('version')})", "", g.get("descripcion", ""), "",
           "Archivo generado por `tools/glosario_md.py`. Para cambiar los textos, edite `app/glosario.json`.", ""]
    familias = {}
    for n in g["nodos"]:
        familias.setdefault(n["familia"], []).append(n)
    for familia, nodos in familias.items():
        out += [f"## {familia}", ""]
        if len(nodos) > 1:
            out += ["Vector: " + " → ".join(n["nombre"] for n in nodos), ""]
        for n in nodos:
            ancla = " · anclaje LOW" if n.get("es_anclaje_low") else ""
            out += [f"### {n['nombre']}", "", f"`({n['x']}, {n['y']}, {n['z']})` · {n['nivel']}{ancla}", ""]
            if n.get("alias"):
                out += ["- **Alias:** " + ", ".join(n["alias"])]
            out += [f"- **{etq}:** {n[k]}" for k, etq in CAMPOS if n.get(k)]
            out += [""]
    SALIDA.write_text("\n".join(out), encoding="utf-8")
    print(f"Escrito {SALIDA.name} ({len(g['nodos'])} nodos)")


if __name__ == "__main__":
    main()
