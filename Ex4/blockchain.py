from block import *
import random
# import transaction
import json
import time
import requests # A bit clunky OOP?

class Blockchain:

    difficulty = 2
    TARGET = '000ffffff'
    LISTEN_RATE = 5             # Higher number => Slower rate

    def __init__(self):
        self.chain =[]
        self.second_chain=[]
        self.fork = {}

    @classmethod
    def new(cls):
        genesis_block = Block(time.time(),0,10,['0','0'])
        myGenesisBlockHeaderHash = genesis_block.getHeaderInHash()
        bc = cls()
        bc.chain.append(genesis_block)
        bc.fork[myGenesisBlockHeaderHash] = bc.chain
        return bc

    @property
    def last_block(self):
        return self.chain[-1]

    def newAdd(self, newBlock, nonceToInsert, toFork=False, depthPosition=0):
        longestChain = self.resolve()
        if toFork:
            targetBlock = longestChain[-depthPosition]
            targetBlock.header["nonce"] = nonceToInsert        # replace current nonce with new nonce
            if self.validate(targetBlock, newBlock):
                newChain = longestChain[:-depthPosition]
                newChain.append(targetBlock)            # targetBlock with new nonce
                newChain.append(newBlock)
                proof_of_work = newBlock.header["prevHeaderHash"]   # Using proof_of_work as dictionary key
                self.fork[proof_of_work] = newChain
        elif toFork == False:
            targetBlock = self.last_block
            targetBlock.header["nonce"] = nonceToInsert
            if self.validate(targetBlock, newBlock):
                longestChain.append(newBlock)
                print("success!")
        else:
            print("toFork not defined")
        self.chain = longestChain

    def validate(self, targetBlock, newBlock):
        """
        Validate: Checks if the hash contains leading zeroes
        """
        proof_of_work = newBlock.header["prevHeaderHash"]
        return (proof_of_work.startswith('0' * Blockchain.difficulty) and proof_of_work == targetBlock.getHeaderInHash())
    
    def proof_of_work(self, block, list_of_otherMiners):
        '''
        Mining and listening if other miners have found a new block
        '''
        print("Working..")
        random.seed()
        found = False
        foundNonce = ''
        listenCounter = Blockchain.LISTEN_RATE
        while (found != True):
            # Mining
            print("Finding..")
            foundNonce = random.randrange(2**256)
            block.header["nonce"] = foundNonce          # TODO: Check if this needs to be a string
            blockHeaderHashWithNewNonce = block.getHeaderInHash()
            listenCounter -= 1
            if (blockHeaderHashWithNewNonce < Blockchain.TARGET) and blockHeaderHashWithNewNonce.startswith('0' * Blockchain.difficulty):
                print("Block: " + str(blockHeaderHashWithNewNonce))
                print("Found!")
                found = True
                return (True, foundNonce, blockHeaderHashWithNewNonce, 0)
            # Listening
            elif listenCounter == 0:
                if len(list_of_otherMiners) == 0:
                    pass
                else:
                    myHeight = len(self.chain)
                    for minerId in list_of_otherMiners:
                        # TODO: do this!
                        r = requests.get('http://127.0.0.1:{}/read-blockchain-height'.format(minerId))
                        if int(r.content) > myHeight:
                            return (False, 0, '', minerId)
                listenCounter = Blockchain.LISTEN_RATE


    def resolve(self):
        return max(self.fork.values(),key=len)

    

if __name__ == "__main__":
    with open("Ex1/transaction_hash.json") as json_file:
        data=json.load(json_file)
    bc = Blockchain.new()
    blockOne = Block(time.time(),bc.last_block.getHeaderInHash(),10,['123','456'])
    proof = bc.proof_of_work(blockOne)
    print(proof)
    bc.add(blockOne,proof,"No",0)

    blockTwo = Block(time.time(),bc.chain[-2].getHeaderInHash(),10,['abc','def'])
    proofTwo = bc.proof_of_work(blockTwo)
    print(proofTwo)
    bc.add(blockTwo,proofTwo,"Yes",2)

    print("Total Chain: " + str(bc.chain))
    print("Forks: " + str(bc.fork.values()))
    print("Resolve: " + str(bc.resolve()))
    

'''
## Week 2: SUTDcoin Blockchain Design v0.1

### Question 1
Design and implement `Blockchain` and `Block` classes. A `Blockchain` object
contains `Block` object(s). Each `Block` object has

- set of transactions that form a hash tree
- header that includes
    - hash of the previous header
    - root of the hash tree
    - timestamp (Unix timestamp expressed as an integer)
    - nonce (a random number needed to generate PoW)

Follow the same interface as in the `Transaction` class from the last week
(there is no signing, thus do not implement `sign()`.)
You need to implement `add()` to add a new block to the blockchain.
Hash of every new block's header should be less than `TARGET` (a global parameter,
set now to `00000fff...f`).

Test your implementation.
What checks have you implemented in `Blockchain`'s `validate()` ?


### Question 2

Introduce forks and their handling in your implementation.  Modify your
implementation, such that `add()` allows to anchor a new block to a given
arbitrary existing block.  Implement the `resolve()` method, that returns the
longest chain (e.g., it can return the latest block of the longest chain).  Test
your implementation.

'''