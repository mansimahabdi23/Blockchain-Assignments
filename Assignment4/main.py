import time
import uuid

# -----------------------------
# Wallet Class
# -----------------------------
class Wallet:
    def __init__(self, initial_balance):
        self.address = str(uuid.uuid4())
        self.balance = initial_balance

# -----------------------------
# Transaction Class
# -----------------------------
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()

# -----------------------------
# Blockchain Simulation
# -----------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def get_balance(self, wallet):
        return wallet.balance

    def validate_transaction(self, tx):
        if tx.sender.balance >= tx.amount:
            return True
        return False

    def add_transaction(self, tx):
        if self.validate_transaction(tx):
            self.pending_transactions.append(tx)
            print(f"✅ Transaction Added: {tx.amount} from A to B")
        else:
            print(f"❌ Transaction Rejected: Insufficient Balance")

    def mine_block(self):
        print("\n⛏️ Mining Block...")
        
        for tx in self.pending_transactions:
            if tx.sender.balance >= tx.amount:
                tx.sender.balance -= tx.amount
                tx.receiver.balance += tx.amount
                self.chain.append(tx)
                print(f"Processed: {tx.amount}")
            else:
                print(f"Skipped (Double Spending Attempt): {tx.amount}")

        self.pending_transactions = []
        print("✅ Block Mined Successfully\n")

# -----------------------------
# Simulation
# -----------------------------
def simulate():
    # Create wallets
    walletA = Wallet(100)
    walletB = Wallet(50)

    blockchain = Blockchain()

    print("Initial Balances:")
    print(f"A: {walletA.balance}, B: {walletB.balance}\n")

    # Normal transaction
    tx1 = Transaction(walletA, walletB, 70)
    blockchain.add_transaction(tx1)
    blockchain.mine_block()

    print("Balances After First Transaction:")
    print(f"A: {walletA.balance}, B: {walletB.balance}\n")

    # Double spending attempt
    tx2 = Transaction(walletA, walletB, 50)
    tx3 = Transaction(walletA, walletB, 60)

    blockchain.add_transaction(tx2)
    blockchain.add_transaction(tx3)

    blockchain.mine_block()

    print("Final Balances:")
    print(f"A: {walletA.balance}, B: {walletB.balance}\n")

# Run simulation
simulate()