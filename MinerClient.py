'''
Reference:
	https://github.com/ethereum/wiki/wiki/White-Paper#ethereum-accounts
	http://docs.python-requests.org/en/master/user/quickstart/

 https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/

Design and implement a Miner class realizing miner's functionalities. Then, implement a simple simulator with miners running Nakamoto consensus and making transactions:

	1. Adjust the TARGET (global and static) parameter, such that on average new blocks arrive every 2-5 seconds.
	2. A miner who found a new block should be rewarded with 100 SUTDcoins.
	3. Introduce random transactions, such that miners (with coins) sends transactions to other miners.
	4. Make sure that coins cannot be double-spent.
		- consider the addr:balance model and the UTXO model. What are pros and cons?
		- do you need to modify (why, if so) the transaction format introduced in the first week? Hint: yes, you need.
	5. Extend the verification checks.
	6. Simulate miners competition.

'''


import requests
import json
# from requests.auth import HTTPBasicAuth
from transaction import Transaction
from ecdsa import SigningKey, VerifyingKey, NIST192p
import hashlib
import random
import pickle
from blockchain import *
from block import Block
import time


MINER_ADDR = [5000, 5010, 5020, 5030, 5040]

class Miner():
	   # TARGET = 5			# Set from 
    
    def __init__(self, myId):
        # HTTP GET Blockchain from other miners
        foundBlockchain = False
        for minerId in MINER_ADDR:
            if minerId == myId:
                continue
            r = requests.get('http://127.0.0.1:{}/read-blockchain'.format(minerId))
            if r.text != 'blockchain unavailable':
                foundBlockchain = True
                bc = pickle.loads(r.content)
                break
        if foundBlockchain == False:
            bc = Blockchain.new()
            f = file('./{}/blockchain'.format(myid),'wb')
            pickle.dump(bc,f)
            f.close()
            # Current Miner writes local. Other Miners read through network
            # r = requests.post('http://127.0.0.1:{}/update-blockchain'.format(myId), data=bc, headers={'Content-Type': 'application/octet-stream'})

        # Read my public & private keys
        vk = VerifyingKey.from_pem(open('vk_{}.pem'.format(myId)).read())
        sk = SigningKey.from_pem(open('sk_{}.pem'.format(myId)).read())
        sk_string = sk.to_string()

        self.blockchain = bc
        self.myId = myId


    def mine_block(self):
        currentBlockchain = self.blockchain         # Note: careful of reference or deepCopy
        currentLastBlock = self.blockchain.last_block
        otherMiners = list(filter(lambda x: x!=self.myId, MINER_ADDR))          # Filter myId from all Ids      

        isVerified = True
        while isVerified:
            # mining and listening???
            hasFound, newNonce, minerId = currentBlockchain.proof_of_work(currentLastBlock, otherMiners)
            if hasFound == True:
                # make new block
                # HTTP GET all transactions
                r = requests.get('http://127.0.0.1:{}/read-transactions'.format(self.myId))
                list_of_pending_tx = json.loads(r.json, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

                # Verify 
                self._validate_with_global_addrBal(list_of_pending_tx,currentBlockchain)
                # TODO: Create block
                newBlock = Block(time.time(),)
                currentBlockchain.add()
                # TODO: Post blockchain to server
                r = requests.post('http://127.0.0.1:{}/update-blockchain'.format(self.myId), data=)
            elif hasFound == False:
                # update block-to-mine
                # TODO: Get latest chain-of-blocks
                payload = { 'header': currentLastBlock['prevHeaderHash'] }
                r = requests.get('http://127.0.0.1:{}/read-blocks'.format(minerId), params=payload)
                list_of_newBlocks = pickle.loads(r.content)
                # TODO: Verify list_of_blocks with current miner's blockchain
                depth = len(list_of_newBlocks)
                for i in range(depth):
                    newBlock = list_of_newBlocks[depth-1-i]
                    prevBlock = list_of_newBlocks[depth-1-i-1]
                    if newBlock.prevHeaderHash != prevBlock.getHeaderInHash:
                        # If hashes not chained, then verification failed
                        print("Verification failed")
                        isVerified = False
                        break
                    if i == depth-1:
                        break
                # TODO: Update current blockchain
                currentLastBlock = list_of_newBlocks[depth-1]
                # Ref: http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
            else:
                print("Mining stopped")
                isVerified = False

        '''
        win
        '''

        currentLastBlock["nonce"] = newNonce
        # HTTP GET transactions
        r = requests.get('http://127.0.0.1:{}/get-transactions'.format(self.myId))
        msg = r.json()
        list_of_transactions = msg["Transactions"]

        # Add Reward
        newBlock = Block(time.time(), currentLastBlock.getHeaderInHash(), '', list_of_transactions)

        self.list_of_previous_balances = blockchain.latest_block.balance


    def _verify_block(self, block, previousBlock):
        validate = False
        # Check coinbase transaction
        coinbaseTx = block.transactions[len(block.transactions) - 1]
        if (coinbaseTx.sender == 'coinbase') and (coinbaseTx.amount == 100):
            validate = True
        else:
            return validate
        # Check if currentBlock["prevHeaderHash"] matches previousBlock.getHeaderInHash()
        # Check previousBlock.getHeaderInHash starts with leading zeroes
        if (previousBlock.getHeaderInHash() == block['prevHeaderHash'] and block['prevHeaderHash'].startswith('0'*Blockchain.difficulty) ):
            validate = True
        else:
            return validate
        return validate

    def _validate_with_global_addrBal(self, list_of_transactions, blockchain):
        current_addrBal = {}
        for tx in list_of_transactions:
            current_addrBal[tx.sender] -= tx.amount
            current_addrBal[tx.receiver] += tx.amount
        # init global addrBal
        global_addrBal = {}
        for block in blockchain:
            for tx in block.transaction_list:
                global_addrBal[tx.sender] -= tx.amount
                global_addrBal[tx.receiver] += tx.amount
        blacklist = []
        for addr in current_addrBal:
            if current_addrBal[addr] < 0:
                if (global_addrBal[addr] - current_addrBal[addr]) < 0:
                    # not enough coinsss
                    for tx in list_of_transactions:
                        if tx.sender == addr:
                            # reverse spender's transactions
                            # refund address balance
                            blacklist.append(addr)
                            current_addrBal[tx.sender] += tx.amount
                            current_addrBal[tx.receiver] -= tx.amount
                else:
                    # enough coinsss
                    pass
        # filter            
        final_list = list(filter(lambda x: x.sender not in blacklist, list_of_transactions))
        return final_list

    # 3. Introduce random transactions, such that miners (with coins) sends transactions to other miners.
    # TODO: Get miners public address
    # TODO: Fix POST transaction
    def share_coins_to_drive_economy(self):
        otherMiners = list(filter(lambda x: x!=self.myId, MINER_ADDR))          # Filter myId from all Ids      
        random.seed()
        luckyMiner = random.choice(otherMiners)
        amt = random.randint(0, 100)
        r = requests.post('http://127.0.0.1:{}/create-transaction'.format(luckyMiner))
        
        requests.post('http://127.0.0.1:{}/create-transaction'.format(myId), headers={'Content-type': 'application/json'})
        pass


new_tx = Transaction.new("you", "me", 5000, sk_string,"First Transaction")
hash_tx = hashlib.sha256(str(new_tx).encode()).hexdigest()
print(hash_tx)
data = {
       'Transaction'  : hash_tx,
    }
r = requests.post('http://127.0.0.1:5000/create-transaction', json=data)
print(r)

r = requests.get('http://127.0.0.1:5000/get-header')
print(r.text)

#while True:
#    r = requests.get('http://127.0.0.1:5000/mine')
#    currBlockHash = r.text
#    block = random.randrange(2**256)
#    str_block = str(block)
#    print("Finding Nonce.." + str_block)
#    if currBlockHash != str_block:
#        data = {
#            'mine'  : block,
#        }
#        r = requests.post('http://127.0.0.1:5000/mine', json=data)
#        print('Nonce Posted')
#    else:
#        block = random.randrange(2**256)
#        str_block = str(block)
#        print("Finding Another Nonce.." + str_block)

data = open("myObject", "rb").read()
r = requests.post('http://127.0.0.1:5000/mine', data=data,
                    headers={'Content-Type': 'application/octet-stream'})

r = requests.get('http://127.0.0.1:5000/mine/binary')
me = pickle.loads(r.content)
print(me.last_block.getHeaderInHash())

'''
Miner Behavior
'''


       
   
    
