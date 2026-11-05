# Rx English

App tipo Duolingo de inglés farmacéutico para CRA: vocabulario por áreas de la industria, situaciones reales de trabajo y audio en inglés americano.

## Estructura

- `docs/` — la web que se publica (GitHub Pages sirve esta carpeta).
  - `index.html` — toda la app: diseño, lógica y contenido (vocabulario, áreas, situaciones e índice de audio).
  - `a/*.mp3` — audios agrupados por unidad (`u1`–`u8`), área (`a1`–`a12`) y situación (`s1`–`s8`). El índice `AIDX` de `index.html` guarda dónde empieza cada frase dentro de cada archivo.
  - `manifest.webmanifest` e iconos — para añadirla a la pantalla de inicio del móvil.
- `tools/` — scripts con los que se generaron los audios (voces Piper «Lessac» y «Ryan», en-US).

## Publicación

GitHub Pages publica la carpeta `docs/` de la rama `main`: cada cambio que llega a `main` se publica solo en un par de minutos. No hay paso de compilación.

## Progreso

El progreso se guarda en el navegador de cada dispositivo (localStorage). Las actualizaciones no lo borran mientras la dirección de la web sea la misma.

## Cambiar el contenido

Si cambia el texto de una frase que tiene audio, hay que regenerar su archivo de audio y actualizar `AIDX`. Si no, sonará el audio antiguo o la voz del dispositivo.

## Versión y botón de actualización

`docs/index.html` contiene `const BUILD=...`. Cambia ese valor en cada publicación: el botón "Buscar actualización" de la app compara contra él y recarga si hay una versión nueva.
