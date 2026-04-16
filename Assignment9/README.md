# Assignment 9: PKI-Based Identity Infrastructure (Educational)

## 1. Objective
Build a very simple PKI-like identity flow:
- Create identity key pair
- Issue certificate from CA
- Verify certificate integrity

## 2. Theory
### Public Key Infrastructure (PKI)
PKI is a trust system based on:
- Public/private keys
- Certificate Authority (CA)
- Digital certificates

A certificate binds identity (person/service) to a public key.

### Real PKI vs This Assignment
Real PKI uses RSA/ECDSA signatures and X.509 certificates.
This assignment uses HMAC as a simplified signing model for easy understanding.

## 3. Practical Implementation
File: `pki_identity_infrastructure.py`
- `CertificateAuthority` class
  - signs certificate data
  - verifies certificate signature
- `generate_identity()`
  - creates toy private/public keys

## 4. Why This Is Used
PKI enables trusted identity in:
- HTTPS/TLS
- Enterprise authentication
- Blockchain identity layers

## 5. Output
Run:
```bash
python pki_identity_infrastructure.py
```
Expected output:
- generated user identity
- issued certificate package
- verification result (`True`)

## 6. Mathematical View
Signature check pattern:
- `sig = HMAC(secret, certificate_data)`
- valid if `sig == recomputed_sig`

## 7. Infrastructure Perspective
In real deployment, PKI infrastructure includes:
- Root CA
- Intermediate CAs
- Certificate repository
- Revocation mechanisms (CRL/OCSP)
- Policy and key rotation controls
