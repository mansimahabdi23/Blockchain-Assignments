"""
Assignment 10: Small DApp Interaction using Python Web3 API
-----------------------------------------------------------
This script interacts with already deployed HelloWorld contract.
It reads current message and optionally updates message.

Required file: helloworld_deployment.json (from Assignment 5)
Required .env:
- RPC_URL
- PRIVATE_KEY
- ACCOUNT_ADDRESS
"""

import json
import os

from dotenv import load_dotenv
from web3 import Web3


if __name__ == "__main__":
    load_dotenv()

    rpc_url = os.getenv("RPC_URL")
    private_key = os.getenv("PRIVATE_KEY")
    account_address = os.getenv("ACCOUNT_ADDRESS")

    if not all([rpc_url, private_key, account_address]):
        raise ValueError("Missing .env values")

    with open("helloworld_deployment.json", "r", encoding="utf-8") as f:
        deployment = json.load(f)

    contract_address = deployment["address"]
    abi = deployment["abi"]

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Cannot connect to RPC")

    contract = web3.eth.contract(address=contract_address, abi=abi)

    current_msg = contract.functions.message().call()
    print("Current contract message:", current_msg)

    # Write transaction: update message.
    nonce = web3.eth.get_transaction_count(account_address)
    tx = contract.functions.setMessage("Hello from DApp client").build_transaction(
        {
            "from": account_address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": web3.eth.gas_price,
            "chainId": web3.eth.chain_id,
        }
    )

    signed = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)

    updated_msg = contract.functions.message().call()
    print("Updated contract message:", updated_msg)
