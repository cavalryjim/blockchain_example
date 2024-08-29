import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = None

    def compute_hash(self):
        block_dict = self.__dict__
        if 'hash' in block_dict:
            del block_dict['hash']
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    difficulty = 2  # Proof of Work difficulty

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, None, str(datetime.now()), "Genesis Block", 0)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, new_hash):
        previous_hash = self.last_block().hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, new_hash):
            return False

        block.hash = new_hash
        
        self.chain.append(block)
        return True
    
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        
        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block()
        new_block = Block(index=last_block.index + 1,
                          previous_hash=last_block.hash,
                          timestamp=str(datetime.now()),
                          data=self.unconfirmed_transactions)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
    
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def check_chain_validity(self):
        result = True
        previous_hash = None

        for block in self.chain:
            if block.index == 0:
                previous_hash = block.hash
                continue 
                
            block_hash = block.hash

            if not self.is_valid_proof(block, block_hash) or previous_hash != block.previous_hash:
                result = False
                break
                
            previous_hash = block_hash

        return result


def example_usage():
    blockchain = Blockchain()
    blockchain.add_new_transaction("James earned 10 LSU_tokens")
    blockchain.mine()
    blockchain.add_new_transaction("James pays Mike_the_tiger 5 LSU_tokens")
    blockchain.mine()

    for block in blockchain.chain:
        print(f"Block {block.__dict__}")


    print("Blockchain valid?", blockchain.check_chain_validity())

example()