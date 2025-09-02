"""
Level 11.0
Carrying on from level 10, in this level you have to patch 2 bytes. One in the integrity check, then the license check
"""

"""
Level 11.1
This one is interesting, as the opcodes used is different.
In the integrity check, instead of a normal 75 2c JNZ, it uses 0f 85 dc. In order to patch this,
We can change it to 0f 80 dc, which is JO (jump on overflow). Since the TEST EAX, EAX statement before this
clears the overflow flag, this condition will always be met (JO always fails)
"""