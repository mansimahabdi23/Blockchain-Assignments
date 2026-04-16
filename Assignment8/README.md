# Assignment 8: Simple Proof-of-Work (PoW) Mining

## 1. Objective
Implement a small PoW miner that finds a nonce to satisfy a hash difficulty target.

## 2. Theory
### Proof-of-Work
Miner must find nonce so that block hash meets target condition:
- Hash starts with `d` leading zeros
- `d` is difficulty

Condition:
- `SHA256(block_data || nonce) < target`

In this simplified assignment, we check string-prefix zeros.

### Difficulty Effect
Expected trials scale exponentially with difficulty:
- Approx average tries \(\approx 16^d\) for hex leading zeros

## 3. Practical Implementation
File: `pow_mining.py`
- Builds block payload
- Iterates nonce from 0 upward
- Stops when hash prefix meets target

## 4. Why This Is Used
PoW makes block creation costly, helping prevent spam and attacks.

## 5. Expected Output
Run:
```bash
python pow_mining.py
```
You should see:
- nonce value
- valid hash
- mining duration

## 6. Mathematical Note
If hash behaves randomly, probability of one hash having `d` leading hex zeros:
- \(P = (1/16)^d\)

So expected attempts:
- \(E = 1/P = 16^d\)
