# Key generation

import miller_rabin
import random


def prime_gen():
    prime = False
    # Upper and lower bounds of 31-bit
    low = 1073741824
    high = 2147483647
    while not prime:
        q = 2
        while not q % 12 == 5:
            q = random.randint(low, high)
        p = 2 * q + 1
        if miller_rabin.prime_test(p) == True:
            prime = True
    return p


def key_gen(seed):
    random.seed(seed)
    p = prime_gen()

    d = random.randint(1, p - 2)
    e1 = 2
    e2 = pow(e1, d, p)

    try:
        # Clear pubkey file and write in new information
        f = open('pubkey.txt', mode='w').close()
        f = open('pubkey.txt', mode='a')
        f.write(f'{p} {e1} {e2}')
        f.close()
    except:
        print('Failed to write public keys to pubkey.txt')

    try:
        # Clear prikey file and write in new information
        f = open('prikey.txt', mode='w').close()
        f = open('prikey.txt', mode='a')
        f.write(f'{p} {e1} {d}')
        f.close()
    except:
        print('Failed to write private keys to prikey.txt')

    return True
