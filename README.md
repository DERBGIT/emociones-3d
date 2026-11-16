# Emociones 3D 5.0

Aplicación web para el autoconocimiento emocional y el acompañamiento. Ubica un estado interior
en tres ejes (X = agrado / desagrado, Y = energía / calma, Z = abrirme / cerrarme), lo nombra a
partir de un glosario de 79 perfiles y acompaña con regulación, reencuadre, pautas para el
acompañante y una pregunta de examen. La persona guarda sus propias notas y trayectorias.

Es la unión de dos versiones anteriores: toma el contenido de la Estación RULER 4.0 (79 nodos,
Rueda de Afinado, cuadernos, exportación cifrada) y la infraestructura de la 3.2 (instalable,
funciona sin internet, importar con fusión, recordatorio de respaldo, modo curador).

Los datos de cada persona se guardan **solo en su dispositivo** (`localStorage` del navegador).
No hay servidor ni cuentas. Salen únicamente cuando la persona pulsa "Exportar".

## Estructura

| Carpeta / archivo | Qué es |
|---|---|
| `app/index.html` | La aplicación. Es lo que se publica. |
| `app/glosario.json` | Los 79 perfiles. Fuente de verdad del contenido. |
| `app/glosario.js` | Copia generada de `glosario.json`; es la que carga la app. No editar a mano. |
| `app/manifest.webmanifest`, `app/sw.js`, `app/icons/` | Hacen que la app sea instalable y funcione sin internet tras la primera carga. |
| `tools/validar_glosario.py` | Revisa el glosario y regenera `glosario.js`. |
| `tools/glosario_md.py` | Genera `GLOSARIO.md`, una versión legible para revisar los textos. |
| `tools/generar_iconos.py` | Regenera los iconos PNG de `app/icons/`. |
| `tools/_salida/` | Informes: `informe_validacion.md` y `vectores.md`. |
| `index.html` (raíz) | Redirige a `app/` para que el enlace público sea corto. |

## Qué trae la 5.0

- **Rueda de Afinado**: LOW (27 emociones cotidianas), MED (79 nodos), HIGH (discernimiento).
- **Cuadernos separados**: Personal, Taller (limpio) y Acompañamiento. Cada uno con sus notas y su respaldo.
- **Exportar** en JSON o cifrado con clave (`.ruler`). **Importar** pregunta siempre si fusionar o reemplazar.
- **Recordatorio de respaldo** cuando un cuaderno lleva más de 7 días con cambios sin exportar.
- **Migración automática** de las notas de la 3.2 al cuaderno Personal (una sola vez, sin borrar las antiguas).
- **Modo curador** (`?curador=1`) para editar los perfiles y exportar `glosario.json`.

## Cómo compartir la app

Envíe el **enlace** de la página publicada (no el archivo HTML). En el teléfono, la persona
abre el enlace y elige "Añadir a pantalla de inicio" (Android: menú de Chrome; iPhone: botón
Compartir en Safari). Desde ese momento le queda como una app y funciona sin internet.

## Cómo publicar (GitHub Pages)

El repositorio es `DERBGIT/emociones-3d` (público). GitHub Pages sirve la raíz de la rama `main`;
el `index.html` de la raíz redirige a `app/`. Enlace: https://derbgit.github.io/emociones-3d/

Esta carpeta contiene solo lo que se publica. Las versiones antiguas (B a 4.0), las notas
exportadas, `Promts.txt` y el artículo de Lövheim están fuera de ella, en
`D:\ProgramasDaniel_2(Desborde)\05_Tools\Emociones3d-historico`. No copie aquí notas personales:
el repositorio es público.

Cada cambio:
```powershell
git add -A; git commit -m "Descripción del cambio"; git push
```

Al publicar una versión nueva de la app o del glosario, suba también `VERSION` en `app/sw.js`
(por ejemplo `emociones3d-v5.0.1`) para que los teléfonos renueven la caché.

## Cómo editar el glosario

Opción A: abra la app con `?curador=1` al final de la URL. Aparece el botón "Editar perfil" en
la ficha del nodo. Al terminar, en "Acerca de" pulse "Exportar glosario.json" y reemplace
`app/glosario.json`.

Opción B: edite `app/glosario.json` directamente.

Después de cualquier edición (obligatorio, porque la app lee `glosario.js`):

```powershell
python tools/validar_glosario.py      # avisa de problemas y regenera app/glosario.js
python tools/glosario_md.py           # regenera GLOSARIO.md para leerlo
```

## Esquema de un perfil

```json
{
  "id": "n_3p5_3p5_3p5",
  "x": 3.5, "y": 3.5, "z": 3.5,
  "dir": [1, 1, 1],
  "nivel": "moderado",
  "familia": "Octante +X+Y+Z · Agrado · Alta Energía · Abrirme",
  "es_anclaje_low": true,
  "nombre_low": "Nombre cotidiano (nivel LOW)",
  "resumen_low": "Resumen en lenguaje directo.",
  "nombre": "Nombre (nivel MED)",
  "nombre_high": "Nombre profundo (nivel HIGH)",
  "alias": [],
  "evaluacion": "", "senales": "", "impulso": "", "pensamientos": "",
  "regula": "", "reencuadra": "",
  "acomp_validar": "", "acomp_evitar": "",
  "examen": ""
}
```

La malla tiene 26 direcciones (6 ejes, 12 planos, 8 octantes) con tres grados cada una
(sutil 1.5, moderado 3.5, desbordante 5.5) más el centro basal: 79 nodos.

## Dónde se guardan las notas en el navegador

`ruler4_<cuaderno>_pins`, `_paths`, `_views`, `_last_change`, `_last_export` (se mantiene el
prefijo de la 4.0 para no perder lo ya guardado), y `e3d_glosario_edits` para el modo curador.

## Nota sobre el modelo

El cubo original de Lövheim (2012) coloca *anger/rage* en serotonina baja, noradrenalina alta
y dopamina alta. Esta revisión coloca la Ira en +X, +Y, −Z. Se documenta en "Acerca de".
