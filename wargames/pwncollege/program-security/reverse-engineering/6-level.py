text = "7a01cbd96caa6c03c30668be7d101b0d70"
text = list(bytes.fromhex(text))

temp = text[3]
text[3] = text[14]
text[14] = temp

for i in range(17):
    if i % 2:
        text[i] = text[i] ^ 0xe8
    else:
        text[i] = text[i] ^ 0x9c


for i in range(17):
    match i % 3:
        case 0:
            text[i] = text[i] ^ 0x89
        case 1:
            text[i] = text[i] ^ 0x9e
        case 2:
            text[i] = text[i] ^ 0x30

print(''.join([chr(char) for char in text ]))
# open('payload', "wb").write(flag)
