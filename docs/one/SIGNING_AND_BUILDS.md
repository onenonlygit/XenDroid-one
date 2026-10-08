# Owner-controlled release signing and builds

The public certificate and SHA-256 fingerprint live in this directory. The
private PKCS12 key and its passwords are delivered separately in the private
signing-backup archive. They must never be committed, attached to a public GitHub
release, included in an APK or copied into build logs.

## Retain and recover the identity

1. Download the signing-backup ZIP immediately. It contains
   `xendroid-one.p12`, `credentials.json`, the public certificate and a recovery
   README. The keystore is password-protected; the ZIP also contains the password,
   so protect the entire ZIP as a private credential backup.
2. Store two independent copies under your control, e.g. an encrypted password
   manager attachment and an encrypted offline drive. Keep the JSON/passwords
   protected along with the key. Verify you can read the key with `keytool -list`
   and compare the public SHA-256 fingerprint before deleting a working copy.
3. Recovery: restore the same file/password/alias and compare the fingerprint.
   Re-create the GitHub secrets below. Never generate a replacement key to fix a
   missing-secret error. Losing the key means normal same-certificate updates
   cannot continue. If compromised, stop distribution and assess migration/key
   rotation separately; no untested rotation scheme is promised.

## GitHub setup (owner action required)

Create/fork `onenonlygit/xendroid-one`, preserving original XenDroid history.
Under Settings > Secrets and variables > Actions, create encrypted repository
secrets:

| Secret | Value from your retained backup |
|---|---|
| `ANDROID_KEYSTORE_BASE64` | Base64 of the PKCS12 bytes, without extra text |
| `KEY_ALIAS` | `xendroid-one` |
| `KEYSTORE_PASSWORD` | `store_password` from credentials.json |
| `KEY_PASSWORD` | `key_password` from credentials.json |

No signing secrets were uploaded or configured by this environment. The connected
GitHub API lacks repository creation/forking, secret administration and workflow
execution operations. Local signed builds do not depend on those permissions.

The workflow runs unsigned checks for PRs. Trusted main builds require persistent
secrets, sign two consecutive releases, verify the pinned public fingerprint,
retain artifacts, then publish a release. It never signs PR code with the key.
Action revisions, Gradle distribution/hash, AGP/Kotlin, SDK35, NDK29.0.14206865,
CMake3.30.3, JDK21.0.12+8 and dependency gitlinks are pinned. Ubuntu host shader
package versions may receive security updates; exact host versions are captured
in the local build report. Workflow execution still needs verification on GitHub.

## Local release build

Follow BUILD.md for toolchain setup. Initialize the pinned Android dependencies
with `python3 tools/one/init_submodules.py`. Configure `sdk.dir` and `cmake.dir`.
Then build (example versionCodes; choose values HIGHER than all installed/shipped
releases, not simply these examples again):

```bash
./gradlew :app:assembleRelease :app:testReleaseUnitTest \
  -PxoneVersionCode=1001 -PxoneVersionName=0.1.0-rc1 --no-daemon --max-workers=4
```

Supply the following through private environment variables or a protected secret
manager, not shell commands saved with literal passwords:
`XONE_KEYSTORE`, `XONE_KEY_ALIAS`, `XONE_STORE_PASSWORD`, `XONE_KEY_PASSWORD`, and
`ANDROID_SDK_ROOT`. Then:

```bash
python3 tools/one/sign_apk.py \
  app/build/outputs/apk/release/app-release-unsigned.apk \
  dist/XenDroid-One-v0.1.0-rc1-arm64.apk
./gradlew :app:assembleRelease \
  -PxoneVersionCode=1002 -PxoneVersionName=0.1.0 --no-daemon --max-workers=4
python3 tools/one/sign_apk.py \
  app/build/outputs/apk/release/app-release-unsigned.apk \
  dist/XenDroid-One-v0.1.0-arm64.apk
python3 tools/one/validate_apk.py dist/XenDroid-One-v0.1.0-arm64.apk \
  --previous dist/XenDroid-One-v0.1.0-rc1-arm64.apk \
  --expected-cert "$(cat docs/one/release-certificate.sha256)" \
  --output dist/validation.json
```

CI versionCodes are `100000 + run_number*2` and the next integer. This intentionally
places the first CI release above local 1001/1002. If workflows/repositories are
recreated or release numbering changes, audit the highest shipped code before
building. Retrying the same workflow is not a new release/versionCode. Keep all
future codes below Android's maximum and increasing globally.

Same source/dependency/toolchain inputs make the build repeatable; byte-for-byte
APK reproducibility was not established merely by building different versions.

## Device update test

`tools/one/device_update_test.sh FIRST.apk SECOND.apk` installs the first APK on a
clean test device and then uses `adb install -r` for the second. It never
uninstalls a pre-existing app. Optionally pass an existing game path for an
explicit launch. Inspect crash logs and output; successful package install alone
does not prove gameplay. No attached Android device or usable Android emulator
was available in this execution, so this install test was not run.
