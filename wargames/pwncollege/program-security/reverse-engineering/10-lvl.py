# You should see 9-lvl.py for the explanation, this challenge is trivial if 9 is done
# However, somehow this challenge doesnt allow using ghidra(?)
# The offset is actually different in the workspace, so you need to use pwndbg (or smth else) to find it
# Offset is 1c38 

"""
For the stripped version, find the start of main, then find the offset based on that (it is not from 0x100000)
The offset is 232c
"""