# Launcher v2.0 Released!!!

## Update Overview

- Continued the migration from the old architecture to Kotlin + Compose, making the UI cleaner and smoother (ultra-smooth with interruptible animations) (we basically rewrote the whole UI 😭😭😭).
- Added an **Announcement System** and an **Update Check System** for better communication and upgrade experience.
- Systematically improved core modules including rendering, launch parameters, control editing, and game configuration management.
- Fixed a batch of Android and input/control-related issues, significantly improving overall stability.

## Key Feature Updates
- Updates and announcements:
  - Added a dedicated **Announcements page** so you can read announcements directly inside the launcher.
  - Added an **Update Check feature**, with localized update flow and refined UI.
- Multilingual support:
  - Continued to expand and integrate **multilingual support** (including Chinese, English, and other language resources) to lower the usage barrier.
- Game launch and configuration:
  - Moved **Game Configuration Editing** to a dedicated screen (bottom-right button on the game card, click Edit), making configuration management clearer.
- Rendering and performance:
  - Introduced a registry-driven rendering pipeline with **per-game render configuration overrides** (bottom-right button on the game card, click Edit).
  - **Added OSMesa paths and multiple rendering/performance options (including quality levels and FPS-related optimizations).**
  - **Added support for overriding audio buffer size and other performance tuning options.**
- Control system:
  - Continued control editor refactor and polish, with support for more control styles and layout capabilities **(polygon key shapes, key snapping and alignment).**
  - Improved input experience for mouse wheel/directional controls and virtual key order.
  - Added a **Wheel control**, allowing swipe input for mapped key values (no more cockpit-like screen clutter 😭😭😭).
- Multiplayer system:
  - **Added an EasyTier-based multiplayer system (experimental) and multiplayer diagnostics.**

## Experience and Stability Improvements
- UI and architecture:
  - Completed multi-stage project refactors (including unified initialization flow, runtime module split, and sub-layout cleanup).
  - Further improved the control editor and shared components experience.
- Critical fixes:
  - Fixed incorrect `TMPDIR` setup on Android versions below 13 **(fixes Everest import issues on devices below Android 13).**
  - Fixed FMOD/SDL related reference issues **(fixes audio delay caused by Everest SDL plugin registration failure; thanks to DENIZTR8008 for the fix direction and bug feedback).**

## Compatibility and Import Support
- Added/enhanced support for multiple games and ecosystems:
  - **Fixed Terraria 1.4.5 base game file import.**
  - **Added SMAPI Native OpenGL ES 3 support.**
  - **Fixed tModLoader server startup issues on certain devices.**
  - **Fixed SMAPI LAN multiplayer.**
  - SMAPI mods directory changed to `/storage/emulated/0/RALauncher/Stardew Valley/Mods`
  - Everest mods directory changed to `/storage/emulated/0/RALauncher/Everest/Mods`

## Known Notes / Migration Reminder
- This version spans major changes, including storage and architecture refactors (such as game list storage and migrator adjustments). So...

# **Please reinstall the launcher!**
# **Please reinstall the launcher!**
# **Please reinstall the launcher!**
