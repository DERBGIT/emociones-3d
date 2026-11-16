# RETOMAR — Emociones 3D 5.0

Última sesión: lunes 16 de noviembre de 2026 (America/Caracas).

## Dónde quedamos, en una frase

La 5.0 está lista en esta carpeta, que ahora contiene solo lo publicable; el repositorio público
`DERBGIT/emociones-3d` ya existe en GitHub y **falta la primera subida y activar GitHub Pages**.

## Dónde está cada cosa

- Esta carpeta (Drive): la app y sus herramientas. Es lo que se publica.
- `D:\ProgramasDaniel_2(Desborde)\05_Tools\Emociones3d-historico`: todo lo anterior (versiones B a 4.0,
  la 3.2 archivada, notas exportadas, `Promts.txt`, el PDF de Lövheim y el historial de git antiguo).

## Lo hecho

- 5.0: une el contenido de la 4.0 (79 nodos, Rueda de Afinado, cuadernos, cifrado) con la
  infraestructura de la 3.2 (instalable, sin internet, importar con fusión, recordatorio de respaldo,
  modo curador) y migra las notas de la 3.2.
- Glosario 5.0.1: 54 nombres afinados a lenguaje cotidiano (los anteriores quedaron como alias) y
  alias nuevos para el buscador. Cuatro cambios de sentido pendientes de su confirmación:
  «Ansiedad / Angustia» (antes Culpa), «Hundimiento / Vacío» (antes Humillación),
  «Miedo / Indefensión» (antes Resignación), «Desconexión total» (antes Acedia).
- App 5.0.2: etiquetas 3D con solo el primer término y la más cercana destacada; rótulos de eje en
  dos líneas con el neurotransmisor pequeño y sin signo; el buscador prefiere el nombre al alias e
  ignora acentos.

## Primeros pasos al retomar

1. Primera subida (PowerShell, en esta carpeta):
   `git init -b main; git add -A; git commit -m "Emociones 3D 5.0"; git remote add origin https://github.com/DERBGIT/emociones-3d.git; git push -u origin main`
2. Activar Pages: Settings > Pages > rama `main`, carpeta `/ (root)`.
3. Probar https://derbgit.github.io/emociones-3d/ en el teléfono y "Añadir a pantalla de inicio".

## Pendientes

- Probar en teléfono (uso táctil, tamaño de etiquetas del cubo sutil).
- Cifrar en reposo el cuaderno de Acompañamiento y exigir una clave de más de 4 caracteres.
- Vista en el tiempo (diario / línea de tiempo) de las notas.
- Empaquetar React, Three.js y Tailwind dentro de `app/` para no depender de servidores externos.
- Decidir si los neurotransmisores salen del cubo y quedan solo en "Acerca de".
- De la 3.2 no se portaron: vistas guardadas, deshacer (Ctrl+Z), pegar coordenadas, orden de pines.
- Confirmar que la colocación de la Ira en (+X, +Y, −Z) es deliberada.

## Notas técnicas para el agente

- Windows + PowerShell: separar comandos con `;`.
- La carpeta vive en Google Drive: evitar operaciones de git mientras Drive sincroniza.
- Tras editar `app/glosario.json`: `python tools/validar_glosario.py` (regenera `glosario.js`).
- Al publicar una versión nueva, subir `VERSION` en `app/sw.js`.
