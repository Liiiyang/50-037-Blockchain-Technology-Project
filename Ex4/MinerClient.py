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
from Transaction import Transaction
from ecdsa import SigningKey, VerifyingKey, NIST192p
import hashlib
import random
import pickle
from blockchain import *
from block import Block
import time
from collections import namedtuple
import copy

MINER_PORT = [5000, 5010, 5020, 5030, 5040]
MINER_PORT = [5000, 5010]
# TODO: Read all miner's public key
MINER_PUBKEY = {}

class Miner():
	   # TARGET = 5			# Set from 
    
    def __init__(self, myId):
        # HTTP GET Blockchain from other miners
        foundBlockchain = False
        for minerId in MINER_PORT:
            if minerId == myId:
                continue
            r = requests.get('http://127.0.0.1:{}/read-blockchain'.format(minerId))
            if r.status_code != 202:
                foundBlockchain = True
                bc = pickle.loads(r.content)
                with open('./{}/blockchain'.format(myId), 'wb') as f:
                    pickle.dump(bc,f)
                # f = open('./{}/blockchain'.format(myId),'wb')       # Redundant code: consider using _update_blockchain instead
                # f.close()
                break
        if foundBlockchain == False:
            bc = Blockchain.new()
            with open('./{}/blockchain'.format(myId), 'wb') as f:
                pickle.dump(bc,f)
            # Current Miner writes local. Other Miners read through network
            # r = requests.post('http://127.0.0.1:{}/update-blockchain'.format(myId), data=bc, headers={'Content-Type': 'application/octet-stream'})

        # TODO: Read my public & private keys
        vk = VerifyingKey.from_pem(open('./{}/vk.pem'.format(myId)).read())
        sk = SigningKey.from_pem(open('./{}/sk.pem'.format(myId)).read())
        sk_string = sk.to_string()

        self.blockchain = bc
        self.myId = myId
        self.myPubKey = vk
        self.mySecretKey = sk_string

    def _update_blockchain(self, newBlockchain):
        with open('./{}/blockchain'.format(self.myId), 'wb') as f:
            pickle.dump(newBlockchain, f)



    def mine_block(self):
        currentBlockchain = copy.deepcopy(self.blockchain)         # Note: careful of reference or deepCopy
        currentLastBlock = copy.deepcopy(self.blockchain.last_block)
        otherMiners = list(filter(lambda x: x!=self.myId, MINER_PORT))          # Filter myId from all Ids      

        isVerified = True
        count = 0
        while isVerified:
            # mining and listening???
            count += 1
            hasFound, newNonce, prevHeaderHash, minerId = currentBlockchain.proof_of_work(currentLastBlock, otherMiners)
            if hasFound == True and count < 100:
                # make new block
                # HTTP GET all transactions
                print("success")
                r = requests.get('http://127.0.0.1:{}/read-transactions'.format(self.myId))
                r_ls = Transaction.from_json(r.text)["AllTransactions"]
                
                list_of_pending_tx = []
                list_of_pending_txObj = []
                for r_tx in r_ls:
                    # print(type(r_tx))
                    tx = Transaction.from_json(r_tx)
                    # tx = json.dumps(r_tx)
                    print(type(tx))
                    list_of_pending_tx.append(tx)
                    list_of_pending_txObj.append(r_tx)
                # print(list_of_pending_tx)
                # print(type(r_ls[0]))
                # print(type(list_of_pending_tx[0]))
                print(r_ls)
                # TODO: Verify 
                # self._validate_with_global_addrBal(list_of_pending_tx, currentBlockchain)
                self._validate_with_global_addrBal(list_of_pending_tx, currentBlockchain)
                # TODO: Create block
                # cTx = Transaction.new(self.myPubKey, 'coinbase', 100, self.mySecretKey)
                cTx = Transaction.new(str(self.myId), 'coinbase', 100, self.mySecretKey)
                cTx = cTx.to_json()
                # list_of_pending_tx.append(cTx)
                # newBlock = Block(time.time(), prevHeaderHash, newNonce, list_of_pending_tx)
                list_of_pending_tx.append(cTx)
                newBlock = Block(time.time(), prevHeaderHash, newNonce, list_of_pending_tx)
                currentBlockchain.newAdd(newBlock, newNonce)
                self._update_blockchain(currentBlockchain)
            elif hasFound == False:
                # update block-to-mine
                # TODO: Get latest chain-of-blocks
                currentLastBlockHeader = currentLastBlock.header['prevHeaderHash']
                payload = { 'header': currentLastBlockHeader }
                r = requests.get('http://127.0.0.1:{}/read-blocks-from-winner'.format(minerId), params=payload)
                list_of_newBlocks = pickle.loads(r.content)
                # TODO: Verify list_of_blocks with current miner's blockchain
                depth = len(list_of_newBlocks)
                for i in range(depth):
                    if i == (depth-1):
                        # print("YUPPPP")
                        resBlockchain = currentBlockchain.chain[:-1]
                        currentBlockchain.chain = resBlockchain + list_of_newBlocks
                        self._update_blockchain(currentBlockchain)
                        continue
                    prevBlock = list_of_newBlocks[i]
                    newBlock = list_of_newBlocks[i+1]      # [42]
                    if i == 0:
                        if currentLastBlock.header['prevHeaderHash'] != prevBlock.header['prevHeaderHash']:
                            # Current last block does not match with link block
                            print("Verification failed")
                            isVerified = False
                            break
                    if newBlock.header['prevHeaderHash'] != prevBlock.getHeaderInHash():
                        isVerified = False
                        break
            else:
                print("Mining stopped")
                isVerified = False


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
        # if len(blockchain.chain) < 5:
            # TODO: Control validation up to certain depth
        current_addrBal = {}
        print(len(list_of_transactions))
        for tx in list_of_transactions:
            print(type(tx))
            snd = tx["sender"]
            rcv = tx["receiver"]
            if snd not in current_addrBal:
                current_addrBal[snd] = 0
            if rcv not in current_addrBal:
                current_addrBal[rcv] = 0
            current_addrBal[snd] -= tx["amount"]
            current_addrBal[rcv] += tx["amount"]
        # init global addrBal
        global_addrBal = {}
        for block in blockchain.chain:
            for tx in block.transactions:
                snd = tx["sender"]
                rcv = tx["rcv"]
                if snd not in global_addrBal:
                    global_addrBal[snd] = 0
                if rcv not in global_addrBal:
                    global_addrBal[rcv] = 0
                global_addrBal[tx["sender"]] -= tx["amount"]
                global_addrBal[tx["receiver"]] += tx["amount"]
        blacklist = []
        # TODO: Handle coinbase
        for addr in current_addrBal:
            if current_addrBal[addr] < 0:
                if (global_addrBal[addr] - current_addrBal[addr]) < 0:
                    # not enough coinsss
                    for tx in list_of_transactions:
                        if tx.sender == addr:
                            # reverse spender's transactions
                            # refund address balance
                            blacklist.append(addr)
                            current_addrBal[tx["sender"]] += tx["amount"]
                            current_addrBal[tx["receiver"]] -= tx["amount"]
                else:
                    # enough coinsss
                    pass
        # filter            
        final_list = list(filter(lambda x: x.sender not in blacklist, list_of_transactions))
        return final_list, True

    # 3. Introduce random transactions, such that miners (with coins) sends transactions to other miners.
    # TODO: Fix POST transaction
    def share_coins_to_drive_economy(self):
        otherMiners = list(filter(lambda x: x!=self.myId, MINER_PORT))          # Filter myId from all Ids      
        random.seed()
        luckyMiner = random.choice(otherMiners)
        luckyMiner_pubkey = MINER_PUBKEY[str(luckyMiner)]
        amt = random.randint(0, 100)
        newTx = Transaction.new(luckyMiner_pubkey, self.myPubKey, amt, self.mySecretKey)
        newTxJSON = newTx.to_json()
        r = requests.post('http://127.0.0.1:{}/create-transaction'.format(luckyMiner),data=newTxJSON)
        
        requests.post('http://127.0.0.1:{}/create-transaction'.format(myId), headers={'Content-type': 'application/json'})
        pass



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

'''
Miner Behavior
'''
from argparse import ArgumentParser

parser = ArgumentParser()  
parser.add_argument('-H', '--host', default='127.0.0.1')  
parser.add_argument('-i', '--id', default=5000, type=int)
args = parser.parse_args()  

if __name__ == "__main__":
    m = Miner(args.id)
    m.mine_block()