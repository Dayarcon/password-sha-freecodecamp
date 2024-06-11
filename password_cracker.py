import hashlib

def read_and_add_to_arr(file_name, arr):
    with open(file_name, "rb") as f:
        line = f.readline().strip()
        while line:
            arr.append(line)
            line = f.readline().strip()

def crack_sha1_hash(hash, use_salts=False):
    passwords_arr = []
    read_and_add_to_arr("top-10000-passwords.txt", passwords_arr)

    if use_salts:
        top_salt_passwords = {}
        top_salts = []
        read_and_add_to_arr("known-salts.txt", top_salts)

        for bsalt in top_salts:
            for bpassword in passwords_arr:
                prepended = hashlib.sha1(bsalt + bpassword).hexdigest()
                appended = hashlib.sha1(bpassword + bsalt).hexdigest()
                top_salt_passwords[prepended] = bpassword.decode("utf-8")
                top_salt_passwords[appended] = bpassword.decode("utf-8")
                
        if hash in top_salt_passwords:
            return top_salt_passwords[hash]

    password_dict = {}
    for p in passwords_arr:
        hash_line = hashlib.sha1(p).hexdigest()
        password_dict[hash_line] = p.decode("utf-8")

    if hash in password_dict:
        return password_dict[hash]

    return "PASSWORD NOT FOUND IN DATABASE"