# Dante's Inferno RP6 test checklist

No gameplay, performance, Adreno or device-install result is asserted without a
real test. Title ID: `454108CF`.

## Existing evidence

- Edge's [occlusion tracking issue #139](https://github.com/has207/xenia-edge/issues/139)
  lists this title among games unaffected by its occlusion changes. Those tests
  concern desktop GPUs, not RP6/Adreno.
- [Canary compatibility report #516](https://github.com/xenia-canary/game-compatibility/issues/516)
  describes a short playable test on a desktop Canary build. This is not Android
  compatibility evidence and does not justify switching cores.
- The inherited game-patches submodule contains optional **60 FPS Cutscenes**
  patches for base executable hash `5C20AFE8455FEE7D` and TU2 hash
  `C81DD5288EA71831`. Both remain disabled by default. They are not crash fixes.
- The queried XenDroid issues returned no Dante-specific match. Absence of a report
  is not proof of compatibility. No speculative title-specific hack is enabled.

## Test, in order

1. Record APK versionCode/certificate, RP6 Android version, GPU driver name/version,
   original game region/executable hash and whether TU2/DLC is installed.
2. Start with inherited default settings, native resolution scale, and the built-in
   driver. Do not enable optional patches for the initial comparison.
3. Cold-start the library, scan the existing game folder and launch the game there.
4. Test the same game launched directly by your existing gaming frontend.
5. Check logos, intro movie, menus, audio, stick axes, triggers, buttons and touch
   controls. Look for a startup hang, Vulkan device loss or missing textures.
6. Play the opening battle for at least 15 minutes. Check depth, shadows, effects,
   camera movement, audio looping/crackle and frame pacing.
7. Create a save/checkpoint, exit completely, relaunch and reload it. Verify the
   expected profile and save directory remain in use.
8. Test suspend/resume, exit/relaunch and a second level/loading boundary.
9. Only then compare a known RP6-compatible custom driver, keeping every other
   setting identical. Record sustained FPS and power/thermal behavior rather than
   a single transient reading.
10. If testing the optional cutscene patch, use the exact matching executable hash
    and test separately. Keep it off if speed/timing changes or instability appear.

For a failure, retain the app session logs under the core data directory and
`adb logcat -d -b crash`, together with the last working screen and reproduction
steps. Compare the same game/settings on desktop Edge with Vulkan when possible.
