# -*- coding: utf-8 -*-
"""
Valida app/glosario.json (Emociones 3D 5.0, 79 nodos) y regenera app/glosario.js,
la copia que carga index.html (funciona con doble clic y con servidor).

Comprueba:
  - Estructura: id y coordenadas unicos; un nodo basal en (0,0,0).
  - Vectores: 26 direcciones (ejes, planos y octantes), cada una con sus tres grados
    sutil (1.5) -> moderado (3.5) -> desbordante (5.5); nivel y "dir" coherentes con las coordenadas.
  - Campos de texto vacios.
  - Nombres repetidos (ignorando mayusculas y acentos).
  - Anclajes del nivel LOW de la Rueda de Afinado (se informa cuantos hay).
Ademas escribe tools/_salida/vectores.md para revisar a ojo la gradualidad de cada vector.

Uso:
  python tools/validar_glosario.py            # informe en pantalla y en tools/_salida/
  python tools/validar_glosario.py --sin-js   # no regenerar glosario.js
"""
import sys, json, unicodedata, itertools
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
GLOSARIO = RAIZ / "app" / "glosario.json"
GLOSARIO_JS = RAIZ / "app" / "glosario.js"
SALIDA = RAIZ / "tools" / "_salida"

GRADOS = {1.5: "sutil", 3.5: "moderado", 5.5: "desbordante"}
CAMPOS_TEXTO = ["familia", "nombre_low", "resumen_low", "nombre", "nombre_high", "evaluacion", "senales",
                "impulso", "pensamientos", "regula", "reencuadra", "acomp_validar", "acomp_evitar", "examen"]


def normalizar(s):
    s = unicodedata.normalize("NFD", s.lower().strip())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def signo(v):
    return (v > 0) - (v < 0)


def main():
    g = json.loads(GLOSARIO.read_text(encoding="utf-8"))
    nodos = g["nodos"]
    errores, avisos = [], []

    ids, coords = set(), {}
    for n in nodos:
        c = (n["x"], n["y"], n["z"])
        if n["id"] in ids:
            errores.append(f"id repetido: {n['id']}")
        ids.add(n["id"])
        if c in coords:
            errores.append(f"coordenada repetida {c}: '{n['nombre']}' y '{coords[c]['nombre']}'")
        coords[c] = n
        for k in CAMPOS_TEXTO:
            if not str(n.get(k, "")).strip():
                errores.append(f"campo vacio '{k}' en {n['id']} ({n.get('nombre', '?')})")
        if not isinstance(n.get("alias", []), list):
            errores.append(f"'alias' debe ser una lista en {n['id']}")

        mags = {abs(v) for v in c if v != 0}
        if not mags:
            if n["nivel"] != "basal":
                errores.append(f"{n['id']}: en el centro pero nivel '{n['nivel']}'")
            continue
        if len(mags) != 1 or next(iter(mags)) not in GRADOS:
            errores.append(f"{n['id']}: coordenadas {c} fuera de la malla (se espera 0 o ±1.5/3.5/5.5, misma magnitud)")
            continue
        esperado = GRADOS[next(iter(mags))]
        if n["nivel"] != esperado:
            errores.append(f"{n['id']}: nivel '{n['nivel']}' pero por coordenadas es '{esperado}'")
        d = [signo(v) for v in c]
        if n.get("dir") != d:
            errores.append(f"{n['id']}: 'dir' {n.get('dir')} no coincide con las coordenadas {d}")

    if (0, 0, 0) not in coords:
        errores.append("falta el nodo basal (0,0,0)")
    elif nodos[0]["nivel"] != "basal":
        errores.append("el nodo basal debe ser el primero de la lista (la app lo toma de ahi)")

    vectores = []
    for d in itertools.product([-1, 0, 1], repeat=3):
        if d == (0, 0, 0):
            continue
        fila = []
        for m in (1.5, 3.5, 5.5):
            n = coords.get(tuple(s * m for s in d))
            if n is None:
                errores.append(f"falta el grado {GRADOS[m]} del vector {d}")
            fila.append(n)
        vectores.append((d, fila))

    por_nombre = defaultdict(list)
    for n in nodos:
        por_nombre[normalizar(n["nombre"])].append(n["id"])
    for nombre, lista in por_nombre.items():
        if len(lista) > 1:
            avisos.append(f"nombre repetido '{nombre}' en {', '.join(lista)}")

    anclajes = sum(1 for n in nodos if n.get("es_anclaje_low"))

    lineas = ["# Informe de validacion", "", f"Glosario version {g.get('version')}. Nodos: {len(nodos)}. Anclajes LOW: {anclajes}.", "",
              f"## Errores ({len(errores)})", ""] + [f"- {e}" for e in errores] + ["", f"## Avisos ({len(avisos)})", ""] + [f"- {a}" for a in avisos]
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "informe_validacion.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    v = ["# Vectores (sutil -> moderado -> desbordante)", ""]
    for d, fila in vectores:
        v.append(f"- {d}: " + " -> ".join(n["nombre"] if n else "(falta)" for n in fila))
    (SALIDA / "vectores.md").write_text("\n".join(v) + "\n", encoding="utf-8")

    print("\n".join(lineas))
    if errores:
        print("\nHay errores: no se regenera glosario.js.")
        return 1
    if "--sin-js" not in sys.argv:
        GLOSARIO_JS.write_text("/* Copia generada de glosario.json por tools/validar_glosario.py. No editar a mano. */\nwindow.__GLOSARIO__ = "
                               + json.dumps(g, ensure_ascii=False) + ";\n", encoding="utf-8")
        print(f"\nRegenerado {GLOSARIO_JS.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
