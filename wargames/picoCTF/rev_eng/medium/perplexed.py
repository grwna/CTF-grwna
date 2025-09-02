huh = [0 for i in range(0x17)]
huh[0] = -0x1f
huh[1] = -0x59
huh[2] = 0x1e
huh[3] = -8
huh[4] = ord('u')
huh[5] = ord('#')
huh[6] = ord('{')
huh[7] = ord('a')
huh[8] = -0x47
huh[9] = -99
huh[10] = -4
huh[0xb] = ord('Z')
huh[0xc] = ord('[')
huh[0xd] = -0x21
huh[0xe] = ord('i')
huh[0xf] = -0x2e
huh[0x10] = -2
huh[0x11] = 0x1b
huh[0x12] = -0x13
huh[0x13] = -0xc
huh[0x14] = -0x13
huh[0x15] = ord('g')
huh[0x16] = -0xc

local20 = 0
correct = [0 for i in range(27)]
param_idx = 0
for i in range(0x17):
    for j in range(8):
        if local20 == 0:
            local20 = 1

        bit = (huh[i]) >> (7 - j) & 1
        correct[param_idx] |= (bit << (7 - local20))

        local20 += 1
        if local20 == 8:
            local20 = 0
            param_idx += 1
        if param_idx == 26:
            break 
        
print(''.join([chr(bit) for bit in correct]))