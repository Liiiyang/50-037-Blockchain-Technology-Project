from block import *
import random
import transaction
import json
import time

class Blockchain:

    difficulty = 2
    TARGET = '000ffffff'

    def __init__(self):
        self.transactionlist =[]
        self.chain =[]
        self.genesisBlock()

    def genesisBlock(self):
        genesis_block = Block(0,time.time(),0,10,0)
        genesis_block.hash = genesis_block.getHeaderInJSON()
        self.chain.append(genesis_block)
        print("Genesis: " + str(self.chain))
      
    @property
    def last_block(self):
        return self.chain[-1]

    def add(self, block, proof):
        print("Adding")
        previous_hash = self.last_block.hash

        if previous_hash != block.header["prevHeaderHash"]:
            print("1")
            return False

        if not self.validate(block, proof):
            print("2")
            return False

        block.hash = proof
        self.chain.append(block)
        print("3")
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
        print("Working..")
        random.seed()
        found = False
        foundNonce = ''
        while (found != True):
            print("Finding..")
            foundNonce = hashlib.sha256(str(random.randrange(2**256)).encode()).hexdigest()
            block.header["nonce"] = foundNonce
            blockWithNewNonce = block.getHeaderInJSON()
            if (blockWithNewNonce < Blockchain.TARGET):
                print("Found!")
                found = True
                return foundNonce
    
if __name__ == "__main__":
    with open("transaction_hash.json") as json_file:
        data=json.load(json_file)
    blockOne = Block(0,time.time(),0,10,data)
    bc = Blockchain()
    proof = bc.proof_of_work(blockOne)
    print(proof)
    bc.add(blockOne,proof)
    print("Total Chain: " + str(bc.chain))