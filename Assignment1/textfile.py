# Block chain with file integrity using the followin scenario:
# Legal Document Registry where you need to prove that a specific contract wasn't tampered with after it was signed.

import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, file_hash, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.file_hash = file_hash
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate the hash of the block's contents."""
        block_string = json.dumps({
            "index" : self.index,
            "timestamp" : self.timestamp,
            "file_hash" : self.file_hash,
            "previous_hash" : self.previous_hash,
            "nonce":self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    

class FileBlockchain:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Create the genesis block."""
        return Block(0, time(), "Genesis block", "0")
    
    def get_latest_block(self):
        """Get the latest block in the chain."""
        return self.chain[-1]
    
    def  mine_block(self, block:Block) -> bool:
        target = "0" * self.difficulty
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    
    def add_file_block(self, file_path):
        """Reads a file, hashes it and adds a new block"""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
            
            new_block = Block(
                index=len(self.chain),
                timestamp=time(),
                file_hash=file_hash,
                previous_hash=self.get_latest_block().hash
            )

            print(f"Mining Block #{new_block.index}...")
            mined_block = self.mine_block(new_block)
            self.chain.append(mined_block)

            print(f"Success: Block added with Hash: {mined_block.hash[:20]}")
            # print(f": {mined_block.hash[:20]}")
            

            self.chain.append(new_block)
            print(f"Success: Block #{new_block.index} added for {file_path}")
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
    
    def is_chain_valid(self):
        target = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print(f"Alert: Block {current.index} has been tampered with")
                return False
            if current.previous_hash != previous.hash:
                print(f"Alert: Block {current.index} previous hash mismatch")
                return False
        return True

# 1. Initialize the Blockchain
my_registry = FileBlockchain(difficulty=4)

# 2. Add a text file to the blockchain 
my_registry.add_file_block("contract.txt")

# 3. View the Chain
for block in my_registry.chain:
    print(f"\nBlock {block.index} | Hash: {block.hash[:20]}")
    print(f"File Hash: {block.file_hash[:20]}")
    print(f"Prev Hash: {block.previous_hash[:20]}")
    # print(f"Timestamp:" {block.time})

print(f"Is blockchain valid? {my_registry.is_chain_valid()}")

print("\n--- Simulating the Tampering ---")
print("\n--- After Tampering!! ---")

my_registry.chain[1].file_hash = "fake_hash_value" 
for block in my_registry.chain:
    print(f"\nBlock {block.index} | Hash: {block.hash[:20]}")
    print(f"File Hash: {block.file_hash[:20]}")
    print(f"Prev Hash: {block.previous_hash[:20]}")

print(f"Is blockchain valid after tampering? {my_registry.is_chain_valid()}")

