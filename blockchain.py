from block import *
import random
# import transaction
import json
import time

class Blockchain:

    difficulty = 2
    TARGET = '000ffffff'

    def __init__(self):
        self.transactionlist =[]
        self.chain =[]
        self.second_chain=[]
        self.fork = {}

    @classmethod
    def new(cls):
        genesis_block = Block(0,time.time(),0,10,0)
        myGenesisBlockHeaderHash = genesis_block.getHeaderInHash()
        bc = cls()
        bc.chain.append(genesis_block)
        bc.fork[myGenesisBlockHeaderHash] = bc.chain
        print("Genesis: " + str(bc.chain))
        return bc

    # def genesisBlock(self):
    #     genesis_block = Block(0,time.time(),0,10,0)
    #     # genesis_block.hash = genesis_block.getHeaderInHash()
    #     myGenesisBlockHeaderHash = genesis_block.getHeaderInHash()
    #     self.chain.append(genesis_block)
    #     self.fork[myGenesisBlockHeaderHash] = self.chain
    #     print("Genesis: " + str(self.chain))
    @property
    def last_block(self):
        return self.chain[-1]

    def add(self, block, proof, fork, position):
        print("Adding")
        if "Yes" in fork:
            if self.resolve()[-position]:
                previous_hash = self.resolve()[-position].getHeaderInHash()
                self.second_chain = self.resolve()[:-position+1]
                print("Prev: " + previous_hash)
                print("Current: " + str(block.header["prevHeaderHash"]))
                if previous_hash != block.header["prevHeaderHash"]:
                    print("1")
                    return False

                if not self.validate(block, proof):
                    print("2")
                    return False

                self.second_chain.append(block)
                self.fork[proof] = self.second_chain
            else:
                print("Invalid Block")
                return False

        elif "No" in fork and self.resolve(): 
            previous_hash = self.last_block.getHeaderInHash()
            print("Prev: " + previous_hash)
            print("Current: " + str(block.header["prevHeaderHash"]))
            if previous_hash != block.header["prevHeaderHash"]:
                print("1")
                return False

            if not self.validate(block, proof):
                print("2")
                return False

            self.chain.append(block)
            #self.fork[block.hash] = self.chain
            print("Block Added")
        return True

    def add_transactions(self, transaction):
        return self.transactionlist.append(transaction)

    def validate(self, block, block_hash):
        """
        Validate: Checks if the hash contains leading zeroes
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.getHeaderInHash())

    def proof_of_work(self, block):
        print("Working..")
        random.seed()
        found = False
        foundNonce = ''
        while (found != True):
            print("Finding..")
            block.header["nonce"] = random.randrange(2**256)
            foundNonce = hashlib.sha256(str(block.header["nonce"]).encode()).hexdigest()
            blockWithNewNonce = block.getHeaderInHash()
            if (blockWithNewNonce < Blockchain.TARGET) and blockWithNewNonce.startswith('0' * Blockchain.difficulty):
                print("Block: " + str(blockWithNewNonce))
                print("Found!")
                found = True
                return blockWithNewNonce

    def resolve(self):
        return max(self.fork.values(),key=len)

    

if __name__ == "__main__":
    with open("Ex1/transaction_hash.json") as json_file:
        data=json.load(json_file)
    bc = Blockchain.new()
    blockOne = Block(0,time.time(),bc.last_block.getHeaderInHash(),10,data)
    proof = bc.proof_of_work(blockOne)
    print(proof)
    bc.add(blockOne,proof,"No",0)

    blockTwo = Block(0,time.time(),bc.chain[-2].getHeaderInHash(),10,data)
    proofTwo = bc.proof_of_work(blockTwo)
    print(proofTwo)
    bc.add(blockTwo,proofTwo,"Yes",2)

    print("Total Chain: " + str(bc.chain))
    print("Forks: " + str(bc.fork.values()))
    print("Resolve: " + str(bc.resolve()))
    