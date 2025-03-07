with open("passwords.txt", "r") as f:
    passwords = [line.strip() for line in f]
with open("usernames.txt", "r") as f:
    usernames = [line.strip() for line in f]

print(passwords[usernames.index("cultiris")])