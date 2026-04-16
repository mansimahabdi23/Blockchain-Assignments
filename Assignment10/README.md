# Assignment 10: Build a Small DApp Client (Web3 Python API)

## 1. Objective
Create a simple client application that interacts with a deployed smart contract.

## 2. Theory
A DApp has two parts:
- Smart contract (on blockchain)
- Client application (Web3.js/Web3.py)

Client operations:
- **Read call** (`call`) - no gas, no state change
- **Write transaction** (`send`) - costs gas, changes state

## 3. Practical Implementation
File: `dapp_interaction.py`
- Reads deployment info from `helloworld_deployment.json`
- Connects to RPC endpoint
- Calls `message()`
- Sends transaction to `setMessage()`
- Reads message again

## 4. Prerequisites
- Complete Assignment 5 (contract deployed)
- Have `helloworld_deployment.json`
- `.env` with RPC and wallet credentials

Install:
```bash
pip install web3 python-dotenv
```

## 5. Run
```bash
python dapp_interaction.py
```

## 6. Expected Output
- Current contract message
- Updated contract message after transaction

## 7. Why This Is Important
This is the core DApp pattern used in real projects:
- UI/Backend client calling contract ABI
- state read and update through wallet signing
