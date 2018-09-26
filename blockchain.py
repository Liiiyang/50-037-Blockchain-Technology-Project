import block
import random
import transaction
import sk

class Blockchain:

    difficulty = 2

    def __init__(self):
        self.transactionlist =[]
        self.chain =[]
        self.genesisBlock()

    def genesisBlock(self):
        genesis_block = block.Block(0,time.time(),0,"0")
        genesis_block.hash = genesis_block.get_block_hash()
        self.chain.append(genesis_block)
      
    @property
    def last_block(self):
        return self.chain[-1]

    def add(self, block, proof):
        previous_hash = self.last_block.hash

        if previous_hash != block.prevhash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def add_transactions(self, transaction):
        return self.transactionlist.append(transaction)

    def validate(self, block, block_hash):
        """
        Validate: Checks if the hash contains leading zeroes
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash
    
    def start():
        return None

if __name__ == "__main__":
    start()