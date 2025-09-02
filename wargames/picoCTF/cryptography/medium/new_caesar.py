import string
LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_encode(plain):
	enc = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		enc += ALPHABET[int(binary[:4], 2)]
		enc += ALPHABET[int(binary[4:], 2)]
	return enc

def b16_decode(ciphertext):
	dec = ""
	twochars = [ciphertext[i:i+2] for i in range(0,len(ciphertext),2)]
	for pairs in twochars:
		high_num = ALPHABET.index(pairs[0])
		low_num = ALPHABET.index(pairs[1])
		
		high_bin = "{0:04b}".format(high_num)
		low_bin = "{0:04b}".format(low_num)
		
		binary = high_bin + low_bin # string of 8 bits
		real_char = chr(int(binary,2))
		
		dec += real_char
	return dec

def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 + t2) % len(ALPHABET)]

def shift_back(ct, k):
    t1 = ALPHABET.index(ct)
    t2 = ALPHABET.index(k)
    return ALPHABET[(t1 - t2) % len(ALPHABET)]


ct = "apbopjbobpnjpjnmnnnmnlnbamnpnononpnaaaamnlnkapndnkncamnpapncnbannaapncndnlnpna"

for key in ALPHABET:
    dec = ""
    for i, char in enumerate(ct):
        dec += shift_back(char,key[i % len(key)])
    result = b16_decode(dec)
    print(result + "\n")