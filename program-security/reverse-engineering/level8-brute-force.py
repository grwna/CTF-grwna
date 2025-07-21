expectedtrue = list(bytes.fromhex("9dff3b3d0cf449f28aa9e13f31393f066dd343564d0a0050be2a3bc7c8eb3cce58a4cbe89c"))
l = len(expectedtrue)

# Flow (this process is reversed in this script)
# REVERSE
# REVERSE
# XOR with 7 bytes
# CONCAT
# REVERSE
# CONCAT
# XOR with 6 bytes 

for p in range(37):
    for j in range(37):
        for k in range(37):
            for z in range(37):
                expected = expectedtrue.copy()
                for i in range(l):
                    match i % 6:
                        case 0:
                            expected[i] = expected[i] ^ 0xf5
                        case 1:
                            expected[i] = expected[i] ^ 0x84
                        case 2:
                            expected[i] = expected[i] ^ 0xf7
                        case 3:
                            expected[i] = expected[i] ^ 99
                        case 4:
                            expected[i] = expected[i] ^ 0xa7
                        case 5:
                            expected[i] = expected[i] ^ 0x91

                var_18 = p
                var_20 = j
                var28 = k
                var27 = z

                temp = expected[var28]
                expected[var28] = expected[var_20]
                expected[var_20] = temp

                expected.reverse()

                temp = expected[var27]
                expected[var27] = expected[var_18]
                expected[var_18] = temp

                for i in range(l):
                    match i % 7:
                        case 0:
                            expected[i] = expected[i] ^ 0xf
                        case 1:
                            expected[i] = expected[i] ^ 3
                        case 2:
                            expected[i] = expected[i] ^ 0xd3
                        case 3:
                            expected[i] = expected[i] ^ 0xa0
                        case 4:
                            expected[i] = expected[i] ^ 0xc6
                        case 5:
                            expected[i] = expected[i] ^ 0x2c
                        case 6:
                            expected[i] = expected[i] ^ 0xaf

                if all(int(i) <= ord('z') and int(i) >= ord('a') for i in expected): 
                    print(f"p = {p}")
                    print(f"j = {j}")
                    print(f"k = {k}")
                    print(f"z = {z}")

                    print(''.join([chr(i) for i in expected]))
