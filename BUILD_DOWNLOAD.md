# XenDroid One v0.1.0

Personal AI-assisted fork maintained by onenonlygit. Independent of the original XenDroid and Xenia maintainers; original source history, licenses and credits are retained.

Extract XenDroid-One-v0.1.0-arm64.zip and install the enclosed release-signed ARM64 APK on your Retroid Pocket 6.

Package: xendroid.compose. VersionCode: 1002. APK SHA-256: 13b580d56625285d6ef58af48e2199e6c12a166170975d4ed402eaa84ee60e21.
Certificate SHA-256: bec10b88d6eb5e50c1b4e4b73a4cb25a49b4e09e358b856e3f3c0947239f0e5d.

Source: original XenDroid base 779680ade075d2d2a4c589c6a8d57a8e26c116c0 plus four reviewed Xenia Edge backports and Android packaging/signing adaptations. Full latest-Edge integration is incomplete. Original package, launch components/intents and storage conventions are retained.

Validation: actual ARM64 release builds passed; 89 frontend unit tests and 7000 randomized NEON semantic cases passed. Two consecutively versioned APKs have the same signing certificate. No Android install/update runtime test or RP6/Dante's Inferno gameplay test was executed.

BEFORE uninstalling original XenDroid, follow docs/one/BACKUP_AND_INSTALL.md: Android removes private and app-specific external storage on uninstall. Back up saves, configuration and custom drivers. Restore the files after first installing this fork. Subsequent releases must use the retained signing identity; do not uninstall this fork for ordinary updates.

Private signing keys are absent from this repository. Future automated signing requires owner-configured encrypted Actions secrets. This ZIP distributes the already built, verified APK; GitHub release-page publication is still pending.
