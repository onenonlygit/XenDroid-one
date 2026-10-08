#!/usr/bin/env python3
"""Initialize exact Android dependency gitlinks, excluding desktop/sample trees."""
import subprocess

excluded = {'DirectX-Headers', 'DirectXShaderCompiler', 'MoltenVK', 'SPIRV-Cross', 'wxWidgets'}
output = subprocess.check_output(['git', 'config', '-f', '.gitmodules', '--get-regexp', r'^submodule\..*\.path$'], text=True)
paths = [line.split(' ', 1)[1] for line in output.splitlines()]
paths = [p for p in paths if p.rsplit('/', 1)[-1] not in excluded]
subprocess.run(['git', 'submodule', 'update', '--init', '--jobs', '4', '--', *paths], check=True)
# boost_context/context and library dependencies required by libadrenotools
# are actual nested gitlinks; initialize them, without FidelityFX sample/media.
for p in paths:
    if p.endswith('/boost_context/context') or p.endswith('/libadrenotools'):
        subprocess.run(['git', '-C', p, 'submodule', 'update', '--init', '--recursive'], check=True)
