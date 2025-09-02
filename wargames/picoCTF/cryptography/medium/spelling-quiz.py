import random

alphabet = list('abcdefghijklmnopqrstuvwxyz')
word = list(open("study-guide.txt").readline())[:-1]


    
# use https://www.dcode.fr/monoalphabetic-substitution to bruteforce
# possible keys

# i got SPRGWHKZOJQLDCUVYEMNBTIAFX
key = "XUNMRYDFWHGLSTIBJCAVOPEZQK"
offset = ord('a') - ord('A')
key = [chr(ord(i) + offset) for i in key]

dictionary = dict(zip(key,alphabet))

enc = open("flag.txt").read().strip()
flag = "".join([dictionary[i] if i in dictionary else i for i in enc])
print(f"picoCTF{{{flag}}}")



