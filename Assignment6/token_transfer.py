"""
Assignment 6: Deploy and Transfer Simple Tokens (Solidity + Python)
--------------------------------------------------------------------
This script:
1. Compiles/deploys SimpleToken.sol
2. Transfers tokens from deployer to receiver account
3. Reads balances before and after

Setup:
- pip install web3 py-solc-x python-dotenv
- .env values:
  RPC_URL
  PRIVATE_KEY
  ACCOUNT_ADDRESS
  RECEIVER_ADDRESS
"""

import os

from dotenv import load_dotenv
from solcx import compile_standard, install_solc
from web3 import Web3


def compile_contract(source_file, contract_name):
    with open(source_file, "r", encoding="utf-8") as f:
        source = f.read()

    install_solc("0.8.20")
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {source_file: {"content": source}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "evm.bytecode"]}
                }
            },
        },
        solc_version="0.8.20",
    )

    data = compiled["contracts"][source_file][contract_name]
    return data["abi"], data["evm"]["bytecode"]["object"]


if __name__ == "__main__":
    load_dotenv()

    rpc_url = os.getenv("RPC_URL")
    private_key = os.getenv("PRIVATE_KEY")
    account_address = os.getenv("ACCOUNT_ADDRESS")
    receiver_address = os.getenv("RECEIVER_ADDRESS")

    if not all([rpc_url, private_key, account_address, receiver_address]):
        raise ValueError("Missing env values. Check RPC_URL, PRIVATE_KEY, ACCOUNT_ADDRESS, RECEIVER_ADDRESS")

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Web3 connection failed")

    abi, bytecode = compile_contract("SimpleToken.sol", "SimpleToken")
    token_contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = web3.eth.get_transaction_count(account_address)
    initial_supply = 1000

    deploy_tx = token_contract.constructor(initial_supply).build_transaction(
        {
            "from": account_address,
            "nonce": nonce,
            "gas": 1000000,
            "gasPrice": web3.eth.gas_price,
            "chainId": web3.eth.chain_id,
        }
    )

    signed_deploy = web3.eth.account.sign_transaction(deploy_tx, private_key)
    deploy_hash = web3.eth.send_raw_transaction(signed_deploy.raw_transaction)
    deploy_receipt = web3.eth.wait_for_transaction_receipt(deploy_hash)

    token = web3.eth.contract(address=deploy_receipt.contractAddress, abi=abi)
    print("Token deployed at:", deploy_receipt.contractAddress)

    sender_before = token.functions.balanceOf(account_address).call()
    receiver_before = token.functions.balanceOf(receiver_address).call()
    print("Before transfer -> sender:", sender_before, ", receiver:", receiver_before)

    nonce += 1
    transfer_amount = 150
    transfer_tx = token.functions.transfer(receiver_address, transfer_amount).build_transaction(
        {
            "from": account_address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": web3.eth.gas_price,
            "chainId": web3.eth.chain_id,
        }
    )

    signed_transfer = web3.eth.account.sign_transaction(transfer_tx, private_key)
    transfer_hash = web3.eth.send_raw_transaction(signed_transfer.raw_transaction)
    web3.eth.wait_for_transaction_receipt(transfer_hash)

    sender_after = token.functions.balanceOf(account_address).call()
    receiver_after = token.functions.balanceOf(receiver_address).call()
    print("After transfer  -> sender:", sender_after, ", receiver:", receiver_after)
