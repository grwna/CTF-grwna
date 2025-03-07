import hashlib
# Get dynamic part of key
hashed = hashlib.sha256(b"MORTON").hexdigest()
order = [4,5,3,6,2,7,1,8]
key_part_dynamic1_trial = "".join([hashed[i] for i in order])


key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_static2_trial = "}"
key_full_template_trial = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
print(key_full_template_trial)

# picoCTF{1n_7h3_|<3y_of_75fc1081}