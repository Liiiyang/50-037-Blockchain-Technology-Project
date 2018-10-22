from ecdsa import SigningKey, VerifyingKey, NIST192p
import requests
from Transaction import Transaction
import json
# Generate keys
# sk = SigningKey.generate(curve=NIST192p)
# vk = sk.get_verifying_key()
# open("sk.pem","wb").write(sk.to_pem())
# open("vk.pem","wb").write(vk.to_pem())

'''
Test if create-transaction can be saved in json file
'''

vk = VerifyingKey.from_pem(open("vk.pem").read())
sk = SigningKey.from_pem(open("sk.pem").read())

rcv = 'Bob'
snd = 'Alice'
amt = 1
sk_string = sk.to_string()

myTx = Transaction.new(rcv, snd, amt, sk_string)
myTxJSON = myTx.to_json()
print(myTxJSON)

myId = 5000
# headers = {'Content-type': 'text/plain'}
headers = {'Content-type': 'application/json'} 
# requests.post('http://127.0.0.1:{}/create-transaction'.format(myId), json=myTxJSON ,headers=headers)

'''
Test if 
'''
r = requests.get('http://127.0.0.1:{}/read-transactions'.format(myId))
msg = Transaction.from_json(r.content)
print(r.content)
# print(msg)
# print(msg["AllTransactions"])
