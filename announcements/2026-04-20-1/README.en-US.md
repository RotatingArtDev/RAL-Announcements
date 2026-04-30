# Launcher 2.1.0 Update Released!!

## Update Overview

- Version 2.1.0 mainly focuses on adapting to the new `tModLoader` release, improving runtime compatibility, and continuing to refine the control editor and interaction experience.
- The dotnet runtime has been upgraded to `v10.0.4`, fixing a range of issues related to input, night mode, texture editing, and page rendering.
- Graphics and memory handling were further improved: this release attempts to ease the 4 GB memory limit on some systems and improves FNA3D rendering performance in extreme scenarios.

## Compatibility and Runtime

- Adapted for `tModLoader v2026.02.3.1`.
- Upgraded the dotnet runtime to `v10.0.4`. After updating, if you want to use the new runtime, open launcher settings and click "Re-extract Runtime Libraries".
- Added the `largeHeap` flag to try to address the 4 GB memory cap on some systems.
- Fixed `SIGILL` crashes on some devices caused by incorrect Xiaomi CoreCLR compatibility hook settings.

## Editor and Interaction

- Refactored part of the codebase and continued cleaning up legacy implementation to improve maintainability.
- Fixed UI issues in long-text scenarios. For example, overly long control names on the control detail page no longer squeeze the "Default" tag.
- Improved the texture selection page and added texture preview support.
- Fixed a bug where control texture transparency was not affected by background transparency.
- Improved the control editor window: the delete control button is no longer fixed in the lower-right corner and is now merged with the copy button into one toolbar.
- Fixed missing button materials in the editor.
- Fixed page colors not refreshing correctly in night mode.
- Restored the touchpad range to 60%-500%.
- Restored the option to force the virtual controller to be the first controller.
- In keyboard mode, the left stick now snaps to eight directions, making it easier to tell the current input direction.
- Added a dead zone to the keyboard mode left stick to reduce accidental input.

## Performance and Stability

- Improved the log sharing flow to make issue reporting and troubleshooting easier.
- Fixed and optimized FNA3D rendering to improve performance in extreme scenarios.

## Install Notes / Migration Tips

- This version supports overwrite installation.
- Some settings may be reset to their default values after the update.
- If you run into runtime-related issues, try re-extracting the runtime libraries from settings first.
