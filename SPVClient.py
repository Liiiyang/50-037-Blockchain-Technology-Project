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

