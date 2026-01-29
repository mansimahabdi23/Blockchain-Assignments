# Create a dummy contract file
contract_content = """
LEGAL AGREEMENT
Date: 2026-01-29
Parties: Alice and Bob
Subject: Transfer of Digital Assets

Alice agrees to transfer 10 units of Asset-X to Bob.
This agreement is final and recorded on the blockchain.
"""

with open("contract.txt", "w") as f:
    f.write(contract_content)

print("File 'contract.txt' created successfully!")