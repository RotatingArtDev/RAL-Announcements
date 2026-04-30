# Launcher 2.0.1 Minor Update Released!!

## Update Overview
- Version 2.0.1 focuses on compatibility fixes, stronger diagnostics, and build/release workflow improvements.
- We addressed CoreCLR initialization failures on some devices (especially certain Xiaomi models) and improved crash log export.
- Graphics-related dependencies (FNA3D and MobileGlues) were updated, with better performance observability added.

## Fixes and Compatibility
- Fixed SMAPI mod loading issues in some scenarios.
- Added and refined `pthread_condattr_setclock` hooks to improve .NET runtime compatibility on specific devices.
- Added compatibility handling and retry logic for CoreCLR initialization failures on some Xiaomi devices.
- Improved crash page interactions and diagnostics collection for more complete troubleshooting.

## Performance and Diagnostics
- Enhanced GPU performance testing/diagnostics to make rendering bottlenecks easier to identify.
- Improved log export flow for clearer issue reporting and reproduction analysis.

## Dependencies and Runtime Updates
- Upgraded MobileGlues to 1.3.4.
- Updated FNA3D and aligned it to an appropriate branch, with profiling-related support improvements.

## Engineering and Release
- Added a GitHub Actions APK auto-build workflow to improve release efficiency and reproducibility.
- Version number has been bumped to 2.0.1.
