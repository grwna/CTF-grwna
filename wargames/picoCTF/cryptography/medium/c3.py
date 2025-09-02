# PART 1
lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

ct = "DLSeGAGDgBNJDQJDCFSFnRBIDjgHoDFCFtHDgJpiHtGDmMAQFnRBJKkBAsTMrsPSDDnEFCFtIbEDtDCIbFCFtHTJDKerFldbFObFCFtLBFkBAAAPFnRBJGEkerFlcPgKkImHnIlATJDKbTbFOkdNnsgbnJRMFnRBNAFkBAAAbrcbTKAkOgFpOgFpOpkBAAAAAAAiClFGIPFnRBaKliCgClFGtIBAAAAAAAOgGEkImHnIl"

prev = 0
flag = ""
for char in ct:
  cur = lookup2.index(char) # disini dipake cur sesudah - prev % 40
  cur = (cur + prev) % 40
  flag += lookup1[cur]
  prev = cur

print(flag)

# PART 2
b = 1 / 1

for i in range(len(flag)):
    if i == b * b * b:
      print(flag[i]) #prints
      b += 1 / 1
# picoCTF{adlibs}