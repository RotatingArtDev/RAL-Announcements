# Lanzamiento de la actualización menor 2.0.1 del Launcher!!

## Resumen de la actualización
- La versión 2.0.1 se centra en correcciones de compatibilidad, mejores capacidades de diagnóstico y mejoras del flujo de compilación/publicación.
- Se resolvieron fallos de inicialización de CoreCLR en algunos dispositivos (especialmente ciertos modelos Xiaomi) y se reforzó la exportación de registros de fallos.
- También se actualizaron dependencias gráficas (FNA3D y MobileGlues) y se añadieron más capacidades de observación de rendimiento.

## Correcciones y compatibilidad
- Se corrigieron problemas de carga de mods de SMAPI en algunos escenarios.
- Se añadieron y ajustaron hooks relacionados con `pthread_condattr_setclock` para mejorar la compatibilidad del runtime de .NET en dispositivos específicos.
- Se agregó manejo de compatibilidad y lógica de reintento para fallos de inicialización de CoreCLR en algunos dispositivos Xiaomi.
- Se mejoró la interacción de la pantalla de fallos y la recopilación de diagnóstico para un análisis más completo.

## Rendimiento y diagnóstico
- Se reforzó la prueba/diagnóstico de rendimiento de GPU para identificar cuellos de botella de renderizado con mayor claridad.
- Se mejoró el flujo de exportación de registros para facilitar los reportes y el análisis de reproducción.

## Actualizaciones de dependencias y runtime
- MobileGlues se actualizó a la versión 1.3.4.
- FNA3D se actualizó y se ajustó a una rama adecuada, con mejoras en soporte relacionado con profiling.

## Ingeniería y publicación
- Se añadió un flujo de compilación automática de APK con GitHub Actions para mejorar la eficiencia y la reproducibilidad de publicaciones.
- La versión se actualizó a 2.0.1.
