expected = list(bytes.fromhex("7a 7a 7a 79 78 78 77 77 77 76 75 75 73 72 72 72 71 71 6f 6d 6d 6d 6d 6c 6c 69 69 69 68 68 67 66 66 64 65 63 62 61 61"))
l = len(expected)



temp = expected[33]
expected[33] = expected[34]
expected[34] = temp

expected.reverse()
expected.sort()
expected.reverse()

temp = expected[19]
expected[19] = expected[12]
expected[12] = temp

print(''.join([chr(i) for i in expected]))