expected = list(bytes.fromhex("072605220d2f2b2a080a16341737133311"))
print(len(expected))

temp = expected[6]
expected[6] = expected[9]
expected[9] = temp

# XOR with key 0x6644, basically if even ox66, if odd 0x44

for i in range(len(expected)):
    if i % 2:
        expected[i] = expected[i] ^ 0x44
    else:
        expected[i] = expected[i] ^ 0x66

expected.sort()

print(''.join([chr(char) for char in  expected]))