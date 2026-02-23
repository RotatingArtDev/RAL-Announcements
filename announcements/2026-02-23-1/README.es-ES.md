# Lanzamiento del Launcher v2.0!!!

## Resumen de esta actualización

- Se completó la migración continua de la estructura antigua a Kotlin + Compose, con una interfaz más clara y fluida (fluidez extrema con animaciones interrumpibles) (prácticamente reescribimos toda la interfaz 😭😭😭).
- Se añadieron el **sistema de anuncios** y el **sistema de comprobación de actualizaciones**, para una mejor comunicación y experiencia de actualización.
- Se reforzaron de forma integral módulos clave como renderizado, parámetros de inicio, edición de controles y gestión de configuraciones de juego.
- Se corrigieron varios problemas de Android y de entrada/control, mejorando notablemente la estabilidad general.

## Actualizaciones de funciones clave
- Actualizaciones y anuncios:
  - Se añadió una **página de anuncios** para consultar anuncios directamente dentro del launcher.
  - Se incorporó la **función de comprobación de actualizaciones**, con flujo de actualización localizado y mejoras de UI.
- Soporte multilenguaje:
  - Se sigue ampliando e integrando el **soporte multilenguaje** (incluyendo chino, inglés y otros recursos de idioma) para reducir la barrera de uso.
- Inicio del juego y configuración:
  - La **edición de configuración del juego** se movió a una pantalla independiente (botón inferior derecho de la tarjeta del juego, pulsa Editar), haciendo la gestión más clara.
- Renderizado y rendimiento:
  - Se introdujo una canalización de renderizado basada en registro, con **anulación de configuración de render por juego** (botón inferior derecho de la tarjeta del juego, pulsa Editar).
  - **Se añadieron rutas OSMesa y múltiples opciones de renderizado/rendimiento (incluyendo niveles de calidad y optimizaciones relacionadas con FPS).**
  - **Se añadió soporte para anular el tamaño del búfer de audio y otros ajustes de rendimiento.**
- Sistema de controles:
  - El editor de controles sigue en refactorización y pulido, con soporte para más formas de controles y capacidades de diseño **(formas poligonales para botones, ajuste y alineación magnética).**
  - Se mejoró la experiencia de entrada en rueda de ratón/controles direccionales y el orden de teclas virtuales.
  - Se añadió un **control de rueda**, donde deslizar permite introducir el valor de tecla correspondiente (mamá ya no tendrá que preocuparse de que la pantalla parezca la cabina de un avión 😭😭😭).
- Sistema multijugador:
  - **Se añadió un sistema multijugador basado en EasyTier (experimental) y diagnóstico de conexión multijugador.**

## Mejoras de experiencia y estabilidad
- UI y estructura:
  - Se completaron refactorizaciones en varias fases del proyecto (incluyendo unificación del flujo de inicialización, separación de módulos en tiempo de ejecución y limpieza de subdiseños).
  - Se optimizó aún más la experiencia del editor de controles y de componentes compartidos.
- Correcciones clave:
  - Se corrigió la configuración incorrecta de `TMPDIR` en Android anterior a 13 **(corrige el problema de importación de Everest en dispositivos por debajo de Android 13).**
  - Se corrigieron problemas de referencias FMOD/SDL **(corrige el retardo de audio causado por fallo al registrar el plugin SDL de Everest; gracias a DENIZTR8008 por la idea de corrección y el reporte).**

## Compatibilidad y soporte de importación
- Se añadió/mejoró soporte para varios juegos y ecosistemas:
  - **Se corrigió la importación de archivos base del juego Terraria 1.4.5.**
  - **Se añadió soporte para SMAPI Native OpenGL ES 3.**
  - **Se corrigió un problema por el cual tModLoader no podía iniciar servidor en algunos dispositivos.**
  - **Se corrigió el multijugador LAN de SMAPI.**
  - El directorio de mods de SMAPI cambió a `/storage/emulated/0/RALauncher/Stardew Valley/Mods`
  - El directorio de mods de Everest cambió a `/storage/emulated/0/RALauncher/Everest/Mods`

## Nota conocida / Recordatorio de migración
- Esta versión incluye cambios grandes, con refactorizaciones a nivel de almacenamiento y estructura (como ajustes del almacenamiento de la lista de juegos y del migrador). Así que...

# **¡Vuelve a instalar el launcher!**
# **¡Vuelve a instalar el launcher!**
# **¡Vuelve a instalar el launcher!**
