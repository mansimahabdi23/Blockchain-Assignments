# Assignment 7: Analyze Bitcoin Block Structure + Compute Merkle Root

## 1. Objective
Understand Bitcoin block header fields and compute a Merkle root from sample transactions.

## 2. Theory
### Bitcoin Block Header Fields
- `version`
- `previous_block_hash`
- `merkle_root`
- `timestamp`
- `bits` (difficulty target in compact form)
- `nonce`

### Merkle Tree
A Merkle tree summarizes all transaction hashes efficiently.
- Leaf nodes: transaction IDs (`txid`)
- Internal node: double SHA256(left || right)
- Root: one final hash that commits all transactions

If odd number of leaves, duplicate last leaf.

## 3. Mathematical Expression
For two child hashes `h1`, `h2`:
- `parent = SHA256(SHA256(h1 || h2))`

## 4. Practical Implementation
File: `bitcoin_merkle_analysis.py`
- Creates sample txids
- Builds Merkle tree iteratively
- Prints root and simplified block header

## 5. Why This Is Useful
Merkle root allows:
- Efficient verification (SPV)
- Proof of inclusion with Merkle proof
- Compact commitment of many transactions

## 6. Expected Output
Run:
```bash
python bitcoin_merkle_analysis.py
```
Output includes:
- Block header values
- Sample transaction hashes
- Final Merkle root
