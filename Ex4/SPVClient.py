'''
Reference:
	http://blog.luisrei.com/articles/flaskrest.html

'''

'''
Design and implement an SPVClient class. SPV clients should implement a simple 
SPV logic, i.e., they should:

	1. have their key pairs associated
	2. be able to receive block headers (not full blocks)
	3. be able to receive transactions (with their presence proofs) and verify them
	4. be able to send transactions

Integrate your implementation with your simulator from the previous exercise. Test your implementation.

'''

import requests
import json
# from requests.auth import HTTPBasicAuth
from transaction import Transaction
from ecdsa import SigningKey, VerifyingKey, NIST192p
import hashlib
import argparse
import pickle

vk = VerifyingKey.from_pem(open("vk.pem").read())
sk = SigningKey.from_pem(open("sk.pem").read())
sk_string = sk.to_string()

new_tx = Transaction.new("you", "me", 5000, sk_string,"First Transaction")
hash_tx = hashlib.sha256(str(new_tx).encode()).hexdigest()
print(hash_tx)

# Instantiate services
class SPVClient():
    def __init__(self,myid):
        path = "./"+ str(myid) + "/"
        vk = VerifyingKey.from_pem(open(path+"vk.pem").read())
        sk = SigningKey.from_pem(open(path+"sk.pem").read())

        sk_string = sk.to_string()
        vk_string = vk.to_string()
        self.verifyKey = vk_string
        self.signingKey = sk_string

           
    def getBlockHeader(self, MinerId, depth):
        return requests.get('http://127.0.0.1:{}/read-block-header'.format(MinerId), params={'depth': depth})
    
    def sendTransaction(self,MinerId,rcv,snd, amt, cmmt):
        new_tx = Transaction.new(rcv, snd, amt, self.signingKey, cmmt)
        tx_string = new_tx.to_json()
        data = {
            "Transaction" : tx_string
            }
        return requests.post('http://127.0.0.1:{}/create-transaction'.format(MinerId), json=data)

    def receiveTransactionASndProofs(self,MinerId,length,receiver):
        return requests.get('http://127.0.0.1:{}/read-tx-and-proof'.format(MinerId), params={'length': length, 'receiver': receiver})

# TODO: Local read private public keys

# TODO: Get all transactions and proofs
    
# TODO: Requests GET block headers

# TODO: While and await for commands (Send transactions)
# while

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', type=int, dest='id',
        help='Name of the folder for the keys')

    args = parser.parse_args()

    if args.id == None:
        print("Please enter the folder id")
    else:
        print(SPVClient(args.id).sendTransaction(5000,"you", "me", 5000,"First Transaction"))

        msg = SPVClient(args.id).receiveTransactionASndProofs(5000, 1, "5000").content
        msg = pickle.loads(msg)
        print(msg)

        msg1 = SPVClient(args.id).getBlockHeader(5000,0).content
        msg1 = pickle.loads(msg1)
        print(msg1)



