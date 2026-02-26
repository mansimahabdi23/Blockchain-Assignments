# Create a dummy contract file
contract_content = """
LEGAL AGREEMENT
Date: 2026-01-29
Parties: Alice and Bob
Subject: Transfer of Digital Assets

Alice agrees to transfer 10 units of Asset-X to Bob.
This agreement is final and recorded on the blockchain.
"""
# "appendix_A.txt": "APPENDIX A: List of involved stakeholders and technical specifications.",
# "terms_of_service.txt": "TERMS OF SERVICE: Usage is subject to the digital agreement dated 2026-02-05."
with open("contract.txt", "w") as f:
    f.write(contract_content)

print("File 'contract.txt' created successfully!")

