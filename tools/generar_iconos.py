# -*- coding: utf-8 -*-
"""
Genera los iconos PNG de la PWA en app/icons/ (cubo isométrico con tres ejes de color).
Uso: python tools/generar_iconos.py
"""
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "app" / "icons"

FONDO = (2, 6, 23)          # #020617
AZUL = (30, 58, 138)         # #1e3a8a
BORDE = (147, 197, 253)      # #93c5fd
EJES = [(74, 222, 128), (251, 191, 36), (192, 132, 252)]  # verde, ambar, violeta
ESFERA = (136, 204, 255)


def dibujar(tam, margen_rel):
    esc = 4
    S = tam * esc
    img = Image.new("RGBA", (S, S), FONDO + (255,))
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = S / 2, S / 2
    r = S * (0.5 - margen_rel)

    # Hexagono isometrico del cubo
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(-90, 270, 60)]
    d.polygon(pts, fill=AZUL + (110,), outline=BORDE + (255,), width=max(2, S // 90))
    # Aristas internas (tres desde el centro a vertices alternos)
    for i in (0, 2, 4):
        d.line([(cx, cy), pts[i]], fill=BORDE + (200,), width=max(2, S // 110))
    # Ejes de color hacia los otros tres vertices
    for i, col in zip((1, 3, 5), EJES):
        d.line([(cx, cy), pts[i]], fill=col + (255,), width=max(3, S // 60))
    # Esfera central
    re = r * 0.22
    d.ellipse([cx - re, cy - re, cx + re, cy + re], fill=ESFERA + (230,), outline=(255, 255, 255, 255), width=max(2, S // 120))
    return img.resize((tam, tam), Image.LANCZOS)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    dibujar(192, 0.10).save(DEST / "icon-192.png")
    dibujar(512, 0.10).save(DEST / "icon-512.png")
    dibujar(512, 0.20).save(DEST / "icon-maskable-512.png")   # zona segura mas amplia
    dibujar(180, 0.12).convert("RGB").save(DEST / "apple-touch-icon.png")
    print(f"Iconos escritos en {DEST}")


if __name__ == "__main__":
    main()
