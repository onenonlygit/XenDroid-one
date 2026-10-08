# XenDroid One

Personally maintained, **AI-assisted** ARM64 Android fork by [onenonlygit](https://github.com/onenonlygit), for Retroid Pocket 6 testing. Engineering, build-system work and documentation were developed with AI assistance and reviewed with the available build and static checks. This fork is independent of the original XenDroid and Xenia maintainers; original licenses, history and credits are preserved.

Release package remains
`xendroid.compose`; visible name is XenDroid One. Original launch activities,
frontend intents, storage names and credits are retained.

**Core scope:** inherited XenDroid/Edge base plus four reviewed recent Edge
backports. A full refresh to current Edge is **not yet complete**. No Dante's
Inferno performance/playability claim has been made.

- **[Download v0.1.0 signed ARM64 APK (ZIP)](https://github.com/onenonlygit/XenDroid-one/raw/a36416000af35a428cc238ee8e5eeb87d59d7959/XenDroid-One-v0.1.0-arm64.zip)** — extract the ZIP, then install the APK on your RP6.
- [Build details and verification](https://github.com/onenonlygit/XenDroid-one/blob/one/build-v0.1.0/BUILD_DOWNLOAD.md)
- [GitHub releases](https://github.com/onenonlygit/XenDroid-one/releases) — release-page publication pending; use the verified ZIP above.
- [Core scope and upgrade ledger](docs/one/CORE_UPGRADE.md)
- [Back up BEFORE uninstalling the original](docs/one/BACKUP_AND_INSTALL.md)
- [Signing identity, recovery and repeatable builds](docs/one/SIGNING_AND_BUILDS.md)
- [Dante's Inferno testing checklist](docs/one/DANTES_INFERNO.md)

Only install XenDroid One releases matching the public certificate in
`docs/one/release-certificate.sha256`. Private signing material is never in source.
The automated workflow must be configured with the owner's persistent secrets.

---

The following is the preserved upstream README and attribution. Its original
release links refer to upstream, not this fork's signing identity.

<p align="center">
       <img height="256px" src="app/src/main/assets/XenDroid_foreground.png"/>
    </a>
</p>

<h1 align="center">XenDroid - Android Xbox 360 Emulator</h1>

## History
XenDroid was initially forked form xa360e, which was based off [Xenia Canary](https://github.com/xenia-canary/xenia-canary).
However, a complete rebase was made on [Xenia Edge](https://github.com/has207/xenia-edge) with a new Kotlin backend.
We are looking foward to keep the project updated alongside the Edge fork,
and keep the code compatible with Xenia licenses.

## Be aware of scams
- XenDroid is a free project. If you paid for this, then you got scammed.
- The ONLY reliable source for the apk is in the [releases](https://github.com/rfandango/XenDroid/releases/latest) section, along with the distributed source code.
  - We cannot be held responsible for edited apks by unkown users, you have been warned.

## Issue Reporting
A dedicated repo will be made to do reports. As of now critical issues are known.

In order to give detailed reports, you must compare the android port with `Xenia Edge` using `Vulkan` as a backend. Make sure that the
issues can be reproduced only on Android. If the issues are on Edge too, then we wait for the developers to fix
them, and align the port as a consequence.


## Building

See [BUILD.md](BUILD.md) for build instructions.

## LICENSE

Please check the LICENSE file under the appropriate file header and directory for detailed information.

## Device Requirements
- Snapdragon SoC, GEN 2 or higher
- Adreno GPU 740 or higher. Lower 7xx have not been tested.

## Recommended Drivers
- You can get the drivers for your GPU from two sources 
  - [Whitebelyash upstream drivers](https://github.com/whitebelyash/AdrenoToolsDrivers/releases)
    - This is a All-In-One driver for a wide range of GPUs
  - [StevenMXZ forked drivers](https://github.com/StevenMXZ/Adreno-Tools-Drivers/releases)
    - This one has different drivers for each GPU series
  
# Applying the driver
  - Check your device specs with [CPU X](https://play.google.com/store/apps/details?id=com.abs.cpu_z_advance&hl=it) to get the matching driver.
  - To apply the drivers go to **Settings** > **Vulkan** > **Custom Vulkan Driver**, then select the zip file.

## About Donations
I would like to take this opportunity to help a friend out. If you are willing to make donations, please consider donating to
[Bitshifter's Kofi](https://ko-fi.com/bitsh1ft3r/goal?g=0). He's the maintainer of the [Xenon Project](https://github.com/xenon-emu/xenon)
and every donation can help making a difference for the maintainer.
Thank you - Fabxx
