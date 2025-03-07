from PIL import Image
import numpy as np

# with open("scrambled1.png", "rb") as f:
#     img1 = f.read()
# with open("scrambled2.png", "rb") as f:
#     img2 = f.read()

# with open("flag.png", "wb") as f:
#     f.write(xor(img1,img2))

img1 = Image.open("scrambled1.png").convert("RGBA")
img2 = Image.open("scrambled2.png").convert("RGBA")

arr1 = np.array(img1)
arr2 = np.array(img2)

add_result = arr1 + arr2

flag = Image.fromarray(add_result)
flag.save("flag.png")