# Replacing XenDroid safely

Do not uninstall the original until the backup is readable outside its app folders.
This procedure applies to the inspected Compose release (`xendroid.compose`). If
Android App Info shows another package, stop: that is a different legacy build.

## What Android removes on uninstall

| Data | Inspected location | Uninstall result |
|---|---|---|
| Core saves, profiles, installed DLC/TUs, settings, touch layout, logs, shader cache | `/storage/emulated/0/Android/data/xendroid.compose/files/compose/` (actual external volume can differ) | App-specific external storage is deleted |
| Per-game configuration | `compose/config/<TITLE_ID>.config.toml` under the location above | Deleted |
| Default content root | `compose/content/` under the location above | Deleted; includes saves and profiles |
| Custom Vulkan drivers | `/data/user/0/xendroid.compose/compose/driver/` | Private app storage is deleted |
| Controller mapping, library folder choices, frontend preferences | `/data/user/0/xendroid.compose/files/datastore/` and private preferences | Deleted |
| Persisted SAF folder permissions | Android's per-app URI grants | Lost; select folders again |
| ROM folders chosen in shared storage or on SD, original driver ZIPs in Downloads | User-selected paths outside `Android/data` / `Android/obb` | Normally retained; confirm actual path first |
| Custom `content_root`, `cache_root`, `storage_root` overrides | Wherever your configuration points | Depends on location; app-owned paths are deleted, shared paths normally remain |

The same folder names and package identity do not stop Android deleting the old
app's data. Android cloud restore across a different signing certificate must not
be relied upon.

## Before uninstalling

1. Close the game and stop XenDroid. Open Android's system **Files/Documents**
   picker and look for the XenDroid document-provider root. It exposes the core
   external data directory. Copy **all** of it to a folder such as
   `Download/XenDroid-backup-2026-10-08`, an SD card shared folder, or a computer.
   Do not place the backup anywhere inside `Android/data` or `Android/obb`.
2. If the provider is unavailable, try USB/ADB access:
   `adb pull /sdcard/Android/data/xendroid.compose/files/compose ./XenDroid-backup/compose`.
   Android versions may deny this. A permission error is NOT a successful backup.
   Find another accessible route before uninstalling.
3. Open the copied directory and verify `content/`, the global
   `xenia-canary.config.toml`, `config/`, and touch-control configuration where
   present. Copy custom save/content locations too. Verify file counts/sizes or
   hashes against the originals where access permits.
4. Keep the original driver ZIP outside the app folder. Record the selected driver,
   library folders, controller mappings and relevant frontend settings/screenshots.
   Private driver installations and DataStore preferences cannot generally be
   copied from a non-debuggable release without root or a supported app export.
   No untested export feature is assumed here.
5. Keep an independent second copy of important saves. If you cannot copy saves,
   do not proceed. No files are moved or overwritten by this project automatically.

## First install

1. After verifying the backup, manually uninstall the original XenDroid.
2. Install the signed `XenDroid-One-v0.1.0-arm64.apk` through Android's package
   installer, enabling installation from the file manager if prompted.
3. Open XenDroid One once to create its directories, then close/force-stop it.
4. Restore the backed-up core directory into the same
   `Android/data/xendroid.compose/files/compose` location using the document provider
   or another permitted route. This intentionally overwrites newly created files:
   review the destination and use your own backup, not somebody else's profile.
   Keep the bundled `default_config.toml` as a current-default reference; the app
   refreshes that file on startup. Do not blindly replace new defaults.
5. Re-select game directories and re-grant storage permissions. Re-import the
   driver ZIP and re-create any private controller/preferences settings.
6. Confirm the save/profile loads before deleting any backup. Then test the
   existing frontend's direct game launch.

## Future updates

Install a later XenDroid One APK directly over the current one (or use
`adb install -r NEW.apk`). Same package + same certificate + increasing
versionCode are required. Do not uninstall between fork releases. Back up saves
before important core upgrades. An unexpected signature-conflict error means the
APK was signed by a different key: stop rather than uninstall to bypass it.
