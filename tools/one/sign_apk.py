#!/usr/bin/env python3
"""Sign with an existing owner-controlled key; never generates or prints secrets."""
import argparse
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('unsigned', type=Path)
p.add_argument('output', type=Path)
p.add_argument('--sdk', type=Path, default=os.environ.get('ANDROID_SDK_ROOT'))
a = p.parse_args()
for key in ['XONE_KEYSTORE', 'XONE_KEY_ALIAS', 'XONE_STORE_PASSWORD', 'XONE_KEY_PASSWORD']:
    if not os.environ.get(key):
        raise SystemExit(f'{key} must be configured; release signing cannot fall back to a debug key')
bt = a.sdk/'build-tools/35.0.0'
a.output.parent.mkdir(parents=True, exist_ok=True)
aligned = a.output.with_suffix('.aligned.apk')
try:
    subprocess.run([str(bt/'zipalign'), '-f', '4', str(a.unsigned), str(aligned)], check=True)
    subprocess.run([str(bt/'apksigner'), 'sign', '--ks', os.environ['XONE_KEYSTORE'],
        '--ks-key-alias', os.environ['XONE_KEY_ALIAS'], '--ks-pass', 'env:XONE_STORE_PASSWORD',
        '--key-pass', 'env:XONE_KEY_PASSWORD', '--v4-signing-enabled', 'false',
        '--out', str(a.output), str(aligned)], check=True)
    subprocess.run([str(bt/'apksigner'), 'verify', '--verbose', '--print-certs', str(a.output)], check=True)
finally:
    aligned.unlink(missing_ok=True)
