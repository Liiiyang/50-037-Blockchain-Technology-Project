from ecdsa import SigningKey, VerifyingKey, NIST192p
import requests
from Transaction import Transaction
import json
import codecs
import pickle
import sys
# Generate keys
# sk = SigningKey.generate(curve=NIST192p)
# vk = sk.get_verifying_key()
# open("sk.pem","wb").write(sk.to_pem())
# open("vk.pem","wb").write(vk.to_pem())

myId = 5000

'''
Test if create-transaction can be saved in json file
'''


vk = VerifyingKey.from_pem(open("./{}/vk.pem".format(myId)).read())
sk = SigningKey.from_pem(open("./{}/sk.pem".format(myId)).read())
rcv = 'Bob'
snd = 'Alice'
amt = 1
sk_string = sk.to_string()
# sk_string = (sk.to_string()).hex()
# codecs.encode(sk_string, 'hex').decode("utf-8")
# print(sk_string)

myTx = Transaction.new(rcv, snd, amt, sk_string)
myTxJSON = myTx.to_json()
# print(myTxJSON)

# headers = {'Content-type': 'text/plain'}
headers = {'Content-type': 'application/json'} 
# requests.post('http://127.0.0.1:{}/create-transactions'.format(myId), json=myTxJSON ,headers=headers)
r = requests.get('http://127.0.0.1:{}/read-transactions'.format(myId))
# print(r.content)
r1 = Transaction.from_json(r.text)["AllTransactions"]
r2 = Transaction.from_json(r1[1])
print(r2["sender"])

# '''
# Test Read blockchain
# '''
# f = requests.get('http://127.0.0.1:{}/read-blockchain'.format(myId))
# if f.status_code == 202 :
#     print("blockchain unavaiable")
# else:
#     myBlockchain = pickle.loads(f.content)
#     print(myBlockchain)


# '''
# Test read-transactions
# '''
# # TODO
# r = requests.get('http://127.0.0.1:{}/read-transactions'.format(myId))
# msg = Transaction.from_json(r.content)
# # print(r.content)
# # print(msg)
# # print(msg["AllTransactions"])

# '''
# Test read-block-header
# '''
# r = requests.get('http://127.0.0.1:{}/read-block-header'.format(myId), params={'depth': 3})
# msg = r.json()
# print(msg)

# '''
# Test read-blockchain-height
# '''
# r = requests.get('http://127.0.0.1:{}/read-blockchain-height'.format(myId))
# msg = r.json()
# print(msg)


# '''
# Test read-blocks-from-winner
# '''
# # r = requests.get('http://127.0.0.1:{}/read-blocks-from-winner'.format(myId), params={'header': '000915faab82855252374df6642cb9de4dd6fa6c475fe82aa8f8b43b8324e91a'})
# r = requests.get('http://127.0.0.1:{}/read-blocks-from-winner'.format(myId), params={'header': '0000b45d78c269f4140d2fed23438338baccf3af290e705d708b26ad17a78e75'})
# msg = r.content
# msg = pickle.loads(msg)
# print(msg)