# RSA Digital Wallet Simulation
# This program:
# 1. Generates RSA public and private keys
# 2. Simulates a simple digital wallet
# 3. Encrypts and decrypts a message

import random
from math import gcd

# -----------------------------
# Step 1: Generate Prime Numbers
# -----------------------------

# List of small prime numbers
prime_numbers = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# Randomly choose two different prime numbers
p = random.choice(prime_numbers)
q = random.choice(prime_numbers)

while p == q:
    q = random.choice(prime_numbers)

print("Selected Prime Numbers:")
print("p =", p)
print("q =", q)

# -----------------------------
# Step 2: Calculate n and phi(n)
# -----------------------------

n = p * q
phi = (p - 1) * (q - 1)

print("\nCalculated Values:")
print("n =", n)
print("phi(n) =", phi)

# -----------------------------
# Step 3: Choose Public Key 'e'
# -----------------------------

# Choose e such that:
# 1 < e < phi
# gcd(e, phi) = 1

e = random.randrange(2, phi)

while gcd(e, phi) != 1:
    e = random.randrange(2, phi)

print("\nPublic Key Exponent:")
print("e =", e)

# -----------------------------
# Step 4: Generate Private Key 'd'
# -----------------------------

# d is modular inverse of e
# (d * e) % phi = 1

def mod_inverse(e, phi):
    for d in range(1, phi):
        if (d * e) % phi == 1:
            return d

d = mod_inverse(e, phi)

print("\nPrivate Key Exponent:")
print("d =", d)

# -----------------------------
# Step 5: Public and Private Keys
# -----------------------------

public_key = (e, n)
private_key = (d, n)

print("\nGenerated RSA Keys")
print("Public Key  =", public_key)
print("Private Key =", private_key)

# -----------------------------
# Step 6: Simulate Digital Wallet
# -----------------------------

wallet = {
    "Owner": "Mansi",
    "Wallet_ID": random.randint(1000, 9999),
    "Public_Key": public_key,
    "Private_Key": private_key
}

print("\n----- Digital Wallet -----")
for key, value in wallet.items():
    print(key, ":", value)

# -----------------------------
# Step 7: Encryption
# -----------------------------

message = int(input("\nEnter numeric message to encrypt: "))

# Encryption Formula:
# cipher = (message ^ e) % n

cipher = pow(message, e, n)

print("Encrypted Message:", cipher)

# -----------------------------
# Step 8: Decryption
# -----------------------------

# Decryption Formula:
# original = (cipher ^ d) % n

decrypted_message = pow(cipher, d, n)

print("Decrypted Message:", decrypted_message)