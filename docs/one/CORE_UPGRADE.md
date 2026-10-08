# XenDroid One core integration scope

Inspected/build baseline: XenDroid `779680ade075d2d2a4c589c6a8d57a8e26c116c0`.
The last explicit Edge synchronization merges
`84cf209221160590768f615a0369a9c4a1456bbf` via XenDroid `59de96daabfe9a62c041ac78a8fc914d38f186e0`.
XenDroid adds later Android, GPU, scheduler, APU and correctness work on top.

Latest upstream Edge inspected at execution:
`669b4266f5682e5169d42552fdf64f02880652a4` (2026-10-07).
This is the **reference revision, not a claim that its whole tree is integrated**.

## What this release integrates

| Upstream commit | Change | Integration |
|---|---|---|
| `a5532a0d193130af1b5dd821c8c83daec27f6d11` | `mcrfs` clears only FPSCR exception bits; preserves control/status and rounding mode | Exact patch imported into core subtree, original author retained |
| `e1e4851f7a1fba0c1ed3583f2faeb776cf763895` | `mtfsfi` decodes the immediate from the correct RB bits | Exact patch, including upstream PPC regression fixtures |
| `1b0e9d00ea33e6148c3429234e44e8c364edbd7d` | Guest writes invalidate overlapping primitive conversions, including a conversion in progress | Exact patch, no Android-facing API changes |
| `968f1ef45921cff8794cbc0305bdf388c8dc3178` | ARM64 REV32/TBL byte permutes and byte/halfword ZIP merge specializations | Adapted byte/halfword forms; retained XenDroid's existing word ZIP specialization and halfword constant-folding fixes |

These patches are present in the latest inspected Edge tree. The integrated core
identity is **Edge base 84cf20922 + inherited XenDroid overlay + the four listed
backports**. No single upstream Edge SHA represents this hybrid tree. The fork
source commit and APK native SHA-256 identify the exact implementation.

The upstream `1b242658e535fbd12645e4d2c12693771075b738` Vulkan shader-layout locking
fix was checked: XenDroid already locks the same shared map/vector in
TranslateAnalyzedShader. It was retained, not applied twice.

## Full refresh remains incomplete

A file-by-file three-way merge trial compared the exact Edge base, current
XenDroid subtree, and current Edge. It found 523 automatically replaceable files,
68 clean three-way merges, 37 deletions, 3 gitlink changes and **70 conflicted
files**. The trial was kept outside the build/source branch. The conflict list is
`full-upgrade-conflicts.txt`; this does not assert a runtime regression or claim a
compile of the unresolved full tree succeeded.

The overlap includes scheduler safepoints/wedge diagnostics, guest blocking I/O,
user-mode page tables, ARM64 FPCR/register allocation, XMA handling, the Android
emulator shell, Vulkan in-pass EDRAM work, resolve/readback paths and custom shader
interpreter behavior. Completing this requires porting those interfaces and
re-testing their semantics. Picking a different merge ancestor is insufficient:
the old and current upstream histories diverge, so raw commit counts include
rewritten/equivalent history. `upstream-diff-numstat.txt` is the tree comparison;
`upstream-change-list.txt` is a discovery ledger, not a list of changes all shipped.

This build deliberately retains the known compiling Android core rather than
silently discarding 37,081 lines of inherited overlay additions. It **does not
meet the requested full-newest-core definition of done**. It supplies a real
signed Android candidate with reviewed, independently buildable upstream fixes.

## Significant work in current upstream (not all integrated)

- ARM64: shorter call/branch sequences, NEON permute specializations, FPCR tracking,
  floating-point NaN correctness, tail-stub/register-liveness work.
- Scheduling/kernel: dispatch-level switches, DPC/timer/APC behavior, file work
  moved off the guest dispatch thread, synchronous resolver blocking fixes.
- Memory: user page-table protections, 4KB mappings, faults and page-table changed
  bits, lazy indirection-table commitment.
- Vulkan/GPU: getBCF border sampling, scaled line width, shader-layout locking,
  resolve readback/memexport ordering and EDRAM/occlusion work.
- Audio/system APIs: XMA changes, title lifecycle and XeFu/original-Xbox support.

No game-speed claim is derived from upstream microbenchmarks. No Canary core
replacement or new speculative Dante hack was introduced.

## Android behavior retained

Package `xendroid.compose`; MainActivity and EmulatorHostActivity; exported game
launch action `xendroid.intent.action.xendroid`; ACTION_VIEW handling;
`game_uri`, `AutoStartFile` and URI normalization; document-provider authority
`xendroid.compose.DocumentsProvider`; separate `:emu` process; all original
storage/profile/config/driver names; touch, controllers, AAudio/OpenSLES, Vulkan
loader/custom drivers and content handling. Manifest source and storage/JNI
bridges are unchanged. `android-overlay-files.txt` inventories the initial
Edge-vs-XenDroid differences, including non-Android customizations.

## Next upstream update

1. Branch from the shipped source commit. Preserve the signing identity and
   manifest/storage contracts. Build the current release before changing core.
2. Fetch Edge, record its SHA, and compare **trees** against the documented base.
   Do not use HEAD's merge-base as the assumed vendored source base.
3. For a full refresh, resolve the conflict ledger by subsystem. Keep Android
   JNI shell/build adapters, GPU driver integration, and launch/storage APIs.
4. Update/pin gitlinks and prefixed `.gitmodules` paths together. Keep desktop-only
   dependencies out of the APK. Compile and inspect native ELF dependencies.
5. Run frontend tests, ARM64 instruction checks and device/game regression tests.
   Write down exactly which upstream changes remain excluded.
6. Choose higher versionCodes, build/sign two releases with the existing key,
   validate certificates/manifests, and actually perform an update install on a
   clean test device before claiming update installation passed.
