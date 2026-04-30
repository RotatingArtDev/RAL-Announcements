# Lanzamiento de la actualización 2.1.0 del Launcher!!

## Resumen de la actualización

- La versión 2.1.0 se centra principalmente en adaptarse a la nueva versión de `tModLoader`, mejorar la compatibilidad del runtime y seguir puliendo el editor de controles y la experiencia de interacción.
- El runtime de dotnet se actualizó a `v10.0.4`, corrigiendo varios problemas relacionados con la entrada, el modo nocturno, la edición de texturas y la visualización de páginas.
- También se siguió optimizando la parte gráfica y la gestión de memoria: esta versión intenta aliviar el límite de 4 GB en algunos sistemas y mejora el rendimiento de renderizado de FNA3D en escenarios extremos.

## Compatibilidad y runtime

- Adaptado para `tModLoader v2026.02.3.1`.
- El runtime de dotnet se actualizó a `v10.0.4`. Después de actualizar, si quieres usar el nuevo runtime, abre la configuración del launcher y pulsa "Volver a extraer las bibliotecas del runtime".
- Se añadió la marca `largeHeap` para intentar resolver el límite de 4 GB de memoria en algunos sistemas.
- Se corrigieron los fallos `SIGILL` en algunos dispositivos causados por una configuración incorrecta de los hooks de compatibilidad de Xiaomi CoreCLR.

## Editor e interacción

- Se refactorizó parte del código y se siguió limpiando implementación heredada para mejorar la mantenibilidad.
- Se corrigieron problemas de UI en escenarios con textos largos. Por ejemplo, los nombres demasiado largos en la página de detalles del control ya no comprimen la etiqueta "Predeterminado".
- Se mejoró la página de selección de texturas y se añadió vista previa de texturas.
- Se corrigió un error por el que la transparencia de la textura del control no se veía afectada por la transparencia del fondo.
- Se mejoró la ventana del editor de controles: el botón de eliminar ya no está fijo en la esquina inferior derecha y ahora se integró con el botón de copiar en una sola barra de herramientas.
- Se corrigió el problema por el que no se mostraban los materiales de los botones en el editor.
- Se corrigió el problema de actualización de colores de página en modo nocturno.
- El rango del touchpad volvió a 60%-500%.
- Se recuperó la opción para forzar que el mando virtual sea el primer mando.
- En el modo teclado, el stick izquierdo ahora se ajusta a ocho direcciones, lo que facilita percibir la dirección de entrada actual.
- Se añadió una zona muerta al stick izquierdo en modo teclado para reducir toques accidentales.

## Rendimiento y estabilidad

- Se mejoró el flujo para compartir registros, facilitando el reporte de problemas y el diagnóstico.
- Se corrigió y optimizó el renderizado de FNA3D para mejorar el rendimiento en escenarios extremos.

## Notas de instalación / Migración

- Esta versión permite instalación por sobrescritura.
- Algunos ajustes pueden restablecerse a sus valores predeterminados después de la actualización.
- Si encuentras problemas relacionados con el runtime, intenta volver a extraer primero las bibliotecas del runtime desde la configuración.
