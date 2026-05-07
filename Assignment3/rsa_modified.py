"""
RSA Digital Wallet Simulator
------------------------------
Covers:
  1. Generating a pool of random prime candidates
  2. Selecting p and q from that pool
  3. Deriving public (e, n) and private (d, n) keys from scratch
  4. Signing & verifying messages
  5. Encrypting & decrypting numbers
"""

import random
import math


# ─── 1. Prime utilities ──────────────────────────────────────────────────────

def is_prime(n: int) -> bool:
    """Check primality by trial division."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_prime_pool(count: int = 16, low: int = 11, high: int = 100) -> list[int]:
    """Return `count` distinct random primes in [low, high]."""
    candidates = [n for n in range(low, high + 1) if is_prime(n)]
    if len(candidates) < count:
        raise ValueError(f"Not enough primes in [{low}, {high}] to fill a pool of {count}.")
    return sorted(random.sample(candidates, count))


# ─── 2. RSA math helpers ─────────────────────────────────────────────────────

def gcd(a: int, b: int) -> int:
    return math.gcd(a, b)


def mod_inverse(e: int, phi: int) -> int:
    """Extended Euclidean Algorithm — returns d such that (e * d) % phi == 1."""
    old_r, r = e, phi
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    if old_r != 1:
        raise ValueError("e and phi are not coprime — no modular inverse exists.")
    return (old_s % phi + phi) % phi


def mod_pow(base: int, exp: int, mod: int) -> int:
    """Fast modular exponentiation using Python's built-in pow."""
    return pow(base, exp, mod)


# ─── 3. Key generation ───────────────────────────────────────────────────────

def generate_keypair(p: int, q: int) -> dict:
    """
    Derive RSA public and private keys from two primes p and q.

    Returns a dict with:
        n, phi, e, d, public_key, private_key
    """
    if p == q:
        raise ValueError("p and q must be distinct primes.")
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both p and q must be prime.")

    n   = p * q
    phi = (p - 1) * (q - 1)

    # Find smallest e that is coprime with phi and 1 < e < phi
    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 2

    d = mod_inverse(e, phi)

    return {
        "p":           p,
        "q":           q,
        "n":           n,
        "phi":         phi,
        "e":           e,
        "d":           d,
        "public_key":  (e, n),
        "private_key": (d, n),
    }


# ─── 4. Sign / Verify ────────────────────────────────────────────────────────

def sign(message: int, private_key: tuple) -> int:
    """
    Sign a numeric message with the private key.
    signature = message^d mod n
    """
    d, n = private_key
    if not (0 < message < n):
        raise ValueError(f"Message must satisfy 0 < message < {n}.")
    return mod_pow(message, d, n)


def verify(signature: int, original_message: int, public_key: tuple) -> bool:
    """
    Verify a signature against the original message using the public key.
    recovered = signature^e mod n  →  must equal original_message
    """
    e, n = public_key
    recovered = mod_pow(signature, e, n)
    return recovered == original_message


# ─── 5. Encrypt / Decrypt ────────────────────────────────────────────────────

def encrypt(plaintext: int, public_key: tuple) -> int:
    """
    Encrypt a number with the public key.
    ciphertext = plaintext^e mod n
    """
    e, n = public_key
    if not (0 < plaintext < n):
        raise ValueError(f"Plaintext must satisfy 0 < plaintext < {n}.")
    return mod_pow(plaintext, e, n)


def decrypt(ciphertext: int, private_key: tuple) -> int:
    """
    Decrypt a ciphertext with the private key.
    plaintext = ciphertext^d mod n
    """
    d, n = private_key
    return mod_pow(ciphertext, d, n)


# ─── 6. Pretty printing helpers ──────────────────────────────────────────────

def print_section(title: str):
    width = 55
    print("\n" + "─" * width)
    print(f"  {title}")
    print("─" * width)


def print_prime_pool(pool: list[int]):
    print_section("Prime pool (pick one p and one q)")
    row = ""
    for i, p in enumerate(pool):
        row += f"  {p:>4}"
        if (i + 1) % 8 == 0:
            print(row)
            row = ""
    if row:
        print(row)


def print_keypair(keys: dict):
    print_section("RSA key derivation")
    print(f"  p              = {keys['p']}")
    print(f"  q              = {keys['q']}")
    print(f"  n  = p × q     = {keys['n']}")
    print(f"  φ(n)= (p-1)(q-1)= {keys['phi']}")
    print(f"  e  (public exp) = {keys['e']}")
    print(f"  d  (private exp)= {keys['d']}")
    print()
    print(f"  ✦ Public  key  → (e={keys['e']},  n={keys['n']})")
    print(f"  ✦ Private key  → (d={keys['d']},  n={keys['n']})")


# ─── 7. Demo ─────────────────────────────────────────────────────────────────

def main():
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║          RSA Digital Wallet Simulator                ║")
    print("╚══════════════════════════════════════════════════════╝")

    # Step 1 — Generate pool
    pool = generate_prime_pool(count=16, low=11, high=100)
    print_prime_pool(pool)

    # Step 2 — Pick p and q from the pool
    # (Selecting indices 0 and 5 as an example — change freely)
    p = pool[0]
    q = pool[5]
    print(f"\n  Selected  →  p = {p},  q = {q}")

    # Step 3 — Derive keys
    keys = generate_keypair(p, q)
    print_keypair(keys)

    pub  = keys["public_key"]   # (e, n)
    priv = keys["private_key"]  # (d, n)

    # ── Sign & Verify ──────────────────────────────────────────
    print_section("Digital wallet — sign & verify")
    message = 42
    if message >= keys["n"]:
        message = keys["n"] - 1          # keep it in valid range

    print(f"  Original message : {message}")
    signature = sign(message, priv)
    print(f"  Signature        : {signature}   (msg^d mod n)")

    valid = verify(signature, message, pub)
    print(f"  Verification     : {'✓ VALID — signature matches' if valid else '✗ INVALID'}")

    # Tamper test
    print()
    tampered = message + 1
    tampered_valid = verify(signature, tampered, pub)
    print(f"  Tampered message : {tampered}")
    print(f"  Tamper check     : {'✓ VALID' if tampered_valid else '✗ INVALID — tampering detected'}")

    # ── Encrypt & Decrypt ─────────────────────────────────────
    print_section("Encrypt & decrypt")
    plaintext = 7
    if plaintext >= keys["n"]:
        plaintext = keys["n"] - 1

    print(f"  Plaintext        : {plaintext}")
    ciphertext = encrypt(plaintext, pub)
    print(f"  Ciphertext       : {ciphertext}   (msg^e mod n)")
    recovered  = decrypt(ciphertext, priv)
    print(f"  Decrypted        : {recovered}")
    print(f"  Round-trip OK    : {'✓ Yes' if recovered == plaintext else '✗ No'}")

    # ── Interactive mode ──────────────────────────────────────
    print_section("Try it yourself")
    print("  Enter any number to sign/verify and encrypt/decrypt.")
    print(f"  (Must be between 1 and {keys['n'] - 1})\n")

    try:
        user_msg = int(input(f"  Enter a number (1–{keys['n'] - 1}): ").strip())
        if not (1 <= user_msg < keys["n"]):
            print(f"  ✗ Out of range. Using {keys['n'] - 2} instead.")
            user_msg = keys["n"] - 2

        sig2 = sign(user_msg, priv)
        print(f"\n  Signed           : {sig2}")
        print(f"  Verified         : {'✓ VALID' if verify(sig2, user_msg, pub) else '✗ INVALID'}")

        ct2  = encrypt(user_msg, pub)
        pt2  = decrypt(ct2, priv)
        print(f"  Encrypted        : {ct2}")
        print(f"  Decrypted back   : {pt2}  {'✓' if pt2 == user_msg else '✗'}")

    except (ValueError, EOFError):
        print("  (Skipping interactive input — not running in a terminal.)")

    print("\n" + "─" * 55 + "\n")


if __name__ == "__main__":
    main()