# -*- coding: utf-8 -*-#

from RsaEncryption import *
from RsaDecryption import *
import string, random


def generatePublicKeyPair():
    """Return public and private key tuple"""

    rsaEncryption = RsaEncryption()

    key_p = rsaEncryption.generateRandPrime()
    key_q = rsaEncryption.generateRandPrime()

    while key_q == key_p:
        key_q = rsaEncryption.generateRandPrime()

    if rsaEncryption.isPrime(key_p):
        pass
    else:
        print("ERROR: p is not prime. Please try again.")
        sys.exit(1)

    if rsaEncryption.isPrime(key_q):
        pass
    else:
        print("ERROR: q is not prime. Please try again.")
        sys.exit(1)

    # Calculate key n
    key_n = rsaEncryption.calculateN(key_p, key_q)

    # Calculate phi(n)
    phiN = rsaEncryption.totient(key_p, key_q)

    # Generate key e
    coPrimeList = []

    for i in range(1, phiN):
        if(rsaEncryption.isCoPrime([i, phiN])):
            coPrimeList.append(i)

    key_e = coPrimeList[random.randint(coPrimeList[0], len(coPrimeList)-1)]

    # Verify e is coprime to phiN
    if gcd(key_e, phiN) == 1:
        pass
    else:
        print("ERROR: E is not coprime. Please try again.")
        sys.exit(1)

    # Generate key d using Extended Euclidean algorithm
    _, key_d, _ = rsaEncryption.egcd(key_e, phiN)

    # ensure key e and d are distinct
    while key_e == key_d:
        _, key_d, _ = rsaEncryption.egcd(key_e, phiN)

    # ensure key d is positive
    if key_d < 0:
        key_d = key_d % phiN

    # verify d is coprime to phiN
    if gcd(key_d,phiN) == 1:
        pass
    else:
        print("ERROR: D is not coprime. Please try again.")
        sys.exit(1)

    # print("key_e ", key_e)
    # print("key_d", key_d)

    publicKey = (key_e, key_n)
    privateKey = (key_d, key_n)

    return (publicKey, privateKey)


def generateNonce(length=8):
    """ Returns a pseudorandom number between 0-9"""

    # https://github.com/joestump/python-oauth2/blob/81326a07d1936838d844690b468660452aafdea9/oauth2/__init__.py#L165

    # return random.randint(0,9)
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def sign_certificate(name, privateKey, totient):
    return pow(name, privateKey, totient)
