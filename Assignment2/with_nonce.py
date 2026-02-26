import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, file_hash, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.file_hash = file_hash
        self.previous_hash = previous_hash
        self.nonce = nonce  # The "counter" used for mining
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        # We now include the nonce in the hash calculation
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "file_hash": self.file_hash,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class FileBlockchain:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty # Number of leading zeros required
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # The first block also needs to be mined
        genesis = Block(0, time(), "Genesis block", "0")
        return self.mine_block(genesis)
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def mine_block(self, block):
        """Finds a hash that starts with the required number of zeros."""
        target = "0" * self.difficulty
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    def add_file_block(self, file_path):
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            new_block = Block(len(self.chain), time(), file_hash, self.get_latest_block().hash)
            
            print(f"Mining Block #{new_block.index}...")
            mined_block = self.mine_block(new_block)
            
            self.chain.append(mined_block)
            print(f"Success: Block added with Hash: {mined_block.hash[:20]}...")
        except FileNotFoundError:
            print("File not found.")

    def is_chain_valid(self):
        target = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            # Verify data hasn't changed
            if current.hash != current.calculate_hash(): return False
            # Verify the link
            if current.previous_hash != previous.hash: return False
            # Verify the Proof of Work was actually done
            if not current.hash.startswith(target): return False
        return True

# --- Execution ---
registry = FileBlockchain(difficulty=4)
registry.add_file_block("contract.txt")