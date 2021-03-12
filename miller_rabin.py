# Miller-Rabin prime test

import random


def prime_test(p):
    # Check base case
    if p % 2 == 0 or p < 3:
        return False

    m = p - 1
    k = 0

    # p - 1 = 2^k * m
    while m % 2 == 0:
        m = m // 2
        k += 1

    # Pick a random value to test Miller-Rabin with
    test_value = random.randrange(2, p - 2)
    x = pow(test_value, m, p)

    if x % p == 1 or x % p == p-1:
        return True

    for i in range(k):
        # Compute x^2 mod p
        x = pow(x, 2, p)
        if x == 1:
            return False
        if x == p-1:
            return True

    return False
