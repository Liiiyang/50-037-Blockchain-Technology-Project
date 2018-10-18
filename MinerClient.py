import requests
import json
# from requests.auth import HTTPBasicAuth
from transaction import Transaction
from ecdsa import SigningKey, VerifyingKey, NIST192p
import hashlib
import random
import pickle
from blockchain import Blockchain



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



       
   
    

