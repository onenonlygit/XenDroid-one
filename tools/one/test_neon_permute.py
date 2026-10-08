#!/usr/bin/env python3
"""Execute backported NEON forms against a PPC byte-order oracle.

Requires unicorn==2.1.4 and the pinned Android NDK. Tests instruction semantics,
not complete JIT register allocation, an Android process, or any game's speed.
"""
import os
from pathlib import Path
import random
import subprocess
import tempfile
from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM
import unicorn.arm64_const as regs

ndk = Path(os.environ['ANDROID_NDK_HOME'])
bin_dir = ndk/'toolchains/llvm/prebuilt/linux-x86_64/bin'
forms = {
    'vperm': 'movi v2.16b, #31\nand v2.16b, v6.16b, v2.16b\nrev32 v0.16b, v4.16b\nrev32 v1.16b, v5.16b\ntbl v8.16b, {v0.16b, v1.16b}, v2.16b',
    'vmrghb': 'rev32 v0.16b, v4.16b\nrev32 v1.16b, v5.16b\nzip1 v8.16b, v0.16b, v1.16b\nrev32 v8.16b, v8.16b',
    'vmrglb': 'rev32 v0.16b, v4.16b\nrev32 v1.16b, v5.16b\nzip2 v8.16b, v0.16b, v1.16b\nrev32 v8.16b, v8.16b',
    'vmrghh': 'zip1 v8.8h, v5.8h, v4.8h\nrev64 v8.4s, v8.4s',
    'vmrglh': 'zip2 v8.8h, v5.8h, v4.8h\nrev64 v8.4s, v8.4s',
    'vmrghw': 'zip1 v8.4s, v4.4s, v5.4s',
    'vmrglw': 'zip2 v8.4s, v4.4s, v5.4s',
}

def host_bytes(logical):
    return bytes(logical[i ^ 3] for i in range(16))

def oracle_merge(a, b, width, high):
    start = 0 if high else 8
    return bytes(x for i in range(start, start+8, width)
                 for piece in (a[i:i+width], b[i:i+width]) for x in piece)

rng = random.Random(0x454108CF)
count = 0
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    for name, asm in forms.items():
        (td/'form.s').write_text('.text\n'+asm+'\n')
        subprocess.run([str(bin_dir/'clang'), '--target=aarch64-linux-android29',
                        '-c', str(td/'form.s'), '-o', str(td/'form.o')], check=True)
        subprocess.run([str(bin_dir/'llvm-objcopy'), '-O', 'binary', '-j', '.text',
                        str(td/'form.o'), str(td/'form.bin')], check=True)
        code = (td/'form.bin').read_bytes()
        cpu = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
        cpu.mem_map(0x10000, 0x1000)
        cpu.mem_write(0x10000, code)
        for _ in range(1000):
            a = rng.randbytes(16)
            b = rng.randbytes(16)
            ctrl = rng.randbytes(16)
            cpu.reg_write(regs.UC_ARM64_REG_Q4, int.from_bytes(host_bytes(a), 'little'))
            cpu.reg_write(regs.UC_ARM64_REG_Q5, int.from_bytes(host_bytes(b), 'little'))
            cpu.reg_write(regs.UC_ARM64_REG_Q6, int.from_bytes(host_bytes(ctrl), 'little'))
            cpu.emu_start(0x10000, 0x10000+len(code))
            actual = cpu.reg_read(regs.UC_ARM64_REG_Q8).to_bytes(16, 'little')
            if name == 'vperm':
                table = a+b
                expected = bytes(table[x & 31] for x in ctrl)
            else:
                width = {'b': 1, 'h': 2, 'w': 4}[name[-1]]
                expected = oracle_merge(a, b, width, name.startswith('vmrgh'))
            assert actual == host_bytes(expected), (name, a.hex(), b.hex(), actual.hex(), expected.hex())
            count += 1
print(f'PASS: {count} randomized PPC-oracle/ARM64-NEON comparisons across {len(forms)} forms')
print('Not a full JIT, Android runtime, device or gameplay test.')
