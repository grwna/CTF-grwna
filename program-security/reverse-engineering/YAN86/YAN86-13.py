import struct

global_buffer = [0 for _ in range (1000)]

def describe_register(register: int):
    byte = struct.pack("B", register)
    if byte == b'\x02': return 'a'
    elif byte == b'\x10': return 'b'
    elif byte == b'\x01': return 'c'
    elif byte == b' ': return 'd'
    elif byte == b'\b': return 's'
    elif byte == b'\x04': return 'i'
    elif byte == b'@': return 'f'
    elif byte == b'\x00': return "NONE"
    else: return b'?'

def write_register(offset, register: int, value):
    byte = struct.pack("B", register)
    if byte == b'\x02': global_buffer[offset + 0x100] = value
    elif byte == b'\x10': global_buffer[offset + 0x101] = value
    elif byte == b'\x01': global_buffer[offset + 0x102] = value
    elif byte == b' ': global_buffer[offset + 0x103] = value
    elif byte == b'\b': global_buffer[offset + 0x104] = value
    elif byte == b'\x04': global_buffer[offset + 0x105] = value
    elif byte == b'@': global_buffer[offset + 0x106] = value
    else : print("Unknown register", register); exit()

def read_register(offset: int, register: bytes):
    byte = struct.pack("B", register)
    if byte == b'\x02': value =  global_buffer[offset + 0x100]
    elif byte == b'\x10': value =  global_buffer[offset + 0x101]
    elif byte == b'\x01': value =  global_buffer[offset + 0x102]
    elif byte == b' ': value =  global_buffer[offset + 0x103]
    elif byte == b'\b': value =  global_buffer[offset + 0x104]
    elif byte == b'\x04': value =  global_buffer[offset + 0x105]
    elif byte == b'@': value =  global_buffer[offset + 0x106]
    else : print("Unknown register", register); exit()

    return value

def write_memory(offset, val1, val2):
      global_buffer[offset + val1] = val2

def interpret_imm(offset, register: bytes, value):
    register_char = describe_register(register)
    print(f"IMM {register_char} = {value}")
    write_register(offset, register, value)

def interpret_stm(offset, register1, register2):
    reg1 = describe_register(register1)
    reg2 = describe_register(register2)

    print(f"STM *{reg1} = {reg2}")

    read1 = read_register(offset, register1)
    read2 = read_register(offset, register2)

    write_memory(offset, read1, read2)

def interpret_add(offset, register1, register2):
    reg1 = describe_register(register1)
    reg2 = describe_register(register2)

    print(f"ADD {reg1} {reg2}")
    
    val1 = read_register(offset, register1)
    val2 = read_register(offset, register2)

    write_register(offset, register1, val1 + val2)

"""
Note: i am dumb
The point of these challenges are to do dynamic reverse engineering, not recoding the decompiled code lmaoooo
"""