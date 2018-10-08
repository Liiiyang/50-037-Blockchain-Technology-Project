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
        self.fork = {}
        self.genesisBlock()

    def genesisBlock(self):
        genesis_block = Block(0,time.time(),0,10,0)
        genesis_block.hash = genesis_block.getHeaderInJSON()       
        self.chain.append(genesis_block)
        print("Genesis: " + str(self.chain))
    
    @property
    def last_block(self):
        return self.chain[-1]

    def add(self, block, proof, fork):
        print("Adding")
        if "Yes" in fork and self.chain[-2]:
            previous_hash = self.chain[-2].hash
            self.second_chain = self.chain[:-2]
            if previous_hash != block.header["prevHeaderHash"]:
                print("1")
                return False

            if not self.validate(block, proof):
                print("2")
                return False

            block.hash = proof
            self.second_chain.append(block)
            self.fork[block.hash] = self.second_chain

        elif "No" in fork and resolve: 
            block.hash = proof
            previous_hash = self.last_block.hash
            print("Prev: " + previous_hash)
            print("Current: " + str(block.header["prevHeaderHash"]))
            if previous_hash != block.header["prevHeaderHash"]:
                print("1")
                return False

            if not self.validate(block, proof):
                print("2")
                return False

            block.hash = proof
            self.chain.append(block)
            self.fork[block.hash] = self.chain
            print("3")
        return True

    def add_transactions(self, transaction):
        return self.transactionlist.append(transaction)

    def validate(self, block, block_hash):
        """
        Validate: Checks if the hash contains leading zeroes
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.getHeaderInJSON())

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
            if (blockWithNewNonce < Blockchain.TARGET) and blockWithNewNonce.startswith('0' * Blockchain.difficulty):
                print("Block: " + str(blockWithNewNonce))
                print("Found!")
                found = True
                return blockWithNewNonce

    def resolve(self):
        return max(self.fork.values,key=len)

if __name__ == "__main__":
    with open("transaction_hash.json") as json_file:
        data=json.load(json_file)
    bc = Blockchain()
    blockOne = Block(0,time.time(),bc.last_block.hash,10,data)
    proof = bc.proof_of_work(blockOne)
    print(proof)
    bc.add(blockOne,proof,"No")
    print("Total Chain: " + str(bc.chain))