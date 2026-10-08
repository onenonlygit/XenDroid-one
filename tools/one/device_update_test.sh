#!/usr/bin/env bash
# Explicitly installs two releases on a test device. Never uninstalls anything.
# Usage: device_update_test.sh FIRST.apk SECOND.apk [existing-game-path]
set -euo pipefail
first=${1:?first APK required}
second=${2:?second APK required}
pkg=xendroid.compose
adb get-state
if adb shell pm path "$pkg" | tr -d '\r' | grep -q '^package:'; then
  echo 'Use a clean test device: xendroid.compose is already installed.' >&2
  exit 1
fi
adb install "$first"
adb shell am start -W -n "$pkg/xendroid.compose.MainActivity"
adb shell am force-stop "$pkg"
adb install -r "$second"
adb shell dumpsys package "$pkg"
adb shell am start -W -n "$pkg/xendroid.compose.MainActivity"
if [ -n "${3:-}" ]; then
  adb shell am force-stop "$pkg"
  adb shell am start -W -a xendroid.intent.action.xendroid \
    -n "$pkg/xendroid.compose.EmulatorHostActivity" --es game_uri "$3"
fi
adb logcat -d -b crash
echo 'Both install commands completed. Inspect launch output and crash log before calling runtime smoke testing successful.'
