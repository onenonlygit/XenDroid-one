#!/usr/bin/env python3
"""Static release checks. Does not assert device installation or game support."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile
import zipfile

SYSTEM_LIBRARIES = {
    'libc.so', 'libm.so', 'libdl.so', 'liblog.so', 'libandroid.so',
    'libvulkan.so', 'libaaudio.so', 'libOpenSLES.so', 'libz.so',
    'libEGL.so', 'libGLESv2.so', 'libGLESv3.so', 'libjnigraphics.so',
    'libmediandk.so', 'libnativewindow.so',
}

def run(*args):
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT)

def inspect(apk, sdk, ndk, expected_cert=None):
    bt = sdk / 'build-tools/35.0.0'
    badging = run(str(bt/'aapt'), 'dump', 'badging', str(apk))
    package = re.search(r"package: name='([^']+)' versionCode='(\d+)' versionName='([^']+)'", badging)
    assert package, 'Missing APK identity'
    pkg, code, version = package.groups()
    assert pkg == 'xendroid.compose', pkg
    assert "application-label:'XenDroid One'" in badging, 'Wrong visible name'
    assert "native-code: 'arm64-v8a'" in badging, 'Wrong ABI set'
    manifest = run(str(bt/'aapt'), 'dump', 'xmltree', str(apk), 'AndroidManifest.xml')
    for required in ['xendroid.compose.MainActivity', 'xendroid.compose.EmulatorHostActivity',
                     'xendroid.intent.action.xendroid', 'android.intent.action.MAIN',
                     'android.intent.category.LAUNCHER', 'android.intent.action.VIEW']:
        assert required in manifest, f'Missing frontend contract: {required}'
    signature = run(str(bt/'apksigner'), 'verify', '--verbose', '--print-certs', str(apk))
    cert = re.search(r'Signer #1 certificate SHA-256 digest: ([0-9a-f]+)', signature).group(1)
    if expected_cert:
        assert cert == expected_cert.strip().lower().replace(':', ''), 'Unexpected signing identity'
    assert 'Verified using v2 scheme (APK Signature Scheme v2): true' in signature
    run(str(bt/'zipalign'), '-c', '4', str(apk))
    libs = {}
    readelf = ndk/'toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-readelf'
    with zipfile.ZipFile(apk) as z, tempfile.TemporaryDirectory() as td:
        native = [n for n in z.namelist() if n.startswith('lib/') and n.endswith('.so')]
        assert native, 'No native libraries'
        assert all(n.startswith('lib/arm64-v8a/') for n in native), 'Non-ARM64 binary'
        assert {'libe.so', 'libhardware_ProcessorInfo.so'} <= {Path(n).name for n in native}
        assert not any('libVkLayer_' in n or 'hwasan' in n for n in native), 'Diagnostic runtime bundled'
        for name in native:
            data = z.read(name)
            assert data[:4] == b'\x7fELF' and data[4:6] == b'\x02\x01', name
            assert struct.unpack_from('<H', data, 18)[0] == 183, f'Not AArch64: {name}'
            assert len(data) > 1024, f'Placeholder-sized library: {name}'
            path = Path(td)/Path(name).name
            path.write_bytes(data)
            dynamic = run(str(readelf), '-d', str(path))
            needed = re.findall(r'\(NEEDED\).*\[([^]]+)\]', dynamic)
            # PT_LOAD alignment, checked directly rather than parsing display spacing.
            phoff = struct.unpack_from('<Q', data, 32)[0]
            phentsize, phnum = struct.unpack_from('<HH', data, 54)
            for i in range(phnum):
                fields = struct.unpack_from('<IIQQQQQQ', data, phoff+i*phentsize)
                if fields[0] == 1:
                    assert fields[7] >= 16384, f'Not 16KB page compatible: {name}'
            libs[Path(name).name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'needed': needed}
        bundled = set(libs)
        for name, meta in libs.items():
            missing = set(meta['needed']) - bundled - SYSTEM_LIBRARIES
            assert not missing, f'{name} has missing runtime libraries: {missing}'
    return {'apk': str(apk), 'sha256': hashlib.sha256(apk.read_bytes()).hexdigest(),
            'package': pkg, 'version_code': int(code), 'version_name': version,
            'certificate_sha256': cert, 'libraries': libs,
            'verification': 'static only; no device installation or gameplay implied'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('apk', type=Path)
    p.add_argument('--previous', type=Path)
    p.add_argument('--sdk', type=Path, default=os.environ.get('ANDROID_SDK_ROOT'))
    p.add_argument('--ndk', type=Path)
    p.add_argument('--expected-cert')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    assert a.sdk, 'Supply --sdk or ANDROID_SDK_ROOT'
    ndk = a.ndk or a.sdk/'ndk/29.0.14206865'
    result = inspect(a.apk, a.sdk, ndk, a.expected_cert)
    if a.previous:
        previous = inspect(a.previous, a.sdk, ndk, result['certificate_sha256'])
        assert result['version_code'] > previous['version_code'], 'versionCode must increase'
        result['previous_apk'] = previous
        result['update_static_checks'] = 'same package and certificate; higher versionCode'
        result['update_install_test'] = 'not executed by this script'
    text = json.dumps(result, indent=2)
    if a.output:
        a.output.write_text(text+'\n')
    print(text)
