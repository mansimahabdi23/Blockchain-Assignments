"""
Assignment 4: Simulate Transaction + Double-Spending Prevention
----------------------------------------------------------------
Goal:
- Simulate wallets and balances
- Perform a transaction
- Prevent double spending by rejecting overspend

Expected output:
- First transaction succeeds
- Second transaction fails if sender has insufficient balance
"""

from dataclasses import dataclass


@dataclass
class Wallet:
    name: str
    balance: float


class SimpleLedger:
    def __init__(self):
        self.transactions = []

    def transfer(self, sender: Wallet, receiver: Wallet, amount: float):
        # Double-spending prevention: sender cannot spend more than balance.
        if amount <= 0:
            print("Transaction rejected: amount must be positive.")
            return False

        if sender.balance < amount:
            print(
                f"Transaction rejected: {sender.name} has {sender.balance}, needs {amount}."
            )
            return False

        sender.balance -= amount
        receiver.balance += amount
        tx = {
            "from": sender.name,
            "to": receiver.name,
            "amount": amount,
        }
        self.transactions.append(tx)
        print(f"Transaction success: {sender.name} -> {receiver.name}, amount={amount}")
        return True

    def show_balances(self, wallets):
        print("Current Balances:")
        for w in wallets:
            print(f"  {w.name}: {w.balance}")


if __name__ == "__main__":
    alice = Wallet("Alice", 100)
    bob = Wallet("Bob", 20)

    ledger = SimpleLedger()

    ledger.show_balances([alice, bob])

    # Valid transaction
    ledger.transfer(alice, bob, 30)
    ledger.show_balances([alice, bob])

    # Attempted double-spend / overspend
    ledger.transfer(alice, bob, 1000)
    ledger.show_balances([alice, bob])