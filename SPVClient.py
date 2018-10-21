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

vk = VerifyingKey.from_pem(open("vk.pem").read())
sk = SigningKey.from_pem(open("sk.pem").read())
sk_string = sk.to_string()

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

r = requests.get('http://127.0.0.1:5000/mine')
print("Mining Results: " + r.text)

# Instantiate services
class SPVClient():
    def __init__(self):
        pass
	
    def getBlockHeader(self, ipAddr):
        pass
	
	def sendTransaction(self, )

# TODO: Local read private public keys

# TODO: Get all transactions and proofs with 

# TODO: Requests GET block headers

# TODO: While and await for commands (Send transactions)
# while