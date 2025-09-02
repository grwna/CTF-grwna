expected = list(bytes.fromhex("9e6283936988966a8b966b958876968c72938f739f83789b867a"))
l = 26

for i in range(l):
    match i % 3:
        case 0:
            expected[i] = expected[i] ^ 0x67
        case 1:
            expected[i] = expected[i] ^ 0x2f
        case 2:
            expected[i] = expected[i] ^ 0x18

for i in range(l):
    match i % 3:
        case 0:
            expected[i] = expected[i] ^ 0xa2
        case 1:
            expected[i] = expected[i] ^ 0x16
        case 2:
            expected[i] = expected[i] ^ 0xc0

expected = expected[::-1]
expected = [x ^ 0x22 for x in expected]
expected.sort()

print(''.join([chr(i) for i in expected]))