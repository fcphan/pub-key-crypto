import random
import key_gen


def encrypt(plaintext, pubkey):
    if(len(plaintext) % 4) != 0:
        pad = len(plaintext) % 4
        for p in range(0, 4 - pad):
            plaintext = plaintext + '.'

    blocks = [plaintext[i:i+4] for i in range(0, len(plaintext), 4)]
    ciphertext = []

    for i in range(0, len(blocks)):

        # format first block to int
        to_hex = ''.join(["{:02x}".format(ord(k)) for k in blocks[i]])
        to_int = int(to_hex, 16)

        c = encrypt_block(to_int, pubkey)
        ciphertext.append(c)

    return ciphertext


def encrypt_block(block, pubkey):
    # Set key parts
    p = pubkey['p']
    g = pubkey['g']
    e = pubkey['e2']

    k = random.randint(0, p - 1)
    c1 = pow(g, k, p)
    # ab mod m = (a mod m * b mod m ) mod m
    a = pow(e, k, p)
    b = block % p
    c2 = (a * b) % p
    cipher_pair = (c1, c2)

    return cipher_pair


def decrypt(ciphertext, key):
    plaintext = ''
    cipherblocks = []
    # Convert to integer cipher pairs
    for c in range(len(ciphertext) // 2):
        c1 = int(ciphertext[c*2+0])
        c2 = int(ciphertext[c*2+1])
        pair = [c1, c2]
        cipherblocks.append(pair)
    # Decrypt each block using private key
    for block in cipherblocks:
        m = decrypt_block(block, key)
        hblock = hex(m)[2:]
        text = bytes.fromhex(hblock).decode("utf-8")
        plaintext = plaintext + text
    return plaintext


def decrypt_block(cipher_pair, key):
    # Set key parts
    c1 = cipher_pair[0]
    c2 = cipher_pair[1]
    p = key['p']
    d = key['d']

    c1_mod_p = pow(c1, p-1-d, p)
    c2_mod_p = c2 % p
    m = (c1_mod_p * c2_mod_p) % p

    return m
