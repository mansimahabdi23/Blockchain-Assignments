from math import gcd
import random

# (e,n ) is the public key
# (d,n ) is the private key 
# e is the encryption exponent, e should be coprime to phi and 1 < e < phi
# d is the decryption exponent, calculate d as multiplicative inverse of e mod phi, i.e. d*e mod phi = 1 

d, e, n = 0, 0, 0
p, q = 0, 0 
# p and q are the two prime numbers used to generate the keys
    
# n = p * q 
# phi = (p -1)*(q -1)

# file = open()

def mod_inverse(e, phi):
    for d in range(1, phi):
        if (d * e) % phi == 1:
            return d
    return None

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_keys():
    p = 17
    q = 11
    if not (is_prime(p) and is_prime(q)):
        print("Both numbers must be prime.")
        return None
    
    n = p * q
    phi = (p - 1) * (q - 1)

    #choosing e such that 1 < e < phi and gcd(e, phi) = 1
    e = 7
    while gcd(e, phi) != 1:
        e += 1
    
    #compute d 
    d = mod_inverse(e, phi)

    return ((e, n), (d, n))

#ecrypt a message using the public key
def encrypt(public_key, msg):
    e, n = public_key
    c = pow(msg, e, n) #pow(base, exp, mod=None) 
    return c 

#decrypt a message using private key

def decrypt(private_key, cipher_text):
    d, n = private_key
    m = pow(cipher_text, d, n)
    return m

if __name__ == "__main__":
    public_key, private_key  = generate_keys()
    print("Public Key:", public_key)
    print("Private Key:", private_key)
    msg = 123
    cipher_text = encrypt(public_key, msg)
    print("Encrypted Message:", cipher_text)
    decrypted_msg = decrypt(private_key, cipher_text)
    print("Decrypted Message:", decrypted_msg)

    #n = 187
    #e = 7
    #d = 23
    #phi = 160
    #msg = 123